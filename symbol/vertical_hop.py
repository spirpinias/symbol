import logging
import pandas as pd
import polars as pl
import numpy as np

from typing import List
from os.path import dirname, basename

logger = logging.getLogger(__name__)

def vertical_hop_analysis(
    samples: List[str],
) -> pl.DataFrame:

    combined_dataset = []

    for file in samples:
        logger.debug("Processing vertical hop file: %s", file)

        dataset = pd.read_csv(
            file,
            skiprows=8,
        )

        pounds = pl.read_csv(
            file,
            truncate_ragged_lines=True
        )[0,1]

        x = basename(dirname(dirname(file)))[-3:]

        kilograms = np.float32(pounds) * 0.453592

        dataset = dataset.drop(columns=["Unnamed: 7"])
        dataset = pl.from_pandas(dataset)

        dataset = dataset.select(["Time", "Z Left", "Z Right"])

        dataset = dataset.with_columns(
            pl.lit(x).alias("Subject"),
            pl.lit(kilograms).alias("Kilograms"),
            # Z Left / Body Weight (kg * 9.8)
            (abs(pl.col("Z Left") / kilograms * 9.8)).alias("Normalized_Left"),
            (abs(pl.col("Z Right") / kilograms * 9.8)).alias("Normalized_Right")
        )

        combined_dataset.append(dataset)
    
    combined_dataset = pl.concat(combined_dataset)
    return combined_dataset
