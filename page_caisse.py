import customtkinter as ctk
from tkinter import messagebox
import database as db
from theme import *

# ============================================
#   PAGE CAISSE
# ============================================

def afficher(app):
    contenu = app.contenu

    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header, text="💰 Caisse | الصندوق",
        font=("Arial", 26, "bold"), text_color=OR
    ).pack(side="left")

    btn_frame = ctk.CTkFrame(header, fg_color="transparent")
    btn_frame.pack(side="right")

    ctk.CTkButton(
        btn_frame, text="💵 Fond de caisse",
        fg_color=GRIS, hover_color="#3a3a3a", text_color=OR,
        font=("Arial", 13, "bold"), width=170, height=40,
        command=lambda: dialog_fond_caisse(app)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame, text="➕ Nouvel encaissement",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 13, "bold"), width=200, height=40,
        command=lambda: dialog_encaissement(app)
    ).pack(side="left", padx=5)

    zone_resume = ctk.CTkFrame(contenu, fg_color="transparent")
    zone_resume.pack(fill="x", padx=30, pady=15)

    fond = db.get_caisse_demarrage()
    ventes = db.get_total_caisse_jour()
    total = fond + ventes

    cartes = [
        ("💵", f"{fond:.0f} DH", "Fond de caisse", OR),
        ("📈", f"{ventes:.0f} DH", "Ventes du jour", VERT),
        ("💰", f"{total:.0f} DH", "TOTAL DU JOUR", OR_CLAIR),
    ]

    for emoji, valeur, label, couleur in cartes:
        carte = ctk.CTkFrame(
            zone_resume, height=110, corner_radius=12,
            fg_color=NOIR_CLAIR, border_width=2, border_color=couleur
        )
        carte.pack(side="left", padx=8, fill="x", expand=True)
        carte.pack_propagate(False)

        ctk.CTkLabel(carte, text=f"{emoji}  {label}",
                     font=("Arial", 13, "bold"), text_color=couleur).pack(pady=(18, 5))
        ctk.CTkLabel(carte, text=valeur,
                     font=("Arial", 26, "bold"), text_color=BLANC).pack()

    ctk.CTkLabel(
        contenu, text="👥 Caisse par serveuse",
        font=("Arial", 16, "bold"), text_color=OR
    ).pack(anchor="w", padx=30, pady=(10, 5))

    cadre_sv = ctk.CTkScrollableFrame(
        contenu, fg_color=NOIR_CLAIR, height=130,
        corner_radius=10, border_width=1, border_color=GRIS,
        orientation="horizontal"
    )
    cadre_sv.pack(fill="x", padx=30, pady=(0, 15))

    caisse_sv = db.get_caisse_par_serveuse()
    if not caisse_sv:
        ctk.CTkLabel(cadre_sv, text="Aucune serveuse enregistrée",
                     font=("Arial", 13), text_color="#888").pack(pady=30)
    else:
        for s in caisse_sv:
            petite = ctk.CTkFrame(
                cadre_sv, width=160, height=90, corner_radius=10,
                fg_color=GRIS, border_width=1, border_color=OR
            )
            petite.pack(side="left", padx=6, pady=8)
            petite.pack_propagate(False)

            ctk.CTkLabel(petite, text=s["nom"],
                         font=("Arial", 13, "bold"),
                         text_color=BLANC).pack(pady=(12, 3))
            ctk.CTkLabel(petite, text=f"{s['total']:.0f} DH",
                         font=("Arial", 18, "bold"),
                         text_color=OR).pack()

    ctk.CTkLabel(
        contenu, text="📋 Détail des encaissements du jour",
        font=("Arial", 16, "bold"), text_color=OR
    ).pack(anchor="w", padx=30, pady=(5, 5))

    scroll = ctk.CTkScrollableFrame(
        contenu, fg_color=NOIR_CLAIR,
        corner_radius=10, border_width=1, border_color=GRIS
    )
    scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))

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

    paiements = db.get_paiements_du_jour()
    if not paiements:
        ctk.CTkLabel(scroll, text="Aucun encaissement aujourd'hui 💤",
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


def dialog_fond_caisse(app):
    popup = ctk.CTkToplevel(app)
    popup.title("Fond de caisse")
    popup.geometry("420x300")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(popup, text="💵 Fond de caisse du jour",
                 font=("Arial", 20, "bold"), text_color=OR).pack(pady=(30, 10))

    ctk.CTkLabel(popup, text="Montant de départ dans la caisse",
                 font=("Arial", 13), text_color=BLANC).pack(pady=(0, 15))

    ent = ctk.CTkEntry(popup, width=280, height=42,
                       font=("Arial", 16), justify="center")
    ent.pack(pady=10)
    fond_actuel = db.get_caisse_demarrage()
    if fond_actuel > 0:
        ent.insert(0, str(int(fond_actuel)))
    ent.focus()

    def valider():
        try:
            montant = float(ent.get().strip() or "0")
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide ❌")
            return

        db.set_caisse_demarrage(montant)
        messagebox.showinfo("Succès", f"Fond de caisse : {montant:.0f} DH ✅")
        popup.destroy()
        app.afficher_page("caisse")

    ctk.CTkButton(popup, text="💾 Enregistrer",
                  fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                  font=("Arial", 14, "bold"), height=42, width=200,
                  command=valider).pack(pady=20)

    ent.bind("<Return>", lambda e: valider())


def dialog_encaissement(app):
    serveuses = db.get_serveuses()
    services = db.get_services()

    if not serveuses:
        messagebox.showwarning("Attention",
            "Aucune serveuse enregistrée.\nAjoutez d'abord une serveuse. ⚠️")
        return

    if not services:
        messagebox.showwarning("Attention", "Aucun service enregistré. ⚠️")
        return

    popup = ctk.CTkToplevel(app)
    popup.title("Nouvel encaissement")
    popup.geometry("620x720")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(popup, text="💰 Nouvel encaissement",
                 font=("Arial", 22, "bold"), text_color=OR).pack(pady=(25, 15))

    ctk.CTkLabel(popup, text="👤 Nom de la cliente (optionnel)",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    ent_client = ctk.CTkEntry(popup, width=520, height=38,
                               font=("Arial", 13),
                               placeholder_text="Nom ou laisser vide")
    ent_client.pack(pady=(5, 12))

    ctk.CTkLabel(popup, text="💇 Serveuse",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)
    combo_sv = ctk.CTkComboBox(
        popup, values=[s["nom"] for s in serveuses],
        width=520, height=38, font=("Arial", 13),
        dropdown_font=("Arial", 13),
        fg_color=GRIS, button_color=OR, border_color=OR
    )
    combo_sv.pack(pady=(5, 12))
    combo_sv.set(serveuses[0]["nom"])

    ctk.CTkLabel(popup, text="✂️ Services (cochez un ou plusieurs)",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=50)

    cadre_serv = ctk.CTkScrollableFrame(
        popup, width=520, height=250,
        fg_color=GRIS, corner_radius=8,
        border_width=1, border_color=OR
    )
    cadre_serv.pack(pady=(5, 12))

    variables = {}
    for s in services:
        if s["prix"] <= 0:
            continue

        ligne = ctk.CTkFrame(cadre_serv, fg_color="transparent", height=35)
        ligne.pack(fill="x", pady=2)
        ligne.pack_propagate(False)

        var = ctk.BooleanVar(value=False)
        chk = ctk.CTkCheckBox(
            ligne, text=s["nom"], variable=var,
            font=("Arial", 13), text_color=BLANC,
            fg_color=OR, hover_color=OR_CLAIR,
            checkmark_color=NOIR, border_color=OR
        )
        chk.pack(side="left", padx=10)

        ctk.CTkLabel(ligne, text=f"{s['prix']:.0f} DH",
                     font=("Arial", 13, "bold"),
                     text_color=OR, width=100).pack(side="right", padx=10)

        variables[s["id"]] = (var, s["prix"], s["nom"])

    if not variables:
        ctk.CTkLabel(cadre_serv,
            text="Aucun service avec prix.\nDéfinissez les prix d'abord.",
            font=("Arial", 13), text_color="#888").pack(pady=30)

    cadre_total = ctk.CTkFrame(popup, fg_color=NOIR_CLAIR,
                                corner_radius=10, border_width=2, border_color=OR)
    cadre_total.pack(fill="x", padx=50, pady=(5, 10))

    label_total = ctk.CTkLabel(cadre_total, text="TOTAL :  0 DH",
                               font=("Arial", 22, "bold"), text_color=OR)
    label_total.pack(pady=15)

    def maj_total():
        total = sum(prix for (var, prix, nom) in variables.values() if var.get())
        label_total.configure(text=f"TOTAL :  {total:.0f} DH")

    for (var, _, _) in variables.values():
        var.trace_add("write", lambda *a: maj_total())

    def valider():
        services_choisis = [
            (sid, prix, nom) for sid, (var, prix, nom) in variables.items()
            if var.get()
        ]

        if not services_choisis:
            messagebox.showwarning("Attention", "Cochez au moins un service ⚠️")
            return

        nom_sv = combo_sv.get()
        sv = next((s for s in serveuses if s["nom"] == nom_sv), None)
        if not sv:
            messagebox.showerror("Erreur", "Serveuse introuvable ❌")
            return

        nom_client = ent_client.get().strip()
        client_id = None
        if nom_client:
            clients = db.get_clients()
            existant = next((c for c in clients if c["nom"].lower() == nom_client.lower()), None)
            if existant:
                client_id = existant["id"]
            else:
                db.ajouter_client(nom_client)
                clients = db.get_clients()
                nouveau = next((c for c in clients if c["nom"].lower() == nom_client.lower()), None)
                client_id = nouveau["id"] if nouveau else None

        total_encaisse = 0
        for sid, prix, nom in services_choisis:
            db.ajouter_paiement(client_id, sv["id"], sid, prix)
            total_encaisse += prix

        messagebox.showinfo("Succès",
            f"Encaissement enregistré ✅\n\n"
            f"Serveuse : {sv['nom']}\n"
            f"Services : {len(services_choisis)}\n"
            f"Total : {total_encaisse:.0f} DH")
        popup.destroy()
        app.afficher_page("caisse")

    ctk.CTkButton(popup, text="💾 Valider l'encaissement",
                  fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                  font=("Arial", 15, "bold"), height=48, width=350,
                  command=valider).pack(pady=(5, 20))