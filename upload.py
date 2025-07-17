
import os
import shutil

def upload_pdf(source_path, dest_folder='upload_files'):
    """
    Uploads a PDF file to the specified destination folder.
    Args:
        source_path (str): Path to the source PDF file.
        dest_folder (str): Folder where the PDF will be uploaded.
    Returns:
        str: Path to the uploaded PDF file.
    """
    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
    if not source_path.lower().endswith('.pdf'):
        raise ValueError("Only PDF files are allowed.")
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(source_path)
    dest_path = os.path.join(dest_folder, filename)
    shutil.copy2(source_path, dest_path)
    return dest_path
