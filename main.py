from tkinter import *
from tkinter import ttk
#good one
def scroll_list(event):
    listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")

liste = ["Élément 1", "Élément 2", "Élément 3"]
def afficher_liste():
    global listbox
      # Liste des éléments à afficher
    global liste
    # Création d'un Listbox pour afficher la liste des éléments
    listbox = Listbox(right_frame)
    for item in liste:
        listbox.insert(END, item)
    listbox.grid(column=0, row=0, sticky=(N, W, E, S))
    listbox.bind('<<ListboxSelect>>', afficher_sous_liste)
    return listbox

def afficher_sous_liste(event):
    bouton_cocher_tout = Button(option_frame, text="Tout cocher  ", command=cocher_tout)
    bouton_cocher_tout.grid(column=2, row=1, sticky="e")
    bouton_decocher_tout = Button(option_frame, text="Tout décocher", command=decocher_tout)
    bouton_decocher_tout.grid(column=2, row=2, sticky="e")
    global sub_listbox, check_buttons, check_var
    clear_sub_list()
    if not listbox.curselection():  # Vérifier s'il y a une sélection
        return
    selected_item = listbox.get(listbox.curselection()[0])
    if selected_item == "Élément 1":
        sous_liste = ["Sous-élément 1.1", "Sous-élément 1.2", "Sous-élément 1.3"]
    elif selected_item == "Élément 2":
        sous_liste = ["Sous-élément 2.1", "Sous-élément 2.2", "Sous-élément 2.3"]
    elif selected_item == "Élément 3":
        sous_liste = ["Sous-élément 3.1", "Sous-élément 3.2", "Sous-élément 3.3"]
    else:
        return
    sub_listbox = ttk.Frame(right_frame)
    check_var = []
    check_buttons = []
    for i, item in enumerate(sous_liste):
        var = BooleanVar()
        check_var.append(var)
        check_button = Checkbutton(sub_listbox, text=item, variable=var)
        check_button.grid(column=0, row=i, sticky="w")
        check_buttons.append(check_button)
    sub_listbox.grid(column=0, row=1, sticky=(N, W, E, S))

def importClefs():
    print("key")
    widgets = option_frame.grid_slaves(column=2)

    # Parcourir les éléments et les supprimer
    for widget in widgets:
        # Vérifier si l'élément se trouve aux rows 1 ou 2
        if widget.grid_info()["row"] in [1, 2]:
            widget.grid_remove()

def importAll():
    print("all")
    widgets = option_frame.grid_slaves(column=2)

    # Parcourir les éléments et les supprimer
    for widget in widgets:
        # Vérifier si l'élément se trouve aux rows 1 ou 2
        if widget.grid_info()["row"] in [1, 2]:
            widget.grid_remove()

def clear_list():
    for widget in right_frame.winfo_children():
        widget.destroy()

def clear_sub_list():
    for widget in right_frame.grid_slaves(row=1):
        widget.destroy()

def switch():
    clear_list()
    clear_sub_list()
    value = var.get()
    if value == "datas":
        importAll()
    elif value == "clefs":
        importClefs()
    elif value == "table":
        afficher_liste()
    else:
        print("Veuillez sélectionner une option.")

def cocher_tout():
    for var in check_var:
        var.set(True)
def decocher_tout():
    for var in check_var:
        var.set(False)
root = Tk()
root.title("Cemineu Import des DATAS")

# Grille de gauche
left_frame = ttk.Frame(root, padding="3 3 12 12")
left_frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

option_frame = ttk.Frame(left_frame)
option_frame.grid(column=0, row=0, sticky=(W, E))
ttk.Label(option_frame, text="Option").grid(column=0, row=0, sticky=(W, E))

# Bouton de la partie option
var = StringVar()

bouton1 = Radiobutton(option_frame, text="Importer toutes les datas", variable=var, value="datas", anchor="w")
bouton1.grid(column=1, row=1, sticky="w")
bouton2 = Radiobutton(option_frame, text="Importer toutes les clefs", variable=var, value="clefs", anchor="w")
bouton2.grid(column=1, row=2, sticky="w")
bouton3 = Radiobutton(option_frame, text="Importer seulement une table", variable=var, value="table", anchor="w")
bouton3.grid(column=1, row=3, sticky="w")

var.set(None)

gros_bouton = Button(option_frame, text="Valider", command=switch)
gros_bouton.grid(column=0, row=4, rowspan=3, columnspan=2, sticky=(N, S, W, E))

# Bouton "Tout cocher"

# fin bouton option

# Grille de droite
right_frame = ttk.Frame(root, padding="3 3 12 12")
right_frame.grid(column=1, row=0, sticky=(N, W, E, S))
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
