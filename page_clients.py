import customtkinter as ctk
from tkinter import messagebox
import database as db
from theme import *

# ============================================
#   PAGE CLIENTS
# ============================================

# Variable globale pour la recherche
filtre_recherche = ""


def afficher(app):
    contenu = app.contenu

    # ===== EN-TÊTE =====
    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header, text="👥 Clients | العملاء",
        font=("Arial", 26, "bold"), text_color=OR
    ).pack(side="left")

    if app.mode_admin:
        ctk.CTkLabel(
            header, text="🔓 Mode Admin activé",
            font=("Arial", 14, "bold"), text_color=VERT
        ).pack(side="right", padx=10)

    ctk.CTkButton(
        header, text="➕ Ajouter une cliente",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 13, "bold"), width=200, height=40,
        command=lambda: dialog_client(app, None)
    ).pack(side="right", padx=10)

    # ===== BARRE DE RECHERCHE =====
    cadre_recherche = ctk.CTkFrame(contenu, fg_color="transparent")
    cadre_recherche.pack(fill="x", padx=30, pady=(0, 10))

    ent_recherche = ctk.CTkEntry(
        cadre_recherche,
        placeholder_text="🔍  Rechercher par nom ou téléphone...",
        width=450, height=40, font=("Arial", 13),
        fg_color=NOIR_CLAIR, border_color=OR, border_width=1
    )
    ent_recherche.pack(side="left")
    ent_recherche.insert(0, filtre_recherche)

    def actualiser_recherche(*args):
        global filtre_recherche
        filtre_recherche = ent_recherche.get().strip().lower()
        # Rafraîchir la liste
        app.afficher_page("clients")

    ent_recherche.bind("<KeyRelease>", actualiser_recherche)

    # Bouton pour effacer
    def effacer_recherche():
        global filtre_recherche
        filtre_recherche = ""
        app.afficher_page("clients")

    ctk.CTkButton(
        cadre_recherche, text="✖ Effacer",
        fg_color=GRIS, hover_color="#3a3a3a", text_color=BLANC,
        font=("Arial", 12), width=100, height=40,
        command=effacer_recherche
    ).pack(side="left", padx=10)

    # ===== ZONE DES CLIENTS =====
    scroll = ctk.CTkScrollableFrame(
        contenu, fg_color=NOIR_CLAIR,
        corner_radius=12, border_width=1, border_color=GRIS
    )
    scroll.pack(fill="both", expand=True, padx=30, pady=(5, 30))

    # En-tête du tableau
    entete = ctk.CTkFrame(scroll, fg_color=GRIS, height=40, corner_radius=8)
    entete.pack(fill="x", pady=(0, 5))
    entete.pack_propagate(False)

    ctk.CTkLabel(entete, text="Nom",
                 font=("Arial", 13, "bold"), text_color=OR, width=200, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Téléphone",
                 font=("Arial", 13, "bold"), text_color=OR, width=160, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Note",
                 font=("Arial", 13, "bold"), text_color=OR, width=180, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Inscrite le",
                 font=("Arial", 13, "bold"), text_color=OR, width=130, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Actions",
                 font=("Arial", 13, "bold"), text_color=OR, width=180).pack(side="left", padx=15)

    # ===== LISTE =====
    clients = db.get_clients()

    # Filtrage
    if filtre_recherche:
        clients = [
            c for c in clients
            if filtre_recherche in (c["nom"] or "").lower()
            or filtre_recherche in (c["telephone"] or "").lower()
        ]

    if not clients:
        ctk.CTkLabel(
            scroll, text="Aucune cliente trouvée.\nCliquez sur ➕ pour en ajouter.",
            font=("Arial", 15), text_color="#888"
        ).pack(pady=50)
    else:
        for c in clients:
            ligne = ctk.CTkFrame(scroll, fg_color="transparent", height=45)
            ligne.pack(fill="x", pady=2)
            ligne.pack_propagate(False)

            ctk.CTkLabel(ligne, text=c["nom"], font=("Arial", 14, "bold"),
                         text_color=BLANC, width=200, anchor="w").pack(side="left", padx=15)

            ctk.CTkLabel(ligne, text=c["telephone"] or "—",
                         font=("Arial", 14), text_color=BLANC,
                         width=160, anchor="w").pack(side="left", padx=15)

            ctk.CTkLabel(ligne, text=c["note"] or "—",
                         font=("Arial", 14), text_color="#aaa",
                         width=180, anchor="w").pack(side="left", padx=15)

            ctk.CTkLabel(ligne, text=c["date_ajout"] or "—",
                         font=("Arial", 13), text_color="#888",
                         width=130, anchor="w").pack(side="left", padx=15)

            # Actions
            zone_actions = ctk.CTkFrame(ligne, fg_color="transparent")
            zone_actions.pack(side="left", padx=15)

            # Bouton historique (toujours visible)
            ctk.CTkButton(
                zone_actions, text="📜", width=45, height=30,
                fg_color=GRIS, hover_color="#3a3a3a", text_color=OR,
                font=("Arial", 14),
                command=lambda cl=c: dialog_historique(app, cl)
            ).pack(side="left", padx=3)

            # Boutons admin
            if app.mode_admin:
                ctk.CTkButton(
                    zone_actions, text="✏️", width=45, height=30,
                    fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                    font=("Arial", 14),
                    command=lambda cl=c: dialog_client(app, cl)
                ).pack(side="left", padx=3)

                ctk.CTkButton(
                    zone_actions, text="🗑️", width=45, height=30,
                    fg_color=ROUGE, hover_color="#e74c3c", text_color=BLANC,
                    font=("Arial", 14),
                    command=lambda cl=c: supprimer_client(app, cl)
                ).pack(side="left", padx=3)


