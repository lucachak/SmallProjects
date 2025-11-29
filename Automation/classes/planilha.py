from EmailHandler import EmailHandler
from ExcelHandler import ExcelHandler
import customtkinter as ctk

# Instantiate handlers
email_handler = EmailHandler()
status_label = None  # placeholder for GUI label

def update_status(text):
    status_label.configure(text=text)

excel_handler = ExcelHandler(email_handler=email_handler, status_callback=update_status)

# GUI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("License Processor")
app.geometry("450x150")

frame = ctk.CTkFrame(app, corner_radius=10)
frame.pack(pady=20, padx=20, fill="both", expand=True)

button = ctk.CTkButton(frame, text="Select Excel File", command=excel_handler.select_file)
button.pack(pady=20)

status_label = ctk.CTkLabel(frame, text="No file processed yet.")
status_label.pack(pady=10)

app.mainloop()

