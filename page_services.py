import customtkinter as ctk
from tkinter import messagebox
import database as db
from theme import *

# ============================================
#   PAGE SERVICES
# ============================================

def afficher(app):
    contenu = app.contenu

    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(
        header, text="✂️ Services | الخدمات",
        font=("Arial", 26, "bold"), text_color=OR
    ).pack(side="left")

    if app.mode_admin:
        ctk.CTkLabel(
            header, text="🔓 Mode Admin activé",
            font=("Arial", 14, "bold"), text_color=VERT
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            header, text="➕ Ajouter un service",
            fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
            font=("Arial", 13, "bold"), width=180, height=40,
            command=lambda: dialog_service(app, None)
        ).pack(side="right", padx=10)

    scroll = ctk.CTkScrollableFrame(
        contenu, fg_color=NOIR_CLAIR,
        corner_radius=12, border_width=1, border_color=GRIS
    )
    scroll.pack(fill="both", expand=True, padx=30, pady=(10, 30))

    entete = ctk.CTkFrame(scroll, fg_color=GRIS, height=40, corner_radius=8)
    entete.pack(fill="x", pady=(0, 5))
    entete.pack_propagate(False)

    ctk.CTkLabel(entete, text="Service (FR)",
                 font=("Arial", 13, "bold"), text_color=OR, width=180, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="الخدمة (AR)",
                 font=("Arial", 13, "bold"), text_color=OR, width=200, anchor="w").pack(side="left", padx=15)
    ctk.CTkLabel(entete, text="Prix (DH)",
                 font=("Arial", 13, "bold"), text_color=OR, width=120, anchor="w").pack(side="left", padx=15)

    if app.mode_admin:
        ctk.CTkLabel(entete, text="Actions",
                     font=("Arial", 13, "bold"), text_color=OR, width=150).pack(side="left", padx=15)

    services = db.get_services(actifs_seulement=False)
    for s in services:
        ligne = ctk.CTkFrame(scroll, fg_color="transparent", height=45)
        ligne.pack(fill="x", pady=2)
        ligne.pack_propagate(False)

        ctk.CTkLabel(ligne, text=s["nom"], font=("Arial", 14),
                     text_color=BLANC, width=180, anchor="w").pack(side="left", padx=15)

        ctk.CTkLabel(ligne, text=s["nom_ar"] or "", font=("Arial", 14),
                     text_color=BLANC, width=200, anchor="w").pack(side="left", padx=15)

        prix_texte = f"{s['prix']:.0f} DH" if s["prix"] > 0 else "— à définir"
        couleur_prix = OR if s["prix"] > 0 else "#888"
        ctk.CTkLabel(ligne, text=prix_texte, font=("Arial", 14, "bold"),
                     text_color=couleur_prix, width=120, anchor="w").pack(side="left", padx=15)

        if app.mode_admin:
            zone_actions = ctk.CTkFrame(ligne, fg_color="transparent")
            zone_actions.pack(side="left", padx=15)

            ctk.CTkButton(
                zone_actions, text="✏️", width=45, height=30,
                fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                font=("Arial", 14),
                command=lambda srv=s: dialog_service(app, srv)
            ).pack(side="left", padx=3)

            ctk.CTkButton(
                zone_actions, text="🗑️", width=45, height=30,
                fg_color=ROUGE, hover_color="#e74c3c", text_color=BLANC,
                font=("Arial", 14),
                command=lambda srv=s: supprimer_service(app, srv)
            ).pack(side="left", padx=3)


def dialog_service(app, service):
    popup = ctk.CTkToplevel(app)
    popup.title("Service" + (" - Modifier" if service else " - Ajouter"))
    popup.geometry("450x420")
    popup.configure(fg_color=NOIR)
    popup.grab_set()

    ctk.CTkLabel(
        popup, text="✏️ Modifier le service" if service else "➕ Nouveau service",
        font=("Arial", 20, "bold"), text_color=OR
    ).pack(pady=(25, 20))

    ctk.CTkLabel(popup, text="Nom (Français)", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_nom = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_nom.pack(pady=(5, 12))
    if service:
        ent_nom.insert(0, service["nom"])

    ctk.CTkLabel(popup, text="الاسم (بالعربية)", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_ar = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_ar.pack(pady=(5, 12))
    if service and service["nom_ar"]:
        ent_ar.insert(0, service["nom_ar"])

    ctk.CTkLabel(popup, text="Prix (DH)", font=("Arial", 13),
                 text_color=BLANC).pack(anchor="w", padx=40)
    ent_prix = ctk.CTkEntry(popup, width=350, height=38, font=("Arial", 13))
    ent_prix.pack(pady=(5, 20))
    if service:
        ent_prix.insert(0, str(int(service["prix"])))

    def valider():
        nom = ent_nom.get().strip()
        nom_ar = ent_ar.get().strip()
        try:
            prix = float(ent_prix.get().strip() or "0")
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre ❌")
            return

        if not nom:
            messagebox.showerror("Erreur", "Le nom est obligatoire ❌")
            return

        if service:
            db.modifier_service(service["id"], nom, nom_ar, prix)
            messagebox.showinfo("Succès", "Service modifié ✅")
        else:
            db.ajouter_service(nom, nom_ar, prix)
            messagebox.showinfo("Succès", "Service ajouté ✅")

        popup.destroy()
        app.afficher_page("services")

    ctk.CTkButton(
        popup, text="💾 Enregistrer",
        fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
        font=("Arial", 14, "bold"), height=42,
        command=valider
    ).pack(pady=10)


def supprimer_service(app, service):
    if messagebox.askyesno("Confirmation", f"Supprimer « {service['nom']} » ?"):
        db.supprimer_service(service["id"])
        app.afficher_page("services")