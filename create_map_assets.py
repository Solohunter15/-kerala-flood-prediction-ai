import base64
import os

assets_dir = os.path.join(os.path.dirname(__file__), "assets")
p2_path = os.path.join(assets_dir, "kerala_map_page2.png")
home_path = os.path.join(assets_dir, "kerala_map_home.png")

with open(p2_path, "rb") as f:
    b64_p2 = base64.b64encode(f.read()).decode("utf-8")

with open(home_path, "rb") as f:
    b64_home = base64.b64encode(f.read()).decode("utf-8")

out_file = os.path.join(assets_dir, "maps_b64.js")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(f'const KERALA_MAP_P2_B64 = "data:image/png;base64,{b64_p2}";\n')
    f.write(f'const KERALA_MAP_HOME_B64 = "data:image/png;base64,{b64_home}";\n')

print("Created maps_b64.js with size:", os.path.getsize(out_file))
