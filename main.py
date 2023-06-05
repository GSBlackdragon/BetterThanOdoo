from tkinter import *
from tkinter import ttk
import json
#good one

with open("tables.json", "r") as fichier:

    data = json.load(fichier)
result = {}

for item in data:
    table_name = item['table_name']
    columns = item['column']
    column_dict = {}
    for column in columns:
        column_name = column['column_name']
        column_type = column['type']
        column_relation = column['relation']
        column_dict[column_name] = {
            'type': column_type,
            'relation': column_relation
        }
    result[table_name] = column_dict

liste =[key for key in result.keys()]
selected_index = None
def afficher_liste():
    global listbox, liste, champ_input_texte



    # Création d'un Listbox pour afficher la liste des éléments
    listbox = Listbox(right_frame)
    for item in liste:
        listbox.insert(END, item)
    listbox.grid(column=0, row=0, sticky=(N, W, E, S))




    # Crée le champ d'entrée
    champ_input = Entry(option_frame, textvariable=champ_input_texte )
    champ_input.grid(column=0, row=125,columnspan=3, pady=5,sticky=(N, W, E, S))
    print(champ_input_texte.get())
    listbox.bind('<<ListboxSelect>>', afficher_sous_liste)

def afficher_sous_liste(event):
    global selected_index
    global result
    if selected_index == None:
        selected_index = listbox.curselection()[0]

    elif selected_index != None and len(listbox.curselection()) !=0:
        selected_index = listbox.curselection()[0]



    # Récupérer l'index de la ligne sélectionnée dans la liste principale

    frame = ttk.Frame(right_frame, padding="10")
    frame.grid(column=0, row=1, sticky=(N, W, E, S))

    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Création de la liste
    sousListe = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=MULTIPLE)
    sousListe.pack(side=LEFT, fill=BOTH, expand=True)

    # Configuration de la barre de défilement pour fonctionner avec la liste
    scrollbar.configure(command=sousListe.yview)

    # Ajout de 15 éléments à la liste avec des cases à cocher
    for index, column_name in  enumerate(result[listbox.get(selected_index)]):

        if result[listbox.get(selected_index)][column_name]["relation"] == "PRIMARY_KEY":
            sousListe.insert(END, "🔑 " +column_name )
        elif result[listbox.get(selected_index)][column_name]["relation"] is not None:
            sousListe.insert(END, "🔗 " + column_name)
        else:
            sousListe.insert(END, "     " + column_name)


        #🔑sousListe.insert(END, column_info['type'] + " " + column_name)

        #sousListe.itemconfig(index, selectbackground='', selectforeground='')
    sousListe.focus_set()



    def update_selection(event):
        selected_indices = sousListe.curselection()
        for i in range(sousListe.size()):
            if i in selected_indices:
                sousListe.itemconfig(i, selectbackground='blue', selectforeground='white')
            else:
                sousListe.itemconfig(i, selectbackground='', selectforeground='')

    def get_selected_items():
        selected_items = [sousListe.get(i) for i in sousListe.curselection()]
        return selected_items

    def process_selected_items():
        items = get_selected_items()
        # Faites quelque chose avec les éléments sélectionnés
        print("Éléments sélectionnés :", items)


    def toggle_select_all_items():
        if len(sousListe.curselection()) == sousListe.size():
            sousListe.selection_clear(0, END)
        else:
            sousListe.select_set(0, END)
        update_selection("")

    buttonFrame = ttk.Frame(right_frame, padding=5)
    buttonFrame.grid(column=0, row=2)
    button = ttk.Button(buttonFrame, text="IMPORTER", command=process_selected_items)
    buttonToggleSelection = ttk.Button(buttonFrame, text="🗘", command=toggle_select_all_items)
    buttonToggleSelection.grid(column=0, row=0)
    button.grid(column=1, row=0)

    sousListe.bind('<<ListboxSelect>>', update_selection)


def clear_list():
    for widget in right_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.grid_slaves(row=1):
        widget.destroy()




def importClefs():

    widgets = option_frame.grid_slaves(column=2)

    # Parcourir les éléments et les supprimer
    for widget in widgets:
        # Vérifier si l'élément se trouve aux rows 1 ou 2
        if widget.grid_info()["row"] in [1, 2]:
            widget.grid_remove()

def importAll():

    widgets = option_frame.grid_slaves(column=2)

    # Parcourir les éléments et les supprimer
    for widget in widgets:
        # Vérifier si l'élément se trouve aux rows 1 ou 2
        if widget.grid_info()["row"] in [1, 2]:
            widget.grid_remove()



def switch():
    clear_list()

    value = var.get()
    if value == "datas":
        importAll()
    elif value == "clefs":
        importClefs()
    elif value == "table":
        afficher_liste()
    else:
        print("Veuillez sélectionner une option.")


def research(*args):
    global liste
    global result
    if champ_input_texte.get() != "":
        liste = []
        tempo = result.keys()
        clear_list()
        for table in tempo:
            if table.lower().startswith(champ_input_texte.get().lower()):
                liste.append(table)
        for table in liste:
            if table.lower().startswith(champ_input_texte.get().lower()) is False:
                liste.remove(table)


    afficher_liste()






root = Tk()
root.title("Cemineu Import des DATAS")
root.geometry("500x500")
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
champ_input_texte = StringVar()
champ_input_texte.trace("w", research)
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