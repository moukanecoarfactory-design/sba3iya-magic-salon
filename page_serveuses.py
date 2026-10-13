import customtkinter as ctk
from tkinter import messagebox
import database as db
from theme import *

# ============================================
#   PAGE SERVEUSES
# ============================================

def afficher(app):
    contenu = app.contenu

    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header, text="💇 Serveuses | العاملات",
        font=("Arial", 26, "bold"), text_color=OR
    ).pack(side="left")

    if app.mode_admin:
        ctk.CTkLabel(
            header, text="🔓 Mode Admin activé",
            font=("Arial", 14, "bold"), text_color=VERT
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            header, text="➕ Ajouter une serveuse",
            fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
            font=("Arial", 13, "bold"), width=210, height=40,
            command=lambda: dialog_serveuse(app, None)
        ).pack(side="right", padx=10)

    scroll = ctk.CTkScrollableFrame(
        contenu, fg_color=NOIR_CLAIR,
        corner_radius=12, border_width=1, border_color=GRIS
    )
    scroll.pack(fill="both", expand=True, padx=30, pady=(10, 30))

    entete = ctk.CTkFrame(scroll, fg_color=GRIS, height=40, corner_radius=8)
    entete.pack(fill="x", pady=(0, 5))
    entete.pack_propagate(False)

    ctk.CTkLabel(entete, text="Nom",
                 font=("Arial", 13, "bold"), text_color=OR, width=200, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Spécialité",
                 font=("Arial", 13, "bold"), text_color=OR, width=220, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Téléphone",
                 font=("Arial", 13, "bold"), text_color=OR, width=180, anchor="w").pack(side="left", padx=15)

    if app.mode_admin:
        ctk.CTkLabel(entete, text="Actions",
                     font=("Arial", 13, "bold"), text_color=OR, width=150).pack(side="left", padx=15)

    serveuses = db.get_serveuses(actives_seulement=False)
    if not serveuses:
        ctk.CTkLabel(
            scroll, text="Aucune serveuse pour le moment.\nCliquez sur ➕ pour en ajouter.",
            font=("Arial", 15), text_color="#888"
        ).pack(pady=50)
    else:
        for s in serveuses:
            ligne = ctk.CTkFrame(scroll, fg_color="transparent", height=45)
            ligne.pack(fill="x", pady=2)
            ligne.pack_propagate(False)

            ctk.CTkLabel(ligne, text=s["nom"], font=("Arial", 14, "bold"),
                         text_color=BLANC, width=200, anchor="w").pack(side="left", padx=15)

            ctk.CTkLabel(ligne, text=s["specialite"] or "—",
                         font=("Arial", 14), text_color=BLANC,
                         width=220, anchor="w").pack(side="left", padx=15)

            ctk.CTkLabel(ligne, text=s["telephone"] or "—",
                         font=("Arial", 14), text_color=BLANC,
                         width=180, anchor="w").pack(side="left", padx=15)

            if app.mode_admin:
                zone_actions = ctk.CTkFrame(ligne, fg_color="transparent")
                zone_actions.pack(side="left", padx=15)

                ctk.CTkButton(
                    zone_actions, text="✏️", width=45, height=30,
                    fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                    font=("Arial", 14),
                    command=lambda srv=s: dialog_serveuse(app, srv)
                ).pack(side="left", padx=3)

                ctk.CTkButton(
                    zone_actions, text="🗑️", width=45, height=30,
                    fg_color=ROUGE, hover_color="#e74c3c", text_color=BLANC,
                    font=("Arial", 14),
                    command=lambda srv=s: supprimer_serveuse(app, srv)
                ).pack(side="left", padx=3)


def dialog_serveuse(app, serveuse):
    popup = ctk.CTkToplevel(app)
    popup.title("Serveuse" + (" - Modifier" if serveuse else " - Ajouter"))
    popup.geometry("450x480")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(
        popup, text="✏️ Modifier la serveuse" if serveuse else "➕ Nouvelle serveuse",
        font=("Arial", 20, "bold"), text_color=OR
    ).pack(pady=(25, 20))

    ctk.CTkLabel(popup, text="Nom", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_nom = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_nom.pack(pady=(5, 12))
    if serveuse:
        ent_nom.insert(0, serveuse["nom"])

    ctk.CTkLabel(popup, text="Spécialité", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)

    services = db.get_services()
    liste_spe = ["Tous les services"] + [s["nom"] for s in services]
    combo = ctk.CTkComboBox(
        popup, values=liste_spe, width=350, height=38,
        font=("Arial", 13), dropdown_font=("Arial", 13),
        fg_color=GRIS, button_color=OR, border_color=OR
    )
    combo.pack(pady=(5, 12))
    if serveuse and serveuse["specialite"]:
        combo.set(serveuse["specialite"])
    else:
        combo.set("Tous les services")

    ctk.CTkLabel(popup, text="Téléphone (optionnel)", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_tel = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_tel.pack(pady=(5, 20))
    if serveuse and serveuse["telephone"]:
        ent_tel.insert(0, serveuse["telephone"])

    def valider():
        nom = ent_nom.get().strip()
        specialite = combo.get().strip()
        telephone = ent_tel.get().strip()

        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire ❌")
            return

        if serveuse:
            db.modifier_serveuse(serveuse["id"], nom, specialite, telephone)
            messagebox.showinfo("Succès", "Serveuse modifiée ✅")
        else:
            db.ajouter_serveuse(nom, specialite, telephone)
            messagebox.showinfo("Succès", "Serveuse ajoutée ✅")

        popup.destroy()
        app.afficher_page("serveuses")

    ctk.CTkButton(
        popup, text="💾 Enregistrer",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 14, "bold"), height=42,
        command=valider
    ).pack(pady=10)


def supprimer_serveuse(app, serveuse):
    if messagebox.askyesno("Confirmation", f"Supprimer « {serveuse['nom']} » ?"):
        db.supprimer_serveuse(serveuse["id"])
        app.afficher_page("serveuses")