from kittyscope.utils import EXTENSION_TYPE_MAPPING
from pathlib import Path
from researchers import ImageResearcher, PdfResearcher, VideoResearcher, AudioResearcher
from pprint import pprint

class ResearchRouter:
    def __init__(self):
        self.researchers = {
            "image": ImageResearcher(),
            "document": PdfResearcher(),
            "video": VideoResearcher(),
            "audio": AudioResearcher()
        }

    def get_file_info(self, file_path: str) -> dict:
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()
        if file_extension in EXTENSION_TYPE_MAPPING:
            file_type = EXTENSION_TYPE_MAPPING[file_extension]
            
            file_info = self.researchers[file_type].get_file_info(file_path)

            return file_info

if __name__ == "__main__":
    router = ResearchRouter()
    pprint(router.get_file_info("/Users/a-/Downloads/IMG_6458.MOV"))