from abc import ABC, abstractmethod

import ffmpeg
from PIL import Image
from PIL.ExifTags import Base
from pypdf import PdfReader


class Researcher(ABC):
    """
    An abstract base class for researchers.

    This class provides a common interface for all researchers, including the [get_file_info](cci:1://file:///Users/a-/Documents/Study/%D0%9C%D0%B0%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0/%D0%9F%D0%90%D0%9D%D0%94%D0%90%D0%9D/6_MODULE/%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/kittyscope/src/kittyscope/models/researchers.py:64:4-68:34) method.
    """

    @abstractmethod
    def get_file_info(self, file_path: str) -> dict:
        """
        Retrieves the file information for the given file path.

        Args:
            file_path (str): The path to the file to retrieve information from.

        Returns:
            dict: A dictionary containing the file information.
        """
        ...


class ImageResearcher(Researcher):
    """
    A researcher for image files.
    """

    def get_file_info(self, file_path: str) -> tuple[str, dict]:
        image = Image.open(file_path)
        common_info = {
            "width": str(image.width),
            "height": str(image.height),
            "format": image.format,
            "color_mode": image.mode,
        }

        image_exif = image.getexif()
        exif_info = {}
        for tag, value in image_exif.items():
            key = Base(tag).name
            exif_info[key] = value

        image_data = {"common_info": common_info, "exif_info": exif_info}
        return "image", image_data


class PdfResearcher(Researcher):
    """
    A researcher for PDF files.
    """

    def get_file_info(self, file_path: str) -> tuple[str, dict]:
        reader = PdfReader(file_path)
        pages_count = len(reader.pages)
        metadata = reader.metadata

        pdf_info = {
            "author": metadata.author if metadata.author else "-",
            "title": metadata.title if metadata.title else "-",
            "pages_count": pages_count if pages_count else "-",
            "subject": metadata.subject if metadata.subject else "-",
            "creator": metadata.creator if metadata.creator else "-",
            "producer": metadata.producer if metadata.producer else "-",
        }

        return "pdf", pdf_info


class VideoResearcher(Researcher):
    """
    A researcher for video files.
    """

    def get_file_info(self, file_path: str) -> tuple[str, dict]:
        probe = ffmpeg.probe(file_path)

        video_info = probe.get("format", None)
        return "video", video_info


class AudioResearcher(Researcher):
    """
    A researcher for audio files.
    """

    def get_file_info(self, file_path: str) -> tuple[str, dict]:
        probe = ffmpeg.probe(file_path)

        audio_info = probe.get("format", None)
        return "audio", audio_info
