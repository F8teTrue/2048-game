import tkinter as tk
import random

bgColor = {
    ' ': '#BBADA0',
    '2': '#eee4da',
    '4': '#ede0c8',
    '8': '#edc850',
    '16': '#edc53f',
    '32': '#f67c5f',
    '64': '#f65e3b',
    '128': '#edcf72',
    '256': '#edcc61',
    '512': '#f2b179',
    '1024': '#f59563',
    '2048': '#edc22e',
}

color = {
    '2': '#776e65',
    '4': '#776e65',
    '8': '#f9f6f2',
    '16': '#f9f6f2',
    '32': '#f9f6f2',
    '64': '#f9f6f2',
    '128': '#f9f6f2',
    '256': '#f9f6f2',
    '512': '#776e65',
    '1024': '#f9f6f2',
    '2048': '#f9f6f2',
}

score = 0

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

# Lager rutene for spillet
labels = [[tk.Label(gameFrame, width=2, height=1, borderwidth=25, font=('Arial', 100, 'bold'))
           for _ in range(4)] for _ in range(4)]

def updateBoard():
    global score
    # Oppdatere GUI basert på statusen til spillbrettet
    for i in range(4):
        for j in range(4):
            value = gameBoard[i][j]
            text = str(gameBoard[i][j]) if gameBoard[i][j] != '' else ' '

            # Henter farge for bakgrunn og tekst basert på tallet i ruten
            bg = bgColor.get(str(value), '#776E65')
            fg = color.get(str(value), '#000000') 

            # Oppdaterer rutene med farge og tekst
            labels[i][j].config(text=text, bg=bg, fg=fg)
            labels[i][j].grid(row=i, column=j, padx=3, pady=3)
            
    print(f"Score: {score}") 

# Kaller funksjonene left og updateBoard når venstre pil blir trykket
def onKeyPress(event):
    if event.keysym == 'Left':
        left()
        updateBoard()

window.bind('<Left>', onKeyPress)

def left():
    for i in range(4):
        slide(gameBoard[i])
        merge(gameBoard[i])
        slide(gameBoard[i])
    addNewTile()
    if not checkForValidMoves():
        gameOver()

# Kaller funksjonene right og updateBoard når høyre pil blir trykket
def onKeyPress(event):
    if event.keysym == 'Right':
        right()
        updateBoard()

window.bind('<Right>', onKeyPress)

def right():
    for i in range(4):
        row = gameBoard[i][::-1] 
        slide(row)
        merge(row)
        slide(row)
        gameBoard[i] = row[::-1] 
    addNewTile()
    if not checkForValidMoves():
        gameOver()

# Kaller funksjonene up og updateBoard når pil opp blir trykket
def onKeyPress(event):
    if event.keysym == 'Up':
        up()
        updateBoard()

window.bind('<Up>', onKeyPress)

def up():
    for i in range(4):
        column = [gameBoard[j][i] for j in range(4)]
        slide(column)
        merge(column)
        slide(column)
        for j in range(4):
            gameBoard[j][i] = column[j]
    addNewTile()
    if not checkForValidMoves():
        gameOver()

# Kaller funksjonene down og updateBoard når pil ned blir trykket
def onKeyPress(event):
    if event.keysym == 'Down':
        down()
        updateBoard()

window.bind('<Down>', onKeyPress)

def down():
    for i in range(4):
        column = [gameBoard[j][i] for j in range(3, -1, -1)]
        slide(column)
        merge(column)
        slide(column)
        for j in range(3, -1, -1):
            gameBoard[3 - j][i] = column[j]
    addNewTile()
    if not checkForValidMoves():
        gameOver()

# Funksjon for å bevege ruter i en rad
def slide(line):
    for i in range(3):
        #Sjekker om et felt er tomt og om feltet etter det ikke er tomt
        if line[i] == '' and any(line[i+1:]):#Sjekker om et felt er tomt og om feltet etter det ikke er tomt
            j = i
            while j < 3 and line[j] == '':
                j += 1
            # Hvis j er mindre eller lik 3 (det tredje feltet),
            # byttes plassen til det tomme feltet line[i] med det første ikke-tomme feltet line[j])
            if j <= 3:
                line[i], line[j] = line[j], line[i]

# Funksjon for å merge ruter i en rad
def merge(line):
    global score
    for i in range(2, -1, -1): # Itererer fra høyre til venstre i raden
        if line[i] == line[i + 1] and line[i] != '': # Sjekker for ruter med lik verdi
            line[i] *= 2 # Merger rutene ved å dobble verdien til den første ruten
            score += line[i] # Øker score med verdien til den merga ruten
            line[i + 1] = '' # Reseter verdien i den andre ruten
        
def addNewTile():
    # Legger til en ny rute med verdi 2 et tilfeldig sted på spillbrettet
    emptyCells = [(i, j) for i in range(4) for j in range(4) if gameBoard[i][j] == '']
    if emptyCells:
        x, y = random.choice(emptyCells)
        gameBoard[x][y] = 2

def checkForValidMoves():
    #Sjekker om det er noen tomme ruter
    for i in range(4):
        for j in range(4):
            if gameBoard[i][j] == '':
                return True
    
    #Sjekker om det er noen ruter som kan merges horisontalt
    for i in range(4):
        for j in range(3):
            if gameBoard[i][j] == gameBoard[i][j + 1]:
                return True
    
    #Sjekker om det er noen ruter som kan merges vertikalt
    for i in range(3):
        for j in range(4):
            if gameBoard[i][j] == gameBoard[i + 1][j]:
                return True
    
    return False

def gameOver():
    global score
    updateBoard()
    print(f'Game over! Final score: {score}')

placeInitialTiles()
updateBoard()

window.mainloop()