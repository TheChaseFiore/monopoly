class makeProperties():
    def __init__(self):
        return makeProperties()

def makeProperties():
    listOfProperties = [("go"),
        ("mediterranean","brown",-60,[2,10,30,90,160,250],30,50),
        ("chest"),
        ("baltic","brown",-60,[4,20,60,180,320,450],30,50),
        ("taxIncome",-200),
        ("railReading"),
        ("oriental","LightBlue",-100,[6,30,90,270,400,550],50,50),
        ("chance"),
        ("vermont","LightBlue",-100,[6,30,90,270,400,550],50,50),
        ("connecticut","LightBlue",-120,[8,40,100,300,450,600],60,50),
        ("jail"),
        ("stCharles","purple",-140,[10,50,150,450,625,750],70,100),
        ("utilityElectricCompany"),
        ("states","purple",-140,[10,50,150,450,625,750],70,100),
        ("virginia","purple",-160,[12,60,180,500,700,900],80,100),
        ("railPennsylvania"),
        ("stJames","orange",-180,[14,70,200,550,750,950],90,100),("chest"),
        ("tennessee","orange",-180,[14,70,200,550,750,950],90,100),
        ("newYork","orange",-200,[16,80,220,600,800,1000],100,100),
        ("freeParking"),
        ("kentucky","red",-220,[18,90,250,700,875,1050],110,150),
        ("chance"),
        ("indiana","red",-220,[18,90,250,700,875,1050],110,150),
        ("illinois","red",-240,[20,100,300,750,925,1100],120,150),
        ("railBO"),
        ("atlantic","yellow",-260,[22,110,330,800,975,1150],130,150),
        ("ventnor","yellow",-260,[22,110,330,800,975,1150],130,150),
        ("utilityWater"),
        ("marvin","yellow",-280,[24,120,360,850,1025,1200],140,150),
        ("goToJail"),
        ("pacific","green",-300,[26,130,390,900,1100,1275],150,200),
        ("northCarolina","green",-300,[26,130,390,900,1100,1275],150,200),
        ("chest"),
        ("pennsylvania","green",-320,[28,150,450,1000,1200,1400],160,200),
        ("railShortLine"),
        ("chance"),
        ("park","blue",-350,[35,175,500,1100,1300,1500],175,200),
        ("taxLux",-100),
        ("boardwalk","blue",-400,[50,200,600,1400,1700,2000],200,200)]
    properties = []
    for ct in xrange(len(listOfProperties)):
        name = listOfProperties[ct]
        if listOfProperties[ct] == "go":
            place = special(name,ct)
        elif listOfProperties[ct] == ("chest"):
            place = chest(name,ct)
        elif listOfProperties[ct] == ("chance"):
            place = chance(name,ct)
        elif listOfProperties[ct] == "jail":
            place = special(name,ct)
        elif listOfProperties[ct] == "goToJail":
            place = special(name,ct)
        elif listOfProperties[ct] == "freeParking":
            place = special(name,ct)
        elif "utility" in listOfProperties[ct]:
            place = utility(name[7:],ct)
        elif "rail" in listOfProperties[ct]:
            place = railRoad(name[4:],ct)
        elif "tax" in listOfProperties[ct][0]:
            place = special(name[0],ct,name[1])
        else:
            place = street(name[0],ct,name[1],name[2],name[3],name[4],name[5])
        properties.append(place)
    return properties
    
class properties(object):
    def __init__(self,name,index,rent=0):
        self.propertyName = name
        self.index = index
        self.rent = rent
        #self.expenses = {purchasePrice: houseCost: hotelCost: }
        #self.income = {base: house1: house2: house3: hotel: mortgageValue: }
    def __str__(self):
        return self.propertyName
    def index(self):
        return self.index
    
    def rentPrice(self):
        return self.rent
    
