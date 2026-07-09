from enum import Enum


class FileType(str, Enum):
    AUDIO = "audio"
    DOCUMENT = "document"


class ProcessingStatus:

    def __init__(self):

        self.transcription = False

        self.summary = False

        self.embedding = False

        self.indexation = False

        self.fingerprint = False