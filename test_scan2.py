import win32com.client
import os, time

wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")

print("Άνοιγμα παραθύρου σάρωσης...")
image = wia_dialog.ShowAcquireImage()

if image:
    output = os.path.join(os.environ.get("TEMP", "."), f"scan_{int(time.time())}.jpg")
    image.SaveFile(output)
    print(f"✅ Η σάρωση αποθηκεύτηκε: {output}")
else:
    print("❌ Η σάρωση ακυρώθηκε.")