import customtkinter as ctk
from PIL import Image, ImageEnhance
import database as db
from theme import *

# ============================================
#   PAGE ACCUEIL - Version premium
# ============================================

def afficher(app):
    contenu = app.contenu

    # ===== IMAGE TIGRE EN FOND =====
    try:
        image_pil = Image.open("tigre.jpg").convert("RGB")
        largeur, hauteur = 940, 720
        image_pil = image_pil.resize((largeur, hauteur))

        enhancer = ImageEnhance.Brightness(image_pil)
        image_pil = enhancer.enhance(0.55)

        enhancer2 = ImageEnhance.Contrast(image_pil)
        image_pil = enhancer2.enhance(1.1)

        image_pil = image_pil.convert("RGBA")
        data = image_pil.getdata()
        nouvelles = []
        for r, g, b, a in data:
            nouvelles.append((r, g, b, 130))
        image_pil.putdata(nouvelles)

        img_fond = ctk.CTkImage(
            light_image=image_pil,
            dark_image=image_pil,
            size=(largeur, hauteur)
        )

        label_fond = ctk.CTkLabel(contenu, image=img_fond, text="")
        label_fond.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"⚠️ Impossible de charger tigre.jpg : {e}")

    # ===== CONTENU PRINCIPAL (fond opaque) =====
    cadre_principal = ctk.CTkFrame(
        contenu,
        fg_color="#0a0a0a",       # ← opaque
        corner_radius=20,
        border_width=2,
        border_color=OR
    )
    cadre_principal.place(relx=0.5, rely=0.5, anchor="center",
                          relwidth=0.9, relheight=0.85)

    inner = ctk.CTkFrame(cadre_principal, fg_color="transparent")
    inner.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)

    # ===== TITRE =====
    ctk.CTkLabel(
        inner,
        text="◆ SBA3IYA MAGIC SALON ◆",
        font=("Georgia", 16, "bold"), text_color=OR
    ).pack(pady=(0, 5))

    ctk.CTkLabel(
        inner,
        text="Bienvenue chez Sba3iya Magic Salon",
        font=("Georgia", 30, "bold"), text_color=OR_CLAIR
    ).pack(pady=(0, 8))

    ctk.CTkLabel(
        inner,
        text="مرحبا بكم في السباعية ماجيك صالون",
        font=("Arial", 18), text_color=BLANC
    ).pack(pady=(0, 10))

    ctk.CTkFrame(inner, height=2, fg_color=OR, width=400).pack(pady=(5, 40))

    # ===== CARTES DE STATS =====
    zone = ctk.CTkFrame(inner, fg_color="transparent")
    zone.pack(pady=10)

    fond_caisse = db.get_caisse_demarrage()
    total_ventes = db.get_total_caisse_jour()
    nb_clients = len(db.get_clients())
    nb_serveuses = len(db.get_serveuses())

    stats = [
        ("👥", str(nb_clients), "Clients", OR),
        ("💇", str(nb_serveuses), "Serveuses", OR),
        ("💵", f"{fond_caisse:.0f} DH", "Fond de caisse", OR),
        ("💰", f"{total_ventes:.0f} DH", "Ventes du jour", VERT),
    ]

    for emoji, valeur, label, couleur in stats:
        carte = ctk.CTkFrame(
            zone, width=175, height=150, corner_radius=15,
            fg_color="#1a1a1a",        # ← opaque
            border_width=2, border_color=couleur
        )
        carte.pack(side="left", padx=10)
        carte.pack_propagate(False)

        ctk.CTkLabel(carte, text=emoji, font=("Arial", 32)).pack(pady=(22, 8))
        ctk.CTkLabel(carte, text=valeur,
                     font=("Georgia", 22, "bold"), text_color=couleur).pack()
        ctk.CTkLabel(carte, text=label,
                     font=("Arial", 12), text_color=BLANC).pack(pady=(3, 15))