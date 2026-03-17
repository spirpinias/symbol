"""Example showing how to enable logging for debugging and visibility."""

import logging

# Configure logging before importing symbol modules.
# Use DEBUG to see per-file processing details, INFO for high-level summaries.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

from symbol import Symbol

sym = Symbol(project_dir="/path/to/your/data")

# All analysis steps will now emit log messages
extended, flexed = sym.run_isokinetic()
horizontal = sym.run_horizontal_hop()
vertical = sym.run_vertical_hop()
