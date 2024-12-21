# Sopravvivenza: ogni cella con due o tre vicini vivi sopravvive per la prossima generazione.
# Morte: ogni cella con quattro o più vicini vivi muore per sovrappopolazione. Allo stesso modo, ogni cella con un vicino vivo o meno muore per isolamento.
# Nascita: ogni cella morta con esattamente tre vicini vivi diventa una cella viva.

import tkinter as tk
import tkinter.messagebox

def regole(evento):
    tk.messagebox.showinfo("Gioco della vita", "Questo gioco si basa su 3 regole:\n\nSopravvivenza: ogni cella con due o tre vicini vivi sopravvive.\n\nMorte: ogni cella con quattro o più vicini vivi muore per sovrappopolazione. Allo stesso modo, ogni cella con un vicino vivo o meno muore per isolamento\n\nNascita: ogni cella morta con esattamente tre vicini vivi diventa una cella viva.")

def crea(lato):
    lista = []
    for i in range(lato):
        temp = []
        for j in range(lato):
            casella = tk.Button(campo, width = "2", height = "1", bg = "white")
            casella.bind("<Button-1>", click)
            casella.grid(row = i, column = j)
            temp.append(casella)
    
        lista.append(temp)
    
    return lista

def avanti(evento):
    esecuzione(True)

def unire_griglia(evento):
    global griglia_unita
    
    if not in_esecuzione:
        if not griglia_unita:
            griglia.config(text = "ON")
            griglia_unita = True
        else:
            griglia.config(text = "OFF")
            griglia_unita = False

def click(evento):
    # Se il gioco non è in esecuzione quando clicco su una cella morta la rendo viva e viceversa
    if not in_esecuzione:
        bottone = evento.widget
        colore = bottone.cget("bg")

        if colore == "black":
            bottone.config(bg = "white")
        else:
            bottone.config(bg = "black")

def pulire(evento):
    # Se il gioco non è in esecuzione tolgo tutte le celle vive dalla tabella
    if not in_esecuzione:
        for riga in tabella:
            for cella in riga:
                cella.config(bg = "white")
        
        contatore.config(text = "0")

def simulazione(evento):
    global in_esecuzione

    if in_esecuzione:
        gioca.config(text = "AVVIA")
        in_esecuzione = False
    else:
        gioca.config(text = "FERMA")
        in_esecuzione = True
        esecuzione()

def conta(nriga, ncolonna):                 # Funzione che conta le celle vive intorno ad una cella di coordinate nriga, ncolonna
    i = 0
    for riga in range(-1, 2):
        if not griglia_unita:
            if nriga == 0 and riga == -1:
                continue
            elif nriga == l-1 and riga == 1:
                break

        for colonna in range(-1, 2):
            if riga == 0 and colonna == 0:
                continue

            if not griglia_unita:
                if ncolonna == 0 and colonna == -1:
                    continue
                elif ncolonna == l-1 and colonna == 1:
                    break
                cella = tabella[nriga + riga][ncolonna + colonna]
            else:
                riga2 = (nriga + riga)%l
                colonna2 = (ncolonna + colonna)%l
                cella  = tabella[riga2][colonna2]

            colore = cella.cget("bg")
            if colore == "black":
                i += 1
    
    return i

def esecuzione(singolo_passo = False):
    global in_esecuzione

    # Se il gioco è in esecuzione e l'utente preme singolo passo interrompo l'esecuzione continua
    if in_esecuzione and singolo_passo:
        simulazione(1)

    if in_esecuzione or singolo_passo:  
        # Conto le cellule vive      
        vive = 0
        for riga in tabella:
            for cella in riga:
                colore = cella.cget("bg")
                if colore == "black":
                    vive += 1

        if vive > 0:
            daEliminare = []
            daGenerare = []

            for riga in tabella:
                for cella in riga:
                    posizioni = cella.grid_info()
                    riga = posizioni["row"]
                    colonna = posizioni["column"]

                    colore = cella.cget("bg")
                    i = conta(riga, colonna)            # Conto quante celle vive ci sono intorno
                    if colore == "black":               # Se trovo una cella viva guardo se è destinata a morire
                        if i >= 4 or i <= 1:
                            daEliminare.append(cella)
                    else:                               # Se trovo una cella morta guardo se può nascere
                        if i == 3:
                            daGenerare.append(cella)
                
            for cella in daEliminare:
                cella.config(bg = "white")
            for cella in daGenerare:
                cella.config(bg = "black")
        
        numero = int(contatore.cget("text"))
        contatore.config(text = str(numero + 1))


        # Se l'utente non ha scelto singolo passo e vuole continuare ad eseguire il gioco
        # guardo la velocità in millisecondi che ha messo
        # Se la velocità non è specificata o è un numero negativo metto la velocità standard di 1 secondo
        if not singolo_passo:
            timer = tempo.get()

            try:
                int(timer)
                if int(timer) <= 0:
                    0/0
            except:
                timer = 1000

            window.after(timer, esecuzione)

window = tk.Tk()
window.geometry("500x600")
window.title("Game Of Life")

in_esecuzione = False
griglia_unita = False

frameTitolo = tk.Frame(window, bg = "blue2")
frameTitolo.pack(fill = "x")
campo = tk.Frame(window)
campo.pack(pady = 10)
opzioni1 = tk.Frame(window, bg = "blue2")
opzioni1.pack(fill = "x")
opzioni2 = tk.Frame(window, bg = "blue2")
opzioni2.pack(fill = "x")

titolo = tk.Label(frameTitolo, text = "Game Of Life", fg = "steelblue1", bg = "blue2", font = "Helvetica 25 bold")
titolo.pack(side = "left")
contatore = tk.Label(frameTitolo, text = "0", fg = "steelblue1", bg = "blue2", font = "Helvetica 10 bold", padx = 20)
contatore.pack(side = "right")
contatoreTitolo = tk.Label(frameTitolo, text = "Generazione: ", fg = "steelblue1", bg = "blue2", font = "Helvetica 10 bold")
contatoreTitolo.pack(side = "right")

l = 15
tabella = crea(l)

successivo = tk.Button(opzioni1, text = "AVANTI")
successivo.bind("<Button-1>", avanti)
successivo.pack(side = "left", padx = 45, pady = 10)

gioca = tk.Button(opzioni1, text = "AVVIA")
gioca.bind("<Button-1>", simulazione)
gioca.pack(side = "left", padx = 30, pady = 10)

pulisci = tk.Button(opzioni1, text = "PULISCI")
pulisci.bind("<Button-1>", pulire)
pulisci.pack(side = "right", padx = 30, pady = 10)

info = tk.Button(opzioni1, text = "INFO")
info.bind("<Button-1>", regole)
info.pack(side = "right", padx = 45, pady = 10)

grigliaTesto = tk.Label(opzioni2, text = "Unisci griglia: ")
grigliaTesto.grid(row = 1, column = 0, sticky="we")
griglia = tk.Button(opzioni2, text = "OFF")
griglia.bind("<Button-1>", unire_griglia)
griglia.grid(row = 1, column = 1, sticky = "w", padx = 5)

tempoTesto = tk.Label(opzioni2, text = "Durata generazione (millisecondi): ")
tempoTesto.grid(row = 2, column = 0)
tempo = tk.Entry(opzioni2)
tempo.grid(row = 2, column = 1, padx = 5, pady = 10)

window.mainloop()