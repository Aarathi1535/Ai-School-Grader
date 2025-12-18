# ocr_azure.py
import fitz  # PyMuPDF
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from config import AZURE_ENDPOINT, AZURE_KEY

client = ImageAnalysisClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)

def ocr_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Render PDF pages to images via PyMuPDF and run Azure OCR.
    Returns plain text (lines joined with newlines).
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_text = []

    for page in doc:
        # 2x zoom is usually enough; tweak if needed.
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("jpeg")

        result = client.analyze(
            image_data=img_bytes,
            visual_features=[VisualFeatures.READ]
        )
        if result.read:
            for block in result.read.blocks:
                for line in block.lines:
                    all_text.append(line.text)

    doc.close()
    return "\n".join(all_text)
