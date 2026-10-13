import customtkinter as ctk
from tkinter import messagebox
import database as db
from theme import *
from datetime import datetime, timedelta

# ============================================
#   PAGE RENDEZ-VOUS
# ============================================

date_selectionnee = None


def afficher(app):
    global date_selectionnee

    if date_selectionnee is None:
        date_selectionnee = datetime.now().strftime("%Y-%m-%d")

    contenu = app.contenu

    # ===== EN-TÊTE =====
    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header, text="📅 Rendez-vous | المواعيد",
        font=("Arial", 26, "bold"), text_color=OR
    ).pack(side="left")

    ctk.CTkButton(
        header, text="➕ Nouveau RDV",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 13, "bold"), width=190, height=40,
        command=lambda: dialog_rdv(app, None)
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
        nouvelle = ent_date.get().strip()
        try:
            datetime.strptime(nouvelle, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur",
                "Format invalide.\nUtilisez AAAA-MM-JJ (ex : 2026-10-15) ❌")
            return
        date_selectionnee = nouvelle
        app.afficher_page("rdv")

    def aujourd_hui():
        global date_selectionnee
        date_selectionnee = datetime.now().strftime("%Y-%m-%d")
        app.afficher_page("rdv")

    def demain():
        global date_selectionnee
        date_selectionnee = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        app.afficher_page("rdv")

    ctk.CTkButton(inner, text="✅ Appliquer",
                  fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                  font=("Arial", 12, "bold"), width=110, height=38,
                  command=appliquer_date).pack(side="left", padx=5)

    ctk.CTkButton(inner, text="Aujourd'hui",
                  fg_color=GRIS, hover_color="#3a3a3a", text_color=OR,
                  font=("Arial", 12), width=110, height=38,
                  command=aujourd_hui).pack(side="left", padx=5)

    ctk.CTkButton(inner, text="Demain",
                  fg_color=GRIS, hover_color="#3a3a3a", text_color=OR,
                  font=("Arial", 12), width=90, height=38,
                  command=demain).pack(side="left", padx=5)

    # ===== RÉSUMÉ =====
    rdv_du_jour = get_rdv_par_date(date_selectionnee)
    nb_total = len(rdv_du_jour)
    nb_prevu = len([r for r in rdv_du_jour if r["statut"] == "prevu"])
    nb_fait = len([r for r in rdv_du_jour if r["statut"] == "fait"])
    nb_annule = len([r for r in rdv_du_jour if r["statut"] == "annule"])

    zone_resume = ctk.CTkFrame(contenu, fg_color="transparent")
    zone_resume.pack(fill="x", padx=30, pady=10)

    stats = [
        ("📋", str(nb_total), "Total RDV", OR),
        ("⏳", str(nb_prevu), "Prévus", "#f39c12"),
        ("✅", str(nb_fait), "Faits", VERT),
        ("❌", str(nb_annule), "Annulés", ROUGE),
    ]

    for emoji, valeur, label, couleur in stats:
        carte = ctk.CTkFrame(
            zone_resume, height=90, corner_radius=10,
            fg_color=NOIR_CLAIR, border_width=2, border_color=couleur
        )
        carte.pack(side="left", padx=6, fill="x", expand=True)
        carte.pack_propagate(False)

        ctk.CTkLabel(carte, text=f"{emoji}  {label}",
                     font=("Arial", 12, "bold"), text_color=couleur).pack(pady=(12, 3))
        ctk.CTkLabel(carte, text=valeur,
                     font=("Arial", 22, "bold"), text_color=BLANC).pack()

    # ===== LISTE DES RDV =====
    ctk.CTkLabel(contenu, text=f"📋 Rendez-vous du {date_selectionnee}",
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
        ("Service", 160), ("Statut", 100), ("Actions", 220)
    ]
    for label, largeur in cols:
        ctk.CTkLabel(entete, text=label, font=("Arial", 12, "bold"),
                     text_color=OR, width=largeur, anchor="w").pack(side="left", padx=8)

    if not rdv_du_jour:
        ctk.CTkLabel(scroll, text=f"Aucun rendez-vous le {date_selectionnee} 💤",
                     font=("Arial", 14), text_color="#888").pack(pady=40)
    else:
        for r in rdv_du_jour:
            ligne = ctk.CTkFrame(scroll, fg_color="transparent", height=40)
            ligne.pack(fill="x", pady=1)
            ligne.pack_propagate(False)

            ctk.CTkLabel(ligne, text=r["heure"] or "—",
                         font=("Arial", 13, "bold"), text_color=OR,
                         width=80, anchor="w").pack(side="left", padx=8)

            ctk.CTkLabel(ligne, text=r["client_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=160, anchor="w").pack(side="left", padx=8)

            ctk.CTkLabel(ligne, text=r["serveuse_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=140, anchor="w").pack(side="left", padx=8)

            ctk.CTkLabel(ligne, text=r["service_nom"] or "—",
                         font=("Arial", 13), text_color=BLANC,
                         width=160, anchor="w").pack(side="left", padx=8)

            # Statut coloré
            statut = r["statut"]
            if statut == "prevu":
                texte_st, couleur_st = "⏳ Prévu", "#f39c12"
            elif statut == "fait":
                texte_st, couleur_st = "✅ Fait", VERT
            else:
                texte_st, couleur_st = "❌ Annulé", ROUGE

            ctk.CTkLabel(ligne, text=texte_st,
                         font=("Arial", 12, "bold"), text_color=couleur_st,
                         width=100, anchor="w").pack(side="left", padx=8)

            # Actions
            zone_actions = ctk.CTkFrame(ligne, fg_color="transparent")
            zone_actions.pack(side="left", padx=8)

            if statut == "prevu":
                ctk.CTkButton(
                    zone_actions, text="✅ Fait", width=70, height=28,
                    fg_color=VERT, hover_color="#2ecc71", text_color=BLANC,
                    font=("Arial", 12, "bold"),
                    command=lambda rd=r: marquer_fait(app, rd)
                ).pack(side="left", padx=2)

                ctk.CTkButton(
                    zone_actions, text="❌", width=40, height=28,
                    fg_color=ROUGE, hover_color="#e74c3c", text_color=BLANC,
                    font=("Arial", 12),
                    command=lambda rd=r: annuler_rdv(app, rd)
                ).pack(side="left", padx=2)

            ctk.CTkButton(
                zone_actions, text="🗑️", width=40, height=28,
                fg_color=GRIS, hover_color="#3a3a3a", text_color=BLANC,
                font=("Arial", 12),
                command=lambda rd=r: supprimer_rdv(app, rd)
            ).pack(side="left", padx=2)


# ============================================
#   RÉCUPÉRER LES RDV PAR DATE
# ============================================
def get_rdv_par_date(date):
    conn = db.get_connexion()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, c.nom as client_nom, s.nom as serveuse_nom, sv.nom as service_nom
        FROM rendez_vous r
        LEFT JOIN clients c ON r.client_id = c.id
        LEFT JOIN serveuses s ON r.serveuse_id = s.id
        LEFT JOIN services sv ON r.service_id = sv.id
        WHERE r.date = ?
        ORDER BY r.heure ASC
    """, (date,))
    rows = cur.fetchall()
    conn.close()
    return rows


# ============================================
#   DIALOG : NOUVEAU RDV
# ============================================
def dialog_rdv(app, rdv_existant):
    clients = db.get_clients()
    serveuses = db.get_serveuses()
    services = db.get_services()

    if not clients:
        messagebox.showwarning("Attention",
            "Aucune cliente enregistrée.\nAjoutez d'abord une cliente. ⚠️")
        return
    if not serveuses:
        messagebox.showwarning("Attention",
            "Aucune serveuse enregistrée. ⚠️")
        return
    if not services:
        messagebox.showwarning("Attention",
            "Aucun service enregistré. ⚠️")
        return

    popup = ctk.CTkToplevel(app)
    popup.title("Nouveau rendez-vous")
    popup.geometry("560x720")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(popup, text="📅 Nouveau rendez-vous",
                 font=("Arial", 22, "bold"), text_color=OR).pack(pady=(25, 15))

    # ===== CLIENTE =====
    ctk.CTkLabel(popup, text="👤 Cliente",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    combo_cl = ctk.CTkComboBox(
        popup, values=[c["nom"] for c in clients],
        width=460, height=38, font=("Arial", 13),
        dropdown_font=("Arial", 13),
        fg_color=GRIS, button_color=OR, border_color=OR
    )
    combo_cl.pack(pady=(5, 12))
    combo_cl.set(clients[0]["nom"])

    # ===== SERVEUSE =====
    ctk.CTkLabel(popup, text="💇 Serveuse",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    combo_sv = ctk.CTkComboBox(
        popup, values=[s["nom"] for s in serveuses],
        width=460, height=38, font=("Arial", 13),
        dropdown_font=("Arial", 13),
        fg_color=GRIS, button_color=OR, border_color=OR
    )
    combo_sv.pack(pady=(5, 12))
    combo_sv.set(serveuses[0]["nom"])

    # ===== SERVICE =====
    ctk.CTkLabel(popup, text="✂️ Service",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    combo_serv = ctk.CTkComboBox(
        popup, values=[s["nom"] for s in services],
        width=460, height=38, font=("Arial", 13),
        dropdown_font=("Arial", 13),
        fg_color=GRIS, button_color=OR, border_color=OR
    )
    combo_serv.pack(pady=(5, 12))
    combo_serv.set(services[0]["nom"])

    # ===== DATE =====
    ctk.CTkLabel(popup, text="📅 Date (AAAA-MM-JJ)",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    ent_date = ctk.CTkEntry(popup, width=460, height=38,
                             font=("Arial", 13), justify="center",
                             fg_color=GRIS, border_color=OR, border_width=1)
    ent_date.pack(pady=(5, 12))
    ent_date.insert(0, date_selectionnee)

    # ===== HEURE =====
    ctk.CTkLabel(popup, text="🕐 Heure (HH:MM)",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    ent_heure = ctk.CTkEntry(popup, width=460, height=38,
                              font=("Arial", 13), justify="center",
                              placeholder_text="ex : 14:30",
                              fg_color=GRIS, border_color=OR, border_width=1)
    ent_heure.pack(pady=(5, 20))

    def valider():
        nom_cl = combo_cl.get()
        nom_sv = combo_sv.get()
        nom_serv = combo_serv.get()
        date_rdv = ent_date.get().strip()
        heure_rdv = ent_heure.get().strip()

        # Validations
        if not heure_rdv:
            messagebox.showerror("Erreur", "L'heure est obligatoire ❌")
            return

        try:
            datetime.strptime(date_rdv, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide ❌")
            return

        try:
            datetime.strptime(heure_rdv, "%H:%M")
        except ValueError:
            messagebox.showerror("Erreur", "Format d'heure invalide (HH:MM) ❌")
            return

        # Récupérer les IDs
        cl = next((c for c in clients if c["nom"] == nom_cl), None)
        sv = next((s for s in serveuses if s["nom"] == nom_sv), None)
        se = next((s for s in services if s["nom"] == nom_serv), None)

        if not (cl and sv and se):
            messagebox.showerror("Erreur", "Sélection invalide ❌")
            return

        # Vérifier les conflits : la serveuse a-t-elle déjà un RDV à cette heure ?
        conn = db.get_connexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) as nb FROM rendez_vous
            WHERE serveuse_id = ? AND date = ? AND heure = ?
            AND statut != 'annule'
        """, (sv["id"], date_rdv, heure_rdv))
        conflit = cur.fetchone()["nb"]

        if conflit > 0:
            conn.close()
            messagebox.showerror("Conflit ⚠️",
                f"{sv['nom']} a déjà un rendez-vous\n"
                f"le {date_rdv} à {heure_rdv}.\n\n"
                "Choisissez une autre heure ou une autre serveuse.")
            return

        # Enregistrer
        cur.execute("""
            INSERT INTO rendez_vous (client_id, serveuse_id, service_id, date, heure, statut)
            VALUES (?, ?, ?, ?, ?, 'prevu')
        """, (cl["id"], sv["id"], se["id"], date_rdv, heure_rdv))
        conn.commit()
        conn.close()

        messagebox.showinfo("Succès",
            f"Rendez-vous enregistré ✅\n\n"
            f"Cliente : {cl['nom']}\n"
            f"Serveuse : {sv['nom']}\n"
            f"Service : {se['nom']}\n"
            f"Date : {date_rdv} à {heure_rdv}")

        popup.destroy()
        # Basculer sur la date du RDV créé
        global date_selectionnee
        date_selectionnee = date_rdv
        app.afficher_page("rdv")

    ctk.CTkButton(popup, text="💾 Enregistrer le RDV",
                  fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                  font=("Arial", 14, "bold"), height=48, width=350,
                  command=valider).pack(pady=(5, 20))


# ============================================
#   MARQUER UN RDV COMME FAIT (+ encaissement)
# ============================================
def marquer_fait(app, rdv):
    # 1) Mettre le statut à "fait"
    conn = db.get_connexion()
    cur = conn.cursor()
    cur.execute("UPDATE rendez_vous SET statut='fait' WHERE id=?", (rdv["id"],))
    conn.commit()
    conn.close()

    # 2) Proposer d'encaisser
    reponse = messagebox.askyesno(
        "Encaisser ? 💰",
        f"Le RDV de {rdv['client_nom']} est marqué comme FAIT ✅\n\n"
        f"Souhaitez-vous enregistrer l'encaissement maintenant ?\n"
        f"• Cliente : {rdv['client_nom']}\n"
        f"• Serveuse : {rdv['serveuse_nom']}\n"
        f"• Service : {rdv['service_nom']}"
    )

    if reponse:
        # Récupérer le prix du service
        conn = db.get_connexion()
        cur = conn.cursor()
        cur.execute("SELECT prix FROM services WHERE id=?", (rdv["service_id"],))
        row = cur.fetchone()
        montant = row["prix"] if row else 0
        conn.close()

        if montant <= 0:
            messagebox.showwarning("Attention",
                "Le prix de ce service n'est pas défini.\n"
                "Définissez son prix dans ✂️ Services d'abord. ⚠️")
        else:
            # Ajouter le paiement
            db.ajouter_paiement(
                rdv["client_id"], rdv["serveuse_id"],
                rdv["service_id"], montant
            )
            messagebox.showinfo("Succès",
                f"Encaissement enregistré ✅\n\n"
                f"Montant : {montant:.0f} DH")

    app.afficher_page("rdv")


# ============================================
#   ANNULER UN RDV
# ============================================
def annuler_rdv(app, rdv):
    if messagebox.askyesno("Confirmation",
                           f"Annuler le RDV de {rdv['client_nom']} ?"):
        conn = db.get_connexion()
        cur = conn.cursor()
        cur.execute("UPDATE rendez_vous SET statut='annule' WHERE id=?", (rdv["id"],))
        conn.commit()
        conn.close()
        app.afficher_page("rdv")


# ============================================
#   SUPPRIMER UN RDV
# ============================================
def supprimer_rdv(app, rdv):
    if messagebox.askyesno("⚠️ Confirmation",
        f"Supprimer définitivement le RDV de {rdv['client_nom']} ?\n"
        "Cette action est irréversible."):
        conn = db.get_connexion()
        cur = conn.cursor()
        cur.execute("DELETE FROM rendez_vous WHERE id=?", (rdv["id"],))
        conn.commit()
        conn.close()
        app.afficher_page("rdv")