from hotwing_core import Profile
from hotwing_core import Rib
from hotwing_core import Machine
from hotwing_core import Panel
from hotwing_core import Coordinate

## Setup Rib
r1 = Rib("http://m-selig.ae.illinois.edu/ads/coord/ah83159.dat",
         scale=10,
         xy_offset=None,
         top_sheet=0.0625,
         bottom_sheet=0.0625,
         front_stock=0.5,
         tail_stock=1.25 )
         
r2 = Rib("http://m-selig.ae.illinois.edu/ads/coord/rg14.dat",
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
m = Machine(24, kerf=0.075, profile_points=300)

# Load panel into machine
m.load_panel(p)
#m.gcode_formatter_name = "debug"

# Generate GCode
gcode = m.generate_gcode(safe_height=3, units="inches")

# Output to screen
# print gcode