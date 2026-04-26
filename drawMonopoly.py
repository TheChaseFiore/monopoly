from Tkinter import *
from makeProperties import *
import time
class Animation(object):

    def init(self,root): 
        rollButton = Button(root, text="Roll (>)", command=self.rollButtonPressed)
        rollButton.pack()
        buyButton = Button(root, text="Buy (b)", command=self.runBuy)
        buyButton.pack()
        mortgageButton = Button(root, text="Mortgage (m)", command=self.mortgageProperty)
        mortgageButton.pack()
        unmortgageButton = Button(root, text="un-Mortgage", command=self.unmortgageProperty)
        unmortgageButton.pack()
        buyHouseButton = Button(root, text="Buy House (h)", command=self.runBuyHouse)
        buyHouseButton.pack()
        sellHouseButton = Button(root, text="Sell House", command=self.runSellHouse)
        sellHouseButton.pack()
    def timerFired(self):pass
            
    def mousePressed(self,event):
        self.mouseX = event.x
        self.mouseY = event.y
        self.trade()
        self.redrawAll()
    def keyPressed(self,event):
        if event.keysym == "Right": #if event.char == "r":
            self.rollButtonPressed()
        elif event.char == "1":
            self.players[self.currentPlayer].move(1)
        elif event.char == "2":
            self.players[self.currentPlayer].move(2)
        elif event.char == "n":
            self.nextPlayer()
        elif event.char == "b":
            self.runBuy()
        elif event.char == "h":
            self.runBuyHouse()
        elif event.char == "m":
            self.mortgageProperty()
        elif event.char == "0":
            self.test()
        self.redrawAll()
    def test(self):
        self.players[0].cash = -100
        self.autoSell()
    def trade(self):
        if self.click1 == True and (self.board[self.parseInput()].owned or self.board[self.parseInput()].mortgaged):
            self.fromTrade = self.parseInput()
            self.click1 = False
        else:
            if self.board[self.parseInput()].owned:
                self.click1 = True
                self.toTrade = self.parseInput()
    
                if str(self.board[self.fromTrade]) in self.players[0].propertiesOwned and \
                    str(self.board[self.toTrade]) not in self.players[0].propertiesOwned:
                    self.players[0].propertiesOwned.remove(str(self.board[self.fromTrade]))
                    self.players[0].propertiesOwned.add(str(self.board[self.toTrade]))
                    self.players[1].propertiesOwned.remove(str(self.board[self.toTrade]))
                    self.players[1].propertiesOwned.add(str(self.board[self.fromTrade]))
                    self.board[self.fromTrade].owner = self.players[0]
                    self.board[self.toTrade].owner = self.players[1]
                if str(self.board[self.fromTrade]) in self.players[1].propertiesOwned and \
                    str(self.board[self.toTrade]) not in self.players[1].propertiesOwned:
                    self.players[1].propertiesOwned.remove(str(self.board[self.fromTrade]))
                    self.players[1].propertiesOwned.add(str(self.board[self.toTrade]))
                    self.players[0].propertiesOwned.remove(str(self.board[self.toTrade]))
                    self.players[0].propertiesOwned.add(str(self.board[self.fromTrade]))
                    self.board[self.toTrade].owner = self.players[1]
                    self.board[self.fromTrade].owner = self.players[0]
    def parseInput(self):
        x = (self.mouseX / self.size) - self.margin
        if self.mouseY > 20 and self.mouseY <= 110:
            y = 1
        elif self.mouseY >=142 and self.mouseY <= 234:
            y = 2
        else: y = 0
        if y == 2:
            if x == 0:
                return 0
            if x > 0:
                final = 0
                final += x
                return final
            if x < 0:
                final = 40
                final += x
                return final
        if y == 1:
            if x == 0:
                return 20
            if x > 0:
                final = 20
                final += x
                return final
            if x < 0:
                final = 20
                final += x
                return final
            
    def runBuy(self):
        self.board[self.players[self.currentPlayer].position].buy(self.players[self.currentPlayer])
    
    def runBuyHouse(self):
        if not self.click1:
            self.board[self.fromTrade].buyHouse(self)
        else:
            self.board[self.players[self.currentPlayer].position].buyHouse(self)
    def runSellHouse(self):
        if not self.click1:
            self.board[self.fromTrade].sellHouse(self)
        else:
            self.board[self.players[self.currentPlayer].position].sellHouse(self)
    
    def rollButtonPressed(self):
        self.nextPlayer()
        self.players[self.currentPlayer].move(self.roll())
        self.redrawAll()
        
    def mortgageProperty(self):
        if not self.click1:
            self.board[self.fromTrade].mortgage(self.players[self.currentPlayer])
        else:
            self.board[self.players[self.currentPlayer].position].mortgage(self.players[self.currentPlayer])
        
    def unmortgageProperty(self):
        if not self.click1:
            self.board[self.fromTrade].unMortgage(self.players[self.currentPlayer],self.players)
            self.click1 = True
        else:
            self.board[self.players[self.currentPlayer].position].unMortgage(self.players[self.currentPlayer],self.players)
        
    def redrawAll(self):
        margin = 10
        self.canvas.delete(ALL)
        self.canvas.create_text(self.width/2,self.height*.9,text="Selected Player: " + str(self.players[self.currentPlayer]) + " - " + str(self.players[self.currentPlayer].color))
        self.canvas.create_text(self.width/2,self.height*.9-15,text=str(self.players[0]) + " $" + self.players[0].money())
        self.canvas.create_text(self.width/2,self.height*.9-30,text=str(self.players[1]) + " $" + self.players[1].money())
        self.canvas.create_text(self.width/2,self.height*.9-45,text="click owned streets for more options")
        if not self.click1:
            self.canvas.create_text(15,self.height/2+50,text=str(self.board[self.fromTrade]) + " is selected",anchor=W)
        #player0 = str(self.players[0].propertiesOwned)
        #player0 = player0[5:-2]
        #player1 = str(self.players[1].propertiesOwned)
        #player1 = player1[5:-2]
        #self.canvas.create_text(15,self.height/2+50,text=str(self.players[0])+" - owned - "+player0,anchor=W)
        #self.canvas.create_text(15,self.height/2+75,text=str(self.players[1])+" - owned - "+player1,anchor=NW)
        if self.lastCard != "":
            self.canvas.create_text(self.width-65,self.height/2+50,text="Last Card:",anchor=E)
            self.canvas.create_text(self.width-15,self.height/2+65,text=self.lastCard,anchor=E)
                                
      
        # row 1
        size = (self.width-(margin*2))/(len(self.board)/2)
        self.size = size
        board = self.board
        position = margin
        self.margin = margin
        for preOffset in xrange(len(self.board)/2):
            ct = preOffset+10
            self.canvas.create_rectangle(position,margin*2,
                                         size+position,size*1.5+margin*2)
            if board[ct].owned == True:
                    for player in self.players:
                        if str(board[ct]) in player.propertiesOwned:
                            self.canvas.create_rectangle(position,margin*2,
                                                 size+position,size*1.5+margin*2,fill="light"+player.color)
                        if str(board[ct]) in player.propertiesMortgaged:
                            self.canvas.create_rectangle(position,margin*2,
                                                 size+position,size*1.5+margin*2,fill="grey")
            if (isinstance(board[ct], street)):
                
                self.canvas.create_rectangle(position,margin*2,
                                            size+position,size*.25+margin*2,
                                            fill=board[ct].color)
                for ct2 in xrange(board[ct].houses): ####houses and hotels
                    if board[ct].houses <= 4:
                        self.canvas.create_rectangle(position+(ct2*(size/4)),margin*2-5,
                                                position+(ct2*(size/4)+(size/4)),margin*2-5+15,
                                                fill="red")
                    if board[ct].houses == 5:
                        self.canvas.create_rectangle(position+15,margin*2-5,
                                                position+size-15,margin*2-5+15,
                                                fill="orange")    
            self.canvas.create_text(position+size/2,margin*5,
                                    text=board[ct],width=size,font=("Helvetica", 11))
            position += size
            
        #### row 2
        position = margin
        for preOffset in xrange(len(self.board)/2):
            ct = preOffset-10
            self.canvas.create_rectangle(position,margin*5+size*1.5,
                                         size+position,margin*5+(size*1.5)*2)
            if board[ct].owned == True:
                    for player in self.players:
                        if str(board[ct]) in player.propertiesOwned:
                            self.canvas.create_rectangle(position,margin*5+size*1.5,
                                                        size+position,margin*5+(size*1.5)*2,fill="light"+player.color)
            if (isinstance(board[ct], street)):
                self.canvas.create_rectangle(position,margin*5+size*1.5,
                                            size+position,margin*5+(size*1.75),
                                            fill=board[ct].color)
                for ct2 in xrange(board[ct].houses): ####houses and hotels
                    if board[ct].houses <= 4:
                        self.canvas.create_rectangle(position+(ct2*(size/4)),margin*5+size*1.5-5,
                                                position+(ct2*(size/4)+(size/4)),margin*5+(size*1.75)-5,
                                                fill="red")
                    if board[ct].houses == 5:
                        self.canvas.create_rectangle(position+15,margin*5+size*1.5-5,
                                                position+size-15,margin*5+(size*1.75)-5,
                                                fill="orange")
            self.canvas.create_text(position+size/2,margin*5+size*2,
                                    text=board[ct],width=size,font=("Helvetica", 11))
            position += size
            
        for player in self.players: #####draw players
            drawPosition = self.convertPosition(player.position)
            
            if drawPosition < 20:
                row = 1
                start = (drawPosition * size)+margin
            else:
                start = ((drawPosition-20) * size)+margin
                row = 2
            if player.color == "blue":
                targetX = start+size/2
                targetY = row*size*1.9
                self.canvas.create_image(targetX,targetY,image=self.dogImage)
                
            else:
                self.canvas.create_image(start+size/2,row*size*1.8,image=self.hatImage)
            if player == self.players[self.currentPlayer]:
                for ct in xrange(2,13): #draw normal line
                    position = self.convertPosition(player.position)
                    if position+ct < 20:
                        row = 1
                        start = ((position+ct) * size)+margin
                    elif position+ct >= 40:
                        row = 1
                        start = ((position+ct-40) * size)+margin
                    else:
                        start = ((position-20+ct) * size)+margin
                        row = 2
                    self.circle(start+size/2,row*size*1.7,size/3.5,"light"+player.color)
        if self.over:
            self.canvas.create_text(self.width/2,self.height/2,
                                    text="game over",font=("Helvetica", 46))
        
    def convertPosition(self,position):
        if position < 10:
            position += 30
        else:
            position -= 10
        return position
    
    def circle(self,x,y,r,color="black"):
        r /= 2
        self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=color)
    
    def startTimerFired(self):
        if (self.timerFiredIsRunning == False):
            self.timerFiredIsRunning = True
            self.timerFiredWrapper()

    def stopTimerFired(self):
        if (self.timerFiredIsRunning == True):
            self.timerFiredIsRunning = False
    
    def timerFiredWrapper(self):
        self.timerFired()
        self.redrawAll()
        if (self.timerFiredIsRunning == True):
            self.canvas.after(self.timerDelay, lambda : self.timerFiredWrapper())

    def run(self):
        # create the root and the canvas
        root = Tk()
        root.resizable(width=FALSE, height=FALSE)
        width = 1250
        height = 400
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        # Set up canvas data and call init
        self.timerDelay = 250
        self.timerFiredIsRunning = False
        self.init(root)  # init(canvas) # DK: init() --> init(canvas)
        self.width = width
        self.height = height
        self.dogImage = PhotoImage(file="dog.gif")
        self.hatImage = PhotoImage(file="hat.gif")
        self.click1 = True
        def f(event):
            self.mousePressed(event)
            self.redrawAll()
        root.bind("<Button-1>", f)
        # DK: Or you can just use an anonymous lamdba function,
        # like this:
        root.bind("<Key>", lambda event: self.keyPressed(event))
        self.startTimerFired()
        # and launch the app
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)