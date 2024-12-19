import customtkinter as ctk
from pages.dashboard import create_dashboard_page
from utils.sidebar import create_sidebar


# Initialize main window
app = ctk.CTk()
app.geometry("1200x800")
app.title("Vankor - 42440")

# Top Section (Title and Alarms)
title_frame = ctk.CTkFrame(app, height=100, corner_radius=10)
title_frame.pack(fill="x", padx=10, pady=10)

title_label = ctk.CTkLabel(title_frame, text="Vankor 1 MEC", font=("Arial", 24))
title_label.pack(side="left", padx=20)

alarms_label = ctk.CTkLabel(
    title_frame, text="Active NOC Alarms: 0", font=("Arial", 18), fg_color="green", corner_radius=5, padx=10, pady=5
)
alarms_hvac_label = ctk.CTkLabel(
    title_frame, text="Active HVAC Alarms: 4", font=("Arial", 18), fg_color="red", corner_radius=5, padx=10, pady=5
)

alarms_label.pack(side="right", padx=20)
alarms_hvac_label.pack(side="right", padx=35)

# Main Layout with Sidebar and Content Area
main_frame = ctk.CTkFrame(app, corner_radius=10)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Sidebar Navigation
sidebar = ctk.CTkFrame(main_frame, width=200, corner_radius=10, fg_color="gray20")
sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

content_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="gray10")
content_frame.grid(row=0, column=1, sticky="nsew")

# Add Sidebar
create_sidebar(sidebar, content_frame)

# Show default page
create_dashboard_page(content_frame)

# Run the app
app.mainloop()
