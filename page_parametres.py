import customtkinter as ctk
from tkinter import messagebox
import database as db
from theme import *
from datetime import datetime

# ============================================
#   PAGE PARAMETRES
# ============================================

def afficher(app):
    contenu = app.contenu

    header = ctk.CTkFrame(contenu, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(25, 10))

    ctk.CTkLabel(header, text="⚙️ Paramètres | الإعدادات",
                 font=("Arial", 26, "bold"), text_color=OR).pack(side="left")

    scroll = ctk.CTkScrollableFrame(contenu, fg_color="transparent")
    scroll.pack(fill="both", expand=True, padx=30, pady=(10, 30))

    # ===== BLOC 1 : Mot de passe =====
    cadre_mdp = ctk.CTkFrame(scroll, fg_color=NOIR_CLAIR,
                              corner_radius=12, border_width=2, border_color=OR)
    cadre_mdp.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(cadre_mdp, text="🔒 Mot de passe Admin",
                 font=("Arial", 18, "bold"), text_color=OR).pack(anchor="w", padx=25, pady=(20, 5))
    ctk.CTkLabel(cadre_mdp, text="Modifiez le mot de passe pour accéder au mode Admin.",
                 font=("Arial", 12), text_color="#aaa").pack(anchor="w", padx=25, pady=(0, 15))

    ctk.CTkLabel(cadre_mdp, text="Ancien mot de passe",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=25)
    ent_ancien = ctk.CTkEntry(cadre_mdp, width=400, height=38, show="●", font=("Arial", 13))
    ent_ancien.pack(anchor="w", padx=25, pady=(5, 12))

    ctk.CTkLabel(cadre_mdp, text="Nouveau mot de passe",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=25)
    ent_nouveau = ctk.CTkEntry(cadre_mdp, width=400, height=38, show="●", font=("Arial", 13))
    ent_nouveau.pack(anchor="w", padx=25, pady=(5, 12))

    ctk.CTkLabel(cadre_mdp, text="Confirmer le nouveau mot de passe",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=25)
    ent_confirm = ctk.CTkEntry(cadre_mdp, width=400, height=38, show="●", font=("Arial", 13))
    ent_confirm.pack(anchor="w", padx=25, pady=(5, 15))

    def changer_mdp():
        ancien = ent_ancien.get()
        nouveau = ent_nouveau.get()
        confirm = ent_confirm.get()
        vrai_mdp = db.get_parametre("admin_password", "admin123")

        if ancien != vrai_mdp:
            messagebox.showerror("Erreur", "Ancien mot de passe incorrect ❌")
            return
        if len(nouveau) < 4:
            messagebox.showerror("Erreur", "Le nouveau mot de passe doit faire au moins 4 caractères ❌")
            return
        if nouveau != confirm:
            messagebox.showerror("Erreur", "Les deux mots de passe ne correspondent pas ❌")
            return

        db.set_parametre("admin_password", nouveau)
        messagebox.showinfo("Succès", "Mot de passe modifié ✅")
        ent_ancien.delete(0, "end")
        ent_nouveau.delete(0, "end")
        ent_confirm.delete(0, "end")

    ctk.CTkButton(cadre_mdp, text="💾 Changer le mot de passe",
                  fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                  font=("Arial", 13, "bold"), height=42, width=250,
                  command=changer_mdp).pack(anchor="w", padx=25, pady=(5, 25))

    # ===== BLOC 2 : Nom du salon =====
    cadre_nom = ctk.CTkFrame(scroll, fg_color=NOIR_CLAIR,
                              corner_radius=12, border_width=2, border_color=OR)
    cadre_nom.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(cadre_nom, text="🏷️ Nom du salon",
                 font=("Arial", 18, "bold"), text_color=OR).pack(anchor="w", padx=25, pady=(20, 5))
    ctk.CTkLabel(cadre_nom, text="Nom affiché dans l'application.",
                 font=("Arial", 12), text_color="#aaa").pack(anchor="w", padx=25, pady=(0, 15))

    ctk.CTkLabel(cadre_nom, text="Nom (Français)",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=25)
    ent_nom_fr = ctk.CTkEntry(cadre_nom, width=400, height=38, font=("Arial", 13))
    ent_nom_fr.pack(anchor="w", padx=25, pady=(5, 12))
    ent_nom_fr.insert(0, db.get_parametre("nom_salon", "Sba3iya Magic Salon"))

    ctk.CTkLabel(cadre_nom, text="الاسم (بالعربية)",
                 font=("Arial", 13), text_color=BLANC).pack(anchor="w", padx=25)
    ent_nom_ar = ctk.CTkEntry(cadre_nom, width=400, height=38, font=("Arial", 13))
    ent_nom_ar.pack(anchor="w", padx=25, pady=(5, 15))
    ent_nom_ar.insert(0, db.get_parametre("nom_salon_ar", "السباعية ماجيك صالون"))

    def sauver_nom():
        n_fr = ent_nom_fr.get().strip()
        n_ar = ent_nom_ar.get().strip()
        if not n_fr:
            messagebox.showerror("Erreur", "Le nom en français est obligatoire ❌")
            return
        db.set_parametre("nom_salon", n_fr)
        db.set_parametre("nom_salon_ar", n_ar)
        messagebox.showinfo("Succès", "Nom du salon enregistré ✅")

    ctk.CTkButton(cadre_nom, text="💾 Enregistrer le nom",
                  fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
                  font=("Arial", 13, "bold"), height=42, width=250,
                  command=sauver_nom).pack(anchor="w", padx=25, pady=(5, 25))

    # ===== BLOC 3 : Infos =====
    cadre_info = ctk.CTkFrame(scroll, fg_color=NOIR_CLAIR,
                               corner_radius=12, border_width=2, border_color=GRIS)
    cadre_info.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(cadre_info, text="ℹ️ Informations",
                 font=("Arial", 18, "bold"), text_color=OR).pack(anchor="w", padx=25, pady=(20, 15))

    infos = [
        ("📦 Version", "Sba3iya Magic Salon v1.0"),
        ("💾 Base de données", "sba3iya.db (SQLite)"),
        ("✂️ Nombre de services", str(len(db.get_services()))),
        ("💇 Nombre de serveuses", str(len(db.get_serveuses()))),
        ("👥 Nombre de clients", str(len(db.get_clients()))),
        ("💰 Paiements aujourd'hui", str(len(db.get_paiements_du_jour()))),
    ]

    for label, valeur in infos:
        ligne = ctk.CTkFrame(cadre_info, fg_color="transparent")
        ligne.pack(fill="x", padx=25, pady=4)
        ctk.CTkLabel(ligne, text=label, font=("Arial", 13),
                     text_color="#aaa", width=250, anchor="w").pack(side="left")
        ctk.CTkLabel(ligne, text=valeur, font=("Arial", 13, "bold"),
                     text_color=BLANC, anchor="w").pack(side="left")

    ctk.CTkFrame(cadre_info, height=15, fg_color="transparent").pack()

    # ===== BLOC 4 : Danger =====
    cadre_danger = ctk.CTkFrame(scroll, fg_color=NOIR_CLAIR,
                                 corner_radius=12, border_width=2, border_color=ROUGE)
    cadre_danger.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(cadre_danger, text="⚠️ Zone dangereuse",
                 font=("Arial", 18, "bold"), text_color=ROUGE).pack(anchor="w", padx=25, pady=(20, 5))
    ctk.CTkLabel(cadre_danger, text="Ces actions sont irréversibles.",
                 font=("Arial", 12), text_color="#aaa").pack(anchor="w", padx=25, pady=(0, 15))

    def reset_caisse_jour():
        if messagebox.askyesno("⚠️ Confirmation",
            "Supprimer tous les paiements d'aujourd'hui ?\n"
            "Cette action est IRRÉVERSIBLE."):
            conn = db.get_connexion()
            cur = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            cur.execute("DELETE FROM paiements WHERE date = ?", (today,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Paiements du jour supprimés ✅")
            app.afficher_page("parametres")

    ctk.CTkButton(cadre_danger, text="🗑️ Réinitialiser la caisse du jour",
                  fg_color=ROUGE, hover_color="#e74c3c", text_color=BLANC,
                  font=("Arial", 13, "bold"), height=42, width=320,
                  command=reset_caisse_jour).pack(anchor="w", padx=25, pady=(5, 25))