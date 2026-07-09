import hashlib
import os
import shutil
import uuid
from pathlib import Path
from app.core.constants import FileType

from fastapi import UploadFile


class FileUtils:

    STORAGE_ROOT = "/storage"

    AUDIO_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".flac",
        ".ogg",
        ".aac",
        ".m4a"
    }

    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".txt"
    }

    @staticmethod
    def generate_uuid():

        return str(uuid.uuid4())

    @staticmethod
    def get_extension(filename: str):

        return Path(filename).suffix.lower()

    @staticmethod
    def get_file_type(extension: str):

       if extension in FileUtils.AUDIO_EXTENSIONS:
        return FileType.AUDIO

       if extension in FileUtils.DOCUMENT_EXTENSIONS:
        return FileType.DOCUMENT

       return None

    @staticmethod
    def calculate_sha256(file_path: str):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):

                sha256.update(chunk)

        return sha256.hexdigest()

    @staticmethod
    def create_directory(directory: str):

        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def save_file(upload_file: UploadFile, destination: str):

        with open(destination, "wb") as buffer:

            shutil.copyfileobj(upload_file.file, buffer)

    @staticmethod
    def calculate_upload_sha256(upload_file: UploadFile):

       sha256 = hashlib.sha256()

       upload_file.file.seek(0)

       while chunk := upload_file.file.read(4096):
          sha256.update(chunk)

       upload_file.file.seek(0)

       return sha256.hexdigest()