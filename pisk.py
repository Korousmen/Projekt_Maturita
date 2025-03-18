from tkinter import *
import  mysql.connector
import random

# Inicializace hlavního okna
root = Tk()
root.geometry("500x600")
root.title("Piškvorky")
root.resizable(0, 0)

# Připojení k databázi
connection =  mysql.connector.connect(
    host='dbs.spskladno.cz',
    port=3306,
    user='student8',
    password='spsnet',
    database='vyuka8'
)

# Globální proměnné
singed_user = "Hráč"  # Jméno hráče bude načítáno z databáze
board = {i: " " for i in range(1, 10)}
turn = "x"
game_end = False
mode = "singlePlayer"

# Funkce pro načtení údajů z databáze
def get_user_info():
    cursor = connection.cursor()
    cursor.execute('''SELECT username, pocet_vyher FROM uziv WHERE username = %s''', (singed_user,))
    result = cursor.fetchone()
    if result:
        return result[0], result[1]  # Vrací jméno uživatele a počet výher
    return singed_user, 0  # Pokud není uživatel nalezen, vrátí výchozí hodnoty

# Vytvoření UI
frame1 = Frame(root)
frame1.pack()

# Titulek hry
titleLabel = Label(frame1, text="Piškvorky", font=("Arial", 26), bg="orange", width=16)
titleLabel.grid(row=0, column=0)

# Informační panel hráče
def update_player_info():
    username, win_count = get_user_info()
    playerInfoLabel.config(text=f"Hráč: {username} | Výhry: {win_count}")

playerInfoLabel = Label(frame1, text=f"Hráč: {singed_user} | Výhry: 0", 
                        font=("Arial", 14), bg="lightgray", width=30)
playerInfoLabel.grid(row=1, column=0)

frame2 = Frame(root, bg="yellow")
frame2.pack()

buttons = []  # Seznam tlačítek

# Vytvoření tlačítek pro hru (automaticky)
for i in range(3):
    for j in range(3):
        btn = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="yellow", relief=RAISED, borderwidth=5)
        btn.grid(row=i, column=j)
        btn.bind("<Button-1>", lambda event, index=len(buttons) + 1: play(index))
        buttons.append(btn)

# Tlačítko pro restart
restartButton = Button(frame2, text="Restart", width=19, height=1, font=("Arial", 20), bg="Green", relief=RAISED, borderwidth=5, command=lambda: restartGame())
restartButton.grid(row=4, column=0, columnspan=3)


def updateBoard():
    """Aktualizuje vizuální podobu tlačítek podle board."""
    for i in range(9):
        buttons[i]["text"] = board[i + 1]


def checkForWin(player):
    """Kontroluje, zda daný hráč vyhrál."""
    return (
        (board[1] == board[2] == board[3] == player) or
        (board[4] == board[5] == board[6] == player) or
        (board[7] == board[8] == board[9] == player) or
        (board[1] == board[4] == board[7] == player) or
        (board[2] == board[5] == board[8] == player) or
        (board[3] == board[6] == board[9] == player) or
        (board[1] == board[5] == board[9] == player) or
        (board[3] == board[5] == board[7] == player)
    )


def checkForDraw():
    """Zkontroluje, zda je remíza."""
    return all(space != " " for space in board.values())


def restartGame():
    """Restartuje hru."""
    global board, turn, game_end
    board = {i: " " for i in range(1, 10)}
    turn = "x"
    game_end = False
    updateBoard()
    titleLabel.config(text="Piškvorky")
    update_player_info()  # Po restartu se opět aktualizuje info o hráči

def play(index):
    """Zpracuje kliknutí na hrací pole."""
    global turn, game_end
    if game_end or board[index] != " ":
        return  # Pokud je hra ukončena nebo je pole obsazené, neprovádí se nic

    board[index] = turn
    updateBoard()

    # Kontrola výhry hráče
    if checkForWin(turn):
        game_end = True
        titleLabel.config(text=f"{singed_user if turn == 'x' else 'Počítač'} vyhrává!")
        cursor = connection.cursor()
        cursor.execute('''UPDATE uziv SET pocet_her = pocet_her + 1 WHERE username = %s''', (singed_user,))
        if turn == "x":
            cursor.execute('''UPDATE uziv SET pocet_vyher = pocet_vyher + 1 WHERE username = %s''', (singed_user,))
        connection.commit()
        update_player_info()  # Aktualizace počtu výher
        return

    # Kontrola remízy
    if checkForDraw():
        game_end = True
        titleLabel.config(text="Remíza")
        cursor = connection.cursor()
        cursor.execute('''UPDATE uziv SET pocet_her = pocet_her + 1 WHERE username = %s''', (singed_user,))
        connection.commit()
        return

    # Přepnutí hráče
    turn = "o" if turn == "x" else "x"

    if mode == "singlePlayer" and turn == "o":
        computer_move = random.choice([i for i in range(1, 10) if board[i] == " "])
        if computer_move:
            board[computer_move] = "o"
            updateBoard()
            if checkForWin("o"):
                game_end = True
                titleLabel.config(text="Počítač vyhrává!")
                cursor = connection.cursor()
                cursor.execute('''UPDATE uziv SET pocet_her = pocet_her + 1 WHERE username = %s''', (singed_user,))
                connection.commit()
                return

            if checkForDraw():
                game_end = True
                titleLabel.config(text="Remíza")
                cursor = connection.cursor()
                cursor.execute('''UPDATE uziv SET pocet_her = pocet_her + 1 WHERE username = %s''', (singed_user,))
                connection.commit()
                return
                    
            turn = "x"  # Přepnutí zpět na hráče
                
def run():
    """Spustí hlavní smyčku Tkinter."""
    root.mainloop()

