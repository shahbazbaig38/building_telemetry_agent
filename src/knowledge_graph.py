from typing import Dict

# ---------- Knowledge Graph for Building Telemetry Sensors ----------
SENSOR_KB: Dict[str, Dict[str, str]] = {
    "timestamp": {
        "electricity_consumption": "timestamps allow time-series analysis of energy usage",
        "indoor_average_temperature": "timestamp provides history of temperature change",
    },
    "electricity_consumption": {
        "district_heating": "both partly represent energy load; one may trade off with the other",
        "indoor_average_temperature": "HVAC electricity rises/as temp veers from comfort range",
        "outside_temperature": "colder outside tends to raise electricity HVAC use in winter",
        "people_counter": "higher occupancy can increase electricity use via lighting/appliances",
    },
    "district_heating": {
        "outside_temperature": "colder outside increases heating demand",
        "indoor_average_temperature": "heating influences indoor temperature",
    },
    "people_counter": {
        "indoor_co2": "higher occupancy causes higher CO2 in enclosed spaces",
        "indoor_average_humidity": "more occupants often raise humidity from respiration",
        "electricity_consumption": "more occupants leads to more power usage for lighting and equipment",
    },
    "indoor_average_temperature": {
        "indoor_average_humidity": "temperature affects relative humidity",
        "indoor_co2": "temperature correlates with ventilation and CO2 removal efficiency",
    },
    "indoor_average_humidity": {
        "outside_humidity": "indoor humidity is partially influenced by outdoor humidity",
    },
    "indoor_co2": {
        "outside_pressure": "pressure can affect ventilation rates and CO2 mixing",
    },
    "outside_temperature": {
        "outside_humidity": "warm air holds more moisture",
        "outside_wind_speed": "wind can influence cooling/heating loads",
    },
    "outside_humidity": {
        "outside_pressure": "humidity and pressure relationships indicate weather fronts",
    },
    "outside_pressure": {
        "outside_precipitation": "lower pressure often precedes precipitation",
    },
    "outside_wind_speed": {
        "outside_solar_radiation": "cloud patterns and wind often influence solar radiation",
    },
    "outside_solar_radiation": {
        "inside_average_temperature": "solar gain can raise indoor temperature",
    },
    "outside_cloud_cover": {
        "outside_solar_radiation": "more cloud cover reduces solar radiation",
    },
    "snow_depth": {
        "outside_temperature": "lower outside temps cause more snow accumulation",
    },
}


def generate_kb_hint() -> str:
    lines = ["Sensor knowledge graph (affect relationships):"]
    for sensor, edges in SENSOR_KB.items():
        for neighbor, effect in edges.items():
            lines.append(f"- {sensor} -> {neighbor}: {effect}")
    return "\n".join(lines)