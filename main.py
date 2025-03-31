import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import shutil
from functools import partial

# Liste des favoris
favoris = []
historique = []
position_historique = -1

# Fonction pour lister les fichiers et dossiers
def afficher_contenu(repertoire):
    global chemin_actuel, historique, position_historique
    
    if position_historique == -1 or (historique and historique[position_historique] != repertoire):
        historique = historique[:position_historique + 1] + [repertoire]
        position_historique += 1
    
    chemin_actuel.set(repertoire)

    for widget in cadre_fichiers.winfo_children():
        widget.destroy()

    try:
        elements = os.listdir(repertoire)
        for i, element in enumerate(elements):
            chemin_complet = os.path.join(repertoire, element)
            img = dossier_icon if os.path.isdir(chemin_complet) else fichier_icon
            
            btn = tk.Button(cadre_fichiers, image=img, text=element, compound="top", 
                            command=partial(ouvrir_dossier, chemin_complet) if os.path.isdir(chemin_complet) 
                            else partial(ouvrir_fichier, chemin_complet))
            btn.bind("<Button-3>", lambda event, p=chemin_complet: menu_contextuel(event, p))
            btn.grid(row=i // 5, column=i % 5, padx=10, pady=10)
    except PermissionError:
        messagebox.showerror("Erreur", "Accès refusé")

# Fonction pour gérer le menu contextuel (clic droit)
def menu_contextuel(event, chemin):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Ouvrir", command=lambda: ouvrir_fichier(chemin) if os.path.isfile(chemin) else ouvrir_dossier(chemin))
    menu.add_command(label="Renommer", command=lambda: renommer(chemin))
    menu.add_command(label="Supprimer", command=lambda: supprimer(chemin))
    menu.add_command(label="Ajouter aux Favoris", command=lambda: ajouter_favori(chemin))
    menu.tk_popup(event.x_root, event.y_root)

# Fonction pour créer un dossier
def creer_dossier():
    nom = simpledialog.askstring("Créer Dossier", "Nom du dossier :")
    if nom:
        chemin_nouveau_dossier = os.path.join(chemin_actuel.get(), nom)
        try:
            os.mkdir(chemin_nouveau_dossier)
            actualiser()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier : {e}")

# Fonction pour ouvrir un dossier
def ouvrir_dossier(chemin):
    if os.path.isdir(chemin):
        afficher_contenu(chemin)

# Fonction pour ouvrir un fichier
def ouvrir_fichier(chemin):
    os.startfile(chemin)

#Fonction pour ajouter aux favories
def ajouter_favori(chemin):
    if chemin not in favoris:
        favoris.append(chemin)
        messagebox.showinfo("Favoris", f"{os.path.basename(chemin)} ajouté aux favoris")
    else:
        messagebox.showinfo("Favoris", "Ce chemin est déjà dans vos favoris.")

# Fonction pour afficher les favoris
def afficher_favoris():
    for widget in cadre_fichiers.winfo_children():
        widget.destroy()
    if not favoris:
        label = tk.Label(cadre_fichiers, text="Aucun favori ajouté.", font=("Arial", 12))
        label.grid(row=0, column=0, padx=10, pady=10)
    else:
        for i, element in enumerate(favoris):
            btn = tk.Button(cadre_fichiers, text=os.path.basename(element), compound="top", 
                            command=partial(ouvrir_fichier, element) if os.path.isfile(element) 
                            else partial(ouvrir_dossier, element))
            btn.grid(row=i // 5, column=i % 5, padx=10, pady=10)


# Fonction pour naviguer en arrière
def dossier_precedent():
    global position_historique
    if position_historique > 0:
        position_historique -= 1
        afficher_contenu(historique[position_historique])

# Fonction pour naviguer en avant
def dossier_suivant():
    global position_historique
    if position_historique < len(historique) - 1:
        position_historique += 1
        afficher_contenu(historique[position_historique])

# Fonction pour actualiser la liste
def actualiser():
    afficher_contenu(chemin_actuel.get())

#Fonction pour renommer
def renommer(chemin):
    nouveau_nom = simpledialog.askstring("Renommer", "Nouveau nom :")
    if nouveau_nom:
        try:
            dossier_parent = os.path.dirname(chemin)
            nouveau_chemin = os.path.join(dossier_parent, nouveau_nom)
            os.rename(chemin, nouveau_chemin)
            actualiser()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de renommer : {e}")

# Fonction pour supprimer un fichier ou dossier
def supprimer(chemin):
    try:
        if os.path.isdir(chemin):
            shutil.rmtree(chemin)
        else:
            os.remove(chemin)
        actualiser()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Explorateur de Fichiers")
root.geometry("800x600")

# Cadre de la barre latérale
cadre_gauche = tk.Frame(root, width=200, bg="#f0f0f0")
cadre_gauche.grid(row=0, column=0, rowspan=2, sticky="ns")

# Boutons de navigation
btn_recents = tk.Button(cadre_gauche, text="Recents", bg="#d9d9d9", relief="flat")
btn_recents.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

btn_favorites = tk.Button(cadre_gauche, text="Favoris", bg="#d9d9d9", relief="flat", command=afficher_favoris)
btn_favorites.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn_computer = tk.Button(cadre_gauche, text="Computer", bg="#d9d9d9", relief="flat")
btn_computer.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

btn_tags = tk.Button(cadre_gauche, text="Tags", bg="#d9d9d9", relief="flat")
btn_tags.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

# Barre de navigation
chemin_actuel = tk.StringVar()
barre_chemin = tk.Entry(root, textvariable=chemin_actuel, state="readonly")
barre_chemin.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

# Boutons de navigation <- et ->
btn_retour = tk.Button(root, text="<-", command=dossier_precedent)
btn_retour.grid(row=0, column=3, padx=5, pady=5)

btn_avancer = tk.Button(root, text="->", command=dossier_suivant)
btn_avancer.grid(row=0, column=4, padx=5, pady=5)

# Cadre principal pour les fichiers
cadre_fichiers = tk.Frame(root)
cadre_fichiers.grid(row=1, column=1, columnspan=4, sticky="nsew", padx=5, pady=5)

# Boutons d'actions
btn_actualiser = tk.Button(root, text="Actualiser", command=actualiser)
btn_actualiser.grid(row=2, column=1, pady=5)

btn_creer_dossier = tk.Button(root, text="Créer Dossier", command=creer_dossier)
btn_creer_dossier.grid(row=2, column=2, pady=5)

# Chargement des icônes
dossier_img = Image.open("dossier_icon.jpeg").resize((50, 50))
dossier_icon = ImageTk.PhotoImage(dossier_img)
fichier_img = Image.open("fichier_icon.jpeg").resize((50, 50))
fichier_icon = ImageTk.PhotoImage(fichier_img)

# Affichage initial
afficher_contenu(os.getcwd())

root.mainloop()
