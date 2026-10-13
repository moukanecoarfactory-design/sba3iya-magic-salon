# ============================================
#   SBA3IYA MAGIC SALON - Base de données
# ============================================
import sqlite3
import os
import shutil
from datetime import datetime

DB_NAME = "sba3iya.db"


# ==========================================
#   CONNEXION
# ==========================================
def get_connexion():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
#   CRÉATION DES TABLES
# ==========================================
def initialiser_bdd():
    conn = get_connexion()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE,
            nom_ar TEXT,
            prix REAL DEFAULT 0,
            actif INTEGER DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS serveuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            specialite TEXT,
            telephone TEXT,
            actif INTEGER DEFAULT 1,
            date_ajout TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telephone TEXT,
            note TEXT,
            date_ajout TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rendez_vous (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            serveuse_id INTEGER,
            service_id INTEGER,
            date TEXT,
            heure TEXT,
            statut TEXT DEFAULT 'prevu',
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(serveuse_id) REFERENCES serveuses(id),
            FOREIGN KEY(service_id) REFERENCES services(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS paiements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            serveuse_id INTEGER,
            service_id INTEGER,
            montant REAL,
            date TEXT,
            heure TEXT,
            mode_paiement TEXT DEFAULT 'espece',
            note TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS parametres (
            cle TEXT PRIMARY KEY,
            valeur TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS caisse_demarrage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            montant REAL,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée")


# ==========================================
#   DONNÉES PAR DÉFAUT
# ==========================================
def inserer_donnees_defaut():
    conn = get_connexion()
    cur = conn.cursor()

    services_defaut = [
        ("Coiffure", "تصفيف الشعر"),
        ("Esthétique", "تجميل"),
        ("Permanent", "بيرماننت"),
        ("Épilation", "إزالة الشعر"),
        ("Soin de visage", "العناية بالوجه"),
        ("Les cils", "الرموش"),
        ("Faux ongles", "الأظافر الاصطناعية"),
        ("Brushing", "بروشينغ"),
        ("Touching", "تاتشينغ"),
        ("Protéine de cheveux", "بروتين الشعر"),
        ("Manucure", "مانيكير"),
        ("Pédicure", "بيديكير"),
        ("Autre", "أخرى"),
    ]

    for nom, nom_ar in services_defaut:
        try:
            cur.execute(
                "INSERT INTO services (nom, nom_ar, prix) VALUES (?, ?, 0)",
                (nom, nom_ar)
            )
        except sqlite3.IntegrityError:
            pass

    defaults = [
        ("admin_password", "admin123"),
        ("nom_salon", "Sba3iya Magic Salon"),
        ("nom_salon_ar", "السباعية ماجيك صالون"),
    ]
    for cle, valeur in defaults:
        try:
            cur.execute(
                "INSERT INTO parametres (cle, valeur) VALUES (?, ?)",
                (cle, valeur)
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print("✅ Données par défaut insérées")


# ==========================================
#   SAUVEGARDE AUTOMATIQUE
# ==========================================
def sauvegarder_bdd():
    """Crée une copie de sauvegarde dans /backups"""
    try:
        dossier = "backups"
        if not os.path.exists(dossier):
            os.makedirs(dossier)

        date = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nom_backup = os.path.join(dossier, f"sba3iya_{date}.db")

        shutil.copy(DB_NAME, nom_backup)
        print(f"✅ Sauvegarde créée : {nom_backup}")

        nettoyer_anciennes_sauvegardes()
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde : {e}")


def nettoyer_anciennes_sauvegardes():
    """Supprime les sauvegardes > 30 jours."""
    try:
        dossier = "backups"
        if not os.path.exists(dossier):
            return
        maintenant = datetime.now()
        for fichier in os.listdir(dossier):
            if fichier.startswith("sba3iya_") and fichier.endswith(".db"):
                chemin = os.path.join(dossier, fichier)
                age = (maintenant - datetime.fromtimestamp(os.path.getmtime(chemin))).days
                if age > 30:
                    os.remove(chemin)
    except Exception:
        pass


# ==========================================
#   PARAMETRES
# ==========================================
def get_parametre(cle, defaut=None):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT valeur FROM parametres WHERE cle = ?", (cle,))
    row = cur.fetchone()
    conn.close()
    return row["valeur"] if row else defaut


def set_parametre(cle, valeur):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO parametres (cle, valeur) VALUES (?, ?)
        ON CONFLICT(cle) DO UPDATE SET valeur = ?
    """, (cle, valeur, valeur))
    conn.commit()
    conn.close()


# ==========================================
#   SERVICES
# ==========================================
def get_services(actifs_seulement=True):
    conn = get_connexion()
    cur = conn.cursor()
    if actifs_seulement:
        cur.execute("SELECT * FROM services WHERE actif = 1 ORDER BY nom")
    else:
        cur.execute("SELECT * FROM services ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return rows


def ajouter_service(nom, nom_ar, prix):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO services (nom, nom_ar, prix) VALUES (?, ?, ?)",
        (nom, nom_ar, prix)
    )
    conn.commit()
    conn.close()


def modifier_service(id_service, nom, nom_ar, prix):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute(
        "UPDATE services SET nom=?, nom_ar=?, prix=? WHERE id=?",
        (nom, nom_ar, prix, id_service)
    )
    conn.commit()
    conn.close()


def supprimer_service(id_service):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM services WHERE id=?", (id_service,))
    conn.commit()
    conn.close()


# ==========================================
#   SERVEUSES
# ==========================================
def get_serveuses(actives_seulement=True):
    conn = get_connexion()
    cur = conn.cursor()
    if actives_seulement:
        cur.execute("SELECT * FROM serveuses WHERE actif = 1 ORDER BY nom")
    else:
        cur.execute("SELECT * FROM serveuses ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return rows


def ajouter_serveuse(nom, specialite="", telephone=""):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO serveuses (nom, specialite, telephone, date_ajout) VALUES (?, ?, ?, ?)",
        (nom, specialite, telephone, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()


def modifier_serveuse(id_serv, nom, specialite, telephone):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute(
        "UPDATE serveuses SET nom=?, specialite=?, telephone=? WHERE id=?",
        (nom, specialite, telephone, id_serv)
    )
    conn.commit()
    conn.close()


def supprimer_serveuse(id_serv):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM serveuses WHERE id=?", (id_serv,))
    conn.commit()
    conn.close()


# ==========================================
#   CLIENTS
# ==========================================
def get_clients():
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return rows


def ajouter_client(nom, telephone="", note=""):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clients (nom, telephone, note, date_ajout) VALUES (?, ?, ?, ?)",
        (nom, telephone, note, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()


def supprimer_client(id_client):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id=?", (id_client,))
    conn.commit()
    conn.close()


# ==========================================
#   CAISSE DE DEMARRAGE
# ==========================================
def get_caisse_demarrage(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT montant FROM caisse_demarrage WHERE date=?", (date,))
    row = cur.fetchone()
    conn.close()
    return row["montant"] if row else 0


def set_caisse_demarrage(montant, note=""):
    date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO caisse_demarrage (date, montant, note) VALUES (?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET montant = ?, note = ?
    """, (date, montant, note, montant, note))
    conn.commit()
    conn.close()


# ==========================================
#   PAIEMENTS
# ==========================================
def ajouter_paiement(client_id, serveuse_id, service_id, montant, note=""):
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO paiements (client_id, serveuse_id, service_id, montant, date, heure, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        client_id, serveuse_id, service_id, montant,
        datetime.now().strftime("%Y-%m-%d"),
        datetime.now().strftime("%H:%M"),
        note
    ))
    conn.commit()
    conn.close()


def get_paiements_du_jour(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*, s.nom as serveuse_nom, sv.nom as service_nom, c.nom as client_nom
        FROM paiements p
        LEFT JOIN serveuses s ON p.serveuse_id = s.id
        LEFT JOIN services sv ON p.service_id = sv.id
        LEFT JOIN clients c ON p.client_id = c.id
        WHERE p.date = ?
        ORDER BY p.heure DESC
    """, (date,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_total_caisse_jour(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(montant), 0) as total FROM paiements WHERE date=?", (date,))
    row = cur.fetchone()
    conn.close()
    return row["total"]


def get_caisse_par_serveuse(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connexion()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.nom, COALESCE(SUM(p.montant), 0) as total
        FROM serveuses s
        LEFT JOIN paiements p ON s.id = p.serveuse_id AND p.date = ?
        WHERE s.actif = 1
        GROUP BY s.id, s.nom
        ORDER BY s.nom
    """, (date,))
    rows = cur.fetchall()
    conn.close()
    return rows


# ==========================================
#   TEST RAPIDE
# ==========================================
if __name__ == "__main__":
    print("🔧 Initialisation de la base...")
    initialiser_bdd()
    inserer_donnees_defaut()
    sauvegarder_bdd()
    print("\n✅ Tout est OK !")