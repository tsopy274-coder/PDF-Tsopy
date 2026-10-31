"""
rename_module.py — Μετονομάζει το module pdf_equilibrist σε pdf_tsopy
"""
from pathlib import Path
import shutil
import re

# Ρυθμίσεις
OLD_NAME = "pdf_equilibrist"
NEW_NAME = "pdf_tsopy"
SRC_DIR = Path("src")

print("=" * 60)
print(f"Μετονομασία: {OLD_NAME} → {NEW_NAME}")
print("=" * 60)

# ─── 1. Έλεγχος αν υπάρχει ο φάκελος ────────────────────────────────
old_path = SRC_DIR / OLD_NAME
new_path = SRC_DIR / NEW_NAME

if not old_path.exists():
    print(f"❌ Δεν υπάρχει ο φάκελος: {old_path}")
    exit(1)

if new_path.exists():
    print(f"⚠️ Υπάρχει ήδη ο φάκελος: {new_path}")
    print("   Διαγραφή...")
    shutil.rmtree(new_path)

# ─── 2. Μετονομασία φακέλου ────────────────────────────────────────
print(f"\n📁 Μετονομασία φακέλου: {old_path} → {new_path}")
shutil.move(str(old_path), str(new_path))

# ─── 3. Αλλαγή imports σε όλα τα .py ──────────────────────────────
print(f"\n📝 Αλλαγή imports σε όλα τα .py αρχεία...")

changed = 0
for py_file in new_path.rglob("*.py"):
    try:
        content = py_file.read_text(encoding="utf-8")
        if OLD_NAME in content:
            new_content = content.replace(OLD_NAME, NEW_NAME)
            py_file.write_text(new_content, encoding="utf-8")
            changed += 1
            print(f"  ✅ {py_file.relative_to(new_path)}")
    except Exception as e:
        print(f"  ❌ Σφάλμα στο {py_file}: {e}")

print(f"\n✅ Άλλαξαν {changed} αρχεία")

# ─── 4. Αλλαγή .spec ──────────────────────────────────────────────
print(f"\n📝 Αλλαγή .spec...")
for spec_file in Path(".").glob("*.spec"):
    try:
        content = spec_file.read_text(encoding="utf-8")
        if OLD_NAME in content:
            new_content = content.replace(OLD_NAME, NEW_NAME)
            spec_file.write_text(new_content, encoding="utf-8")
            print(f"  ✅ {spec_file.name}")
    except Exception as e:
        print(f"  ❌ Σφάλμα στο {spec_file}: {e}")

# ─── 5. Διαγραφή egg-info ─────────────────────────────────────────
print(f"\n📁 Διαγραφή egg-info...")
egg_info = SRC_DIR / f"{OLD_NAME}.egg-info"
if egg_info.exists():
    shutil.rmtree(egg_info)
    print(f"  ✅ Διαγράφηκε: {egg_info}")

# ─── 6. Διαγραφή __pycache__ ──────────────────────────────────────
print(f"\n📁 Διαγραφή __pycache__...")
for cache in SRC_DIR.rglob("__pycache__"):
    shutil.rmtree(cache, ignore_errors=True)
    print(f"  ✅ {cache}")

print("\n" + "=" * 60)
print("🎉 ΟΛΟΚΛΗΡΩΘΗΚΕ!")
print("=" * 60)
print()
print("Επόμενα βήματα:")
print("1. Διέγραψε τα build\\ και dist\\")
print("2. Τρέξε: pyinstaller PDF-Tsopy.spec")
print()