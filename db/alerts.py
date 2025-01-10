
# db for Network/HVAC/BAS Alerts


network_alerts_db = [
        {
            "id": 1,
            "description": "High latency detected",
            "acknowledge": False
        },
         {
             "id": 2,
            "description": "Weak signal",
            "acknowledge": False
        },
         {
             "id": 3,
            "description": "Network currently unavailable",
            "acknowledge": False
        },
         {  "id": 4,
            "description": "Network timeout for 192.168.5 ",
            "acknowledge": False
        },
         {
             "id": 5,
            "description": "Packets lost for 192.168.1",
            "acknowledge": False
        },
       {
            "id": 6,
            "description": "Network Error",
            "acknowledge": False
        }

]

# hvac_sensor_zone_db = [
#     {"zone_id": 1, "severity": "Warning", "temp": "27°C"},
#     {"zone_id": 2, "severity": "Critical", "temp": "35°C"},
#     {"zone_id": 3, "severity": "Normal", "temp": "15°C"},
#     {"zone_id": 4, "severity": "Normal", "temp": "25°C"},
#     {"zone_id": 5, "severity": "Normal", "temp": "27°C"},
#     {"zone_id": 6, "severity": "Warning", "temp": "30°C"},
# ]

# for item in network_alerts_db:
#     if item['id'] == 1:
#         item['acknowledge'] = True
#
# for item in network_alerts_db:
#     print(item)

hvac_alerts_db = [
    {"zone_id": "Comm Room", "severity": "Critical", "temp": "27°C"}, #testing to see if i see the text
    {"zone_id": "Net Room", "severity": "Warning", "temp": "30°C"},
    {"zone_id": "Generator Room", "severity": "Warning", "temp": "29°C"},
    {"zone_id": "IT Room", "severity": "Critical", "temp": "35°C"},
    {"zone_id": "Lobby Area", "severity": "Good", "temp": "22°C"},
    {"zone_id": "Admin Office", "severity": "Good", "temp": "27°C"},
    {"zone_id": "General Space", "severity": "Good", "temp": "27°C"}
]