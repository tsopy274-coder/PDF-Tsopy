"""
ui/scan_job.py — Thread de numérisation
=======================================
Exécute ``scan_to_pdf()`` dans un ``QThread`` pour éviter de figer
l'interface pendant que le dialogue du pilote de scanner est ouvert.

Signaux
-------
- ``finished_ok(Path)``  : PDF produit avec succès.
- ``cancelled()``        : l'utilisateur a annulé la numérisation.
- ``failed(str)``        : erreur (pas de scanner, driver, etc.).
"""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal


class ScanJob(QThread):
    finished_ok = pyqtSignal(Path)
    cancelled = pyqtSignal()
    failed = pyqtSignal(str)

    def run(self) -> None:
        try:
            from pdf_tsopy.operations.scan import (
                NoScannerFoundError,
                ScanNotSupportedError,
                scan_to_pdf,
            )
        except Exception as exc:
            self.failed.emit(f"Impossible de charger le module scan : {exc}")
            return

        try:
            pdf_path = scan_to_pdf()
        except (NoScannerFoundError, ScanNotSupportedError) as exc:
            self.failed.emit(str(exc))
            return
        except Exception as exc:
            self.failed.emit(f"Erreur de numérisation : {exc}")
            return

        if pdf_path is None:
            self.cancelled.emit()
        else:
            self.finished_ok.emit(pdf_path)