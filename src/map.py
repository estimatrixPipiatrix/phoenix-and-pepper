import json
import folium


def load_jsonl(filepath):
    with open(filepath) as f:
        return [json.loads(line) for line in f]


def create_base_map():
    m = folium.Map(
        # lat and lon go into location
        location=[39.0, 15.0],
        zoom_start=5.0,
        tiles="OpenStreetMap",
    )
    return m


def load_ports(filepath):
    raw = load_jsonl(filepath)
    return {p["name"]: p for p in raw}


def add_ports(m, ports):
    for p in ports.values():
        radius = p["size"] * 2 + 3
        popup_html = (
            f"<b>{p['name']}</b><br>"
            f"Size: {p['size']}/5<br>"
            f"Port fee: {p['base_fee']} denarii"
        )
        folium.CircleMarker(
            location=[p["latitude"], p["longitude"]],
            radius=radius,
            color="#222",
            weight=1.5,
            fill=True,
            fill_color="#534AB7",
            fill_opacity=0.85,
            tooltip=p["name"],
            popup=folium.Popup(popup_html, max_width=200),
        ).add_to(m)


def load_routes(filepath):
    """Load routes from JSONL and return as a list of dicts."""
    return load_jsonl(filepath)


def add_routes(m, routes, ports):
    """Add route lines to the map, colored by danger level."""
    danger_colors = {
        1: "#4a7fb5",
        2: "#7ab648",
        3: "#e8a735",
        4: "#d44a2e",
    }
    for r in routes:
        origin = ports[r["origin"]]
        dest = ports[r["destination"]]
        color = danger_colors.get(r["danger_level"], "#888")
        folium.PolyLine(
            locations=[
                [origin["latitude"], origin["longitude"]],
                [dest["latitude"], dest["longitude"]],
            ],
            color=color,
            weight=2 if r["danger_level"] <= 2 else 3,
            opacity=0.6,
            tooltip=f"{r['origin']} → {r['destination']} · {r['distance_km']}km · {r['base_sailing_days']}d",
        ).add_to(m)


if __name__ == "__main__":
    m = create_base_map()
    ports = load_ports("../data/ports.jsonl")
    routes = load_routes("../data/routes.jsonl")
    add_routes(m, routes, ports)
    add_ports(m, ports)
    m.save("../docs/trade_map.html")
    print("Map saved.")
