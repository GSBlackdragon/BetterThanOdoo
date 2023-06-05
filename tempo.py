import tkinter as tk

# Dictionnaire de résultats
resultats = {
    "pomme": 10,
    "banane": 5,
    "orange": 8,
    "raisin": 15,
    "fraise": 12
}


# Fonction pour mettre à jour les résultats
def mettre_a_jour_resultats(*args):
    # Obtient le texte de l'entrée utilisateur
    recherche = champ_input.get()

    # Efface la liste des résultats précédents
    liste_resultats.delete(0, tk.END)

    # Parcourt le dictionnaire de résultats
    for resultat in resultats:
        # Vérifie si la recherche est vide ou si elle correspond au nom du résultat
        if not recherche or recherche.lower() in resultat.lower():
            # Ajoute le résultat à la liste
            liste_resultats.insert(tk.END, f"{resultat}: {resultats[resultat]}")


# Crée la fenêtre principale
fenetre = tk.Tk()

# Crée la variable pour lier à l'entrée utilisateur
champ_input_texte = tk.StringVar()

# Crée le champ d'entrée
champ_input = tk.Entry(fenetre, textvariable=champ_input_texte)
champ_input.pack()

# Crée la liste des résultats
liste_resultats = tk.Listbox(fenetre)
liste_resultats.pack()

# Lie l'événement de modification à la fonction mettre_a_jour_resultats
champ_input_texte.trace("w", mettre_a_jour_resultats)

# Lance la boucle principale
fenetre.mainloop()
