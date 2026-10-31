"""
fill_translations.py — Γράφει όλες τις ελληνικές μεταφράσεις στο .ts
"""
import xml.etree.ElementTree as ET
from pathlib import Path

TS_FILE = Path(__file__).parent / "src" / "pdf_equilibrist" / "translations" / "pdf_equilibrist_el.ts"

TRANSLATIONS = {
    # ── BatchDialog ───────────────────────────────────────────────
    "Traitement par lot": "Μαζική επεξεργασία",
    "Fichiers PDF à traiter :": "Αρχεία PDF προς επεξεργασία:",
    "➕  Ajouter des fichiers…": "➕  Προσθήκη αρχείων…",
    "🗑  Vider la liste": "🗑  Καθαρισμός λίστας",
    "Opération :": "Λειτουργία:",
    "Texte du filigrane :": "Κείμενο υδατογραφήματος:",
    "Dossier de sortie :": "Φάκελος εξόδου:",
    "Choisir un dossier…": "Επιλογή φακέλου…",
    "Fermer": "Κλείσιμο",
    "▶  Lancer le traitement": "▶  Έναρξη επεξεργασίας",
    "Ajouter des PDFs": "Προσθήκη PDF",
    "Fichiers PDF (*.pdf)": "Αρχεία PDF (*.pdf)",
    "Dossier de sortie": "Φάκελος εξόδου",
    "⚠ Aucun fichier sélectionné.": "⚠ Δεν επιλέχθηκε αρχείο.",
    "⚠ Choisissez un dossier de sortie.": "⚠ Επιλέξτε φάκελο εξόδου.",
    "\n── Terminé : {0} réussi(s), {1} erreur(s) ──": "\n── Ολοκληρώθηκε: {0} επιτυχίες, {1} σφάλματα ──",

    # ── CVEDialog ─────────────────────────────────────────────────
    "Vérifier les vulnérabilités CVE": "Έλεγχος ευπαθειών CVE",
    "Analyse des paquets installés et du code source…": "Ανάλυση εγκατεστημένων πακέτων και πηγαίου κώδικα…",
    "Les résultats s'afficheront ici une fois l'analyse terminée.": "Τα αποτελέσματα θα εμφανιστούν εδώ μετά την ολοκλήρωση της ανάλυσης.",
    "Relancer": "Επανάληψη",
    "Aucun paquet installé détecté.": "Δεν εντοπίστηκε εγκατεστημένο πακέτο.",
    "Aucune vulnérabilité CVE détectée ({0} paquets analysés).\n": "Δεν εντοπίστηκε ευπάθεια CVE ({0} πακέτα αναλύθηκαν).\n",
    "{0} paquet(s) vulnérable(s) sur {1} analysés :": "{0} ευάλωτο(α) πακέτο(α) από {1} που αναλύθηκαν:",
    "    Gravité : {0}": "    Σοβαρότητα: {0}",
    "    Résumé : {0}": "    Σύνοψη: {0}",
    "Paquets sans vulnérabilité connue :": "Πακέτα χωρίς γνωστή ευπάθεια:",
    "Analyse statique du code source (bandit)": "Στατική ανάλυση πηγαίου κώδικα (bandit)",
    "Aucun problème détecté dans le code source du projet.": "Δεν εντοπίστηκε πρόβλημα στον πηγαίο κώδικα του έργου.",
    "{0} problème(s) détecté(s) dans le code source :": "{0} πρόβλημα(τα) εντοπίστηκε(αν) στον πηγαίο κώδικα:",
    "[{0}/confiance {1}] {2}:{3} — {4} ({5})": "[{0}/βεβαιότητα {1}] {2}:{3} — {4} ({5})",
    "Analyse en cours… {0}/{1} paquets": "Ανάλυση σε εξέλιξη… {0}/{1} πακέτα",
    "Vérification CVE en ligne ignorée : connexions Internet bloquées": "Ο διαδικτυακός έλεγχος CVE παραλείφθηκε: οι συνδέσεις Internet είναι αποκλεισμένες",
    "⚠ {0} paquet(s) vulnérable(s)/{1}": "⚠ {0} ευάλωτο(α) πακέτο(α)/{1}",
    "✓ {0} paquets OK": "✓ {0} πακέτα OK",
    "⚠ {0} problème(s) dans le code": "⚠ {0} πρόβλημα(τα) στον κώδικα",
    "✓ code source OK": "✓ πηγαίος κώδικας OK",
    "Échec de l'analyse": "Αποτυχία ανάλυσης",
    "Erreur : {0}": "Σφάλμα: {0}",
    "Connexions Internet bloquées : aucune requête envoyée à api.osv.dev (menu Aide › Connexions Internet). Seule l'analyse locale du code est faite.": "Οι συνδέσεις Internet είναι αποκλεισμένες: δεν στάλθηκε κανένα αίτημα στο api.osv.dev (μενού Βοήθεια › Συνδέσεις Internet). Γίνεται μόνο τοπική ανάλυση του κώδικα.",
    "Connexion à api.osv.dev (OSV) : seuls les noms et versions des bibliothèques utilisées par l'application sont envoyés.": "Σύνδεση στο api.osv.dev (OSV): αποστέλλονται μόνο τα ονόματα και οι εκδόσεις των βιβλιοθηκών που χρησιμοποιεί η εφαρμογή.",

    # ── MainWindow ────────────────────────────────────────────────
    "Afficher": "Προβολή",
    "Modifier": "Επεξεργασία",
    "Convertir": "Μετατροπή",
    "Annoter": "Σχολιασμός",
    "Page": "Σελίδα",
    "Protéger": "Προστασία",
    "Aucun document ouvert": "Κανένα ανοιχτό έγγραφο",
    "Fichier": "Αρχείο",
    "Numériser…": "Σάρωση…",
    "Ouvrir…": "Άνοιγμα…",
    "Ouvrir récemment": "Πρόσφατα αρχεία",
    "Imprimer…": "Εκτύπωση…",
    "Enregistrer": "Αποθήκευση",
    "Enregistrer sous…": "Αποθήκευση ως…",
    "Fermer l'onglet": "Κλείσιμο καρτέλας",
    "Quitter": "Έξοδος",
    "Édition": "Επεξεργασία",
    "Annuler": "Αναίρεση",
    "Rechercher…": "Αναζήτηση…",
    "Aide": "Βοήθεια",
    "Vérifier les mises à jour…": "Έλεγχος ενημερώσεων…",
    "Vérifier les vulnérabilités CVE…": "Έλεγχος ευπαθειών CVE…",
    "Connexions Internet": "Συνδέσεις Internet",
    "Bloquer toutes les connexions Internet": "Αποκλεισμός όλων των συνδέσεων Internet",
    "Vérifier les mises à jour au démarrage (api.github.com)": "Έλεγχος ενημερώσεων στην εκκίνηση (api.github.com)",
    "À propos de PDF-Equilibrist…": "Σχετικά με το PDF-Equilibrist…",
    "Recherche de mise à jour (api.github.com)…": "Έλεγχος ενημερώσεων (api.github.com)…",
    "Vérification des mises à jour": "Έλεγχος ενημερώσεων",
    "Impossible d'ouvrir le dialogue de mise à jour :\n{0}": "Αδυναμία ανοίγματος του διαλόγου ενημέρωσης:\n{0}",
    "Vérification CVE": "Έλεγχος CVE",
    "Impossible d'ouvrir le dialogue CVE :\n{0}": "Αδυναμία ανοίγματος του διαλόγου CVE:\n{0}",
    "(vide)": "(κενό)",
    "Effacer l'historique": "Καθαρισμός ιστορικού",
    "Numérisation": "Σάρωση",
    "Ouvrir un PDF": "Άνοιγμα PDF",
    "{0} page": "{0} σελίδα",
    "{0} pages": "{0} σελίδες",
    "Enregistré : {0}": "Αποθηκεύτηκε: {0}",
    "Enregistrer sous": "Αποθήκευση ως",
    "PDF (*.pdf)": "PDF (*.pdf)",

    # ── PrintDialog ───────────────────────────────────────────────
    "Imprimer — {0}": "Εκτύπωση — {0}",
    "Imprimante": "Εκτυπωτής",
    "Nom :": "Όνομα:",
    "Propriétés avancées…": "Σύνθετες ιδιότητες…",
    "Ouvre les propriétés natives de l'imprimante\n(agrafe, perforation, format rouleau, découpe, …)": "Ανοίγει τις εγγενείς ιδιότητες του εκτυπωτή\n(συρραφή, διάτρηση, μορφή ρολού, κοπή, …)",
    "Copies": "Αντίγραφα",
    "Nombre :": "Αριθμός:",
    "Pages à imprimer": "Σελίδες προς εκτύπωση",
    "Tout": "Όλες",
    "Pages personnalisées": "Προσαρμοσμένες σελίδες",
    "Plage :": "Εύρος:",
    "ex: 1-3, 5, 8-10": "π.χ. 1-3, 5, 8-10",
    "Numéros :": "Αριθμοί:",
    "Format papier": "Μέγεθος χαρτιού",
    "Format :": "Μέγεθος:",
    "Orientation": "Προσανατολισμός",
    "Auto (par page)": "Αυτόματο (ανά σελίδα)",
    "Portrait": "Κατακόρυφος",
    "Paysage": "Οριζόντιος",
    "Échelle / Dimensionnement": "Κλίμακα / Μέγεθος",
    "Ajuster (remplir le papier)": "Προσαρμογή (γέμισμα χαρτιού)",
    "Réduire uniquement": "Μόνο σμίκρυνση",
    "100 % (rogner si déborde)": "100 % (περικοπή αν υπερχειλίζει)",
    "Recto / Verso": "Μπρος / Πίσω",
    "Désactivé": "Απενεργοποιημένο",
    "Retourner sur le bord long": "Εκτύπωση στον μακρύ άξονα",
    "Retourner sur le bord court": "Εκτύπωση στον κοντό άξονα",
    "Couleur": "Χρώμα",
    "Nuances de gris": "Αποχρώσεις του γκρι",
    "Impression en cours…": "Εκτύπωση σε εξέλιξη…",
    "Imprimer": "Εκτύπωση",
    "Propriétés avancées ✓": "Σύνθετες ιδιότητες ✓",
    "Réglages driver configurés (agrafe, finition…)\nCes réglages seront transmis directement au driver à l'impression.\nCliquer pour modifier.": "Ρυθμίσεις προγράμματος οδήγησης (συρραφή, φινίρισμα…)\nΑυτές οι ρυθμίσεις θα μεταδοθούν απευθείας στον οδηγό κατά την εκτύπωση.\nΚλικ για αλλαγή.",
    "Impression en cours… page {0}/{1}": "Εκτύπωση σε εξέλιξη… σελίδα {0}/{1}",
    "Erreur d'impression": "Σφάλμα εκτύπωσης",
    "Impossible de démarrer le travail d'impression.\nVérifiez que l'imprimante est disponible.": "Αδυναμία έναρξης εκτύπωσης.\nΒεβαιωθείτε ότι ο εκτυπωτής είναι διαθέσιμος.",

    # ── SearchBar ─────────────────────────────────────────────────
    "Rechercher dans le document…": "Αναζήτηση στο έγγραφο…",
    "Résultat précédent (Maj+Entrée)": "Προηγούμενο αποτέλεσμα (Shift+Enter)",
    "Résultat suivant (Entrée)": "Επόμενο αποτέλεσμα (Enter)",
    "Fermer (Échap)": "Κλείσιμο (Esc)",
    "Aucun résultat": "Κανένα αποτέλεσμα",
    "{0} résultat": "{0} αποτέλεσμα",
    "{0} résultats": "{0} αποτελέσματα",
    "{0} sur {1}": "{0} από {1}",

    # ── SignatureDialog ───────────────────────────────────────────
    "Signature / Tampon": "Υπογραφή / Σφραγίδα",
    "Tampons prédéfinis": "Προκαθορισμένες σφραγίδες",
    "Signature PNG": "Υπογραφή PNG",
    "Page :": "Σελίδα:",
    "Aucune image sélectionnée": "Δεν επιλέχθηκε εικόνα",
    "📁  Choisir une image PNG / JPG…": "📁  Επιλογή εικόνας PNG / JPG…",
    "Largeur :": "Πλάτος:",
    "px   Hauteur :": "px   Ύψος:",
    "Insérer la signature": "Εισαγωγή υπογραφής",
    "Choisir une signature": "Επιλογή υπογραφής",
    "Images (*.png *.jpg *.jpeg *.bmp)": "Εικόνες (*.png *.jpg *.jpeg *.bmp)",

    # ── SplashScreen ──────────────────────────────────────────────
    "Initialisation…": "Αρχικοποίηση…",

    # ── TabAfficher ───────────────────────────────────────────────
    "Zoom": "Ζουμ",
    "Gauche": "Αριστερά",
    "Droite": "Δεξιά",
    "Rotation": "Περιστροφή",
    "Impression": "Εκτύπωση",

    # ── TabAnnoter ────────────────────────────────────────────────
    "Surligner": "Επισήμανση",
    "Barrer": "Διαγραφή",
    "Souligner": "Υπογράμμιση",
    "Marquage": "Σήμανση",
    "Zone\ntexte": "Πεδίο\nκειμένου",
    "Annotation": "Σχολιασμός",
    "À venir": "Σύντομα",
    "Crayon": "Μολύβι",
    "Forme": "Σχήμα",
    "Signature": "Υπογραφή",
    "Sélectionnez du texte en faisant glisser la souris sur la page": "Επιλέξτε κείμενο σύροντας το ποντίκι στη σελίδα",
    "Sélectionnez d'abord du texte en faisant glisser la souris sur la page.": "Επιλέξτε πρώτα κείμενο σύροντας το ποντίκι στη σελίδα.",
    "Zone de texte": "Πεδίο κειμένου",
    "Contenu :": "Περιεχόμενο:",

    # ── TabConvertir ──────────────────────────────────────────────
    "Power\nPoint": "Power\nPoint",
    "PDF → Office": "PDF → Office",
    "Image": "Εικόνα",
    "PDF → Image": "PDF → Εικόνα",
    "PDF → Texte": "PDF → Κείμενο",
    "OCR →\nPDF": "OCR →\nPDF",
    "OCR →\nMarkdown": "OCR →\nMarkdown",
    "OCR →\nWord": "OCR →\nWord",
    "OCR →\nExcel": "OCR →\nExcel",
    "Office\nen PDF": "Office\nσε PDF",
    "Image\nen PDF": "Εικόνα\nσε PDF",
    "→ PDF": "→ PDF",
    "Traitement\npar lot": "Μαζική\nεπεξεργασία",
    "Lot": "Παρτίδα",
    "Vers Markdown": "Σε Markdown",
    "Markdown (*.md)": "Markdown (*.md)",
    "Conversion": "Μετατροπή",
    "Markdown enregistré :\n{0}": "Markdown αποθηκεύτηκε:\n{0}",
    "Conversion impossible": "Αδύνατη μετατροπή",
    "Erreur": "Σφάλμα",
    "Un OCR est déjà en cours (ou en cours d'annulation).": "Ένα OCR εκτελείται ήδη (ή ακυρώνεται).",
    "OCR — Erreur": "OCR — Σφάλμα",
    "Initialisation OCR…": "Αρχικοποίηση OCR…",
    "Annulation en cours…": "Ακύρωση σε εξέλιξη…",
    "OCR → PDF cherchable": "OCR → PDF αναζητήσιμο",
    "OCR → PDF": "OCR → PDF",
    "PDF cherchable enregistré :\n{0}": "Αναζητήσιμο PDF αποθηκεύτηκε:\n{0}",
    "OCR → Markdown": "OCR → Markdown",
    "OCR → Word": "OCR → Word",
    "Word (*.docx)": "Word (*.docx)",
    "Word enregistré :\n{0}": "Word αποθηκεύτηκε:\n{0}",
    "OCR → Excel": "OCR → Excel",
    "Excel (*.xlsx)": "Excel (*.xlsx)",
    "Excel enregistré :\n{0}": "Excel αποθηκεύτηκε:\n{0}",
    "Vers Word": "Σε Word",
    "Vers Excel": "Σε Excel",
    "Vers PowerPoint": "Σε PowerPoint",
    "PowerPoint (*.pptx)": "PowerPoint (*.pptx)",
    "PowerPoint enregistré :\n{0}": "PowerPoint αποθηκεύτηκε:\n{0}",
    "{0} image(s) dans :\n{1}": "{0} εικόνα(ες) σε:\n{1}",
    "Office en PDF": "Office σε PDF",
    "Aucun moteur trouvé.\nInstallez Microsoft Office ou LibreOffice.": "Δεν βρέθηκε μηχανή μετατροπής.\nΕγκαταστήστε Microsoft Office ή LibreOffice.",
    "Fichiers Office à convertir": "Αρχεία Office προς μετατροπή",
    "Office (*.docx *.xlsx *.pptx *.doc *.xls *.ppt *.odt *.ods *.odp)": "Office (*.docx *.xlsx *.pptx *.doc *.xls *.ppt *.odt *.ods *.odp)",
    "Moteur : {0}\n{1} fichier(s) converti(s).": "Μηχανή: {0}\n{1} αρχείο(α) μετατράπηκε(αν).",
    "Erreurs :": "Σφάλματα:",
    "Choisir des images": "Επιλογή εικόνων",
    "Images (*.png *.jpg *.jpeg *.bmp *.tiff)": "Εικόνες (*.png *.jpg *.jpeg *.bmp *.tiff)",
    "Enregistrer le PDF": "Αποθήκευση PDF",
    "PDF créé :\n{0}": "PDF δημιουργήθηκε:\n{0}",

    # ── TabModifier ───────────────────────────────────────────────
    "Modifier\ntexte": "Επεξεργασία\nκειμένου",
    "Valider": "Επιβεβαίωση",
    "Édition texte": "Επεξεργασία κειμένου",
    "Ajouter\ntexte": "Προσθήκη\nκειμένου",
    "Ajouter\nimage": "Προσθήκη\nεικόνας",
    "Insertion": "Εισαγωγή",
    "Filigrane": "Υδατογράφημα",
    "Compres\nser": "Συμπίεση",
    "Mise en page": "Διάταξη σελίδας",
    "Rendre\ncherchable": "Κάντε το\nαναζητήσιμο",
    "Signature\n/ Tampon": "Υπογραφή\n/ Σφραγίδα",
    "Lien": "Σύνδεσμος",
    "Aucun texte extractible (PDF scanné ?).": "Δεν υπάρχει εξαγώγιμο κείμενο (σαρωμένο PDF;).",
    "✎\nActif": "✎\nΕνεργό",
    "Modifications": "Τροποποιήσεις",
    "Terminé — Fichier › Enregistrer pour sauvegarder.": "Ολοκληρώθηκε — Αρχείο › Αποθήκευση για αποθήκευση.",
    "✎\nModifier\ntexte": "✎\nΕπεξεργασία\nκειμένου",
    "Ajouter du texte": "Προσθήκη κειμένου",
    "Texte à insérer :": "Κείμενο προς εισαγωγή:",
    "Choisir une image": "Επιλογή εικόνας",
    "Aucune page scannée détectée.\nLe document contient déjà une couche texte.": "Δεν εντοπίστηκε σαρωμένη σελίδα.\nΤο έγγραφο περιέχει ήδη επίπεδο κειμένου.",
    "{0} page(s) rendue(s) cherchables.\nPensez à enregistrer le document.": "{0} σελίδα(ες) έγιναν αναζητήσιμες.\nΘυμηθείτε να αποθηκεύσετε το έγγραφο.",
    "OCR — Rendre cherchable": "OCR — Κάντε το αναζητήσιμο",
    "Enregistrer compressé": "Αποθήκευση συμπιεσμένου",
    "_compressé": "_συμπιεσμένο",
    "Compresser": "Συμπίεση",
    "Enregistré :\n{0}": "Αποθηκεύτηκε:\n{0}",

    # ── TabPage ───────────────────────────────────────────────────
    "Insérer": "Εισαγωγή",
    "Diviser": "Διαχωρισμός",
    "Fusion\nner": "Συγχώνευση",
    "Inverser": "Αντιστροφή",
    "Organisation": "Οργάνωση",
    "Rogner": "Περικοπή",
    "Taille": "Μέγεθος",
    "Insérer après la page (1–{0}) :": "Εισαγωγή μετά τη σελίδα (1–{0}):",
    "PDF source (vide = page blanche)": "PDF προέλευσης (κενό = λευκή σελίδα)",
    "{0} fichier(s) dans :\n{1}": "{0} αρχείο(α) σε:\n{1}",
    "PDF à fusionner": "PDF προς συγχώνευση",
    "PDF fusionné": "Συγχωνευμένο PDF",
    "Fusionner": "Συγχώνευση",
    "PDF fusionné :\n{0}": "Συγχωνευμένο PDF:\n{0}",

    # ── TabProteger ───────────────────────────────────────────────
    "Chiffrer": "Κρυπτογράφηση",
    "Déchif\nfrer": "Αποκρυπτο\nγράφηση",
    "Protection": "Προστασία",
    "PDF chiffré": "Κρυπτογραφημένο PDF",
    "_chiffré": "_κρυπτογραφημένο",
    "PDF chiffré :\n{0}": "Κρυπτογραφημένο PDF:\n{0}",
    "Déchiffrer": "Αποκρυπτογράφηση",
    "Ce document n'est pas chiffré.": "Αυτό το έγγραφο δεν είναι κρυπτογραφημένο.",
    "Document déchiffré.": "Το έγγραφο αποκρυπτογραφήθηκε.",
    "Mot de passe incorrect.": "Λανθασμένος κωδικός πρόσβασης.",

    # ── ThumbnailPanel ────────────────────────────────────────────
    "Pages": "Σελίδες",
    "Insertion PDF": "Εισαγωγή PDF",
    "Impossible d'ouvrir :\n{0}": "Αδυναμία ανοίγματος:\n{0}",
    "↑  Monter la sélection ({0} pages)": "↑  Μετακίνηση επιλογής ({0} σελίδες)",
    "↓  Descendre la sélection ({0} pages)": "↓  Μετακίνηση επιλογής προς τα κάτω ({0} σελίδες)",
    "↑  Monter  ({0}/{1} → {2}/{3})": "↑  Μετακίνηση  ({0}/{1} → {2}/{3})",
    "↓  Descendre  ({0}/{1} → {2}/{3})": "↓  Μετακίνηση προς τα κάτω  ({0}/{1} → {2}/{3})",
    " ({0} pages)": " ({0} σελίδες)",
    "↻  Rotation horaire": "↻  Δεξιόστροφη περιστροφή",
    "↺  Rotation antihoraire": "↺  Αριστερόστροφη περιστροφή",
    "⧉  Dupliquer la sélection ({0} pages)": "⧉  Διπλοποίηση επιλογής ({0} σελίδες)",
    "⇥  Extraire la sélection ({0} pages)…": "⇥  Εξαγωγή επιλογής ({0} σελίδες)…",
    "⧉  Dupliquer la page {0}": "⧉  Διπλοποίηση σελίδας {0}",
    "⇥  Extraire la page {0}…": "⇥  Εξαγωγή σελίδας {0}…",
    "🗑  Supprimer la sélection ({0} pages)": "🗑  Διαγραφή επιλογής ({0} σελίδες)",
    "🗑  Supprimer la page {0}": "🗑  Διαγραφή σελίδας {0}",
    "🖶  Imprimer la sélection ({0} pages)…": "🖶  Εκτύπωση επιλογής ({0} σελίδες)…",
    "🖶  Imprimer la page {0}…": "🖶  Εκτύπωση σελίδας {0}…",
    "Supprimer": "Διαγραφή",
    "Impossible de supprimer toutes les pages.": "Αδυναμία διαγραφής όλων των σελίδων.",
    "Extraire les pages": "Εξαγωγή σελίδων",
    "Extraire": "Εξαγωγή",
    "{0} page(s) extraite(s) dans :\n{1}": "{0} σελίδα(ες) εξήχθη(σαν) σε:\n{1}",

    # ── TitleBar ──────────────────────────────────────────────────
    "Ouvrir un PDF (Ctrl+O)": "Άνοιγμα PDF (Ctrl+O)",
    "Langue / Language": "Γλώσσα / Language",
    "Réduire": "Ελαχιστοποίηση",
    "Agrandir / Restaurer": "Μεγιστοποίηση / Επαναφορά",
    "Langue modifiée": "Η γλώσσα άλλαξε",
    "Le changement de langue sera appliqué au prochain démarrage.": "Η αλλαγή γλώσσας θα εφαρμοστεί στην επόμενη εκκίνηση.",
    "Redémarrer maintenant": "Επανεκκίνηση τώρα",
    "Plus tard": "Αργότερα",

    # ── UpdateDialog ──────────────────────────────────────────────
    "À propos de PDF-Equilibrist": "Σχετικά με το PDF-Equilibrist",
    "Éditeur PDF de bureau — © 2026 PDF Equilibrist — Licence GPLv3": "Επιτραπέζιος επεξεργαστής PDF — © 2026 PDF Equilibrist — Άδεια GPLv3",
    "Dépôt GitHub": "Αποθετήριο GitHub",
    "Vérification des nouvelles versions…": "Έλεγχος νέων εκδόσεων…",
    "Connexion à api.github.com (GitHub) pour la version et les statistiques. Aucun document ni aucune donnée personnelle n'est envoyé.": "Σύνδεση στο api.github.com (GitHub) για την έκδοση και τα στατιστικά. Δεν αποστέλλονται έγγραφα ή προσωπικά δεδομένα.",
    "Téléchargements": "Λήψεις",
    "Cette version (v{0}) :": "Αυτή η έκδοση (v{0}):",
    "Total toutes versions :": "Σύνολο όλων των εκδόσεων:",
    "Copier": "Αντιγραφή",
    "Mise à jour :": "Ενημέρωση:",
    "Ouvrir la page de la release": "Άνοιγμα σελίδας έκδοσης",
    "Télécharger et installer": "Λήψη και εγκατάσταση",
    "Version installée : v{0}": "Εγκατεστημένη έκδοση: v{0}",
    "Connexions Internet bloquées : aucune requête envoyée (menu Aide › Connexions Internet).": "Οι συνδέσεις Internet είναι αποκλεισμένες: δεν στάλθηκε κανένα αίτημα (μενού Βοήθεια › Συνδέσεις Internet).",
    "v{0} — version la plus récente.": "v{0} — η πιο πρόσφατη έκδοση.",
    "Nouvelle version disponible : {0}": "Νέα έκδοση διαθέσιμη: {0}",
    "Erreur lors de la vérification : {0}": "Σφάλμα κατά τον έλεγχο: {0}",
    "Téléchargement en cours…": "Λήψη σε εξέλιξη…",
    "Téléchargé : {0}": "Λήφθηκε: {0}",
    "Échec du téléchargement : {0}": "Αποτυχία λήψης: {0}",

    # ── _PageLabel ────────────────────────────────────────────────
    "Ouverture d'un fichier externe": "Άνοιγμα εξωτερικού αρχείου",
    "Ce document PDF demande à ouvrir :\n\n{0}\n\nN'acceptez que si vous faites confiance à ce document.": "Αυτό το PDF ζητά να ανοίξει:\n\n{0}\n\nΑποδεχτείτε μόνο αν εμπιστεύεστε αυτό το έγγραφο.",
    "Ouverture d'un lien Internet": "Άνοιγμα συνδέσμου Internet",
    "Ce document PDF contient un lien vers :\n\n{0}\n\nL'ouvrir dans votre navigateur ?": "Αυτό το PDF περιέχει σύνδεσμο προς:\n\n{0}\n\nΆνοιγμα στον περιηγητή σας;",

    # ── _WelcomePage ──────────────────────────────────────────────
    "Glissez un PDF ici ou utilisez  Fichier › Ouvrir": "Σύρετε ένα PDF εδώ ή χρησιμοποιήστε  Αρχείο › Άνοιγμα",

    # ── _Worker ───────────────────────────────────────────────────
    "fusionné.pdf": "συγχωνευμένο.pdf",
    "✓ Fusionné → {0}": "✓ Συγχωνεύτηκε → {0}",
    "✗ Erreur fusion : {0}": "✗ Σφάλμα συγχώνευσης: {0}",
    "✓ {0}": "✓ {0}",
    "✗ {0} : {1}": "✗ {0}: {1}",

    # ── dialogs ───────────────────────────────────────────────────
    "OK": "OK",
    "Mot de passe :": "Κωδικός πρόσβασης:",
    "Chiffrer le PDF": "Κρυπτογράφηση PDF",
    "Mot de passe utilisateur :": "Κωδικός χρήστη:",
    "Mot de passe propriétaire (optionnel) :": "Κωδικός ιδιοκτήτη (προαιρετικό):",
    "Après la page n° :": "Μετά τη σελίδα αρ.:",
    "Numéro de page": "Αριθμός σελίδας",
    "Texte du filigrane :": "Κείμενο υδατογραφήματος:",
    "ex: CONFIDENTIEL": "π.χ. ΕΜΠΙΣΤΕΥΤΙΚΟ",
    "Format d'image": "Μορφή εικόνας",

    # ── main ──────────────────────────────────────────────────────
    "Chargement de PyMuPDF…": "Φόρτωση του PyMuPDF…",
    "Chargement de PyQt6…": "Φόρτωση του PyQt6…",
    "Chargement des convertisseurs…": "Φόρτωση των μετατροπέων…",
    "Chargement de l'interface…": "Φόρτωση του περιβάλλοντος…",
    "Initialisation de la fenêtre…": "Αρχικοποίηση του παραθύρου…",
    "Prêt !": "Έτοιμο!",
    "Erreur au démarrage": "Σφάλμα κατά την εκκίνηση",
    "PDF Equilibrist n'a pas pu démarrer.": "Το PDF Equilibrist δεν μπόρεσε να ξεκινήσει.",
}

# Φόρτωση
tree = ET.parse(TS_FILE)
root = tree.getroot()

filled = 0
not_found = 0
already = 0

for msg in root.findall(".//message"):
    source_el = msg.find("source")
    trans_el = msg.find("translation")
    if source_el is None or source_el.text is None:
        continue

    src = source_el.text

    # Αν έχει ήδη μετάφραση, παράλειψε
    if trans_el is not None and trans_el.text and trans_el.text.strip():
        already += 1
        continue

    if trans_el is None:
        trans_el = ET.SubElement(msg, "translation")

    if src in TRANSLATIONS:
        trans_el.text = TRANSLATIONS[src]
        if "type" in trans_el.attrib:
            del trans_el.attrib["type"]
        filled += 1
    else:
        trans_el.text = src
        not_found += 1
        print(f"⚠ Δεν βρέθηκε μετάφραση για: {src[:60]!r}")

# Αποθήκευση
tree.write(TS_FILE, encoding="utf-8", xml_declaration=True)

print()
print("=" * 60)
print(f"✅ Μεταφράστηκαν: {filled}")
print(f"⚠  Χωρίς μετάφραση: {not_found}")
print(f"⏭  Ήδη μεταφρασμένα: {already}")
print("=" * 60)