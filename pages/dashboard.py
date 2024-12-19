import customtkinter as ctk
from customtkinter import CTkImage
from weather import fetch_detailed_weather, fetch_weather_icon
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from tkdial import Meter
from tkinter import messagebox
import random


def create_dashboard_page(content_frame):
    # Clear the current content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Configure the grid layout for the dashboard
    content_frame.grid_columnconfigure((0, 1), weight=1)
    content_frame.grid_rowconfigure((0, 1), weight=1)

    # ========== Weather Frame (Top Left) ==========
    weather_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="gray20")
    weather_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    weather_title = ctk.CTkLabel(weather_frame, text="☁️ Weather Overview", font=("Arial Bold", 18))
    weather_title.pack(pady=(10, 5))

    try:
        weather = fetch_detailed_weather()
        if weather:
            icon_image = fetch_weather_icon(weather["icon_url"])
            icon_photo = CTkImage(light_image=icon_image, size=(100, 100)) if icon_image else None

            if icon_photo:
                icon_label = ctk.CTkLabel(weather_frame, text="", image=icon_photo)
                icon_label.pack(pady=10)

            weather_data = [
                ("Temperature", f"{weather['temp']}°F"),
                ("Feels Like", f"{weather['feels_like']}°F"),
                ("Description", weather['description']),
                ("Wind Speed", f"{weather['wind_speed']} m/s"),
                ("Humidity", f"{weather['humidity']}%"),
            ]

            for label, value in weather_data:
                row = ctk.CTkFrame(weather_frame, fg_color="gray15", corner_radius=10)
                row.pack(fill="x", padx=10, pady=5)

                key_label = ctk.CTkLabel(row, text=label, font=("Arial", 14), anchor="w", width=120)
                key_label.pack(side="left", padx=10, pady=5)

                value_label = ctk.CTkLabel(row, text=value, font=("Arial Bold", 14), anchor="e", wraplength=200)
                value_label.pack(side="right", padx=10, pady=5)
        else:
            error_label = ctk.CTkLabel(weather_frame, text="Failed to fetch weather data", font=("Arial", 14))
            error_label.pack(pady=10)
    except Exception as e:
        error_label = ctk.CTkLabel(weather_frame, text=f"Error: {str(e)}", font=("Arial", 14))
        error_label.pack(pady=10)

    # ========== Nexus Frame with Gauges (Top Right) ==========
    nexus_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="black")
    nexus_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    nexus_title = ctk.CTkLabel(nexus_frame, text="System Performance", font=("Arial Bold", 18), text_color="white")
    nexus_title.grid(row=0, column=0, columnspan=3, pady=10)

    # Restored meters
    meters = [
        {"label": "CPU", "value": 80, "max_value": 160, "mark": (140, 160)},
        {"label": "Memory", "value": 60, "max_value": 100, "mark": (90, 100)},
        {"label": "Disk", "value": 45, "max_value": 80, "mark": (70, 80)},
    ]

    for i, meter_info in enumerate(meters):
        meter = Meter(
            nexus_frame, radius=250, start=0, end=meter_info["max_value"], border_width=0,
            fg="black", text_color="white", start_angle=270, end_angle=-270,
            text_font="DS-Digital 20", scale_color="white", needle_color="red",
            scroll=False
        )
        meter.set_mark(*meter_info["mark"])  # Set red marking range
        meter.set(meter_info["value"])  # Set current value
        meter.grid(row=1, column=i, padx=20, pady=30)

    # ========== Power Usage Frame with Voice AI Controls (Bottom Left) ==========
    power_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="darkblue")
    power_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    power_title = ctk.CTkLabel(power_frame, text="Admin", font=("Arial Bold", 18), text_color="white")
    power_title.pack(pady=10)

    activate_v1_button = ctk.CTkButton(
        power_frame, text="Activate V1 AI", fg_color="lime", hover_color="green",
        command=lambda: messagebox.showinfo("Action", "V1 AI Activated")
    )
    activate_v1_button.pack(pady=10)

    deactivate_v1_button = ctk.CTkButton(
        power_frame, text="Deactivate V1 AI", fg_color="red", hover_color="darkred",
        command=lambda: messagebox.showinfo("Action", "V1 AI Deactivated")
    )
    deactivate_v1_button.pack(pady=10)

    # ========== HVAC Frame with Line Graph (Bottom Right) ==========
    hvac_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="white")
    hvac_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    hvac_title = ctk.CTkLabel(hvac_frame, text="HVAC Status", font=("Arial Bold", 18), text_color="black")
    hvac_title.pack(pady=10)

    # Example data for the line graph
    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    hvac_values = [90, 85, 78, 92, 88, 75, 80]

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.bar(dates, hvac_values, color="lime", edgecolor="white")
    ax.set_title("HVAC Performance", fontsize=14, color="black")
    ax.set_xlabel("Date", fontsize=10, color="black")
    ax.set_ylabel("Performance (%)", fontsize=10, color="black")
    ax.tick_params(axis='x', rotation=45, colors="black")
    ax.tick_params(axis='y', colors="black")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=hvac_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()
