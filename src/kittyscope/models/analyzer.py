import polars as pl

from kittyscope.utils import EXTENSION_TYPE_MAPPING

EXTENSION_TYPE_MAPPING_DF = pl.DataFrame(
    {
        "extension": list(EXTENSION_TYPE_MAPPING.keys()),
        "file_type": list(EXTENSION_TYPE_MAPPING.values()),
    }
)


class Analyzer:
    def get_type_stat(self, df: pl.DataFrame) -> dict[str, dict[str, list]]:
        """
        Calculates statistics for the given DataFrame by grouping data based on type and extension.

        Args:
            df (pl.DataFrame): The DataFrame containing file information with columns "type" and "extension".

        Returns:
            dict[str, dict[str, list]]: A dictionary containing two keys:
                - "type_stat": A dictionary with the count of entries for each file type.
                - "extension_stat": A dictionary with the count of entries for each file extension.
        """
        df_type_stat = df.group_by("type").len()
        df_extension_stat = (
            df.filter(pl.col("type") == "file", pl.col("extension").is_not_null())
            .group_by("extension")
            .len()
        )

        stat_data = {
            "type_stat": df_type_stat.to_dict(as_series=False),
            "extension_stat": df_extension_stat.to_dict(as_series=False),
        }

        return stat_data

    def get_file_type_stat(self, df: pl.DataFrame):
        """
        Calculates the count of entries for each file type in the given DataFrame.

        Args:
            df (pl.DataFrame): The DataFrame containing file information with columns "extension".

        Returns:
            dict[str, list]: A dictionary with the count of entries for each file type.
        """
        df_with_file_types = df.join(
            EXTENSION_TYPE_MAPPING_DF, on="extension", how="inner"
        )

        stat_data = (
            df_with_file_types.group_by("file_type")
            .len(name="count")
            .to_dict(as_series=False)
        )
        stat_data["group_count"] = len(stat_data["file_type"])

        return stat_data
