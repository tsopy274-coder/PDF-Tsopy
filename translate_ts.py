"""
translate_ts.py — Αυτόματη μετάφραση .ts με Google Translate (batch mode)
==========================================================================
Χρησιμοποιεί translate_batch για να αποφύγει το rate limit.
"""
import time
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from deep_translator import GoogleTranslator

BASE = Path(__file__).parent
TS_FILE = BASE / "src" / "pdf_equilibrist" / "translations" / "pdf_equilibrist_el.ts"
BACKUP = TS_FILE.with_suffix(".ts.bak")

if not TS_FILE.exists():
    print(f"❌ Δεν βρέθηκε: {TS_FILE}")
    raise SystemExit(1)

shutil.copy2(TS_FILE, BACKUP)
print(f"✅ Backup: {BACKUP}")

translator = GoogleTranslator(source="fr", target="el")

tree = ET.parse(TS_FILE)
root = tree.getroot()

messages = root.findall(".//message")
to_translate = []

for msg in messages:
    source_el = msg.find("source")
    trans_el = msg.find("translation")
    if source_el is None or source_el.text is None:
        continue
    if trans_el is not None and trans_el.text and trans_el.text.strip():
        continue
    to_translate.append((source_el.text, msg, trans_el))

total = len(to_translate)
print(f"\n📝 Βρέθηκαν {total} κείμενα προς μετάφραση\n")

if total == 0:
    print("✅ Όλα μεταφρασμένα!")
    raise SystemExit(0)

# ─── BATCH MODE ────────────────────────────────────────────────────────
BATCH_SIZE = 50   # 50 κείμενα ανά αίτημα
success = 0
failed = 0

for start in range(0, total, BATCH_SIZE):
    batch = to_translate[start:start + BATCH_SIZE]
    texts = [t[0] for t in batch]

    print(f"→ Batch {start+1}-{start+len(batch)} / {total} ... ", end="", flush=True)

    try:
        translations = translator.translate_batch(texts)
        print(f"✅ {len(translations)} μεταφράσεις")

        for (text, msg, trans_el), translated in zip(batch, translations):
            if trans_el is None:
                trans_el = ET.SubElement(msg, "translation")
            trans_el.text = translated
            if "type" in trans_el.attrib:
                del trans_el.attrib["type"]
            success += 1

    except Exception as e:
        print(f"❌ Σφάλμα: {str(e)[:80]}")
        failed += len(batch)

    # Αποθήκευση μετά από κάθε batch
    tree.write(TS_FILE, encoding="utf-8", xml_declaration=True)
    print(f"   💾 Αποθηκεύτηκε (πρόοδος: {min(start+BATCH_SIZE, total)}/{total})")

    # Παύση 2 δευτερολέπτων μεταξύ batch (αποφυγή rate limit)
    time.sleep(2)

print()
print("=" * 60)
print(f"🎉 ΟΛΟΚΛΗΡΩΘΗΚΕ! Επιτυχίες: {success}, Αποτυχίες: {failed}")
print("=" * 60)