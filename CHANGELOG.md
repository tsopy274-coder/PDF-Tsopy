# Changelog — PDF-Tsopy

Όλες οι σημαντικές αλλαγές καταγράφονται εδώ.
Η μορφή ακολουθεί το [Keep a Changelog](https://keepachangelog.com/) και η αρίθμηση το [Semantic Versioning](https://semver.org/).

---

## 🇬🇷 Ελληνικά (Greek)

### [1.4] — 2026-11-16
**Προστέθηκε**
- **Νέος Launcher (PDF-Tsopy Launcher):** Μια μικρή εφαρμογή εκκίνησης που εμφανίζει αμέσως το λογότυπο του PDF-Tsopy με το γρανάζι, μέχρι να φορτώσει η κύρια εφαρμογή. Έτσι, ο χρήστης βλέπει άμεσα ότι το πρόγραμμα ξεκίνησε.
- **Ανανεωμένο σύστημα ενημερώσεων:** Το κουμπί «Λήψη» ανοίγει απευθείας την επίσημη ιστοσελίδα της εφαρμογής.
- Πολλαπλοί μηχανισμοί (fallbacks) για σωστό άνοιγμα του browser σε όλα τα Windows.
- Ενημέρωση του installer (Inno Setup) ώστε να συμπεριλαμβάνει τον Launcher και τα απαραίτητα αρχεία εικόνων (assets).

**Διορθώθηκε**
- **Πλήρης ελληνική μετάφραση:** Μενού «Επεξεργασία», «Σελίδα», «Προστασία» και μηνύματα Splash Screen.
- Κρίσιμο σφάλμα όπου τα κουμπιά του παραθύρου ενημερώσεων δεν ανταποκρίνονταν στα κλικ (ζήτημα QProgressBar).
- `ModuleNotFoundError` που εμπόδιζε το άνοιγμα του παραθύρου ενημερώσεων στο εκτελέσιμο (exe).
- Βελτιστοποίηση φόρτωσης μεταφράσεων (`.qm`) κατά την εκκίνηση.

### [1.3] — 2026-11-08
**Προστέθηκε**
- Νέο Splash Screen με το λογότυπο PDF-Tsopy, κεντραρισμένο.

**Αφαιρέθηκε**
- Η επιλογή «Συνδέσεις Internet» από το μενού Βοήθεια.

**Διορθώθηκε**
- Ορθογραφικά λάθη και ασυνέπειες στα γλωσσικά αρχεία.
- Επιτυχής μεταγλώττιση και πακετάρισμα χωρίς σφάλματα.

### [1.2] — 2026-11-02
**Προστέθηκε**
- Ελληνικό μοντέλο OCR (PP-OCRv5) για καλύτερη αναγνώριση ελληνικών κειμένων.
- Ρύθμιση ανάλυσης OCR (300 / 400 / 500 / 600 DPI).

**Βελτιώθηκε**
- Αναγνώριση ελληνικών κειμένων σε τιμολόγια, σαρωμένα έγγραφα και πίνακες.
- Ενημέρωση PDF-Tsopy.spec και ρυθμίσεων.

### [1.1] και παλαιότερα
Οι πρώτες εκδόσεις περιελάμβαναν τον αρχικό πυρήνα προβολής και επεξεργασίας PDF, μετατροπή, σχολιασμό, διαχείριση σελίδων, κρυπτογράφηση και πολυγλωσσική διεπαφή (EL / EN / FR / DE).

---

## 🇬🇧 English

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [1.4] — 2026-11-16
**Added**
- **New Launcher (PDF-Tsopy Launcher):** A small startup application that immediately displays the PDF-Tsopy logo with the gear, until the main application loads. This gives users instant feedback that the program is starting.
- **Revamped update system:** The "Download" button now opens the official application website directly.
- Multiple fallbacks to ensure the browser opens correctly across all Windows environments.
- Updated the installer (Inno Setup) to include the Launcher and necessary image assets.

**Fixed**
- **Complete Greek translation:** "Edit", "Page", and "Protect" menus, as well as Splash Screen messages.
- Critical issue where update dialog buttons were unresponsive to clicks (QProgressBar issue).
- `ModuleNotFoundError` that prevented the update dialog from opening in the executable (exe).
- Optimized translation loading (`.qm` files) on startup.

### [1.3] — 2026-11-08
**Added**
- New Splash Screen with the centered PDF-Tsopy logo.

**Removed**
- The "Internet Connections" option from the Help menu.

**Fixed**
- Spelling mistakes and inconsistencies in language files.
- Successful compilation and packaging without errors.

### [1.2] — 2026-11-02
**Added**
- Greek OCR model (PP-OCRv5) for better recognition of Greek texts.
- OCR resolution settings (300 / 400 / 500 / 600 DPI).

**Improved**
- Recognition of Greek texts in invoices, scanned documents, and tables.
- Updated PDF-Tsopy.spec and configurations.

### [1.1] and earlier
The initial releases included the core PDF viewing and editing engine, conversion, annotation, page management, encryption, and multilingual interface (EL / EN / FR / DE).
