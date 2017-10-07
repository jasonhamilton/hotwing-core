# About

This repository consists of a Python Module, which contains the core libraries for the HotWing-CLI and HotWing-GUI projects.  This Module provides a series of classes and functions to aid in creating GCode for 4-Axis CNC foam cutters, specifically working with wing profiles, interpolating new profiles, and computing reverse kinematics for the CNC.


# Example Usage

```py

from hotwing_core import Profile
from hotwing_core import Rib
from hotwing_core import Machine
from hotwing_core import Panel
from hotwing_core import Coordinate

## Setup Rib
r1 = Rib("profiles/s6063.dat",
         scale=10,
         xy_offset=None,
         top_sheet=0.0625,
         bottom_sheet=0.0625,
         front_stock=0.5,
         tail_stock=1.25 )
         
r2 = Rib("profiles/rg14.dat",
         scale=10,
         xy_offset=Coordinate(0, 0),
         top_sheet=0.0625,
         bottom_sheet=0.0625,
         front_stock=0.5,
         tail_stock=1.25 )

# Setup Panel
p = Panel(r1, r2, 24)

# Trim Panel
p = Panel.trim_panel(p, 0, 12)

# Setup Machine
m = Machine(24, kerf=0.075, profile_points=100, output_profile_images=True)

# Load panel into machine
m.load_panel(p)
m.gcode_formatter_name = "debug"

# Generate GCode
gcode = m.generate_gcode(safe_height=1, normalize=False)

# Output to screen
print gcode
```

# Docs

You can find the docs here : https://jasonhamilton.github.io/hotwing-core/index.html