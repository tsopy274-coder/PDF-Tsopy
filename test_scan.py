import win32com.client

# Δημιουργία WIA manager
wia = win32com.client.Dispatch("WIA.DeviceManager")

print("Διαθέσιμες συσκευές σάρωσης:")
print("-" * 50)

if wia.DeviceInfos.Count == 0:
    print("Δεν βρέθηκε καμία συσκευή.")
else:
    for i in range(1, wia.DeviceInfos.Count + 1):
        info = wia.DeviceInfos.Item(i)
        # Type 1 = Scanner, Type 2 = Camera
        type_name = {1: "Σαρωτής", 2: "Κάμερα"}.get(info.Type, f"Άλλο ({info.Type})")
        print(f"[{i}] {type_name}: {info.Properties('Name').Value}")
        print(f"    ID: {info.DeviceID}")