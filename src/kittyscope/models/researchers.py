from abc import ABC, abstractmethod
from pypdf import PdfReader
from PIL import Image
from PIL.ExifTags import Base
from pprint  import pprint
import ffmpeg


class Researcher(ABC):
    @abstractmethod
    def get_file_info(self, file_path: str) -> dict:
        ...


class ImageResearcher(Researcher):
    def get_file_info(self, file_path: str) -> dict:
        image = Image.open(file_path)
        common_info = {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "color_mode": image.mode
        }

        image_exif = image.getexif()
        exif_info = {}
        for tag, value in image_exif.items():
            key = Base(tag).name
            exif_info[key] = value
        
        image_data = {
            "common_info": common_info,
            "exif_info": exif_info
        }
        return image_data


class PdfResearcher(Researcher):
    def get_file_info(self, file_path: str) -> dict:
        reader = PdfReader(file_path)
        pages_count = len(reader.pages)
        metadata = reader.metadata

        pdf_info = {
            "author": metadata.author,
            "title": metadata.title,
            "pages_count": pages_count,
            "subject": metadata.subject,
            "creator": metadata.creator,
            "producer": metadata.producer
        }

        return pdf_info
    
class VideoResearcher(Researcher):
    def get_file_info(self, file_path: str) -> dict:
        probe = ffmpeg.probe(file_path)

        video_info = probe.get("format", None)
        return video_info

class AudioResearcher(Researcher):
    def get_file_info(self, file_path: str) -> dict:
        probe = ffmpeg.probe(file_path)

        audio_info = probe.get("format", None)
        return audio_info


if __name__ == "__main__":
    audio_researcher = VideoResearcher()
    pprint(audio_researcher.get_file_info("/Users/a-/Downloads/The-Substance-Original-Motion-Picture-Score.m4a"))

