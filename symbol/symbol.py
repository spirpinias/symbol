from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json, config

from pathlib import Path

from symbol.isokinetic import isokinetic_analysis


@dataclass_json
@dataclass
class Symbol:

    """VALD Force Plate"""

    project_dir: str
    samples: str = field(init=False, default=None)
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
        except Exception as e:
            print(e)

    def run_isokinetic(self):
        extended, flexed = isokinetic_analysis(files = self.__kinetics_data)
        return extended, flexed