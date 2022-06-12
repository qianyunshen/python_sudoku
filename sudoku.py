#Qianyun Shen 
import PySimpleGUI as sg
import random
import csv

###################################
# Logique de résolution de Sudoku #
###################################

# Information pertinente: Différence entre "initial state" et "state":
# "initial state" => Les valeurs des éléments text input de la boucle
# principale (donc soit des '1','2',...,'9' ou des '') sous la forme 
# d'une liste 2D 9X9

# "state" => l'état de notre solution en contruction composé d'un
# tableau 2D de ints 9x9. Initialement, toutes les cases correspondant
# aux cases vides dans "initialState" (ayant une valeur de '') ont 
# une valeur de 0

# Prend initialState et retourne un tableau 2D 9x9 de ints
# où des zéros ont été placés aux cases "vides" ('')
def createInitialGrid(initialState):
    result = []
    for i in range(len(initialState)):
        rows = []
        for j in range(len(initialState[i])):
            if '' == initialState[i][j]:
                rows += [0]
            elif initialState[i][j].isdigit() and int(initialState[i][j]) >= 1 and int(initialState[i][j]) <= 9:
                rows += [int(initialState[i][j])]
            else:
                return []
        result += [rows]

    return result

# Prend un état de la solution, un nombre et retourne si ce nombre
# peut être placé à une certaine position. Au sudoku, on ne peut pas
# placer un même nombre à la même ligne, colonne, ou dans le même bloc
# Une position est un tuple (ligne, colonne)
def isPossible(state, number, position):
    # Valeur dans la même ligne
    x = position[0]
    y = position[1]
    for i in range(len(state[x])):
        if state[x][i] == number and i != y:
            return False

    # Valeur dans la même colonne
    for i in range(len(state)):
        if state[i][y] == number and i != x:
            return False

    # Valeur dans le même bloc
    if x % 3 == 0:
        if y % 3 == 0:
            if state[x+1][y] == number or state[x+2][y] == number \
            or state[x][y+1] == number or state[x+1][y+1] == number or state[x+2][y+1] == number\
            or state[x][y+2] == number or state[x+1][y+2] == number or state[x+2][y+2] == number:
                return False
        if y % 3 == 1:
            if state[x+1][y] == number or state[x+2][y] == number\
            or state[x][y+1] == number or state[x+1][y+1] == number or state[x+2][y+1] == number\
            or state[x][y-1] == number or state[x+1][y-1] == number or state[x+2][y-1] == number:
                return False
        if y % 3 == 2:
            if state[x+1][y] == number or state[x+2][y] == number\
            or state[x][y-2] == number or state[x+1][y-2] == number or state[x+2][y-2] == number\
            or state[x][y-1] == number or state[x+1][y-1] == number or state[x+2][y-1] == number:
                return False
    if x % 3 ==1:
        if y % 3 == 0:
             if state[x+1][y] == number or state[x-1][y] == number\
            or state[x][y+1] == number or state[x+1][y+1] == number or state[x-1][y+1] == number\
            or state[x][y+2] == number or state[x+1][y+2] == number or state[x-1][y+2] == number:
                return False
        if y % 3 == 1:
            if state[x+1][y] == number or state[x-1][y] == number\
            or state[x][y+1] == number or state[x+1][y+1] == number or state[x-1][y+1] == number\
            or state[x][y-1] == number or state[x+1][y-1] == number or state[x-1][y-1] == number:
                return False
        if y % 3 == 2:
            if state[x+1][y] == number or state[x-1][y] == number\
            or state[x][y-2] == number or state[x+1][y-2] == number or state[x-1][y-2] == number\
            or state[x][y-1] == number or state[x+1][y-1] == number or state[x-1][y-1] == number:
                return False
    if x % 3 ==2:
        if y % 3 == 0:
            if state[x-2][y] == number or state[x-1][y] == number\
            or state[x][y+1] == number or state[x-2][y+1] == number or state[x-1][y+1] == number\
            or state[x][y+2] == number or state[x-2][y+2] == number or state[x-1][y+2] == number:
                return False
        if y % 3 == 1:
            if state[x-2][y] == number or state[x-1][y] == number\
            or state[x][y+1] == number or state[x-2][y+1] == number or state[x-1][y+1] == number\
            or state[x][y-1] == number or state[x-2][y-1] == number or state[x-1][y-1] == number:
                return False
        if y % 3 == 2:
            if state[x-2][y] == number or state[x-1][y] == number\
            or state[x][y-2] == number or state[x-2][y-2] == number or state[x-1][y-2] == number\
            or state[x][y-1] == number or state[x-2][y-1] == number or state[x-1][y-1] == number:
                return False
   
    return True
    

