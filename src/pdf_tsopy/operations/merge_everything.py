"""
operations/merge_everything.py — Συγχώνευση πολλών αρχείων σε ένα PDF
=====================================================================
Δέχεται PDF, Word, Excel, PowerPoint, εικόνες και τα ενώνει σε ένα PDF.
"""
from pathlib import Path
import pymupdf
from PIL import Image
import tempfile
import os
import subprocess  # nosec B404
import logging

logger = logging.getLogger(__name__)

# Υποστηριζόμενοι τύποι
PDF_EXTS = {".pdf"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"}
OFFICE_EXTS = {".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".ods", ".odp"}


def _convert_office_to_pdf(input_path: Path, output_dir: Path) -> Path:
    """Μετατρέπει ένα αρχείο Office σε PDF (χρησιμοποιεί Word/LibreOffice)."""
    try:
        from docx2pdf import convert
        if input_path.suffix.lower() in {".docx", ".doc"}:
            output_path = output_dir / f"{input_path.stem}.pdf"
            convert(str(input_path), str(output_path))
            return output_path
    except ImportError:
        pass
    except Exception as exc:
        logger.warning(
            "docx2pdf απέτυχε για %s: %s — δοκιμή LibreOffice", input_path, exc
        )

    soffice = None
    for path in [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]:
        if Path(path).exists():
            soffice = path
            break
    if not soffice:
        raise RuntimeError("Δεν βρέθηκε Microsoft Office ή LibreOffice για μετατροπή.")

    if not input_path.is_file():
        raise FileNotFoundError(f"Input not found: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{input_path.stem}.pdf"
    subprocess.run(  # nosec B603
        [
            soffice, "--headless", "--convert-to", "pdf",
            "--outdir", str(output_dir), str(input_path),
        ],
        check=True,
        capture_output=True,
    )
    if not output_path.exists():
        raise RuntimeError(f"Το LibreOffice δεν παρήγαγε: {output_path}")
    return output_path


def _image_to_pdf(input_path: Path, output_dir: Path) -> Path:
    """Μετατρέπει μια εικόνα σε PDF."""
    output_path = output_dir / f"{input_path.stem}.pdf"
    with Image.open(input_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(str(output_path), "PDF", resolution=300.0)
    return output_path


def merge_everything(file_paths: list[Path], output_path: Path) -> None:
    """Συγχωνεύει οποιαδήποτε αρχεία (PDF, Office, εικόνες) σε ένα PDF."""
    if not file_paths:
        raise ValueError("Δεν δόθηκαν αρχεία.")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        pdf_files = []

        for fp in file_paths:
            suffix = fp.suffix.lower()
            if suffix in PDF_EXTS:
                pdf_files.append(fp)
            elif suffix in IMAGE_EXTS:
                pdf_files.append(_image_to_pdf(fp, tmp_dir))
            elif suffix in OFFICE_EXTS:
                pdf_files.append(_convert_office_to_pdf(fp, tmp_dir))
            else:
                raise ValueError(f"Μη υποστηριζόμενος τύπος: {fp.suffix}")

        merged = pymupdf.open()
        for pdf in pdf_files:
            doc = pymupdf.open(str(pdf))
            merged.insert_pdf(doc)
            doc.close()

        merged.save(str(output_path))
        merged.close()