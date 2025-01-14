
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

hvac_alerts_db = [
    {"zone_id": "Comm Room", "severity": "Critical", "temp": "27°C"}, #testing to see if i see the text
    {"zone_id": "Net Room", "severity": "Warning", "temp": "30°C"},
    {"zone_id": "Generator Room", "severity": "Warning", "temp": "29°C"},
    {"zone_id": "IT Room", "severity": "Critical", "temp": "35°C"},
    {"zone_id": "Lobby Area", "severity": "Good", "temp": "22°C"},
    {"zone_id": "Admin Office", "severity": "Good", "temp": "27°C"},
    {"zone_id": "General Space", "severity": "Good", "temp": "27°C"}
]

# ping_data = [
#             ("192.168.1.1", "10ms", "Good"),
#             ("192.168.1.2", "15ms", "Good"),
#             ("192.168.1.3", "Timeout", "Critical"),
#             ("192.168.1.4", "20ms", "Average"),
#             ("192.168.1.5", "5ms", "Good"),
#         ]

ping_data_db = [
    {"IP": "192.168.1.1", "ping": "10ms", "status": "Good"},
    {"IP": "192.168.1.1", "ping": "10ms", "status": "Average"},
    {"IP": "192.168.1.1", "ping": "Timeout","status": "Critical"},
    {"IP": "192.168.1.1", "ping": "10ms", "status": "Average"},
    {"IP": "192.168.1.1", "ping": "10ms", "status": "Good"},
    {"IP": "192.168.1.1", "ping": "10ms", "status": "Good"},
]
