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
    Render PDF pages to images and run Azure OCR.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    lines = []
    for page in doc:
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("jpeg")

        result = client.analyze(
            image_data=img_bytes,
            visual_features=[VisualFeatures.READ],
        )
        if result.read:
            for block in result.read.blocks:
                for line in block.lines:
                    lines.append(line.text)
    doc.close()
    return "\n".join(lines)
