from typing import List, Tuple
import polars as pl
import numpy as np
from os.path import basename


def isokinetic_analysis(
        files: List[str],
) -> Tuple[pl.DataFrame, pl.DataFrame]:

    flexed = []
    extended = []

    for file in files:

        num_sample = basename(file).split('_')[0]
        hip_type = basename(file).split('_')[2].removesuffix(".csv")

        dataset = pl.read_csv(file)

        pounds = dataset[1, 1]
        kilograms = np.float32(pounds) * 0.453592
        dataset = dataset[72:, 1:]
        headers = dataset.row(0)
        dataset = dataset.rename(dict(zip(dataset.columns, headers)))
        dataset = dataset[1:, :]

        dataset = dataset.with_columns(
            [
                pl.col("SIDE").cast(pl.String),
                pl.col("Set").cast(pl.String),
                pl.col("Rep").cast(pl.String),
                pl.col("mSec").cast(pl.Int64),
                pl.col("TORQUE").cast(pl.Float32),
                pl.col("POSITION").cast(pl.Float32),
                pl.col("POS_(ANAT)").cast(pl.Float32),
                pl.col("VELOCITY").cast(pl.Float32),
            ]
        )

        dataset = dataset.with_columns(
            pl.lit(num_sample).alias("Subject"),
            pl.lit(kilograms).alias("Kilograms"),
            (abs(pl.col("TORQUE") * 1.3558 / kilograms)).alias("Normalized"),
            (pl.col("mSec") / 1000).alias("Sec")
        )

        dataset = dataset.filter(pl.col("Rep") != "-")

        if hip_type == "Flexed":
            flexed.append(dataset)
        else:
            extended.append(dataset)

    combined_flex = pl.concat(flexed)
    combined_extended = pl.concat(extended)

    return combined_flex, combined_extended