# Retourne la position (ligne, colonne) de la première entrée dans
# intialState qui n'est pas un indice (donc non-vide)
# Retourne None sinon
def findStart(initialState):
    for i in range(len(initialState)):
        for j in range(len(initialState[i])):
            if ''==initialState[i][j]:
                return(i, j)

    return (-1, -1)

# Étant donné la position des indices initiaux, retourne la prochaine
# position qui n'est pas un indice. On traverse le tableau de haut
# en bas, gauche à droite.
def nextCell(initialState, position):
    x = position[0]
    y = position[1]
    for j in range(y+1,9):
        if initialState[x][j] == '':
            return (x, j)
    for i in range(x+1,9):
        for j in range(9):
            if initialState[i][j] == '':
                return(i, j)
    return (-1, -1)

# Étant donné la position des indices initiaux, retourne la position
# antérieure qui n'est pas un indice. On traverse le tableau de haut
# en bas, gauche à droite.
def previousCell(initialState, position):
    x = position[0]
    y = position[1]
    for j in range(y-1,-1,-1):
        if initialState[x][j] == '':
            return(x, j)
    for i in range(x-1,-1,-1):
        for j in range(8,-1,-1):
            if initialState[i][j] =='':
                return(i, j)
    return (-1, -1)


# Retourne si un état initial est valide
# Ne contient pas donc des entrées contradictoires
# i.e. deux chiffres sur la même ligne, colonne, dans le même bloc
# Ainsi qu'un état étant composé de seulement 0-9
def isValid(state):
    for i in range(len(state)):
        for j in range(len(state[i])):

            number = state[i][j]
            position = (i,j)
            if state[i][j] not in range(10):
                return False
            if state[i][j] != 0:
                a = isPossible(state,number,position)
                if a == False:
                    return a
    return True
    


# Retourne si un état de recherche est complété
# (Pssst! Ne contiendra pas de zéros!)
def isCompleted(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] not in range(1,10):
                return False
    
    return True

# Création de la grille initiale à partir du "initialState"
# Implémentation de l'algorithme de "backtracking" jusqu'à
# l'atteinte d'une solution ou de réaliser qu'il n'en existe pas
# Retourne si une solution existe et affiche la solution
def solve(initialState):
    initialGrid = createInitialGrid(initialState)
    if not initialGrid:
        return False
    if not isValid(initialGrid):
        return False
    pos = findStart(initialState)
    i, j = pos
    left = 1
    while i != -1 and j != -1:
        left = initialGrid[i][j] + 1
        for e in range(left, 10):
            if isPossible(initialGrid, e, (i, j)):
                initialGrid[i][j] = e
                displaySudoku(initialGrid)
                if isValid(initialGrid):
                    break
                else:
                    initialGrid[i][j] = 0
            else:
                initialGrid[i][j] = 0
        if initialGrid[i][j] == 0 or left >= 10:
            initialGrid[i][j] = 0
            i, j = previousCell(initialState, (i, j))
        else:
            i, j = nextCell(initialState, (i, j))
    
    if isCompleted(initialGrid):
        displaySudoku(initialGrid)


########################################################
# Fonctions faisant le pont entre la logique et le GUI #
########################################################

# Affiche '' à chaque InputText
def clearTable():
    for i in range(9):
        for j in range(9):
            cell = (i, j)
            window[cell].update('')
    

# Reçois un tableau de 2 dimensions et affiche son contenu dans la grille d'InputText
def displaySudoku(tab):
    for r in range(len(tab)):
        for c in range(len(tab)):
            cell = (r, c)
            if tab[r][c] == 0:
                window[cell].update('')
            else:
                window[cell].update(str(tab[r][c]))


    
'''
# Retourne un tableau 2D à partir du dictionnaire values de la boucle principale
# Les clefs définies pour vos éléments InputText seront utilisées ici
'''
def getDisplayedSudoku(values):
    initialState = []
    for i in range(9):
        rows = []
        for j in range(9):
            cell = (i, j)
            rows += [values[cell]]
        initialState += [rows]
    return initialState