class street(properties):
    def __init__(self,name,index,color="black",buyPrice=-100,rent=[0,0,0,0,0,0],value=100,housePrice=100,owned=False,mortgaged=False):
        self.propertyName = name
        self.index = index
        self.owned = owned
        self.owner = ""
        self.mortgaged = mortgaged
        self.mortageValue = value
        self.color = color
        self.permaColor = color
        self.houses = 0
        self.buyPrice = buyPrice
        self.rent = rent
        self.housePrice = housePrice
        
    def buy(self,player):
        if not str(self) in player.propertiesOwned and \
            not self.owned and player.cash >= abs(self.buyPrice) and \
            not self.mortgaged:
            player.propertiesOwned.add(str(self))
            player.cash += self.buyPrice
            self.owned = True
            self.color = self.permaColor
            self.owner = player
    
    def mortgage(self,player):
        player.propertiesOwned.remove(str(self))
        player.propertiesMortgaged.add(str(self))
        player.cash += self.mortageValue
        self.owned = False
        self.mortgaged = True
        self.color = "grey"
    
    def rentPrice(self):
        return self.rent[self.houses]  
    
    def allOwned(self,game):
        color = self.color
        owner = self.owner
        ct = 0
        for prop in game.board:
            if prop.color != "black" and prop.color == color and prop.owned and prop.owner == game.players[game.currentPlayer]:
                ct += 1
        if ct == 3:
            return True
        elif ct == 2 and (self.color == "brown" or self.color == "blue"):
            return True
        else:
            return False
        
        
    def unMortgage(self,player,board):
        if self.owner == player:
            player.propertiesOwned.add(str(self))
            for players in board:
                if str(self) in player.propertiesMortgaged:
                    player.propertiesMortgaged.remove(str(self))
            player.cash -= int(self.mortageValue*1.10) #add 10%
            self.owned = True
            self.mortgaged = False
            self.color = self.permaColor
        
    def owned(self):
        return self.owned
    
    def buyHouse(self,game):
        if self.allOwned(game) and game.players[game.currentPlayer].cash >= self.housePrice:
            game.players[game.currentPlayer].cash -= self.housePrice
            if self.houses < 5:
                self.houses += 1
            
    def sellHouse(self,game):
        if self.allOwned(game):
            if game.players[0].position == self.index:
                game.players[0].cash += int(self.housePrice*.5)
            elif game.players[1].position == self.index:
                game.players[1].cash += int(self.housePrice*.5)
            else: pass
        if self.houses > 0:
            self.houses -= 1
    
class special(properties):
    def __init__(self,name,ct,rent=0):
        self.color = "black"
        self.propertyName = name
        self.index = ct
        self.rent = rent
        self.owned = False
    def buy(self,other):pass
    def allOwned(self,board1):
        return False
    def rentPrice(self):
        return self.rent


class railRoad(special):
    def __init__(self,name,index,buyPrice=-200,owned=False,mortgaged=False):
        self.propertyName = name
        self.index = index
        self.owned = owned
        self.owner = ""
        self.mortgaged = mortgaged
        self.houses = 0
        self.color = "railRoad"
        self.buyPrice = buyPrice
        self.rent = [25,50,100,200]
    def buy(self,player):
        if not str(self) in player.propertiesOwned and not self.owned and player.cash >= abs(self.buyPrice):
            player.propertiesOwned.add(str(self))
            player.cash += -200
            self.owned = True
            player.railOwned += 1
            self.owner = player
    def owned(self):
        return self.owned
    def rentPrice(self,game,owner):
        ct = 0
        if game.board[5].owner == owner:
            ct += 1
        if game.board[15].owner == owner:
            ct += 1
        if game.board[25].owner == owner:
            ct += 1
        if game.board[35].owner == owner:
            ct += 1
        return self.rent[ct-1]
    def mortgage(self,player):
        player.propertiesOwned.remove(str(self))
        player.propertiesMortgaged.add(str(self))
        player.cash += self.mortageValue
        self.owned = False
        self.mortgaged = True
        self.color = "grey"
    def unMortgage(self,player,board):
        if self.owner == player:
            player.propertiesOwned.add(str(self))
            for players in board:
                if str(self) in player.propertiesMortgaged:
                    player.propertiesMortgaged.remove(str(self))
            player.cash -= int(self.mortageValue*1.10) #add 10%
            self.owned = True
            self.mortgaged = False
    
class utility(special):
    def __init__(self,name,ct):
        self.color = "black"
        self.propertyName = name
        self.index = ct
        self.rent = 0
        self.owned = False
        self.owner = ""
        self.buyPrice = 150
        self.mortgaged = False
        self.mortgageValue = 75
    def rentPrice(self,roll,game,owner):
        if game.board[12].owner == owner and game.board[28].owner == owner:
            return roll * 10
        return roll * 4
    def owned(self):
        return self.owned
    def buy(self,player):
        if not str(self) in player.propertiesOwned and not self.owned and player.cash >= abs(self.buyPrice):
            player.propertiesOwned.add(str(self))
            player.cash += -150
            self.owned = True
            self.owner = player
    def mortgage(self,player):
        player.propertiesOwned.remove(str(self))
        player.propertiesMortgaged.add(str(self))
        player.cash += self.mortageValue
        self.owned = False
        self.mortgaged = True
        self.color = "grey"
    def unMortgage(self,player,board):
        if self.owner == player:
            player.propertiesOwned.add(str(self))
            for players in board:
                if str(self) in player.propertiesMortgaged:
                    player.propertiesMortgaged.remove(str(self))
            player.cash -= int(self.mortageValue*1.10) #add 10%
            self.owned = True
            self.mortgaged = False


class card(object):
    def __init__(self,name,index):
        self.propertyName = name
        self.index = index
        self.color = "black"
        self.rent = 0
        self.owned = False
    def __str__(self):
        return self.propertyName
    def rentPrice(self):
        return 0
    def buyHouse(self):pass
    def sellHouse(self):pass
    def mortgage(self):pass
    def unMortgage(self):pass
    def buy(self,other):pass
class chest(card):
    pass

class chance(card):
    pass