# ============================================
#   DIALOG : AJOUTER / MODIFIER UNE CLIENTE
# ============================================
def dialog_client(app, client):
    popup = ctk.CTkToplevel(app)
    popup.title("Cliente" + (" - Modifier" if client else " - Ajouter"))
    popup.geometry("450x500")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(
        popup, text="✏️ Modifier la cliente" if client else "➕ Nouvelle cliente",
        font=("Arial", 20, "bold"), text_color=OR
    ).pack(pady=(25, 20))

    # Nom
    ctk.CTkLabel(popup, text="Nom *", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_nom = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_nom.pack(pady=(5, 12))
    if client:
        ent_nom.insert(0, client["nom"])

    # Téléphone
    ctk.CTkLabel(popup, text="Téléphone", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_tel = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13),
                            placeholder_text="06 xx xx xx xx")
    ent_tel.pack(pady=(5, 12))
    if client and client["telephone"]:
        ent_tel.insert(0, client["telephone"])

    # Note
    ctk.CTkLabel(popup, text="Note (ex : VIP, cliente fidèle...)", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_note = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_note.pack(pady=(5, 20))
    if client and client["note"]:
        ent_note.insert(0, client["note"])

    def valider():
        nom = ent_nom.get().strip()
        tel = ent_tel.get().strip()
        note = ent_note.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire ❌")
            return

        if client:
            # Modification
            conn = db.get_connexion()
            cur = conn.cursor()
            cur.execute(
                "UPDATE clients SET nom=?, telephone=?, note=? WHERE id=?",
                (nom, tel, note, client["id"])
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Cliente modifiée ✅")
        else:
            # Ajout
            db.ajouter_client(nom, tel, note)
            messagebox.showinfo("Succès", "Cliente ajoutée ✅")

        popup.destroy()
        app.afficher_page("clients")

    ctk.CTkButton(
        popup, text="💾 Enregistrer",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 14, "bold"), height=42,
        command=valider
    ).pack(pady=10)


# ============================================
#   DIALOG : HISTORIQUE D'UNE CLIENTE
# ============================================
def dialog_historique(app, client):
    popup = ctk.CTkToplevel(app)
    popup.title(f"Historique - {client['nom']}")
    popup.geometry("750x600")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(
        popup, text=f"📜 Historique de {client['nom']}",
        font=("Arial", 22, "bold"), text_color=OR
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        popup, text=f"📞 {client['telephone'] or '—'}    🏷️ {client['note'] or '—'}",
        font=("Arial", 13), text_color="#aaa"
    ).pack(pady=(0, 15))

    # Récupérer les paiements de cette cliente
    conn = db.get_connexion()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*, s.nom as serveuse_nom, sv.nom as service_nom
        FROM paiements p
        LEFT JOIN serveuses s ON p.serveuse_id = s.id
        LEFT JOIN services sv ON p.service_id = sv.id
        WHERE p.client_id = ?
        ORDER BY p.date DESC, p.heure DESC
    """, (client["id"],))
    paiements = cur.fetchall()
    conn.close()

    # ===== RÉSUMÉ =====
    total_depense = sum(p["montant"] for p in paiements)
    nb_visites = len(paiements)

    cadre_resume = ctk.CTkFrame(popup, fg_color=NOIR_CLAIR,
                                 corner_radius=10, border_width=2, border_color=OR)
    cadre_resume.pack(fill="x", padx=30, pady=(0, 15))

    info_frame = ctk.CTkFrame(cadre_resume, fg_color="transparent")
    info_frame.pack(pady=15)

    ctk.CTkLabel(info_frame, text="💰 Total dépensé :",
                 font=("Arial", 14), text_color=BLANC).pack(side="left", padx=10)
    ctk.CTkLabel(info_frame, text=f"{total_depense:.0f} DH",
                 font=("Arial", 18, "bold"), text_color=OR).pack(side="left", padx=10)

    ctk.CTkLabel(info_frame, text="   |   ",
                 font=("Arial", 14), text_color="#555").pack(side="left")

    ctk.CTkLabel(info_frame, text="🛍️ Visites :",
                 font=("Arial", 14), text_color=BLANC).pack(side="left", padx=10)
    ctk.CTkLabel(info_frame, text=str(nb_visites),
                 font=("Arial", 18, "bold"), text_color=OR).pack(side="left", padx=10)

    # ===== LISTE DES PAIEMENTS =====
    ctk.CTkLabel(popup, text="📋 Détail des visites",
                 font=("Arial", 15, "bold"), text_color=OR).pack(anchor="w", padx=30, pady=(5, 5))

    scroll = ctk.CTkScrollableFrame(popup, fg_color=NOIR_CLAIR,
                                     corner_radius=10, border_width=1, border_color=GRIS)
    scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    if not paiements:
        ctk.CTkLabel(scroll, text="Aucune visite enregistrée 💤",
                     font=("Arial", 14), text_color="#888").pack(pady=40)
    else:
        # En-tête
        entete = ctk.CTkFrame(scroll, fg_color=GRIS, height=35, corner_radius=6)
        entete.pack(fill="x", pady=(0, 5))
        entete.pack_propagate(False)

        for label, largeur in [("Date", 120), ("Heure", 80), ("Serveuse", 150), ("Service", 180), ("Montant", 100)]:
            ctk.CTkLabel(entete, text=label, font=("Arial", 12, "bold"),
                         text_color=OR, width=largeur, anchor="w").pack(side="left", padx=8)

        # Lignes
        for p in paiements:
            ligne = ctk.CTkFrame(scroll, fg_color="transparent", height=35)
            ligne.pack(fill="x", pady=1)
            ligne.pack_propagate(False)

            ctk.CTkLabel(ligne, text=p["date"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=120, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=p["heure"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=80, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=p["serveuse_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=150, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=p["service_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=180, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(ligne, text=f"{p['montant']:.0f} DH",
                         font=("Arial", 13, "bold"), text_color=OR,
                         width=100, anchor="w").pack(side="left", padx=8)


# ============================================
#   SUPPRIMER UNE CLIENTE
# ============================================
def supprimer_client(app, client):
    if messagebox.askyesno("Confirmation",
                           f"Supprimer « {client['nom']} » ?\n"
                           "Son historique de paiements sera conservé."):
        db.supprimer_client(client["id"])
        app.afficher_page("clients")