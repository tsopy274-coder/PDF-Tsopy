# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
)

def _collect_pywin32_system32_binaries():
    """Συλλογή των pythoncom/pywintypes DLL από τον κατάλογο pywin32_system32"""
    bins = []
    seen = set()
    for p in map(Path, sys.path):
        cand = p / "pywin32_system32"
        if not cand.exists():
            continue
        for pattern in ("pythoncom*.dll", "pywintypes*.dll"):
            for dll in cand.glob(pattern):
                item = (str(dll), "pywin32_system32")
                if item not in seen:
                    bins.append(item)
                    seen.add(item)
    return bins

a = Analysis(
    ['src/pdf_tsopy/main.py'],
    pathex=[],
    binaries=_collect_pywin32_system32_binaries(),
    datas=collect_data_files('win32com') + [
        ('translations', 'translations'),
        ('assets', 'assets'),
    ] + collect_data_files('pymupdf'),
    hiddenimports=collect_submodules('win32com') + [
        'pythoncom',
        'pywintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF-Tsopy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF-Tsopy',
)