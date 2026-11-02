"""
ui/main_window.py — Fenêtre principale de PDF-Equilibrist
==========================================================
Ce module contient ``MainWindow``, le widget racine de l'application.

Fenêtre frameless
-----------------
``MainWindow`` hérite de ``QWidget`` (et non ``QMainWindow``) avec le flag
``FramelessWindowHint``. Cela supprime la barre de titre et les bordures
système pour permettre un design personnalisé :

- ``TitleBar`` custom en haut (logo, onglets documents, contrôles fenêtre)
- Bordure 1px dessinée dans ``paintEvent``
- Déplacement via ``TitleBar.mousePressEvent`` → ``startSystemMove()``
- Redimensionnement via ``mousePressEvent`` sur les bords → ``startSystemResize()``

Gestion multi-documents
------------------------
``MainWindow`` maintient une liste de ``Document`` (un par onglet ouvert).

Ribbon
------
Le ribbon est implémenté avec ``QTabBar`` + ``QStackedWidget`` séparés.

Résolution des chemins
-----------------------
Le viewer et le panneau miniatures accèdent aux assets via ``resource_path()``
de ``utils.py`` pour la compatibilité dev/exe PyInstaller.
"""
from __future__ import annotations
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTabBar, QStackedWidget, QFileDialog, QLabel, QSplitter,
)
from PyQt6.QtGui import QAction, QKeySequence, QColor, QPainter, QPen, QActionGroup
from PyQt6.QtCore import Qt, QPoint, QSettings, QThread, pyqtSignal

from pdf_tsopy.ui.title_bar import TitleBar
from pdf_tsopy.ui.tabs.tab_afficher  import TabAfficher
from pdf_tsopy.ui.tabs.tab_modifier  import TabModifier
from pdf_tsopy.ui.tabs.tab_convertir import TabConvertir
from pdf_tsopy.ui.tabs.tab_annoter   import TabAnnoter
from pdf_tsopy.ui.tabs.tab_page      import TabPage
from pdf_tsopy.ui.tabs.tab_proteger  import TabProteger
from pdf_tsopy.ui.viewer             import PdfViewer
from pdf_tsopy.ui.thumbnail_panel    import ThumbnailPanel
from pdf_tsopy.ui.dialogs            import ensure_suffix
from pdf_tsopy.core.document         import Document
from pdf_tsopy.ui.scan_job           import ScanJob

_RECENT_MAX = 10   # nombre maximum de fichiers dans "Ouvrir récemment"

ACCENT       = "#6BBF4E"
BORDER_COLOR = "#2A2A2A"
RESIZE_MARGIN = 6

TABBAR_STYLE = """
QTabBar { background: #1A1A1A; padding: 3px 4px 0 4px; }
QTabBar::tab {
    background: transparent; color: #888888;
    padding: 5px 18px; border: none;
    border-radius: 5px 5px 0 0;
    font-size: 12px; font-family: "Segoe UI"; margin-right: 2px;
}
QTabBar::tab:selected { background: #2D2D2D; color: #F0F0F0; }
QTabBar::tab:hover:!selected { background: #242424; color: #C0C0C0; }
"""


class _StartupUpdateCheckThread(QThread):
    """Vérifie en arrière-plan si une nouvelle version est disponible."""
    found = pyqtSignal(object)

    def run(self):
        try:
            from pdf_tsopy import __version__
            from pdf_tsopy import update as updater
            release = updater.get_latest_release_info(__version__)
        except Exception:
            release = None
        self.found.emit(release)


