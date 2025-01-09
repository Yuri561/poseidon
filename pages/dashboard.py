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
import plotly.graph_objects as go


def create_dashboard_page(content_frame):
    # Clear the current content
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Configure the grid layout for the dashboard
    content_frame.grid_columnconfigure((0, 1), weight=1)
    content_frame.grid_rowconfigure((0, 1, 2), weight=1)

    # Resize all widgets to make them more compact

    # ========== Weather Frame (Top Left) ==========
    weather_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="gray20")
    weather_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    weather_title = ctk.CTkLabel(weather_frame, text="☁️ Weather Overview", font=("Arial Bold", 14))
    weather_title.pack(pady=(5, 2))

    try:
        weather = fetch_detailed_weather()
        if weather:
            icon_image = fetch_weather_icon(weather["icon_url"])
            icon_photo = CTkImage(light_image=icon_image, size=(50, 50)) if icon_image else None

            if icon_photo:
                icon_label = ctk.CTkLabel(weather_frame, text="", image=icon_photo)
                icon_label.pack(pady=5)

            weather_data = [
                ("Temperature", f"{weather['temp']}°F"),
                ("Feels Like", f"{weather['feels_like']}°F"),
                ("Description", weather['description']),
                ("Wind Speed", f"{weather['wind_speed']} m/s"),
                ("Humidity", f"{weather['humidity']}%"),
            ]

            for label, value in weather_data:
                row = ctk.CTkFrame(weather_frame, fg_color="gray15", corner_radius=10)
                row.pack(fill="x", padx=5, pady=2)

                key_label = ctk.CTkLabel(row, text=label, font=("Arial", 10), anchor="w")
                key_label.pack(side="left", padx=5, pady=2)

                value_label = ctk.CTkLabel(row, text=value, font=("Arial Bold", 10), anchor="e")
                value_label.pack(side="right", padx=5, pady=2)
        else:
            error_label = ctk.CTkLabel(weather_frame, text="Failed to fetch weather data", font=("Arial", 10))
            error_label.pack(pady=5)
    except Exception as e:
        error_label = ctk.CTkLabel(weather_frame, text=f"Error: {str(e)}", font=("Arial", 10))
        error_label.pack(pady=5)

    # ========== Nexus Frame with Plotly Gauges (Top Right) ==========
    nexus_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="black")
    nexus_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    nexus_title = ctk.CTkLabel(nexus_frame, text="Generator Meter", font=("Arial Bold", 14), text_color="white")
    nexus_title.pack(pady=5)

    # Data for the Plotly gauges
    meters = [
        {"label": "CPU Usage", "value": 80, "max_value": 160, "range": [0, 160]},
        {"label": "Memory Usage", "value": 60, "max_value": 100, "range": [0, 100]},
        {"label": "Disk Usage", "value": 45, "max_value": 80, "range": [0, 80]},
    ]

    # Create a Plotly gauge for each meter
    for meter_info in meters:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=meter_info["value"],
            title={"text": meter_info["label"], "font": {"size": 12, "color": "white"}},
            gauge={
                "axis": {"range": meter_info["range"], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "red"},
                "steps": [
                    {"range": [meter_info["range"][0], meter_info["range"][1] * 0.7], "color": "lightgreen"},
                    {"range": [meter_info["range"][1] * 0.7, meter_info["range"][1] * 0.9], "color": "yellow"},
                    {"range": [meter_info["range"][1] * 0.9, meter_info["range"][1]], "color": "red"}
                ],
            }
        ))

        fig.update_layout(
            width=200, height=200,  # Set size for each gauge
            margin=dict(l=20, r=20, t=40, b=20),  # Adjust margins
            paper_bgcolor="black",  # Background color
            font=dict(color="white", family="Arial")
        )

        # Embed Plotly gauge into CustomTkinter using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig.to_image(format="png"), master=nexus_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side="left", padx=10, pady=10)


    # ========== Security Frame (Middle Left) ==========
    security_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="gray20")
    security_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    security_title = ctk.CTkLabel(security_frame, text="🔒 Security System", font=("Arial Bold", 14))
    security_title.pack(pady=5)

    security_status = [
        ("Cameras Online", "10"),
        ("Intrusion Alarms", "0"),
        ("Access Logs", "Updated"),
    ]
    for label, value in security_status:
        row = ctk.CTkFrame(security_frame, fg_color="gray15", corner_radius=10)
        row.pack(fill="x", padx=5, pady=2)

        key_label = ctk.CTkLabel(row, text=label, font=("Arial", 10), anchor="w")
        key_label.pack(side="left", padx=5, pady=2)

        value_label = ctk.CTkLabel(row, text=value, font=("Arial Bold", 10), anchor="e")
        value_label.pack(side="right", padx=5, pady=2)

    # ========== Alarm List (Middle Right) ==========
    alarms_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="gray20")
    alarms_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    alarms_title = ctk.CTkLabel(alarms_frame, text="🚨 Active Alarms", font=("Arial Bold", 14))
    alarms_title.pack(pady=5)

    alarms_list = ctk.CTkTextbox(alarms_frame, height=50, corner_radius=10)
    alarms_list.insert("0.0", "No active alarms.")
    alarms_list.configure(state="disabled")
    alarms_list.pack(fill="both", padx=5, pady=5)

    # ========== HVAC Frame with Line Graph (Bottom Left) ==========
    hvac_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="white")
    hvac_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

    hvac_title = ctk.CTkLabel(hvac_frame, text="HVAC Status", font=("Arial Bold", 14), text_color="black")
    hvac_title.pack(pady=5)

    dates = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    hvac_values = [90, 85, 78, 92, 88, 75, 80]

    fig, ax = plt.subplots(figsize=(3, 2), dpi=100)
    ax.bar(dates, hvac_values, color="lime", edgecolor="white")
    ax.set_title("Performance", fontsize=10, color="black")
    ax.tick_params(axis='x', rotation=45, colors="black")
    ax.tick_params(axis='y', colors="black")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=hvac_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)
    canvas.draw()

    # ========== Admin Controls (Bottom Right) ==========
    admin_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="darkblue")
    admin_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    admin_title = ctk.CTkLabel(admin_frame, text="Admin Controls", font=("Arial Bold", 14), text_color="white")
    admin_title.pack(pady=5)

    activate_button = ctk.CTkButton(
        admin_frame, text="Activate V1 AI", fg_color="lime", hover_color="green",
        command=lambda: messagebox.showinfo("Action", "V1 AI Activated")
    )
    activate_button.pack(pady=5)

    deactivate_button = ctk.CTkButton(
        admin_frame, text="Deactivate V1 AI", fg_color="red", hover_color="darkred",
        command=lambda: messagebox.showinfo("Action", "V1 AI Deactivated")
    )
    deactivate_button.pack(pady=5)
