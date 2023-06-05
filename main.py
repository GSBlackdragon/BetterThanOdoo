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
    frame = ttk.Frame(right_frame, padding="10")
    frame.grid(column=0, row=1, sticky=(N, W, E, S))

    # Création de la barre de défilement
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Création de la liste
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=MULTIPLE)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)

    # Configuration de la barre de défilement pour fonctionner avec la liste
    scrollbar.configure(command=listbox.yview)

    # Ajout de 15 éléments à la liste avec des cases à cocher
    for i in range(15):
        listbox.insert(END, f"Élément {i + 1}")
        listbox.itemconfig(i, selectbackground='', selectforeground='')

    def update_selection():
        selected_indices = listbox.curselection()
        for i in range(listbox.size()):
            if i in selected_indices:
                listbox.itemconfig(i, selectbackground='blue', selectforeground='white')
            else:
                listbox.itemconfig(i, selectbackground='', selectforeground='')
        # Configuration de la fonction de mise à jour de la sélection lorsqu'un élément est cliqué
        listbox.bind("<<ListboxSelect>>", lambda event: update_selection())

        # Fonction pour récupérer les éléments sélectionnés
    def get_selected_items():
            selected_items = [listbox.get(i) for i in listbox.curselection()]
            return selected_items

        # Exemple de fonction utilisant les éléments sélectionnés
    def process_selected_items():
            items = get_selected_items()
            # Faites quelque chose avec les éléments sélectionnés
            print("Éléments sélectionnés :", items)

    def toggle_select_all_items():
        if len(listbox.curselection()) == listbox.size():
            listbox.selection_clear(0, END)
        else:
            listbox.select_set(0, END)
        update_selection()
    buttonFrame = ttk.Frame(right_frame,padding=5)
    buttonFrame.grid(column=0,row=2)
    button = ttk.Button(buttonFrame, text="IMPORTER", command=process_selected_items)
    buttonToggleSelection = ttk.Button(buttonFrame, text="🗘", command=toggle_select_all_items)
    buttonToggleSelection.grid(column=0, row=0)
    button.grid(column=1, row=0)

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