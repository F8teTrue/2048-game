import tkinter as tk
import random

# Lager vinduet for spillet
window = tk.Tk()
window.title('2048')

# Lager en ramme som inneholder grid-et til spillbrettet
gameFrame = tk.Frame(window)
gameFrame.pack()

# Lager et 4x4 rutenett for spillet
gameBoard = [['' for _ in range(4)] for _ in range(4)]
tilePositions = []

def placeInitialTiles():
    # Plasserer de 2 første rutene med verdi 2 tilfeldig på brettet.
    for _ in range(2):
        while True:
            x, y = random.randint(0, 3), random.randint(0, 3)
            if gameBoard[x][y] == '':
                gameBoard[x][y] = 2
                tilePositions.append((x, y))
                break

def updateBoard():
    # Oppdatere GUI basert på statusen til spillbrettet
    for i in range(4):
        for j in range(4):
            text = str(gameBoard[i][j]) if gameBoard[i][j] != '' else ' '
            label = tk.Label(gameFrame, text=text, width=5, height=2, borderwidth=1.5, relief="ridge")
            label.grid(row = i, column = j, padx = 3, pady = 3)

# Kaller funksjonene left og updateBoard når høyre pil blir trykket
def onKeyPress(event):
    if event.keysym == 'Left':
        left()
        updateBoard()

window.bind('<Left>', onKeyPress)

def left():
    for i in range(4):
        slideRow(gameBoard[i])
        mergeRow(gameBoard[i])
        slideRow(gameBoard[i])
    addNewTile()

# Kaller funksjonene right og updateBoard når høyre pil blir trykket
def onKeyPress(event):
    if event.keysym == 'Right':
        right()
        updateBoard()

window.bind('<Right>', onKeyPress)

def right():
    for i in range(4):
        row = gameBoard[i][::-1] 
        slideRow(row)
        mergeRow(row)
        slideRow(row)
        gameBoard[i] = row[::-1] 
    addNewTile()

# Funksjon for å bevege ruter i en rad
def slideRow(row):
    for i in range(3):
        if row[i] == '' and any(row[i+1:]):
            j = i
            while j < 3 and row[j] == '':
                j += 1
            if j <= 3:
                row[i], row[j] = row[j], row[i]

# Funksjon for å merge ruter i en rad
def mergeRow(row):
    for i in range(2, -1, -1): # Itererer fra høyre til venstre i raden
        if row[i] == row[i + 1] and row[i] != '': # Sjekker for ruter med lik verdi
            row[i] *= 2 # Merger rutene ved å dobble verdien til den første ruten
            row[i + 1] = '' # Reseter verdien i den andre ruten
        
def addNewTile():
    # Legger til en ny rute med verdi 2 et tilfeldig sted på spillbrettet
    emptyCells = [(i, j) for i in range(4) for j in range(4) if gameBoard[i][j] == '']
    if emptyCells:
        x, y = random.choice(emptyCells)
        gameBoard[x][y] = 2

placeInitialTiles()
updateBoard()

window.mainloop()