"""Splash screen PyQt6 — fond transparent + barre verte + signature."""
from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QLabel, QProgressBar, QVBoxLayout, QApplication
from PyQt6.QtGui import QPixmap, QColor, QPalette
from PyQt6.QtCore import Qt
from pdf_tsopy.utils import resource_path

ACCENT   = "#6BBF4E"
W, H     = 600, 338   # taille fixe = même que splash PyInstaller
OVERLAY  = 74         # hauteur de la bande bas (augmentée pour la signature)


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SplashScreen
        )
        self.setFixedSize(W, H)

        # ── Fond transparent (plus de noir) ──────────────────────────────────
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)

        # ── Image de fond ─────────────────────────────────────────────────────
        bg = QLabel(self)
        bg.setGeometry(0, 0, W, H)
        bg.setStyleSheet("background: transparent;")
        pix = QPixmap()
        for rel in ("assets/splash.png", "assets/Splashscreen.jpg",
                    "assets/Splashscreen.png"):
            path = resource_path(rel)
            if path.exists():
                pix.load(str(path))
                break
        if not pix.isNull():
            pix = pix.scaled(W, H,
                             Qt.AspectRatioMode.IgnoreAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)
            bg.setPixmap(pix)

        # ── Overlay bas (ημιδιαφανές) ─────────────────────────────────────────
        overlay = QWidget(self)
        overlay.setGeometry(0, H - OVERLAY, W, OVERLAY)
        overlay.setStyleSheet("background: rgba(10,10,10,180);")

        ov = QVBoxLayout(overlay)
        ov.setContentsMargins(14, 6, 14, 10)
        ov.setSpacing(5)

        # ── Υπογραφή δημιουργού ───────────────────────────────────────────────
        self._author = QLabel("By Tsopy")
        self._author.setStyleSheet(
            "color: #FFFFFF; font-family:'Segoe UI'; font-size:10px;"
            "font-style:italic; background:transparent;")
        self._author.setAlignment(Qt.AlignmentFlag.AlignRight)
        ov.addWidget(self._author)

        self._status = QLabel(self.tr("Initialisation…"))
        self._status.setStyleSheet(
            f"color: {ACCENT}; font-family:'Segoe UI'; font-size:11px;"
            "background:transparent;")
        ov.addWidget(self._status)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(7)
        self._bar.setStyleSheet(f"""
            QProgressBar {{
                background:#2A2A2A; border:none; border-radius:3px;
            }}
            QProgressBar::chunk {{
                background:{ACCENT}; border-radius:3px;
            }}
        """)
        ov.addWidget(self._bar)

        self._center()

    def _center(self):
        geo = QApplication.primaryScreen().availableGeometry()
        self.move(geo.center().x() - W // 2,
                  geo.center().y() - H // 2)

    def set_progress(self, value: int, text: str = ""):
        self._bar.setValue(max(0, min(value, 100)))
        if text:
            self._status.setText(text)
        QApplication.processEvents()