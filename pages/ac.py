import customtkinter as ctk

def create_ac_page(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

    title = ctk.CTkLabel(content_frame, text="AC Power Room Details", font=("Arial Bold", 24))
    title.pack(pady=20)

    info = ctk.CTkLabel(content_frame, text="Monitoring AC power distribution and backup systems.",
                        font=("Arial", 16))
    info.pack(pady=10)
