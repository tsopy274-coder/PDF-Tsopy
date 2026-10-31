"""
ui/scanner_dialog.py — Διάλογος επιλογής σαρωτή
================================================
Δείχνει λίστα με όλους τους διαθέσιμους σαρωτές (WIA) και
επιτρέπει σάρωση απευθείας ή άνοιγμα του IJ Scan Utility.
"""
from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QMessageBox,
)
from PyQt6.QtCore import Qt


class ScannerDialog(QDialog):
    """Διάλογος επιλογής σαρωτή."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Επιλογή σαρωτή"))
        self.setMinimumSize(500, 350)
        self.setStyleSheet("""
            QDialog { background: #2D2D2D; }
            QLabel { color: #F0F0F0; font-size: 12px; }
            QListWidget {
                background: #1E1E1E;
                color: #F0F0F0;
                border: 1px solid #3A3A3A;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background: #6BBF4E;
                color: #FFFFFF;
            }
            QListWidget::item:hover {
                background: #3A3A3A;
            }
            QPushButton {
                background: #3A3A3A;
                color: #F0F0F0;
                border: 1px solid #4A4A4A;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #4A4A4A;
                border-color: #6BBF4E;
            }
            QPushButton:default {
                background: #6BBF4E;
                border-color: #6BBF4E;
                color: #FFFFFF;
            }
            QPushButton:default:hover {
                background: #7FCF5E;
            }
        """)

        self.selected_scanner = None

        # ── Layout ─────────────────────────────────────────────
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Τίτλος
        title = QLabel(self.tr("Διαθέσιμοι σαρωτές:"))
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Λίστα σαρωτών
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Κουμπιά
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_scan_wia = QPushButton(self.tr("Σάρωση (WIA)"))
        self.btn_scan_wia.setToolTip(
            self.tr("Άμεση σάρωση μέσω WIA — δουλεύει με USB σαρωτές")
        )
        self.btn_scan_wia.clicked.connect(self._scan_wia)
        self.btn_scan_wia.setEnabled(False)
        btn_layout.addWidget(self.btn_scan_wia)

        self.btn_scan_ij = QPushButton(self.tr("IJ Scan Utility"))
        self.btn_scan_ij.setToolTip(
            self.tr("Άνοιγμα του Canon IJ Scan Utility — δουλεύει με ADF")
        )
        self.btn_scan_ij.clicked.connect(self._scan_ij)
        btn_layout.addWidget(self.btn_scan_ij)

        btn_layout.addStretch()

        self.btn_cancel = QPushButton(self.tr("Άκυρο"))
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)

        # ── Φόρτωση σαρωτών ────────────────────────────────────
        self._load_scanners()

        # ── Σύνδεση σήματος ────────────────────────────────────
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self.list_widget.itemDoubleClicked.connect(self._on_double_click)

    def _load_scanners(self):
        """Φορτώνει τη λίστα με τους διαθέσιμους σαρωτές."""
        self.list_widget.clear()

        try:
            from pdf_tsopy.operations.scan import list_scanners
            scanners = list_scanners()
        except Exception as e:
            self.list_widget.addItem(
                self.tr(f"⚠ Σφάλμα φόρτωσης: {e}")
            )
            return

        if not scanners:
            item = QListWidgetItem(
                self.tr("⚠ Δεν βρέθηκε σαρωτής")
            )
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.list_widget.addItem(item)
            return

        for s in scanners:
            name = s.get("name", "Άγνωστος σαρωτής")
            item = QListWidgetItem(f"🖨  {name}")
            item.setData(Qt.ItemDataRole.UserRole, s)
            self.list_widget.addItem(item)

        # Επίλεξε τον πρώτο
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _on_selection_changed(self):
        """Ενεργοποιεί το κουμπί σάρωσης όταν επιλεγεί σαρωτής."""
        has_selection = self.list_widget.currentItem() is not None
        self.btn_scan_wia.setEnabled(has_selection)

    def _on_double_click(self, item: QListWidgetItem):
        """Διπλό κλικ → άμεση σάρωση WIA."""
        self._scan_wia()

    def _scan_wia(self):
        """Σαρώνει με τον επιλεγμένο σαρωτή μέσω WIA."""
        item = self.list_widget.currentItem()
        if not item:
            return

        scanner = item.data(Qt.ItemDataRole.UserRole)
        if not scanner:
            return

        self.selected_scanner = scanner

        # Έλεγξε αν είναι Canon (δικτυακός) — προειδοποίηση
        name = scanner.get("name", "").lower()
        if "canon" in name:
            reply = QMessageBox.question(
                self,
                self.tr("Προσοχή"),
                self.tr(
                    "Ο σαρωτής Canon μπορεί να μην υποστηρίζει ADF μέσω WIA.\n\n"
                    "Αν κολλήσει, χρησιμοποίησε το κουμπί «IJ Scan Utility».\n\n"
                    "Θέλεις να συνεχίσεις με WIA;"
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.accept()

    def _scan_ij(self):
        """Ανοίγει το IJ Scan Utility."""
        from PyQt6.QtCore import QProcess
        from pathlib import Path

        ij_path = Path(r"C:\Program Files (x86)\Canon\IJ Scan Utility\SCANUTILITY.exe")

        if not ij_path.exists():
            QMessageBox.warning(
                self,
                self.tr("IJ Scan Utility"),
                self.tr(
                    "Το IJ Scan Utility δεν βρέθηκε:\n"
                    f"{ij_path}\n\n"
                    "Εγκατέστησέ το από το site της Canon."
                ),
            )
            return

        QProcess.startDetached(str(ij_path))
        self.reject()