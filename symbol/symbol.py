import logging
from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json, config

from pathlib import Path

from symbol.isokinetic import isokinetic_analysis
from symbol.horizontal_hop import horizontal_hop_analysis
from symbol.vertical_hop import vertical_hop_analysis

logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class Symbol:

    """VALD Force Plate"""

    project_dir: str
    weights: list[int] = field(init=False, default=None)
    samples: list[str] = field(init=False, default=None)

    __kinetics_data: list[str] = field(
        default_factory=list,
        init=False,
        repr=False,
        metadata=config(exclude=lambda x: True)
    )
    __horizontal_hop_data: list[str] = field(
        default_factory=list,
        init=False,
        repr=False,
        metadata=config(
            exclude=lambda x: True)
    )
    __vertical_hop_data: list[str] = field(
        default_factory=list,
        init=False,
        repr=False,
        metadata=config(exclude=lambda x: True)
    )

    def __post_init__(self):
        logger.info("Initializing Symbol with project_dir=%s", self.project_dir)
        self.__get_metadata()

    def __get_metadata(self):
        try:
            p = Path(self.project_dir)
            self.__kinetics_data = list(
                p.glob('**/Isokinetic/*.csv')
            )
            self.__horizontal_hop_data = list(
                p.glob('**/SL_Horizontal_Hop/*.csv')
            )
            self.__vertical_hop_data = list(
                p.glob('**/SL_Vertical_Hop/*.csv')
            )
            samples = list(
                p.glob('SUBJECT*')
            )
            self.samples = [
                ''.join(filter(str.isdigit, x.name))
                for x in samples
            ]
            logger.info(
                "Discovered %d isokinetic, %d horizontal hop, %d vertical hop files for %d subjects",
                len(self.__kinetics_data),
                len(self.__horizontal_hop_data),
                len(self.__vertical_hop_data),
                len(self.samples),
            )

        except Exception as e:
            logger.error("Failed to read metadata from %s: %s", self.project_dir, e)

    def run_isokinetic(self):
        logger.info("Running isokinetic analysis on %d files", len(self.__kinetics_data))
        extended, flexed = isokinetic_analysis(
            files=self.__kinetics_data
        )
        logger.info("Isokinetic analysis complete: extended=%d rows, flexed=%d rows", len(extended), len(flexed))

        return extended, flexed

    def run_horizontal_hop(self):
        logger.info("Running horizontal hop analysis on %d files", len(self.__horizontal_hop_data))
        combined = horizontal_hop_analysis(
            samples=self.__horizontal_hop_data
        )
        logger.info("Horizontal hop analysis complete: %d rows", len(combined))

        return combined

    def run_vertical_hop(self):
        logger.info("Running vertical hop analysis on %d files", len(self.__vertical_hop_data))
        combined = vertical_hop_analysis(
            samples=self.__vertical_hop_data
        )
        logger.info("Vertical hop analysis complete: %d rows", len(combined))

        return combined
