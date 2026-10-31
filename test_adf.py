"""Test ADF για τον Canon MX490 (δικτυακός)."""
import win32com.client

# Σταθερές WIA
WIA_DPS_DOCUMENT_HANDLING_SELECT = "3088"
WIA_DPS_DOCUMENT_HANDLING_STATUS = "3087"

FEEDER = 1
FLATBED = 2

m = win32com.client.Dispatch("WIA.DeviceManager")
d = m.DeviceInfos.Item(1).Connect()

# Δείξε τρέχουσα κατάσταση
for p in d.Properties:
    if p.Name in ("Document Handling Capabilities", "Document Handling Select", "Document Handling Status"):
        print(f"{p.Name} = {p.Value}")

# Προσπάθησε να αλλάξεις σε FEEDER
print("\n→ Ρύθμιση σε FEEDER (ADF)...")
try:
    d.Properties(WIA_DPS_DOCUMENT_HANDLING_SELECT).Value = FEEDER
    print("✅ Ορίστηκε FEEDER")
except Exception as e:
    print(f"❌ Σφάλμα: {e}")

# Δείξε νέα κατάσταση
for p in d.Properties:
    if p.Name == "Document Handling Select":
        print(f"\nDocument Handling Select = {p.Value} (1=FEEDER, 2=FLATBED)")

# Δοκίμασε σάρωση
print("\n→ Δοκιμή σάρωσης από ADF...")
try:
    item = d.Items[1]
    image = item.Transfer("{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}")  # JPEG
    if image:
        out = r"C:\temp\test_adf.jpg"
        import os
        os.makedirs(r"C:\temp", exist_ok=True)
        image.SaveFile(out)
        print(f"✅ Αποθηκεύτηκε: {out}")
    else:
        print("❌ Δεν επέστρεψε εικόνα")
except Exception as e:
    print(f"❌ Σφάλμα: {e}")