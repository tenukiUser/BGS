
__author__ = "tenukibestmove"

""" this code allows to prepare the algorithm which repairs the groups and 
the interactive goban made with the sdl / pygame"""

def Goban():
    alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s"]
    board = [] # a1,b:2
    cooList = []
    cooDict = {} # a1:(x,y)
    stonePosition = {} # a1 : "b" or a1:"w" and a1: "n" if there is nothing
    



    i = 0 
    it = 0
    # Make a bord be like this : a1 , a2 ... a19, b1 , b2
    while i != 19:
        it = 1
        while it <= 19:
            ad = alpha[i] + str(it)
            it += 1
            board.append(ad)
               
        i += 1
   

    
    
    
    
    cooTuple = (0,0) 
    cooTr = [13,14]
    cooTuple = (cooTr[0],cooTr[1])
    cooList.append(cooTuple)
    
    # makes a list containing all possible coordinates or can find a stone in the goban image(useful for sdl) 
    i = 0
    it = 2
    while i < 19:
        
        it = 1
        while it < 19:
            cooTr[0] +=23
            cooTuple =(cooTr[0],cooTr[1])
            cooList.append(cooTuple)
            it +=1
        cooTr[1] += 23
        cooTr[0] = 13
        
        cooTuple =(cooTr[0],cooTr[1])
        cooList.append(cooTuple)
        i +=1 
    cooList.pop()
    
    
    
    # make the dict stonePostion
    # there is no stone at the start so the dict is filled with none
    i = 0
    while i < len(board):
        
        stonePosition[board[i]] = "n"
        i+=1

    
    #make the dict cooDict
    i=0
    while i < len(board):
        
        cooDict[board[i]] = cooList[i]
        i+=1 
    





