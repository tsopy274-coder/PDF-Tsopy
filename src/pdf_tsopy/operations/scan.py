"""
operations/scan.py — Acquisition depuis un scanner
==================================================
Version qui lance le logiciel Canon IJ Scan Utility (qui gère
parfaitement le chargeur automatique de documents - ADF).
"""
from __future__ import annotations

import os
import subprocess  # nosec
import sys
import time
from pathlib import Path


class ScanNotSupportedError(RuntimeError):
    """Le système d'exploitation ne supporte pas la numérisation."""


class NoScannerFoundError(RuntimeError):
    """Aucun scanner détecté sur le poste."""


# Chemin vers IJ Scan Utility
IJ_SCAN_UTILITY = Path(r"C:\Program Files (x86)\Canon\IJ Scan Utility\SCANUTILITY.exe")

# Dossier surveillé pour le PDF résultant (là où IJ Scan Utility enregistre par défaut)
# Modifie ce chemin si nécessaire !
# Χρήση του φακέλου "Documents" του τρέχοντος χρήστη για συμβατότητα με άλλους υπολογιστές
DEFAULT_SCAN_DIR = Path.home() / "Documents" / "Scan"


def _require_windows() -> None:
    if sys.platform != "win32":
        raise ScanNotSupportedError(
            "La numérisation n'est disponible que sous Windows."
        )


def scan_to_pdf(tmp_dir: Path | None = None) -> Path | None:
    """
    Lance IJ Scan Utility. L'utilisateur scanne manuellement, puis on
    cherche le PDF le plus récent dans le dossier de sortie.
    """
    _require_windows()

    # Vérifie que IJ Scan Utility existe
    if not IJ_SCAN_UTILITY.exists():
        raise NoScannerFoundError(
            f"IJ Scan Utility introuvable :\n{IJ_SCAN_UTILITY}\n\n"
            "Installez Canon IJ Scan Utility depuis le site de Canon."
        )

    # Dossier à surveiller
    if tmp_dir is None:
        tmp_dir = DEFAULT_SCAN_DIR
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Enregistre les PDF existants AVANT la numérisation
    existing_pdfs = {p: p.stat().st_mtime for p in tmp_dir.glob("*.pdf")}

    # Lance IJ Scan Utility
    try:
        subprocess.Popen([str(IJ_SCAN_UTILITY)], shell=False)    # nosec
    except Exception as e:
        raise RuntimeError(f"Impossible de lancer IJ Scan Utility : {e}")

    # Attend que l'utilisateur scanne (max 5 minutes)
    timeout = 300
    start = time.time()
    new_pdf = None

    while time.time() - start < timeout:
        time.sleep(2)

        # Cherche un nouveau PDF dans le dossier
        for p in tmp_dir.glob("*.pdf"):
            if p not in existing_pdfs:
                # Vérifie qu'il est stable (pas en cours d'écriture)
                size1 = p.stat().st_size
                time.sleep(1)
                size2 = p.stat().st_size
                if size1 == size2 and size1 > 0:
                    new_pdf = p
                    break

        if new_pdf:
            break

    if new_pdf is None:
        return None  # annulation ou timeout

    return new_pdf


def scan_image(tmp_dir: Path | None = None) -> Path | None:
    """Compatibilité — délègue à scan_to_pdf()."""
    return scan_to_pdf(tmp_dir=tmp_dir)


def image_to_pdf(image_path: Path, pdf_path: Path | None = None) -> Path:
    """Convertit une image (JPG/PNG/…) en PDF d'une page."""
    from PIL import Image

    if pdf_path is None:
        pdf_path = image_path.with_suffix(".pdf")

    with Image.open(image_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(str(pdf_path), "PDF", resolution=300.0)

    return pdf_path


def list_scanners() -> list[dict]:
    """Retourne la liste des scanners WIA détectés (compatibilité)."""
    _require_windows()
    import win32com.client

    manager = win32com.client.Dispatch("WIA.DeviceManager")
    scanners: list[dict] = []
    for i in range(1, manager.DeviceInfos.Count + 1):
        info = manager.DeviceInfos.Item(i)
        if info.Type == 1:
            scanners.append({
                "name": str(info.Properties("Name").Value),
                "device_id": str(info.DeviceID),
            })
    return scanners
