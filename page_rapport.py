import customtkinter as ctk
from tkinter import messagebox, filedialog
import database as db
from theme import *
from datetime import datetime, timedelta
import csv

# ============================================
#   PAGE RAPPORT
# ============================================

# Variable globale pour la date sélectionnée
date_selectionnee = None


def afficher(app):
    global date_selectionnee

    # Initialiser à aujourd'hui si pas encore fait
    if date_selectionnee is None:
        date_selectionnee = datetime.now().strftime("%Y-%m-%d")

    contenu = app.contenu

    # ===== EN-TÊTE =====
    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header, text="📊 Rapport | التقرير",
        font=("Arial", 26, "bold"), text_color=OR
    ).pack(side="left")

    # Bouton Export CSV
    ctk.CTkButton(
        header, text="📥 Exporter en CSV",
        fg_color=VERT, hover_color="#2ecc71", text_color=BLANC,
        font=("Arial", 13, "bold"), width=190, height=40,
        command=lambda: exporter_csv(app)
    ).pack(side="right", padx=10)

    # ===== SÉLECTEUR DE DATE =====
    cadre_date = ctk.CTkFrame(contenu, fg_color=NOIR_CLAIR,
                               corner_radius=10, border_width=1, border_color=GRIS)
    cadre_date.pack(fill="x", padx=30, pady=(0, 15))

    inner = ctk.CTkFrame(cadre_date, fg_color="transparent")
    inner.pack(pady=12)

    ctk.CTkLabel(inner, text="📅 Date :",
                 font=("Arial", 14, "bold"), text_color=OR).pack(side="left", padx=10)

    ent_date = ctk.CTkEntry(
        inner, width=160, height=38, font=("Arial", 14),
        justify="center", fg_color=GRIS, border_color=OR, border_width=1
    )
    ent_date.pack(side="left", padx=10)
    ent_date.insert(0, date_selectionnee)

    def appliquer_date():
        global date_selectionnee
        nouvelle_date = ent_date.get().strip()
        # Validation du format
        try:
            datetime.strptime(nouvelle_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur",
                "Format de date invalide.\nUtilisez AAAA-MM-JJ (ex : 2026-01-15) ❌")
            return
        date_selectionnee = nouvelle_date
        app.afficher_page("rapport")

    def aujourd_hui():
        global date_selectionnee
        date_selectionnee = datetime.now().strftime("%Y-%m-%d")
        app.afficher_page("rapport")

    def hier():
        global date_selectionnee
        date_selectionnee = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        app.afficher_page("rapport")

    def semaine():
        global date_selectionnee
        date_selectionnee = datetime.now().strftime("%Y-%m-%d")
        app.afficher_page("rapport")

    ctk.CTkButton(
        inner, text="✅ Appliquer",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 12, "bold"), width=110, height=38,
        command=appliquer_date
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        inner, text="Aujourd'hui",
        fg_color=GRIS, hover_color="#3a3a3a", text_color=OR,
        font=("Arial", 12), width=110, height=38,
        command=aujourd_hui
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        inner, text="Hier",
        fg_color=GRIS, hover_color="#3a3a3a", text_color=OR,
        font=("Arial", 12), width=80, height=38,
        command=hier
    ).pack(side="left", padx=5)

    # ===== RÉSUMÉ DU JOUR CHOISI =====
    fond = db.get_caisse_demarrage(date_selectionnee)
    ventes = db.get_total_caisse_jour(date_selectionnee)
    total = fond + ventes

    zone_resume = ctk.CTkFrame(contenu, fg_color="transparent")
    zone_resume.pack(fill="x", padx=30, pady=15)

    cartes = [
        ("💵", f"{fond:.0f} DH", "Fond de caisse", OR),
        ("📈", f"{ventes:.0f} DH", "Ventes", VERT),
        ("💰", f"{total:.0f} DH", "TOTAL DU JOUR", OR_CLAIR),
    ]

    for emoji, valeur, label, couleur in cartes:
        carte = ctk.CTkFrame(
            zone_resume, height=100, corner_radius=12,
            fg_color=NOIR_CLAIR, border_width=2, border_color=couleur
        )
        carte.pack(side="left", padx=8, fill="x", expand=True)
        carte.pack_propagate(False)

        ctk.CTkLabel(carte, text=f"{emoji}  {label}",
                     font=("Arial", 13, "bold"), text_color=couleur).pack(pady=(15, 5))
        ctk.CTkLabel(carte, text=valeur,
                     font=("Arial", 24, "bold"), text_color=BLANC).pack()

    # ===== CAISSE PAR SERVEUSE (2 colonnes) =====
    zone_milieu = ctk.CTkFrame(contenu, fg_color="transparent")
    zone_milieu.pack(fill="x", padx=30, pady=(5, 15))

    # --- Colonne gauche : par serveuse ---
    cadre_sv = ctk.CTkFrame(zone_milieu, fg_color=NOIR_CLAIR,
                             corner_radius=10, border_width=1, border_color=GRIS)
    cadre_sv.pack(side="left", fill="both", expand=True, padx=(0, 5))

    ctk.CTkLabel(cadre_sv, text="👥 Caisse par serveuse",
                 font=("Arial", 15, "bold"), text_color=OR).pack(pady=(12, 8))

    caisse_sv = db.get_caisse_par_serveuse(date_selectionnee)
    caisse_sv_avec_total = [s for s in caisse_sv if s["total"] > 0]

    if not caisse_sv_avec_total:
        ctk.CTkLabel(cadre_sv, text="Aucune vente ce jour",
                     font=("Arial", 12), text_color="#888").pack(pady=20)
    else:
        for s in caisse_sv_avec_total:
            ligne = ctk.CTkFrame(cadre_sv, fg_color="transparent")
            ligne.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(ligne, text=f"• {s['nom']}",
                         font=("Arial", 13), text_color=BLANC,
                         anchor="w").pack(side="left")
            ctk.CTkLabel(ligne, text=f"{s['total']:.0f} DH",
                         font=("Arial", 13, "bold"), text_color=OR).pack(side="right")
        ctk.CTkFrame(cadre_sv, height=10, fg_color="transparent").pack()

    # --- Colonne droite : Top services ---
    cadre_top = ctk.CTkFrame(zone_milieu, fg_color=NOIR_CLAIR,
                              corner_radius=10, border_width=1, border_color=GRIS)
    cadre_top.pack(side="left", fill="both", expand=True, padx=(5, 0))

    ctk.CTkLabel(cadre_top, text="🛍️ Top services",
                 font=("Arial", 15, "bold"), text_color=OR).pack(pady=(12, 8))

    # Calculer le top services
    conn = db.get_connexion()
    cur = conn.cursor()
    cur.execute("""
        SELECT sv.nom, COUNT(*) as nb, SUM(p.montant) as total
        FROM paiements p
        LEFT JOIN services sv ON p.service_id = sv.id
        WHERE p.date = ?
        GROUP BY sv.nom
        ORDER BY nb DESC
        LIMIT 5
    """, (date_selectionnee,))
    top_services = cur.fetchall()
    conn.close()

    if not top_services:
        ctk.CTkLabel(cadre_top, text="Aucun service vendu ce jour",
                     font=("Arial", 12), text_color="#888").pack(pady=20)
    else:
        for i, s in enumerate(top_services, 1):
            ligne = ctk.CTkFrame(cadre_top, fg_color="transparent")
            ligne.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(ligne, text=f"{i}. {s['nom'] or '—'}",
                         font=("Arial", 13), text_color=BLANC,
                         anchor="w").pack(side="left")
            ctk.CTkLabel(ligne, text=f"{s['nb']}x  ({s['total']:.0f} DH)",
                         font=("Arial", 13, "bold"), text_color=OR).pack(side="right")
        ctk.CTkFrame(cadre_top, height=10, fg_color="transparent").pack()

    # ===== DÉTAIL DES PAIEMENTS =====
    ctk.CTkLabel(contenu, text=f"📋 Détail des encaissements — {date_selectionnee}",
                 font=("Arial", 15, "bold"), text_color=OR).pack(anchor="w", padx=30, pady=(5, 5))

    scroll = ctk.CTkScrollableFrame(
        contenu, fg_color=NOIR_CLAIR,
        corner_radius=10, border_width=1, border_color=GRIS
    )
    scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    # En-tête
    entete = ctk.CTkFrame(scroll, fg_color=GRIS, height=35, corner_radius=6)
    entete.pack(fill="x", pady=(0, 5))
    entete.pack_propagate(False)

    cols = [
        ("Heure", 80), ("Cliente", 160), ("Serveuse", 140),
        ("Service", 180), ("Montant", 100)
    ]
    for label, largeur in cols:
        ctk.CTkLabel(entete, text=label, font=("Arial", 12, "bold"),
                     text_color=OR, width=largeur, anchor="w").pack(side="left", padx=8)

    paiements = db.get_paiements_du_jour(date_selectionnee)
    if not paiements:
        ctk.CTkLabel(scroll, text=f"Aucun encaissement le {date_selectionnee} 💤",
                     font=("Arial", 14), text_color="#888").pack(pady=40)
    else:
        for p in paiements:
            ligne = ctk.CTkFrame(scroll, fg_color="transparent", height=35)
            ligne.pack(fill="x", pady=1)
            ligne.pack_propagate(False)

            ctk.CTkLabel(ligne, text=p["heure"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=80, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=p["client_nom"] or "Anonyme",
                         font=("Arial", 13), text_color=BLANC,
                         width=160, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=p["serveuse_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=140, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=p["service_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=180, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=f"{p['montant']:.0f} DH",
                         font=("Arial", 13, "bold"), text_color=OR,
                         width=100, anchor="w").pack(side="left", padx=8)


# ============================================
#   EXPORT CSV
# ============================================
def exporter_csv(app):
    global date_selectionnee

    paiements = db.get_paiements_du_jour(date_selectionnee)

    if not paiements:
        messagebox.showwarning("Attention",
            f"Aucun paiement à exporter pour le {date_selectionnee} ⚠️")
        return

    # Demander où sauvegarder
    chemin = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Fichier CSV", "*.csv"), ("Tous les fichiers", "*.*")],
        initialfile=f"rapport_sba3iya_{date_selectionnee}.csv",
        title="Enregistrer le rapport en CSV"
    )

    if not chemin:
        return  # utilisateur a annulé

    try:
        # Écrire le CSV (avec encodage UTF-8 + BOM pour Excel)
        with open(chemin, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")

            # Titre
            writer.writerow(["RAPPORT SBA3IYA MAGIC SALON"])
            writer.writerow([f"Date : {date_selectionnee}"])
            writer.writerow([])

            # Résumé
            fond = db.get_caisse_demarrage(date_selectionnee)
            ventes = db.get_total_caisse_jour(date_selectionnee)
            total = fond + ventes

            writer.writerow(["RÉSUMÉ"])
            writer.writerow(["Fond de caisse", f"{fond:.0f} DH"])
            writer.writerow(["Ventes", f"{ventes:.0f} DH"])
            writer.writerow(["TOTAL", f"{total:.0f} DH"])
            writer.writerow([])

            # Caisse par serveuse
            writer.writerow(["CAISSE PAR SERVEUSE"])
            for s in db.get_caisse_par_serveuse(date_selectionnee):
                writer.writerow([s["nom"], f"{s['total']:.0f} DH"])
            writer.writerow([])

            # Détail des paiements
            writer.writerow(["DÉTAIL DES PAIEMENTS"])
            writer.writerow(["Heure", "Cliente", "Serveuse", "Service", "Montant (DH)"])
            for p in paiements:
                writer.writerow([
                    p["heure"] or "",
                    p["client_nom"] or "Anonyme",
                    p["serveuse_nom"] or "",
                    p["service_nom"] or "",
                    f"{p['montant']:.0f}"
                ])

        messagebox.showinfo("Succès",
            f"Rapport exporté avec succès ✅\n\n"
            f"Fichier :\n{chemin}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'exporter :\n{e}")