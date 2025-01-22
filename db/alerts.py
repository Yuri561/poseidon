
# db for Network/HVAC/BAS Alerts
from math import floor

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
    {"zone_id": "Comm Room", "severity": "Critical", "temp": 27}, #testing to see if i see the text
    {"zone_id": "Net Room", "severity": "Warning", "temp": 30},
    {"zone_id": "Generator Room", "severity": "Warning", "temp": 29},
    {"zone_id": "IT Room", "severity": "Critical", "temp": 35},
    {"zone_id": "Lobby Area", "severity": "Good", "temp": 22},
    {"zone_id": "Admin Office", "severity": "Good", "temp": 27},
    {"zone_id": "General Space", "severity": "Good", "temp": 27}
]

for item in hvac_alerts_db:
    temp_f = item['temp']* 9/5 + 32
    item['temp'] = floor(temp_f)
# print(hvac_alerts_db) testing only




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

hvac_performance = [
    ("RTU-1", 90),
    ("RTU-2", 85),
    ("FCU-1", 78),
    ("FCU-2", 92),
    ("Tower", 88),
    ("RTU-3", 95),
    ("RTU-4", 65),
    ("FCU-3", 80),
    ("FCU-4", 75),
    ("Cooling Tower", 85),
]

hvac_performance_db = [{
    "equipment_name": "RTU-1", "performance": 90},
    {"equipment_name": "RTU-2", "performance": 90},
    {"equipment_name": "FCU-1", "performance": 70},
    {"equipment_name": "FCU-2", "performance": 60},
    {"equipment_name": "TOWER-1", "performance": 80},
    {"equipment_name": "RTU-3", "performance": 90},
    {"equipment_name": "AHU-1", "performance": 60},
    {"equipment_name": "AHU-2", "performance": 70},
    {"equipment_name": "AHU-3", "performance": 90},
    { "equipment_name": "CU-1", "performance": 70}

]