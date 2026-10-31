"""
ui/about_dialog.py — Παράθυρο «Σχετικά με το HarisPDF»
=======================================================
Εμφανίζει πληροφορίες για την εφαρμογή σε 3 γλώσσες.
"""
from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont


# ── Κείμενα σε 3 γλώσσες ────────────────────────────────────────────────
TEXTS = {
    "el": {
        "title": "HarisPDF — Έκδοση 1.0",
        "author": "Ανάπτυξη / Δημιουργία: Χάρης Τσόπελας",
        "desc": "Ελαφρύ και ισχυρό εργαλείο για την επεξεργασία\nκαι οργάνωση των PDF εγγράφων σας.",
        "copyright": "Copyright © 2026 Haris Tsopelas. All rights reserved.",
        "close": "Κλείσιμο",
    },
    "en": {
        "title": "HarisPDF — Version 1.0",
        "author": "Development / Created by: Haris Tsopelas",
        "desc": "Lightweight and powerful tool for editing\nand organizing your PDF documents.",
        "copyright": "Copyright © 2026 Haris Tsopelas. All rights reserved.",
        "close": "Close",
    },
    "fr": {
        "title": "HarisPDF — Version 1.0",
        "author": "Développement / Créé par : Haris Tsopelas",
        "desc": "Outil léger et puissant pour éditer\net organiser vos documents PDF.",
        "copyright": "Copyright © 2026 Haris Tsopelas. Tous droits réservés.",
        "close": "Fermer",
    },
}


def _get_lang() -> str:
    """Επιστρέφει την τρέχουσα γλώσσα (el, en, fr)."""
    try:
        from pdf_tsopy.i18n import current_lang
        lang = current_lang()
        if lang in TEXTS:
            return lang
    except Exception:    # nosec
            pass
    return "el"  # προεπιλογή


class AboutDialog(QDialog):
    """Παράθυρο «Σχετικά με το HarisPDF»."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # ── Γλώσσα ───────────────────────────────────────────────────────
        self.lang = _get_lang()
        txt = TEXTS[self.lang]

        self.setWindowTitle(txt["title"])
        self.setMinimumWidth(480)
        self.setStyleSheet("""
            QDialog { background: #2D2D2D; }
            QLabel { color: #F0F0F0; }
            QPushButton {
                background: #6BBF4E;
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7FCF5E;
            }
        """)

        # ── Layout ───────────────────────────────────────────────────────
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ── Logo ─────────────────────────────────────────────────────────
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            from pdf_tsopy.utils import resource_path
            for rel in ("assets/logo/PDF-by-tsopy.png",
            "assets/logo/PDF-Equilibrist-custom.png",
            "assets/logo/PDF-Equilibrist-logo.png"):
                path = resource_path(rel)
                if path.exists():
                    pix = QPixmap(str(path))
                    if not pix.isNull():
                        pix = pix.scaled(
                            96, 96,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                        logo_label.setPixmap(pix)
                    break
        except Exception:  # nosec
            pass

        layout.addWidget(logo_label)

        # ── Τίτλος ───────────────────────────────────────────────────────
        title_label = QLabel(txt["title"])
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #6BBF4E;")
        layout.addWidget(title_label)

        # ── Συγγραφέας ───────────────────────────────────────────────────
        author_label = QLabel(txt["author"])
        author_font = QFont("Segoe UI", 11)
        author_label.setFont(author_font)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author_label.setStyleSheet("color: #CCCCCC;")
        layout.addWidget(author_label)

        # ── Διαχωριστικό ─────────────────────────────────────────────────
        sep = QLabel("─" * 40)
        sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sep.setStyleSheet("color: #3A3A3A;")
        layout.addWidget(sep)

        # ── Περιγραφή ────────────────────────────────────────────────────
        desc_label = QLabel(txt["desc"])
        desc_font = QFont("Segoe UI", 10)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #E0E0E0; line-height: 140%;")
        layout.addWidget(desc_label)

        # ── Κενό ─────────────────────────────────────────────────────────
        layout.addSpacing(10)

        # ── Copyright ────────────────────────────────────────────────────
        copy_label = QLabel(txt["copyright"])
        copy_font = QFont("Segoe UI", 9)
        copy_label.setFont(copy_font)
        copy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copy_label.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(copy_label)

        # ── Κουμπί κλεισίματος ───────────────────────────────────────────
        layout.addSpacing(10)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_close = QPushButton(txt["close"])
        btn_close.setDefault(True)
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)