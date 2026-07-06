import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings

UPLOAD_FOLDER = settings.upload_dir


def save_pdf(file: UploadFile):
    """
    Save uploaded PDF to the uploads folder.

    Returns:
        filename: Stored filename
        file_path: Full path of the saved file
    """

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = f"{uuid4()}_{file.filename}"

    file_path = os.path.join(UPLOAD_FOLDER,filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return filename, file_path