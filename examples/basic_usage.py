"""Basic usage of the Symbol package for VALD force plate analysis."""

from symbol import Symbol

# Point to the directory containing SUBJECT* folders
sym = Symbol(project_dir="/path/to/your/data")

# Show discovered subjects
print(f"Found subjects: {sym.samples}")

# Run isokinetic analysis — returns (extended, flexed) DataFrames
extended, flexed = sym.run_isokinetic()
print(f"\nIsokinetic Extended:\n{extended.head()}")
print(f"\nIsokinetic Flexed:\n{flexed.head()}")

# Run horizontal hop analysis
horizontal = sym.run_horizontal_hop()
print(f"\nHorizontal Hop:\n{horizontal.head()}")

# Run vertical hop analysis
vertical = sym.run_vertical_hop()
print(f"\nVertical Hop:\n{vertical.head()}")
