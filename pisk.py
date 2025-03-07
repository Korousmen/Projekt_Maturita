from tkinter import *
import psycopg2

root = Tk()
root.geometry("500x600")
root.title("Piškvorky")

singed_user = None

connection = psycopg2.connect(
        dbname='projekt',
        user='postgres',
        password='heslo',
        host='localhost',
        port='5432'
         )

root.resizable(0, 0)

frame1 = Frame(root)
frame1.pack()
titleLabel = Label(frame1,
                   text="Piškvorky",
                   font=("Arial", 26),
                   bg="orange",
                   width=16)
titleLabel.grid(row=0, column=0)

optionFrame = Frame(root, bg="grey")
optionFrame.pack()

frame2 = Frame(root, bg="yellow")
frame2.pack()

board = {
  1: " ",
  2: " ",
  3: " ",
  4: " ",
  5: " ",
  6: " ",
  7: " ",
  8: " ",
  9: " "
}

turn = "x"
game_end = False
mode = "singlePlayer"

def changeModeToSinglePlayer():
  global mode
  mode = "singlePlayer"
  
def changeModeToMultiplayer():
  global mode
  mode = "multiPlayer"
  
def updateBoard():
  for key in board.keys():
    buttons[key - 1]["text"] = board[key]

def checkForWin(player):
  # rows
  if board[1] == board[2] and board[2] == board[3] and board[3] == player:
    return True

  elif board[4] == board[5] and board[5] == board[6] and board[6] == player:
    return True

  elif board[7] == board[8] and board[8] == board[9] and board[9] == player:
    return True

  # columns
  elif board[1] == board[4] and board[4] == board[7] and board[7] == player:
    return True

  elif board[2] == board[5] and board[5] == board[8] and board[8] == player:
    return True

  elif board[3] == board[6] and board[6] == board[9] and board[9] == player:
    return True

  # diagonals
  elif board[1] == board[5] and board[5] == board[9] and board[9] == player:
    return True

  elif board[3] == board[5] and board[5] == board[7] and board[7] == player:
    return True

  return False


def checkForDraw():
  for i in board.keys():
    if board[i] == " ":
      return False

  return True


def restartGame():
  global game_end
  game_end = False
  cursor = connection.cursor()
  cursor.execute('''UPDATE uziv SET pocet_her = pocet_her + 1 WHERE username = %s''', (singed_user,))
  connection.commit()
  for button in buttons:
    button["text"] = " "

  for i in board.keys():
    board[i] = " "

  titleLabel = Label(frame1,
                     text="Piškvorky",
                     font=("Arial", 30),
                     bg="orange",
                     width=15)
  titleLabel.grid(row=0, column=0)


def minimax(board, isMaximizing):

  if checkForWin("o"):
    return 1

  if checkForWin("x"):
    return -1

  if checkForDraw():
    return 0

  if isMaximizing:
    bestScore = -100

    for key in board.keys():
      if board[key] == " ":
        board[key] = "o"
        score = minimax(board, False)  # minimax
        board[key] = " "
        if score > bestScore:
          bestScore = score

    return bestScore

  else:
    bestScore = 100

    for key in board.keys():
      if board[key] == " ":
        board[key] = "x"
        score = minimax(board, True)  # minimax
        board[key] = " "
        if score < bestScore:
          bestScore = score

    return bestScore


def playComputer():
  bestScore = -100
  bestMove = 0

  for key in board.keys():
    if board[key] == " ":
      board[key] = "o"
      score = minimax(board, False)  # minimax
      board[key] = " "
      if score > bestScore:
        bestScore = score
        bestMove = key

  board[bestMove] = "o"


# Function to play
def play(event):
  global turn, game_end
  if game_end:
    return

  button = event.widget
  buttonText = str(button)
  clicked = buttonText[-1]
  if clicked == "n":
    clicked = 1
  else:
    clicked = int(clicked)

  if button["text"] == " ":
    if turn == "x":
      board[clicked] = turn
      if checkForWin(turn):
        cursor = connection.cursor()
        cursor.execute('''UPDATE uziv SET pocet_vyher = pocet_vyher + 1 WHERE username = %s''', (singed_user,))
        connection.commit()
        winningLabel = Label(frame1,
                             text=f"{singed_user} vyhrává",
                             bg="orange",
                             font=("Arial", 26),
                             width=16)
        winningLabel.grid(row=0, column=0, columnspan=3)
        print(singed_user)
        game_end = True
      turn = "o"

      updateBoard()

      if mode == "singlePlayer":

        playComputer()

        if checkForWin(turn):
          winningLabel = Label(frame1,
                               text=f"Hráč {turn} vyhrává",
                               bg="orange",
                               font=("Arial", 26),
                               width=16)
          winningLabel.grid(row=0, column=0, columnspan=3)
          game_end = True

        turn = "x"

        updateBoard()

    else:
      board[clicked] = turn
      updateBoard()
      if checkForWin(turn):
        winningLabel = Label(frame1,
                             text=f"Hráč {turn} vyhrává",
                             bg="orange",
                             font=("Arial", 26),
                             width=16)
        winningLabel.grid(row=0, column=0, columnspan=3)
        game_end = True
      turn = "x"

    if checkForDraw():
      drawLabel = Label(frame1,
                        text=f"Remíza",
                        bg="orange",
                        font=("Arial", 26),
                        width=16)
      drawLabel.grid(row=0, column=0, columnspan=3)


# ------ UI --------

# Change Mode options



# Tic Tac Toe Board

#  First row

button1 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button1.grid(row=0, column=0)
button1.bind("<Button-1>", play)

button2 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button2.grid(row=0, column=1)
button2.bind("<Button-1>", play)

button3 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button3.grid(row=0, column=2)
button3.bind("<Button-1>", play)

#  second row

button4 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button4.grid(row=1, column=0)
button4.bind("<Button-1>", play)

button5 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button5.grid(row=1, column=1)
button5.bind("<Button-1>", play)

button6 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button6.grid(row=1, column=2)
button6.bind("<Button-1>", play)

#  third row

button7 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button7.grid(row=2, column=0)
button7.bind("<Button-1>", play)

button8 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button8.grid(row=2, column=1)
button8.bind("<Button-1>", play)

button9 = Button(frame2,
                 text=" ",
                 width=4,
                 height=2,
                 font=("Arial", 30),
                 bg="yellow",
                 relief=RAISED,
                 borderwidth=5)
button9.grid(row=2, column=2)
button9.bind("<Button-1>", play)

restartButton = Button(frame2,
                       text="Restart",
                       width=19,
                       height=1,
                       font=("Arial", 20),
                       bg="Green",
                       relief=RAISED,
                       borderwidth=5,
                       command=restartGame)
restartButton.grid(row=4, column=0, columnspan=3)

buttons = [
  button1, button2, button3, button4, button5, button6, button7, button8,
  button9
]
def run():
  root.mainloop()