# Affiche les indices d'un sudoku aléatoire du fichier sudoku.csv
def loadRandomSudoku(data):
    indice = random.randint(0,99)
    choice = data[indice]
    idx = 0
    for r in range(9):
        for c in range(9):
            cell = (r, c)
            if choice[idx] != 0:
                window[cell].update(str(choice[idx]))
            idx += 1

data = []

with open('sudoku.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

sg.theme('DarkAmber')

layout = []

# Ajout de 81 InputText au layout. Ne pas utiliser une boucle ici
# sera sévèrement pénalisé. Attention d'également bien choisir vos "key"s

for fr in range(3):
    fcol = []
    for fc in range(3):
        row = []
        for r in range(3):
            col = []
            for c in range(3):
                #print(fr*3+r,fc*3+c)
                col += [sg.Input(key=(fr*3+r,fc*3+c),size=[3,1])]
            row += [col]
        fcol += [sg.Frame('', row)]
    layout += [fcol]

layout += [[sg.Button('Load'), 
            sg.Button('Solve'), 
            sg.Button('Clear')]]

# Create the Window
window = sg.Window('Sudoku Solver', layout, element_justification='c')

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Clear':
        clearTable()
    elif event == 'Load':
        loadRandomSudoku(data)
    elif event == 'Solve':
        solve(getDisplayedSudoku(values))


window.close()

#########
# TESTS #
#########

# Ajouter les tests nécessaires pour chaque fonction
# Voici quelques exemples (qui sont loin d'être suffisants):
assert isPossible([[4,0,0,0,0,0,0,0,5],
                   [0,0,9,4,0,2,8,0,0],
                   [0,6,0,0,5,0,0,9,0],
                   [0,3,0,0,8,0,0,2,0],
                   [0,0,2,5,0,1,3,0,0],
                   [0,9,0,0,4,0,0,7,0],
                   [0,1,0,0,6,0,0,5,0],
                   [0,0,8,1,0,5,9,0,0],
                   [5,0,0,0,0,0,0,0,7]], 9, (6,0)) == True

assert isPossible([[4,0,0,0,0,0,0,0,5],
                   [0,0,9,4,0,2,8,0,0],
                   [0,6,0,0,5,0,0,9,0],
                   [0,3,0,0,8,0,0,2,0],
                   [0,0,2,5,0,1,3,0,0],
                   [0,9,0,0,4,0,0,7,0],
                   [0,1,0,0,6,0,0,5,0],
                   [0,0,8,1,0,5,9,0,0],
                   [5,0,0,0,0,0,0,0,7]], 9, (7,0)) == False

assert isPossible([[4,0,0,0,0,0,0,0,5],
                   [0,0,9,4,0,2,8,0,0],
                   [0,6,0,0,5,0,0,9,0],
                   [0,3,0,0,8,0,0,2,0],
                   [0,0,2,5,0,1,3,0,0],
                   [0,9,0,0,4,0,0,7,0],
                   [0,1,0,0,6,0,0,5,0],
                   [0,0,8,1,0,5,9,0,0],
                   [5,0,0,0,0,0,0,0,7]], 5, (7,0)) == False


assert nextCell([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']], (2,5)) == (2,8)

assert nextCell([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']], (2,4)) == (2,8)

assert previousCell([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']], (2,4)) == (2,3)


assert isValid([[4,0,9,0,0,0,0,0,5],
                   [0,0,9,4,0,2,8,0,0],
                   [0,6,0,0,5,0,0,9,0],
                   [0,3,0,0,8,0,0,2,0],
                   [0,0,2,5,0,1,3,0,0],
                   [0,9,0,0,4,0,0,7,0],
                   [0,1,0,0,6,0,0,5,0],
                   [0,0,8,1,0,5,9,0,0],
                   [5,0,0,0,0,0,0,0,7]]) == False

assert isValid([[4,0,0,0,0,0,0,0,5],
                   [0,0,9,4,0,2,8,0,0],
                   [0,6,0,0,5,0,0,9,0],
                   [0,3,0,0,8,0,0,2,0],
                   [0,0,2,5,0,1,3,0,0],
                   [0,9,0,0,4,0,0,7,0],
                   [0,1,0,0,6,0,0,5,0],
                   [0,0,8,1,0,5,9,0,0],
                   [5,0,0,0,0,0,0,0,712312301203]]) == False


assert isValid([[9, 0, 0, 0, 4, 0, 0, 0, 8],
                [5, 0, 1, 7, 0, 8, 4, 0, 0],
                [0, 8, 3, 9, 0, 0, 0, 0, 0], 
                [7, 0, 4, 0, 1, 0, 9, 0, 3], 
                [0, 1, 0, 0, 0, 0, 0, 7, 0], 
                [3, 0, 6, 0, 5, 0, 2, 0, 4], 
                [0, 0, 0, 0, 0, 5, 7, 3, 0], 
                [0, 0, 5, 1, 0, 3, 8, 0, 2], 
                [8, 0, 0, 0, 6, 0, 0, 0, 1]]) == True

assert createInitialGrid([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']],) ==  [[9, 0, 0, 0, 2, 0, 0, 0, 7], 
                                                                [0, 6, 0, 7, 0, 8, 0, 9, 5], 
                                                                [0, 0, 0, 0, 0, 6, 8, 4, 0], 
                                                                [8, 2, 0, 0, 6, 0, 0, 5, 3], 
                                                                [0, 0, 7, 0, 0, 0, 4, 0, 0], 
                                                                [4, 3, 0, 0, 7, 0, 0, 1, 8], 
                                                                [0, 8, 9, 1, 0, 0, 0, 0, 0], 
                                                                [6, 7, 0, 4, 0, 9, 0, 3, 0], 
                                                                [1, 0, 0, 0, 3, 0, 0, 0, 9]]

assert findStart([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']],) == (0,1)  
assert isCompleted([[9, 0, 0, 0, 4, 0, 0, 0, 8],
                [5, 0, 1, 7, 0, 8, 4, 0, 0],
                [0, 8, 3, 9, 0, 0, 0, 0, 0], 
                [7, 0, 4, 0, 1, 0, 9, 0, 3], 
                [0, 1, 0, 0, 0, 0, 0, 7, 0], 
                [3, 0, 6, 0, 5, 0, 2, 0, 4], 
                [0, 0, 0, 0, 0, 5, 7, 3, 0], 
                [0, 0, 5, 1, 0, 3, 8, 0, 2], 
                [8, 0, 0, 0, 6, 0, 0, 0, 1]]) == False
assert isCompleted([[9, 1, 2, 3, 4, 5, 9, 4, 8],
                [5, 3, 1, 7, 8, 8, 4, 9, 3],
                [2, 8, 3, 9, 8, 9, 1, 4, 6], 
                [7, 9, 4, 5, 1, 3, 9, 7, 3], 
                [2, 1, 9, 9, 2, 4, 5, 7, 3], 
                [3, 7, 6, 8, 5, 2, 2, 6, 4], 
                [4, 8, 9, 1, 6, 5, 7, 3, 9], 
                [3, 2, 5, 1, 4, 3, 8, 3, 2], 
                [8, 1, 7, 5, 6, 3,2, 7, 1]]) == True  
assert isValid([[7,2,5,4,1,3,8,6,9],
            [1,3,8,9,6,5,4,2,7],
            [6,4,9,8,2,7,1,5,3],
            [3,5,7,6,8,4,2,9,1],
            [4,9,1,3,5,2,7,8,6],
            [2,8,6,7,9,1,3,4,5],
            [8,1,4,5,3,9,6,7,2],
            [9,7,3,2,4,6,5,1,8],
            [5,6,2,1,7,8,9,3,4]]) == True
assert findStart([['9', '4', '9', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']]) == (0,3) 
assert nextCell([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']],(3,3)) ==(3,5)
assert  createInitialGrid([['3', '4', '8', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''], 
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''], 
                 ['6', '7', '', '4', '', '9', '', '3', ''], 
                 ['1', '', '', '', '3', '', '', '', '9']]) ==[[3, 4, 8, 0, 2, 0, 0, 0, 7],
                                                              [0, 6, 0, 7, 0, 8, 0, 9, 5],
                                                              [0, 0, 0, 0, 0, 6, 8, 4, 0],
                                                              [8, 2, 0, 0, 6, 0, 0, 5, 3],
                                                              [0, 0, 7, 0, 0, 0, 4, 0, 0],
                                                              [4, 3, 0, 0, 7, 0, 0, 1, 8],
                                                              [0, 8, 9, 1, 0, 0, 0, 0, 0],
                                                              [6, 7, 0, 4, 0, 9, 0, 3, 0],
                                                              [1, 0, 0, 0, 3, 0, 0, 0, 9]]                             