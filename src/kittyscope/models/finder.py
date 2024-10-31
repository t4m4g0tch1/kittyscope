from os.path import getmtime, getatime, getsize
from datetime import datetime
import polars as pl
from pathlib import Path

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class Finder:
    def get_elements_info(self, path: str) -> pl.DataFrame:

        path = Path(path)
        if path.is_dir():
            elements_info = []
            for element in path.iterdir():
                if element.is_file():
                    element_type = "file"
                elif element.is_dir():
                    element_type = "folder"
                else:
                    element_type = "unknown"
                
                element_size = getsize(element)
                element_access_time = datetime.fromtimestamp(getatime(element)).strftime(DATETIME_FORMAT)
                element_modification_time = datetime.fromtimestamp(getmtime(element)).strftime(DATETIME_FORMAT)

                elements_info.append(
                    {
                        "name": element.name,
                        "type": element_type,
                        "size": element_size,
                        "extension": element.suffix.lower() if len(element.suffix) > 0 else None,
                        "access_time": element_access_time,
                        "modification_time": element_modification_time
                    }
                )
        else:
            raise Exception("Path is not a directory")

        df = pl.DataFrame(elements_info)
        return df
    
    def sort__elements(self, df: pl.DataFrame, sort_by: str, descending: bool) -> pl.DataFrame:
        return df.sort(by = sort_by, descending=descending)
    
    def filter_elements(self, df: pl.DataFrame, filter_by: str, value: str) -> pl.DataFrame:
        return df.filter(pl.col(filter_by) == value)
                