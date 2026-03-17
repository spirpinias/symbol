"""Example showing how to export analysis results to CSV and inspect summary stats."""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

from symbol import Symbol

sym = Symbol(project_dir="/path/to/your/data")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Isokinetic
extended, flexed = sym.run_isokinetic()
extended.write_csv(output_dir / "isokinetic_extended.csv")
flexed.write_csv(output_dir / "isokinetic_flexed.csv")
print(f"Isokinetic extended: {extended.shape}, flexed: {flexed.shape}")
print(extended.describe())

# Horizontal hop
horizontal = sym.run_horizontal_hop()
horizontal.write_csv(output_dir / "horizontal_hop.csv")
print(f"\nHorizontal hop: {horizontal.shape}")
print(horizontal.describe())

# Vertical hop
vertical = sym.run_vertical_hop()
vertical.write_csv(output_dir / "vertical_hop.csv")
print(f"\nVertical hop: {vertical.shape}")
print(vertical.describe())

print(f"\nAll results exported to {output_dir.resolve()}")
