from pages.dashboard import create_dashboard_page
from pages.network import create_network_page
from pages.battery import create_battery_page
from pages.ac import create_ac_page
from pages.generator import create_generator_page
from pages.telco import create_telco_page
from pages.fuel import create_fuel_page
from pages.cooling import create_cooling_page
from pages.security import create_security_page
from pages.lighting import create_lighting_page
from pages.settings import create_settings_page
from pages.logs import create_logs_page

import customtkinter as ctk


def create_sidebar(sidebar, content_frame):
    pages = {
        "Dashboard": lambda: create_dashboard_page(content_frame),
        "Network": lambda: create_network_page(content_frame),
        "Battery": lambda: create_battery_page(content_frame),
        "AC": lambda: create_ac_page(content_frame),
        "Generator": lambda: create_generator_page(content_frame),
        "Telco": lambda: create_telco_page(content_frame),
        "Fuel": lambda: create_fuel_page(content_frame),
        "Cooling": lambda: create_cooling_page(content_frame),
        "Security": lambda: create_security_page(content_frame),
        "Lighting": lambda: create_lighting_page(content_frame),
        "Settings": lambda: create_settings_page(content_frame),
        "Logs": lambda: create_logs_page(content_frame),
    }

    for page_name, page_func in pages.items():
        btn = ctk.CTkButton(sidebar, text=page_name, command=page_func)
        btn.pack(fill="x", pady=5, padx=10)
