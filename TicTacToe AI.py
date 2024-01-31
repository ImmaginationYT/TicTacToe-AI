from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy

sign=0 #turn counter

gboard=[[" " for x in range(3)] for y in range(3)] #global board variable

def winner(board,player): #endgame conditions
    return ((board[0][0]==player and board[0][1]==player and board[0][2]==player) or
            (board[1][0]==player and board[1][1]==player and board[1][2]==player) or
            (board[2][0]==player and board[2][1]==player and board[2][2]==player) or
            (board[0][0]==player and board[1][0]==player and board[2][0]==player) or
            (board[0][1]==player and board[1][1]==player and board[2][1]==player) or
            (board[0][2]==player and board[1][2]==player and board[2][2]==player) or
            (board[0][0]==player and board[1][1]==player and board[2][2]==player) or
            (board[0][2]==player and board[1][1]==player and board[2][0]==player))

def isfree(board,i,j): #check is a spot is free
    return board[i][j]==" "

def isfull(board): #check if board has no free space left
    flag=True
    for i in board:
        if i.count(" ")>0:
            flag=False
    return flag

def compmove(): #move computer should make
    global gboard
    bestscore=-2
    bestmove=[-1,-1]
    board=deepcopy(gboard)
    scoreandmove=minimax(board,0,True)
    if scoreandmove[0]>bestscore:
        bestmove=scoreandmove[1]
    return bestmove

def minimax(board,depth,needmax): #main logic behind computer's move (minimax algorithm)
    if winner(board,"0"):
        return 1,depth
    elif winner(board,"X"):
        return -1,depth
    elif isfull(board):
        return 0,depth

    if needmax:
        currentscore=-2
        for i in range(len(board)):
            for j in range(len(board)):
                if isfree(board,i,j):
                    board[i][j]="0"
                    testscore=minimax(board,depth+1,False)[0]
                    if testscore>currentscore:
                        currentscore=testscore
                        pos=[i,j]
                    board[i][j]=" "
    else:
        currentscore=2
        for i in range(len(board)):
            for j in range(len(board)):
                if isfree(board,i,j):
                    board[i][j]="X"
                    testscore=minimax(board,depth+1,True)[0]
                    if testscore<currentscore:
                        currentscore=testscore
                        pos=[i,j]
                    board[i][j]=" "
    return currentscore,pos

def buttontextcomputer(i,j,gameboard,l1,l2): #computer's move
    global sign
    global gboard
    if gboard[i][j]==" ":
        if sign%2==0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            gboard[i][j]="X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            gboard[i][j]="0"
        sign+=1
        button[i][j].config(text=gboard[i][j])
    if winner(gboard,"X"):
        messagebox.showinfo("Winner","Player won the match")
        gameboard.destroy()
        for i in range(0,3):
            for j in range(0,3):
                gboard[i][j]=" "
        play()
    elif winner(gboard,"0"):
        messagebox.showinfo("Winner","Computer won the match")
        gameboard.destroy()
        for i in range(0,3):
            for j in range(0,3):
                gboard[i][j]=" "
        play()
    elif isfull(gboard):
        messagebox.showinfo("Tie Game","Tie Game")
        gameboard.destroy()
        for i in range(0,3):
            for j in range(0,3):
                gboard[i][j]=" "
        play()
    else:
        if sign%2!=0:
            move=compmove()
            button[move[0]][move[1]].config(state=DISABLED)
            buttontextcomputer(move[0],move[1],gameboard,l1,l2)

def buttontextplayer(i,j,gameboard,l1,l2): #player's move
    global sign
    global gboard
    if gboard[i][j]==" ":
        if sign%2==0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            gboard[i][j]="X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            gboard[i][j]="0"
        sign+=1
        button[i][j].config(text=gboard[i][j])
    if winner(gboard,"X"):
        messagebox.showinfo("Winner","Player 1 won the match")
        gameboard.destroy()
        for i in range(0,3):
            for j in range(0,3):
                gboard[i][j]=" "
        play()
    elif winner(gboard,"0"):
        messagebox.showinfo("Winner","Player 2 won the match")
        gameboard.destroy()
        for i in range(0,3):
            for j in range(0,3):
                gboard[i][j]=" "
        play()
    elif isfull(gboard):
        messagebox.showinfo("Tie Game","Tie Game")
        gameboard.destroy()
        for i in range(0,3):
            for j in range(0,3):
                gboard[i][j]=" "
        play()

def boardcomputer(gameboard,l1,l2): #computer's turn
    global button
    button=[]
    for i in range(3):
        m=3+i
        button.append(i)
        button[i]=[]
        for j in range(3):
            n=j
            button[i].append(j)
            textforcomputer=partial(buttontextcomputer,i,j,gameboard,l1,l2)
            button[i][j]=Button(gameboard,bd=5,command=textforcomputer,height=4,width=8)
            button[i][j].grid(row=m,column=n)
    gameboard.mainloop()

def boardplayer(gameboard,l1,l2): #computer's turn
    global button
    button=[]
    for i in range(3):
        m=3+i
        button.append(i)
        button[i]=[]
        for j in range(3):
            n=j
            button[i].append(j)
            textforplayer=partial(buttontextplayer,i,j,gameboard,l1,l2)
            button[i][j]=Button(gameboard,bd=5,command=textforplayer,height=4,width=8)
            button[i][j].grid(row=m,column=n)
    gameboard.mainloop()

def againstcomputer(gameboard): #vs computer gamemode
    gameboard.destroy()
    gameboard=Tk()
    gameboard.title("vs Comp")
    l1=Button(gameboard,text="Player : X",width=10)
    l1.grid(row=1,column=1)
    l2=Button(gameboard,text="Computer : O",width=10,state=DISABLED)
    l2.grid(row=2,column=1)
    boardcomputer(gameboard,l1,l2)

def againstplayer(gameboard): #vs player gamemode
    gameboard.destroy()
    gameboard=Tk()
    gameboard.title("vs Player")
    l1=Button(gameboard,text="Player 1 : X",width=10)
    l1.grid(row=1,column=1)
    l2 = Button(gameboard,text="Player 2 : O",width=10,state=DISABLED)
    l2.grid(row=2,column=1)
    boardplayer(gameboard,l1,l2)

def play(): #main function
    global sign
    sign=0
    menu=Tk()
    menu.geometry("300x182")
    menu.title("Boolean Fighters")
    ac=partial(againstcomputer,menu)
    ap=partial(againstplayer,menu)
    head=Label(menu,text="Welcome to Boolean Fighters!!!",bg="light green",fg="red",width=250,font="Times",bd=10)
    b1=Button(menu,text="Single-Player (vs Computer)",command=ac,activeforeground="magenta",activebackground="yellow",bg="pink",fg="blue",width=250,font="summer",bd=5)
    b2=Button(menu,text="Multi-Player (vs Player)",command=ap,activeforeground="magenta",activebackground="yellow",bg="pink",fg="blue",width=250,font="summer",bd=5)
    b3=Button(menu,text="Exit",command=menu.quit,activeforeground="magenta",activebackground="yellow",bg="pink",fg="blue",width=250,font="summer",bd=5)
    head.pack(side="top")
    b1.pack(side="top")
    b2.pack(side="top")
    b3.pack(side="top")
    menu.mainloop()

if __name__=="__main__":
    play()