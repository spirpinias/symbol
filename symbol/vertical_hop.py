import pandas as pd
import polars as pl
import numpy as np

from typing import List


def vertical_hop_analysis(
    samples: List[str],
) -> pl.DataFrame:

    combined_dataset = []

    for x in samples:

        dataset = pd.read_csv(
            f'/Users/stephenpirpinias/Desktop/SYMBOL_ORIGINAL/SUBJECT{x}/SL_Vertical_Hop/SL_Vertical_Hop.csv',
            skiprows=8,
        )
        pounds_frame = pl.read_csv(
            f'/Users/stephenpirpinias/Desktop/SYMBOL_ORIGINAL/SUBJECT{x}/Isokinetic/{x}_Hip_Flexed.csv',
        )

        pounds = pounds_frame[1, 1]
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
