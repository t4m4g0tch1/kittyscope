import polars as pl
from finder import Finder
from kittyscope.utils import EXTENSION_TYPE_MAPPING

EXTENSION_TYPE_MAPPING_DF = pl.DataFrame({
    "extension": list(EXTENSION_TYPE_MAPPING.keys()),
    "file_type": list(EXTENSION_TYPE_MAPPING.values())
})

class Analyzer:
    def get_type_stat(self, df: pl.DataFrame) -> dict[str, dict[str, list]]:
        df_type_stat = df.group_by("type").len()
        df_extension_stat = df.filter(pl.col("type") == "file", pl.col("extension").is_not_null()).group_by("extension").len()

        stat_data = {
            "type_stat": df_type_stat.to_dict(as_series=False),
            "extension_stat": df_extension_stat.to_dict(as_series=False)
        }

        return stat_data
    
    def get_file_type_stat(self, df: pl.DataFrame):
        df_with_file_types = df.join(EXTENSION_TYPE_MAPPING_DF, on="extension", how="inner")

        return df_with_file_types.group_by("file_type").len().to_dict(as_series=False)


if __name__ == "__main__":
    finder = Finder()
    df = finder.get_elements_info("/Users/a-/Documents/Study/Магистратура/ПАНДАН/6_MODULE/технологии_программирования/kitty_test_data/thread1/041")
    analyzer = Analyzer()
    print(analyzer.get_type_stat(df))