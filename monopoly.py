from makeProperties import *
from drawMonopoly import *
import random
import time

class game(Animation):
    def __init__(self):
        self.timerDelay = 1
        self.housesLeft = 32
        self.hotelsLeft = 12
        self.board = makeProperties()
        self.players = [player("Dog"),player("Hat")]
        self.currentPlayer = 0
        self.lastRoll = 0
        self.lastCard = ""
        self.over = False
        self.chanceCards = [["self.players[self.currentPlayer].position = 10","Go Directly to Jail"],
                            ["self.players[self.currentPlayer].position -= 3","Go Back Three Spaces"],
                            ["self.players[self.currentPlayer].cash -= int(15)","Speeding Find $15"],
                            ["self.players[self.currentPlayer].advanceTo(5)","Take a Ride on the Reading Railroad"],
                            ["self.players[self.currentPlayer].cash += int(150)","Your Building Loan Matures. Collect $150"],
                            ["self.players[self.currentPlayer].advanceTo(24)","Advance to Illinois Ave."],
                            ["self.players[self.currentPlayer].advanceTo(11)","Advance to St. Charles Place"],
                            ["self.players[self.currentPlayer].advanceTo(39)","Advance to Boardwalk"],
                            ["self.players[self.currentPlayer].cash += int(50)","Bank Pays You Dividend of $50"],
                            ["self.players[self.currentPlayer].advanceTo(0)","Advance to Go"],
                            ['self.players[self.currentPlayer].advanceTo("rail")',"Advance to Nearest Railroad"],
                            ['self.players[self.currentPlayer].advanceTo("rail")',"Advance to Nearest Railroad"],
                            ['self.players[self.currentPlayer].advanceTo("utility")',"Advance to Nearest Utility"]]
        self.communityChestCards = [["self.players[self.currentPlayer].advanceTo(0)","Advance to Go"],
                                    ["self.players[self.currentPlayer].cash += int(200)","Bank Error In Your Favor. Collect $200"],
                                    ["self.players[self.currentPlayer].cash += int(10)","You Have Won A Beauty Contest. Collect $10"],
                                    ["self.players[self.currentPlayer].cash -= int(50)","Pay School Fees of $50"],
                                    ["self.players[self.currentPlayer].cash += int(20)","Income Tax Refund. Collect $20"],
                                    ["self.players[self.currentPlayer].cash -= int(100)","Pay Hospital Fees of $100"],
                                    ["self.players[self.currentPlayer].advanceTo(10)","Go to Jail"],
                                    ["self.players[self.currentPlayer].cash += int(25)","Receive $25 Consultancy Fee"],
                                    ["self.players[self.currentPlayer].cash += int(100)","You Inherit $100"],
                                    ["self.players[self.currentPlayer].cash += int(50)","From Sales of Stock You Get $50"],
                                    ["self.players[self.currentPlayer].cash -= int(50)","Doctor's Fees. Pay $50"],
                                    ["self.players[self.currentPlayer].cash += int(100)","Holiday Fund Matures. Receive $100"],
                                    ["self.players[self.currentPlayer].cash += int(100)","Life Insurance Matures. Receive $100"]]

    def roll(self):
        int1 = random.randint(1,6)
        int2 = random.randint(1,6)
        if int1 == int2:
            pass
        self.lastRoll = int1 + int2
        return int1 + int2
    
    def autoSell(game):
        for player in game.players:
            if player.cash < 0:
                for space in game.board:
                    if str(space) in player.propertiesOwned:
                        if player.cash < 0:
                            if space.houses > 0:
                                space.sellHouse(game)
                            else:
                                space.mortgage(player)
                            game.autoSell()
                if player.cash < 0:
                    game.over = True
                
    def nextPlayer(self):
        if self.currentPlayer != len(self.players)-1:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 0
            
    def utilityRent(self,player,other):
        player.cash -= self.board[player.position].rentPrice(self.lastRoll,self,other)
        other.cash += self.board[player.position].rentPrice(self.lastRoll,self,other)
        
    def railRent(self,player,other):
        player.cash -= self.board[player.position].rentPrice(self,other)
        other.cash += self.board[player.position].rentPrice(self,other)
        
    def chanceCard(self):
        number = random.randint(0,len(self.chanceCards)-1)
        command = self.chanceCards[number][0]
        exec command
        self.lastCard = "Chance - "+self.chanceCards[number][1]
        
    def communityChest(self):
        number = random.randint(0,len(self.communityChestCards)-1)
        command = self.communityChestCards[number][0]
        exec command
        self.lastCard = "Community Chest - "+self.communityChestCards[number][1]

class player(game):
    def __init__(self,player):
        self.playerName = player
        self.cash = 1500
        self.position = 0
        self.propertiesOwned = set()
        self.propertiesMortgaged = set()
        self.getOutOfJailFree = 0
        self.railOwned = 0
        if player=="Dog":
            self.color="blue"
        else:
            self.color="green"
    
    def __str__(self):
        return self.playerName
    
    def position(self):
        return self.position
    
    def move(self,spaces):
        """Moves the player the given number of spaces"""
        passGo = self.position
        self.position += spaces
        if self.position >= 40: # 40 = number of spaces on the board
            self.position -= 40
        if self.position <= passGo:
            self.cash += 200
        if self.position == 30:
            time.sleep(1)
            self.position = 10
        if self.position == 7 or self.position == 22 or self.position == 36: #chance cards
            game.chanceCard()
        if self.position == 2 or self.position == 17 or self.position == 33: #community chest
            game.communityChest()
        self.takeRent()
        game.autoSell()
        
    def advanceTo(self,space):
        if space == "utility":
            if self.position > 12 and self.position < 28:
                self.move(28-self.position)
            elif self.position > 28:
                self.advanceTo(0)
                self.advanceTo(12)
            elif self.position < 12:
                self.move(12-self.position)
        elif space == "rail":
            if self.position < 5:
                self.move(5-self.position)
            elif self.position < 15:
                self.move(15-self.position)
            elif self.position < 25:
                self.move(25-self.position)
            elif self.position < 35:
                self.move(35-self.position)
            elif self.position > 35:
                self.advanceTo(0)
                self.advanceTo(5)
        else:
            delta = space - self.position
            self.move(delta)
            self.takeRent()
        
    def takeRent(self):
        for player in game.players:
            if str(game.board[self.position]) in player.propertiesOwned and \
                str(game.board[self.position]) not in self.propertiesOwned and \
                not isinstance(game.board[self.position],card):
                    if isinstance(game.board[self.position],utility):
                        game.utilityRent(self,player)
                    elif isinstance(game.board[self.position],railRoad):
                        game.railRent(self,player)
                    elif game.board[self.position].allOwned(game) and game.board[self.position].houses==0:
                        self.cash -= game.board[self.position].rentPrice() * 2
                        player.cash += game.board[self.position].rentPrice() * 2
                    else:
                        self.cash -= game.board[self.position].rentPrice()
                        player.cash += game.board[self.position].rentPrice()
        if self.position == 4:
            self.cash -= 200
        elif self.position == 38:
            self.cash -= 100
    def money(self):
        return str(self.cash)

game = game()
game.run()
