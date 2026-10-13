import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageEnhance

import database as db
from theme import *

import page_accueil
import page_services
import page_serveuses
import page_caisse
import page_parametres
import page_clients
import page_rapport
import page_rdv

# ============================================
#   SBA3IYA MAGIC SALON - Application
# ============================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SalonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        db.initialiser_bdd()
        db.inserer_donnees_defaut()
        db.sauvegarder_bdd()      # ← sauvegarde auto au démarrage

        self.mode_admin = False

        self.title("Sba3iya Magic Salon 🐯")
        self.geometry("1200x720")
        self.configure(fg_color=NOIR)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.creer_sidebar()
        self.creer_zone_contenu()
        self.afficher_page("accueil")

    # ==========================================
    #   SIDEBAR
    # ==========================================
    def creer_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=260, corner_radius=0,
            fg_color=NOIR_CLAIR, border_width=2, border_color=OR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # Image tigre en fond
        try:
            image_pil = Image.open("tigre.jpg").convert("RGB")
            image_pil = image_pil.resize((260, 720))
            enhancer = ImageEnhance.Brightness(image_pil)
            image_pil = enhancer.enhance(0.5)
            image_pil = image_pil.convert("RGBA")
            data = image_pil.getdata()
            nouvelles = [(r, g, b, 150) for r, g, b, a in data]
            image_pil.putdata(nouvelles)
            self.img_fond = ctk.CTkImage(
                light_image=image_pil, dark_image=image_pil, size=(260, 720)
            )
            label_fond = ctk.CTkLabel(self.sidebar, image=self.img_fond, text="")
            label_fond.place(x=0, y=0)
        except Exception as e:
            print(f"⚠️ tigre.jpg (sidebar) : {e}")

        cadre_titre = ctk.CTkFrame(
            self.sidebar, fg_color="#0a0a0a",
            corner_radius=10, border_width=1, border_color=OR
        )
        cadre_titre.pack(pady=(25, 5), padx=15, fill="x")

        ctk.CTkLabel(
            cadre_titre, text="🐯 SBA3IYA\nMAGIC SALON",
            font=("Georgia", 20, "bold"), text_color=OR
        ).pack(pady=12)

        ctk.CTkFrame(self.sidebar, height=2, fg_color=OR, width=180).pack(pady=(15, 20))

        boutons = [
            ("🏠  Accueil    |  الرئيسية", "accueil"),
            ("👥  Clients    |  العملاء", "clients"),
            ("💇  Serveuses  |  العاملات", "serveuses"),
            ("✂️  Services    |  الخدمات", "services"),
            ("📅  Rendez-vous  |  المواعيد", "rdv"),
            ("💰  Caisse    |  الصندوق", "caisse"),
            ("📊  Rapport    |  التقرير", "rapport"),
            ("⚙️  Paramètres  |  الإعدادات", "parametres"),
        ]

        for texte, page in boutons:
            ctk.CTkButton(
                self.sidebar, text=texte,
                font=("Arial", 13, "bold"),
                fg_color="#0a0a0a", hover_color=OR, text_color=BLANC,
                anchor="w", height=42, corner_radius=8,
                border_width=1, border_color="#333",
                command=lambda p=page: self.afficher_page(p)
            ).pack(fill="x", padx=15, pady=3)

        self.btn_admin = ctk.CTkButton(
            self.sidebar, text="🔒  Admin",
            font=("Georgia", 14, "bold"),
            fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
            height=45, corner_radius=10,
            border_width=2, border_color=OR_CLAIR,
            command=self.demander_admin
        )
        self.btn_admin.pack(side="bottom", fill="x", padx=15, pady=20)

    # ==========================================
    #   ZONE DE CONTENU
    # ==========================================
    def creer_zone_contenu(self):
        self.contenu = ctk.CTkFrame(self, corner_radius=0, fg_color=NOIR)
        self.contenu.grid(row=0, column=1, sticky="nsew")

    # ==========================================
    #   NAVIGATION
    # ==========================================
    def afficher_page(self, nom_page):
        for widget in self.contenu.winfo_children():
            widget.destroy()

        if nom_page == "accueil":
            page_accueil.afficher(self)
        elif nom_page == "clients":
            page_clients.afficher(self)
        elif nom_page == "serveuses":
            page_serveuses.afficher(self)
        elif nom_page == "services":
            page_services.afficher(self)
        elif nom_page == "caisse":
            page_caisse.afficher(self)
        elif nom_page == "rapport":
            page_rapport.afficher(self)
        elif nom_page == "parametres":
            page_parametres.afficher(self)
        elif nom_page == "rdv":
            page_rdv.afficher(self)

    # ==========================================
    #   PAGE VIDE
    # ==========================================
    def page_vide(self, titre_texte, message):
        ctk.CTkLabel(self.contenu, text=titre_texte,
                     font=("Arial", 28, "bold"), text_color=OR).pack(pady=(50, 20))
        ctk.CTkLabel(self.contenu, text=message,
                     font=("Arial", 18), text_color=BLANC).pack()

    # ==========================================
    #   ADMIN
    # ==========================================
    def demander_admin(self):
        if self.mode_admin:
            self.mode_admin = False
            self.btn_admin.configure(text="🔒  Admin", fg_color=OR, text_color=NOIR)
            messagebox.showinfo("Info", "Mode Admin désactivé 🔒")
            self.afficher_page("accueil")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Accès Admin 🔒")
        popup.geometry("400x220")
        popup.configure(fg_color=NOIR)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Mot de passe Admin",
                     font=("Georgia", 18, "bold"), text_color=OR).pack(pady=(30, 15))

        champ = ctk.CTkEntry(popup, placeholder_text="Entrez le mot de passe...",
                             show="●", width=280, height=40, font=("Arial", 14))
        champ.pack(pady=10)
        champ.focus()

        def verifier():
            mdp_ok = db.get_parametre("admin_password", "admin123")
            if champ.get() == mdp_ok:
                popup.destroy()
                self.mode_admin = True
                self.btn_admin.configure(text="🔓  Admin (actif)", fg_color=VERT)
                messagebox.showinfo("Succès", "Mode Admin activé ✅")
                self.afficher_page("accueil")
            else:
                messagebox.showerror("Erreur", "Mot de passe incorrect ❌")

        ctk.CTkButton(
            popup, text="Valider",
            fg_color=OR, hover_color=OR_CLAIR, text_color=NOIR,
            font=("Arial", 14, "bold"), height=40,
            command=verifier
        ).pack(pady=15)

        champ.bind("<Return>", lambda e: verifier())


# ============================================
#   LANCEMENT
# ============================================
if __name__ == "__main__":
    app = SalonApp()
    app.mainloop()