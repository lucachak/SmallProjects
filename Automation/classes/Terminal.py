
#!/usr/bin/env python3
import subprocess
import threading
from customtkinter import *
from customtkinter import CTkInputDialog


class Terminal(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="black")

        self.textbox = CTkTextbox(
            self,
            fg_color="black",
            text_color="white",
            font=("Courier", 12)
        )
        self.textbox.pack(fill="both", expand=True, padx=5, pady=5)

        self.entry = CTkEntry(self, placeholder_text="Type here and press Enter...")
        self.entry.pack(fill="x", padx=5, pady=2)
        self.entry.bind("<Return>", self.send_input)

        self.process = None
        self._lock = threading.Lock()

    # ---------------------------
    # Run external command
    # ---------------------------
    def run_command(self, task_name: str, cmd: str):
        def looks_like_password_prompt(line: str) -> bool:
            if not line:
                return False
            s = line.strip().lower()
            return (
                "password" in s and ("sudo" in s or "password for" in s or s.endswith("password:"))
            ) or s.endswith("sudo:")

        def target():
            with self._lock:
                self.append_text(f"$ {cmd}\n")

                try:
                    proc = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        stdin=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                    )
                except Exception as e:
                    self.append_text(f"[!] Failed to start process: {e}\n")
                    return

                self.process = proc
                pending_password_sent = False
                buf = ""

                try:
                    while True:
                        ch = proc.stdout.read(1)
                        if ch == "" and proc.poll() is not None:
                            break
                        if ch == "":
                            continue

                        buf += ch
                        # flush on newline
                        if ch == "\n":
                            line = buf
                            buf = ""
                            self.append_text(line)
                            if looks_like_password_prompt(line) and not pending_password_sent:
                                pw = self._ask_password("Enter sudo password")
                                if pw:
                                    proc.stdin.write(pw + "\n")
                                    proc.stdin.flush()
                                else:
                                    self.append_text("[!] No password entered — aborting.\n")
                                    proc.terminate()
                                pending_password_sent = True
                        else:
                            # handle inline password prompts (without newline)
                            lowbuf = buf.lower()
                            if (lowbuf.endswith("password:") or lowbuf.endswith("sudo:")) and not pending_password_sent:
                                self.append_text(buf)
                                buf = ""
                                pw = self._ask_password("Enter sudo password")
                                if pw:
                                    proc.stdin.write(pw + "\n")
                                    proc.stdin.flush()
                                else:
                                    self.append_text("[!] No password entered — aborting.\n")
                                    proc.terminate()
                                pending_password_sent = True

                    if buf:
                        self.append_text(buf)
                        buf = ""
                except Exception as e:
                    self.append_text(f"[!] Error reading process output: {e}\n")

                rc = proc.wait()
                self.append_text(f"\n[Process '{task_name}' exited with code {rc}]\n")
                self.process = None

        threading.Thread(target=target, daemon=True).start()

    # ---------------------------
    # Helper: GUI password dialog
    # ---------------------------
    def _ask_password(self, prompt="Enter password"):
        dialog = CTkInputDialog(text=prompt, title="Authentication")
        pw = dialog.get_input()
        return pw

    # ---------------------------
    # Insert text into terminal
    # ---------------------------
    def append_text(self, text: str):
        self.textbox.insert("end", text)
        self.textbox.see("end")

    # ---------------------------
    # Send input from entry
    # ---------------------------
    def send_input(self, event=None):
        if self.process and self.process.stdin:
            cmd = self.entry.get() + "\n"
            try:
                self.process.stdin.write(cmd)
                self.process.stdin.flush()
                self.append_text(f"> {cmd}")
            except Exception as e:
                self.append_text(f"[!] Failed to send input: {e}\n")
            self.entry.delete(0, "end")

