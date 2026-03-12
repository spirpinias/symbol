from typing import List
from pathlib import Path

def get_sample_count(top_level: str) -> List[str]:

    p = Path(top_level)
    samples = list(p.glob('SUBJECT*'))
    digits = [''.join(filter(str.isdigit, x.name)) for x in samples]

    return digits

def get_isokinetic_data(top_level: str) -> List[str]:

    p = Path(top_level)
    isokinetic_hip = list(p.glob('**/Isokinetic/*.csv'))

    return isokinetic_hip

def get_horizontal_hop_data(top_level: str) -> List[str]:

    p = Path(top_level)
    horizontal_hop = list(p.glob('**/SL_Horizontal_Hop/*.csv'))

    return horizontal_hop

def get_vertical_hop_data(top_level: str) -> List[str]:

    p = Path(top_level)
    vertical_hop = list(p.glob('**/SL_Vertical_Hop/*.csv'))

    return vertical_hop