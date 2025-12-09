import signal
import os
import subprocess
import sys
import threading

class ApiHandler:
    def __init__(self, terminal):
        self.api_process = None
        self.terminal = terminal

    def _log(self, msg: str):
        """Send logs to terminal instead of console."""
        if self.terminal:
            self.terminal.append_text(msg + "\n")
        else:
            print(msg)

    def start_api(self):
        if self.api_process and self.api_process.poll() is None:
            self._log("⚠️ API already running")
            return

        try:
            # Start Flask API process
            
            self.api_process = subprocess.Popen(
                [sys.executable, "./commands/start_api.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                preexec_fn=os.setsid   # <-- important
            )

            self._log("✅ API starting on http://127.0.0.1:5000 ...")

            # Stream Flask output into terminal
            def stream_output(proc):
                for line in proc.stdout:
                    self._log(line.strip())
            threading.Thread(target=stream_output, args=(self.api_process,), daemon=True).start()

        except Exception as e:
            self._log(f"[!] Failed to start API: {e}")

    def stop_api(self):
        try:

            os.killpg(os.getpgid(self.api_process.pid), signal.SIGTERM)
            self._log("❌ API stopped")
            self.api_process = None

        except AttributeError as e:

            self._log(f"pid not found {e}")
