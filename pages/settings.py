import customtkinter as ctk

def create_settings_page(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

    title = ctk.CTkLabel(content_frame, text="Settings", font=("Arial Bold", 24))
    title.pack(pady=20)

    info = ctk.CTkLabel(content_frame, text="Configure application settings and preferences.",
                        font=("Arial", 16))
    info.pack(pady=10)