class MainWindow(QWidget):
    """
    Fenêtre principale frameless de PDF-Equilibrist.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("By Tsopy")
        self.resize(1280, 800)
        self.setMinimumSize(800, 600)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        self._documents: list[Document] = []
        self._active_idx = -1

        self._title_bar = TitleBar(self)
        self._title_bar.minimize_requested.connect(self.showMinimized)
        self._title_bar.maximize_requested.connect(self._toggle_maximize)
        self._title_bar.close_requested.connect(self.close)
        self._title_bar.new_tab_requested.connect(self._open_file_dialog)
        self._title_bar.tab_close_requested.connect(self._close_tab)
        self._title_bar.tab_changed.connect(self._switch_to)

        self._current_doc = Document()
        self.viewer  = PdfViewer(self._current_doc)
        self._thumbs = ThumbnailPanel(self._current_doc, self.viewer)
        self._thumbs.width_changed.connect(self._on_thumbs_width_changed)
        self.viewer.open_pdf_requested.connect(self._open_document)
        self._thumbs.open_pdf_requested.connect(self._open_document)

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.addWidget(self._thumbs)
        self._splitter.addWidget(self.viewer)
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setHandleWidth(1)
        self._splitter.setStyleSheet("QSplitter::handle { background: #3A3A3A; }")

        TABBAR_H = 30
        STACK_H  = 84
        RIBBON_H = TABBAR_H + STACK_H

        self._ribbon_tabbar = QTabBar()
        self._ribbon_tabbar.setStyleSheet(TABBAR_STYLE)
        self._ribbon_tabbar.setExpanding(False)
        self._ribbon_tabbar.setDrawBase(False)
        self._ribbon_tabbar.setFixedHeight(TABBAR_H)

        self._ribbon_stack = QStackedWidget()
        self._ribbon_stack.setFixedHeight(STACK_H)
        self._ribbon_stack.setStyleSheet("background: #2D2D2D;")

        self._tab_afficher  = TabAfficher(self._current_doc, self.viewer)
        self._tab_modifier  = TabModifier(self._current_doc, self.viewer)
        self._tab_convertir = TabConvertir(self._current_doc)
        self._tab_annoter   = TabAnnoter(self._current_doc, self.viewer)
        self._tab_page      = TabPage(self._current_doc, self.viewer)
        self._tab_proteger  = TabProteger(self._current_doc)

        for name, widget in [
            (self.tr("Afficher"),  self._tab_afficher),
            (self.tr("Modifier"),  self._tab_modifier),
            (self.tr("Convertir"), self._tab_convertir),
            (self.tr("Annoter"),   self._tab_annoter),
            (self.tr("Page"),      self._tab_page),
            (self.tr("Protéger"),  self._tab_proteger),
        ]:
            self._ribbon_tabbar.addTab(name)
            widget.setStyleSheet("background: #2D2D2D;")
            self._ribbon_stack.addWidget(widget)

        self._ribbon_tabbar.currentChanged.connect(self._ribbon_stack.setCurrentIndex)

        ribbon = QWidget()
        ribbon.setStyleSheet("background: #1A1A1A; border-bottom: 1px solid #333;")
        ribbon.setFixedHeight(RIBBON_H)
        r_layout = QVBoxLayout(ribbon)
        r_layout.setContentsMargins(0, 0, 0, 0)
        r_layout.setSpacing(0)
        r_layout.addWidget(self._ribbon_tabbar)
        sc = QWidget()
        sc.setStyleSheet("background: #2D2D2D;")
        sc_l = QHBoxLayout(sc)
        sc_l.setContentsMargins(0, 0, 0, 0)
        sc_l.addWidget(self._ribbon_stack)
        r_layout.addWidget(sc)

        self._menu_bar = self._build_menu_bar()

        self._status_file = QLabel(self.tr("Aucun document ouvert"))
        self._status_page = QLabel("")
        status = QWidget()
        status.setFixedHeight(22)
        status.setStyleSheet(
            "background: #141414; border-top: 1px solid #2A2A2A;")
        sl = QHBoxLayout(status)
        sl.setContentsMargins(8, 0, 8, 0)
        self._status_net = QLabel("")
        sl.addWidget(self._status_file)
        sl.addStretch()
        sl.addWidget(self._status_net)
        sl.addSpacing(12)
        sl.addWidget(self._status_page)
        self._status_file.setStyleSheet("color: #666666; font-size: 11px;")
        self._status_net.setStyleSheet("color: #6BBF4E; font-size: 11px;")
        self._status_page.setStyleSheet("color: #666666; font-size: 11px;")

        from pdf_tsopy.ui.search_bar import SearchBar
        self._search_bar = SearchBar(self.viewer)
        self._search_bar.hide()

        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)
        root.addWidget(self._title_bar)
        root.addWidget(self._menu_bar)
        root.addWidget(ribbon)
        root.addWidget(self._search_bar)
        root.addWidget(self._splitter, 1)
        root.addWidget(status)

        self._set_ribbon_enabled(False)
        self._resize_edge = ""
        self.setAcceptDrops(True)
        self._current_doc.changed.connect(self._on_doc_changed)

        self._max_btn_rect_screen = None

    def showEvent(self, event):
        super().showEvent(event)
        self.setAcceptDrops(True)
        if sys.platform == "win32":
            self._apply_win32_styles()

    def _apply_win32_styles(self):
        try:
            import ctypes
            hwnd = int(self.winId())
            GWL_STYLE    = -16
            WS_THICKFRAME  = 0x00040000
            WS_MAXIMIZEBOX = 0x00010000
            WS_MINIMIZEBOX = 0x00020000
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style |= WS_THICKFRAME | WS_MAXIMIZEBOX | WS_MINIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            SWP_FLAGS = 0x0027
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP_FLAGS)
        except Exception:  # nosec B110
            pass

    def keyPressEvent(self, event):
        from PyQt6.QtCore import Qt as _Qt
        mods = event.modifiers()
        ctrl = _Qt.KeyboardModifier.ControlModifier
        if event.key() == _Qt.Key.Key_P and mods == ctrl:
            self._print()
        elif event.key() == _Qt.Key.Key_Z and mods == ctrl:
            self._undo()
        elif event.key() == _Qt.Key.Key_F and mods == ctrl:
            self._search_bar.toggle()
        else:
            super().keyPressEvent(event)

    def _print(self):
        if not self._current_doc.is_open:
            return
        from pdf_tsopy.ui.print_dialog import print_document
        print_document(self._current_doc, self)

    def _undo(self):
        if self._current_doc.undo():
            self.viewer.clear_search()

    def _build_menu_bar(self) -> QWidget:
        from PyQt6.QtWidgets import QMenuBar
        mb = QMenuBar()
        mb.setStyleSheet("""
            QMenuBar { background:#1A1A1A; color:#AAAAAA;
                       border-bottom:1px solid #2A2A2A; padding:2px 0; }
            QMenuBar::item:selected { background:#2D2D2D; color:#FFFFFF; }
            QMenu { background:#2D2D2D; color:#F0F0F0; border:1px solid #3A3A3A; }
            QMenu::item:selected { background:#3A3A3A; }
            QMenu::separator { height:1px; background:#3A3A3A; margin:3px 0; }
        """)

        fichier = mb.addMenu(self.tr("Fichier"))

        # ── ΕΠΙΛΟΓΗ 1: Συγχώνευση όλων σε PDF (νέα λειτουργία) ────────────────
        act_merge_all = QAction(self.tr("Συγχώνευση όλων σε PDF…"), self)
        act_merge_all.setShortcut(QKeySequence("Ctrl+M"))
        act_merge_all.triggered.connect(self._merge_everything)
        fichier.addAction(act_merge_all)

        # ── ΕΠΙΛΟΓΗ 2: Οι υπάρχουσες λειτουργίες (PDF merge, Office→PDF, Img→PDF) ──
        # Οι επιλογές αυτές βρίσκονται ήδη στις καρτέλες "Convertir" και "Page".
        # Εδώ προσθέτουμε συντομεύσεις για ευκολία.
        act_merge_pdf = QAction(self.tr("Συγχώνευση PDF…"), self)
        act_merge_pdf.triggered.connect(self._merge_pdfs_only)
        fichier.addAction(act_merge_pdf)

        fichier.addSeparator()

        # ── Numérisation ─────────────────────────────────────────────────────
        act_scan = QAction(self.tr("Numériser…"), self)
        act_scan.setShortcut(QKeySequence("Ctrl+Shift+N"))
        act_scan.triggered.connect(self._scan_document)
        fichier.addAction(act_scan)

        act_scanner = QAction(self.tr("Επιλογή σαρωτή…"), self)
        act_scanner.triggered.connect(self._choose_scanner)
        fichier.addAction(act_scanner)
        fichier.addSeparator()

        act_open = QAction(self.tr("Ouvrir…"), self)
        act_open.setShortcut(QKeySequence.StandardKey.Open)
        act_open.triggered.connect(self._open_file_dialog)
        fichier.addAction(act_open)

        self._recent_menu = fichier.addMenu(self.tr("Ouvrir récemment"))
        self._rebuild_recent_menu()
        fichier.addSeparator()

        self._act_print = QAction(self.tr("Imprimer…"), self)
        self._act_print.setShortcut(QKeySequence.StandardKey.Print)
        self._act_print.triggered.connect(self._print)
        fichier.addAction(self._act_print)
        fichier.addSeparator()

        self._act_save = QAction(self.tr("Enregistrer"), self)
        self._act_save.setShortcut(QKeySequence.StandardKey.Save)
        self._act_save.triggered.connect(self._save)
        fichier.addAction(self._act_save)

        self._act_save_as = QAction(self.tr("Enregistrer sous…"), self)
        self._act_save_as.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self._act_save_as.triggered.connect(self._save_as)
        fichier.addAction(self._act_save_as)
        fichier.addSeparator()

        self._act_close_doc = QAction(self.tr("Fermer l'onglet"), self)
        self._act_close_doc.setShortcut(QKeySequence("Ctrl+W"))
        self._act_close_doc.triggered.connect(
            lambda: self._close_tab(self._active_idx))
        fichier.addAction(self._act_close_doc)
        fichier.addSeparator()

        act_quit = QAction(self.tr("Quitter"), self)
        act_quit.setShortcut(QKeySequence.StandardKey.Quit)
        act_quit.triggered.connect(self.close)
        fichier.addAction(act_quit)

        edition = mb.addMenu(self.tr("Édition"))
        self._act_undo = QAction(self.tr("Annuler"), self)
        self._act_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self._act_undo.triggered.connect(self._undo)
        self._act_undo.setEnabled(False)
        edition.addAction(self._act_undo)

        act_search = QAction(self.tr("Rechercher…"), self)
        act_search.setShortcut(QKeySequence.StandardKey.Find)
        act_search.triggered.connect(lambda: self._search_bar.toggle())
        edition.addAction(act_search)

        aide = mb.addMenu(self.tr("Aide"))
        act_updates = QAction(self.tr("Vérifier les mises à jour…"), self)
        act_updates.triggered.connect(self._check_for_updates)
        aide.addAction(act_updates)

        act_cve = QAction(self.tr("Vérifier les vulnérabilités CVE…"), self)
        act_cve.triggered.connect(self._check_for_cves)
        aide.addAction(act_cve)

        from pdf_tsopy import settings
        net_menu = aide.addMenu(self.tr("Connexions Internet"))
        self._act_block_net = QAction(self.tr("Bloquer toutes les connexions Internet"), self)
        self._act_block_net.setCheckable(True)
        self._act_block_net.setChecked(settings.network_blocked())
        self._act_block_net.toggled.connect(self._on_block_network_toggled)
        net_menu.addAction(self._act_block_net)

        self._act_startup_check = QAction(
            self.tr("Vérifier les mises à jour au démarrage (api.github.com)"), self)
        self._act_startup_check.setCheckable(True)
        self._act_startup_check.setChecked(settings.startup_update_check())
        self._act_startup_check.setEnabled(not settings.network_blocked())
        self._act_startup_check.toggled.connect(settings.set_startup_update_check)
        net_menu.addAction(self._act_startup_check)

        # ── Ρύθμιση ανάλυσης OCR (DPI) ──────────────────────────────────────
        ocr_menu = aide.addMenu(self.tr("Ανάλυση OCR (DPI)"))
        _ocr_group = QActionGroup(self)
        _ocr_group.setExclusive(True)
        _current_dpi = settings.ocr_dpi()
        for _dpi in (300, 400, 500, 600):
            _act = QAction(f"{_dpi} DPI", self)
            _act.setCheckable(True)
            _act.setChecked(_dpi == _current_dpi)
            _act.triggered.connect(lambda _checked=False, d=_dpi: settings.set_ocr_dpi(d))
            _ocr_group.addAction(_act)
            ocr_menu.addAction(_act)

        aide.addSeparator()

        from pdf_tsopy.i18n import current_lang
        _about_texts = {
            "el": "Σχετικά με το HarisPDF…",
            "en": "About HarisPDF…",
            "fr": "À propos de HarisPDF…",
        }
        _about_label = _about_texts.get(current_lang(), _about_texts["el"])
        act_about = QAction(_about_label, self)
        act_about.triggered.connect(self._show_about)
        aide.addAction(act_about)

        return mb

    def check_updates_on_startup(self):
        from pdf_tsopy import settings
        from pdf_tsopy import update as updater
        if updater.is_flatpak():
            return
        if settings.network_blocked() or not settings.startup_update_check():
            return
        self._status_net.setText(
            self.tr("Recherche de mise à jour (api.github.com)…"))
        self._startup_update_thread = _StartupUpdateCheckThread(self)
        self._startup_update_thread.found.connect(self._on_startup_update_found)
        self._startup_update_thread.start()

    def _on_startup_update_found(self, release: object | None):
        self._status_net.setText("")
        if release:
            self._check_for_updates()

    def _on_block_network_toggled(self, blocked: bool):
        from pdf_tsopy import settings
        settings.set_network_blocked(blocked)
        self._act_startup_check.setEnabled(not blocked)

    def _show_about(self):
        from pdf_tsopy.ui.about_dialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.exec()

    def _check_for_updates(self):
        try:
            from pdf_tsopy.ui.update_dialog import UpdateDialog
            dlg = UpdateDialog(self)
            dlg.exec()
        except Exception as exc:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, self.tr("Vérification des mises à jour"),
                                self.tr("Impossible d'ouvrir le dialogue de mise à jour :\n{0}").format(exc))

    def _check_for_cves(self):
        try:
            from pdf_tsopy.ui.cve_dialog import CVEDialog
            dlg = CVEDialog(self)
            dlg.exec()
        except Exception as exc:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, self.tr("Vérification CVE"),
                                self.tr("Impossible d'ouvrir le dialogue CVE :\n{0}").format(exc))

    def _add_recent(self, path: str):
        s = QSettings("PDFEquilibrist", "PDFEquilibrist")
        recents: list[str] = s.value("recent_files", []) or []
        norm = str(Path(path))
        if norm in recents:
            recents.remove(norm)
        recents.insert(0, norm)
        recents = recents[:_RECENT_MAX]
        s.setValue("recent_files", recents)
        self._rebuild_recent_menu()

    def _rebuild_recent_menu(self):
        self._recent_menu.clear()
        s = QSettings("PDFEquilibrist", "PDFEquilibrist")
        recents: list[str] = s.value("recent_files", []) or []
        recents = [r for r in recents if Path(r).exists()]
        if not recents:
            empty = QAction(self.tr("(vide)"), self)
            empty.setEnabled(False)
            self._recent_menu.addAction(empty)
            return
        for path in recents:
            p = Path(path)
            act = QAction(p.name, self)
            act.setToolTip(str(p))
            act.setStatusTip(str(p))
            act.triggered.connect(lambda checked=False, fp=path: self._open_document(fp))
            self._recent_menu.addAction(act)
        self._recent_menu.addSeparator()
        act_clear = QAction(self.tr("Effacer l'historique"), self)
        act_clear.triggered.connect(self._clear_recents)
        self._recent_menu.addAction(act_clear)

    def _clear_recents(self):
        QSettings("PDFEquilibrist", "PDFEquilibrist").remove("recent_files")
        self._rebuild_recent_menu()

    def _set_ribbon_enabled(self, enabled: bool):
        self._ribbon_stack.setEnabled(enabled)
        for act in (self._act_print, self._act_save,
                    self._act_save_as, self._act_close_doc):
            act.setEnabled(enabled)
        if not enabled:
            self._act_undo.setEnabled(False)

    # ── ΣΥΓΧΩΝΕΥΣΗ ΟΛΩΝ (ΝΕΟ) ──────────────────────────────────────────────────
    def _merge_everything(self):
        """Συγχώνευση πολλών αρχείων (PDF, Office, εικόνες) σε ένα PDF."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            self.tr("Επιλέξτε αρχεία για συγχώνευση"),
            "",
            self.tr("Όλα τα υποστηριζόμενα (*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt *.jpg *.jpeg *.png *.bmp *.tiff);;PDF (*.pdf);;Office (*.docx *.xlsx *.pptx);;Εικόνες (*.jpg *.png)")
        )
        if not paths:
            return

        output, _ = QFileDialog.getSaveFileName(
            self, self.tr("Αποθήκευση συγχωνευμένου PDF"), "", self.tr("PDF (*.pdf)")
        )
        if not output:
            return

        try:
            from pdf_tsopy.operations.merge_everything import merge_everything
            merge_everything([Path(p) for p in paths], Path(output))
            QMessageBox.information(self, self.tr("Συγχώνευση"),
                                    self.tr("Το PDF δημιουργήθηκε:\n{0}").format(output))
            self._open_document(output)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Σφάλμα"), str(e))

    # ── ΣΥΓΧΩΝΕΥΣΗ ΜΟΝΟ PDF (υπάρχουσα λειτουργία) ────────────────────────────
    def _merge_pdfs_only(self):
        """Συγχώνευση μόνο αρχείων PDF."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        paths, _ = QFileDialog.getOpenFileNames(
            self, self.tr("Επιλέξτε PDF για συγχώνευση"),
            "", self.tr("PDF (*.pdf)"))
        if not paths:
            return
        output, _ = QFileDialog.getSaveFileName(
            self, self.tr("Αποθήκευση συγχωνευμένου PDF"), "", self.tr("PDF (*.pdf)"))
        if not output:
            return
        try:
            import pymupdf
            merged = pymupdf.open()
            for p in paths:
                d = pymupdf.open(p)
                merged.insert_pdf(d)
                d.close()
            merged.save(output)
            merged.close()
            QMessageBox.information(self, self.tr("Συγχώνευση"),
                                    self.tr("Το PDF δημιουργήθηκε:\n{0}").format(output))
            self._open_document(output)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Σφάλμα"), str(e))

    def _choose_scanner(self):
        from pdf_tsopy.ui.scanner_dialog import ScannerDialog
        dlg = ScannerDialog(self)
        if dlg.exec() == dlg.DialogCode.Accepted:
            self._scan_document()

    def _scan_document(self):
        self._scan_job = ScanJob(self)
        def _on_ok(path):
            self._open_document(str(path))
        def _on_failed(msg):
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, self.tr("Numérisation"), msg)
        self._scan_job.finished_ok.connect(_on_ok)
        self._scan_job.failed.connect(_on_failed)
        self._scan_job.start()

    def _open_file_dialog(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, self.tr("Ouvrir un PDF"), "", self.tr("Fichiers PDF (*.pdf)"))
        for path in paths:
            self._open_document(path)

    def _open_document(self, path: str):
        for i, doc in enumerate(self._documents):
            if doc.path and str(doc.path) == path:
                self._title_bar.set_current_index(i)
                return
        doc = Document()
        doc.open(path)
        self._documents.append(doc)
        idx = len(self._documents) - 1
        self._add_recent(path)
        self._title_bar.add_tab(Path(path).name)
        self._switch_to(idx)

    def _close_tab(self, idx: int):
        if idx < 0 or idx >= len(self._documents):
            return
        self._documents[idx].close()
        self._documents.pop(idx)
        self._title_bar.remove_tab(idx)
        if not self._documents:
            self._active_idx = -1
            self._rebind_doc(Document())
            self._set_ribbon_enabled(False)
            self._update_status()
        else:
            new_idx = min(idx, len(self._documents) - 1)
            self._title_bar.set_current_index(new_idx)

    def _switch_to(self, idx: int):
        if idx < 0 or idx >= len(self._documents):
            return
        self._active_idx = idx
        doc = self._documents[idx]
        self._rebind_doc(doc)
        self._set_ribbon_enabled(doc.is_open)
        self._update_status()

    def _rebind_doc(self, doc: Document):
        old = self._current_doc
        try:
            old.changed.disconnect()
        except RuntimeError:
            pass
        self._current_doc = doc
        doc.changed.connect(self._on_doc_changed)
        doc.changed.connect(self.viewer._on_doc_changed)
        doc.changed.connect(self._thumbs.rebuild)
        for tab in (self._tab_afficher, self._tab_modifier,
                    self._tab_annoter, self._tab_page,
                    self._tab_convertir, self._tab_proteger):
            tab.document = doc
        self.viewer.document = doc
        self._thumbs.document = doc
        self.viewer._on_doc_changed()
        self._thumbs.rebuild()

    def _on_doc_changed(self):
        doc = self._current_doc
        if doc.is_open:
            n = len(doc.fitz_doc)
            self._title_bar.set_tab_title(self._active_idx, doc.path.name)
            self._status_file.setText(str(doc.path))
            self._status_page.setText(
                self.tr("{0} page").format(n) if n <= 1 else self.tr("{0} pages").format(n))
            self._set_ribbon_enabled(True)
            self._act_undo.setEnabled(doc.can_undo)
        else:
            self._update_status()

    def _update_status(self):
        doc = self._current_doc
        if doc.is_open:
            n = len(doc.fitz_doc)
            self._status_file.setText(str(doc.path))
            self._status_page.setText(
                self.tr("{0} page").format(n) if n <= 1 else self.tr("{0} pages").format(n))
        else:
            self._status_file.setText(self.tr("Aucun document ouvert"))
            self._status_page.setText("")

    def _save(self):
        if self._current_doc.is_open:
            self._current_doc.save()
            self._status_file.setText(
                self.tr("Enregistré : {0}").format(self._current_doc.path.name))

    def _save_as(self):
        if not self._current_doc.is_open:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Enregistrer sous"),
            str(self._current_doc.path), self.tr("PDF (*.pdf)"))
        if path:
            self._current_doc.save(ensure_suffix(path, ".pdf"))

    def _on_thumbs_width_changed(self, new_w: int):
        viewer_w = self._splitter.width() - new_w - self._splitter.handleWidth()
        self._splitter.setSizes([new_w, max(viewer_w, 400)])

    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self._title_bar.update_max_button(False)
        else:
            self.showMaximized()
            self._title_bar.update_max_button(True)

    def changeEvent(self, event):
        super().changeEvent(event)
        from PyQt6.QtCore import QEvent
        if event.type() == QEvent.Type.WindowStateChange:
            self._title_bar.update_max_button(self.isMaximized())

    def paintEvent(self, event):
        p = QPainter(self)
        p.setPen(QPen(QColor(BORDER_COLOR), 1))
        p.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos  = event.position().toPoint()
        edge = self._edge_at(pos)
        if edge is not None:
            handle = self.windowHandle()
            if handle:
                handle.startSystemResize(edge)

    def mouseMoveEvent(self, event):
        edge   = self._edge_at(event.position().toPoint())
        cursor = self._EDGE_CURSORS.get(edge, Qt.CursorShape.ArrowCursor)
        self.setCursor(cursor)

    def _edge_at(self, pos: QPoint):
        x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
        m = RESIZE_MARGIN
        top    = y < m
        bottom = y > h - m
        left   = x < m
        right  = x > w - m
        if top    and left:  return Qt.Edge.TopEdge    | Qt.Edge.LeftEdge
        if top    and right: return Qt.Edge.TopEdge    | Qt.Edge.RightEdge
        if bottom and left:  return Qt.Edge.BottomEdge | Qt.Edge.LeftEdge
        if bottom and right: return Qt.Edge.BottomEdge | Qt.Edge.RightEdge
        if top:              return Qt.Edge.TopEdge
        if bottom:           return Qt.Edge.BottomEdge
        if left:             return Qt.Edge.LeftEdge
        if right:            return Qt.Edge.RightEdge
        return None

    _EDGE_CURSORS = {
        Qt.Edge.TopEdge:                         Qt.CursorShape.SizeVerCursor,
        Qt.Edge.BottomEdge:                      Qt.CursorShape.SizeVerCursor,
        Qt.Edge.LeftEdge:                        Qt.CursorShape.SizeHorCursor,
        Qt.Edge.RightEdge:                       Qt.CursorShape.SizeHorCursor,
        Qt.Edge.TopEdge    | Qt.Edge.LeftEdge:   Qt.CursorShape.SizeFDiagCursor,
        Qt.Edge.BottomEdge | Qt.Edge.RightEdge:  Qt.CursorShape.SizeFDiagCursor,
        Qt.Edge.TopEdge    | Qt.Edge.RightEdge:  Qt.CursorShape.SizeBDiagCursor,
        Qt.Edge.BottomEdge | Qt.Edge.LeftEdge:   Qt.CursorShape.SizeBDiagCursor,
    }

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if any(u.toLocalFile().lower().endswith(".pdf")
                   for u in event.mimeData().urls()):
                event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self._open_document(path)