import os

from fastapi import UploadFile, HTTPException

from app.kafka.producer import kafka_producer
from app.kafka.topics import DOCUMENT_UPLOADED

from app.core.constants import DocumentStatus, FileType
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_schema import DocumentSchema
from app.utils.file_utils import FileUtils


class UploadService:

    def __init__(self):
        self.repository = DocumentRepository()

    async def upload(self, file: UploadFile):

        print("========== STEP 1 : UploadService started ==========")

        # Vérifier l'extension
        extension = FileUtils.get_extension(file.filename)

        # Déterminer le type du fichier
        file_type = FileUtils.get_file_type(extension)

        if file_type is None:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type."
            )

        print("========== STEP 2 : File type detected ==========")

        # Calcul du SHA256
        sha256 = FileUtils.calculate_upload_sha256(file)

        # Vérifier les doublons
        existing_document = await self.repository.get_by_sha256(sha256)

        if existing_document:
            raise HTTPException(
                status_code=409,
                detail="This file already exists."
            )

        print("========== STEP 3 : SHA256 OK ==========")

        # Générer un nom unique
        file_uuid = FileUtils.generate_uuid()

        stored_filename = f"{file_uuid}{extension}"

        # Choisir le dossier
        if file_type == FileType.AUDIO:
            folder = "/storage/audio/original"
        else:
            folder = "/storage/documents"

        FileUtils.create_directory(folder)

        storage_path = os.path.join(folder, stored_filename)

        # Sauvegarder le fichier
        FileUtils.save_file(file, storage_path)

        file_size = os.path.getsize(storage_path)

        print("========== STEP 4 : File saved ==========")

        # Construire le document MongoDB
        document = DocumentSchema(

            title=os.path.splitext(file.filename)[0],

            original_filename=file.filename,

            stored_filename=stored_filename,

            storage_path=storage_path,

            file_type=file_type,

            mime_type=file.content_type,

            file_size=file_size,

            sha256=sha256,

            status=DocumentStatus.UPLOADED

        )

        # Enregistrer dans MongoDB
        document_id = await self.repository.create(
            document.model_dump()
        )

        print("========== STEP 5 : Saved in MongoDB ==========")

        print("========== STEP 6 : Sending to Kafka ==========")

        await kafka_producer.send(
            DOCUMENT_UPLOADED,
            {
                "document_id": document_id,
                "file_type": file_type,
                "storage_path": storage_path
            }
        )

        print("========== STEP 7 : Kafka message sent ==========")

        return document_id