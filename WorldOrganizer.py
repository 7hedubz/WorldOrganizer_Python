import sys, json, DescriptorClasses 
import Relationship as Rela
from PySide2 import QtGui, QtCore, QtWidgets

VERSION_CONTROL = "World Creator Files (*.wc1)"

#Class for the button and text field to add a button. 
#*** later to be changed into the user being able to hit enter and create their country. 
# MainWindow contains AddCountry & AddFeature & *CountryNotebook* widgets
# CountryNotebook contains CountryTab
# CountryTab contains treeObject
# CountryTab & treeObject contains INFORMATION for use by the DescWindow class to create a window description.

class AddCountry(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.countryName_QLineEdit = QtWidgets.QLineEdit()
        self.countryCreate_QPushButton = QtWidgets.QPushButton("Create Country")

        #Set the layout var, add the widgets, apply the layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Country Name"))
        self.layout.addWidget(self.countryName_QLineEdit)
        self.layout.addWidget(self.countryCreate_QPushButton)
        self.layout.addSpacing(200)
        self.setLayout(self.layout)

class AddFeature(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.featureChoices = QtWidgets.QComboBox()
        self.featureNameField = QtWidgets.QLineEdit()
        self.featureCreateButton = QtWidgets.QPushButton("Create Feature")
        self.featureChoices.addItem("Landscape", "ls")

        self.layout = QtWidgets.QHBoxLayout()
        # self.layout.addWidget(QtWidgets.QLabel("Feature Type"))
        self.layout.addWidget(self.featureChoices)
        self.layout.addWidget(QtWidgets.QLabel("Feature Name"))
        self.layout.addWidget(self.featureNameField)
        self.layout.addWidget(self.featureCreateButton)
        self.setLayout(self.layout)

class CountryNotebook(QtWidgets.QWidget):
    def changeSwitching(self):
        self.doubleClickToMove = not self.doubleClickToMove
        if self.doubleClickToMove:
            self.moveDescLabel.setText("We Are : MOVING      ")
        else:
            self.moveDescLabel.setText("We Are : OPENING DESC")
        self.connectionSetup(True)

    def moveTreeItem(self):
        #"We Are : OPENING"
        #"We Are : MOVING"
        print("Wants to move tree item...")

        currCountry = self.currCountrySelection()
        currCountryIndex = self.countries.index(currCountry)
        currItem = currCountry.tree.currentItem()

        print("Checking to see if we've already clicked one...")
        if self.moveVar1:
            print("We have already chosen one! Checking to see if it's us...")
            if self.moveVar1.pos == currItem.pos:
                print("It's us! Let's cancel out.")
                self.moveVar1 = 0
                self.moveVar2 = 0
                self.moveDescLabel.setText("We Are MOVING : ")
                return
            if self.moveVar2:
                print("We have already chose two! Checking to see if it's us. (We have to be a landscape to move from country to country!")
                if (self.moveVar2.pos == currItem.pos and self.moveVar2.type == "ls"):
                    print("It's us! Let's try to move! First we need to figure out what one is, so we know how we are moving.")
                    if self.moveVar1.type == "c":
                        print("It's a country, let's change our pos, and our childrens pos's, to our new home.")
                        for ea in currItem.children:
                            ea.changePos(0, currCountryIndex)
                        currItem.pos[0] = currCountryIndex
                        self.reload()
            if not self.moveVar2:
                self.moveDescLabel.setText("We Are MOVING : "+self.moveVar1.uName+" WITH "+self.moveVar2.uName)
                #Here we go to move them.
        if not self.moveVar1:
            self.moveVar1 = currItem
            self.moveDescLabel.setText("We Are MOVING : "+currItem.uName+" WITH")

    def moveCountry(self):
        #"We Are : OPENING"
        #"We Are : MOVING"
        print("Wants to move country...")
        currCountry = self.currCountrySelection()
        currCountryIndex = self.countries.index(currCountry)

        currItem = currCountry.tree.currentItem()

    def selfDestruct(self):
        for ea in self.countries:
            ea.selfDestruct()
        self.countries = []

    def currCountrySelection(self):
        return self.notebook.currentWidget()
        pass

    def isUniq(self, text, listToSrch, typ = None):
        if typ == "ls":
            for ea in listToSrch:
                if ea.type == "ls":
                    if ea.uName == text:
                        return False
            else:
                return True
        else:
            for ea in listToSrch:
                if text == ea.uName:
                    return False
            return True

    def choicesReset(self):
        for i in range(999):
            try:
                self.featureCreateGroup.featureChoices.removeItem(1)
            except:
                return

    def tabBarDblClk(self, index):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()

        for ea in self.openDescWindows:
            if currCountry.pos == ea.clas.pos:
                return

        self.openDescWindows.append(DescWindow(currItem, currCountry, index, notebook = self)) #index tells it it's a country

    def treeItemDblClk(self):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()

        for ea in self.openDescWindows:
            if currItem.pos == ea.pos:
                return

        self.openDescWindows.append(DescWindow(currItem, currCountry, notebook = self))


        if currCountry.tree.isItemExpanded(currItem):
            currCountry.tree.setItemExpanded(currItem, False)
        else:
            try:
                currCountry.tree.setItemExpanded(currItem, True)
            except:
                pass

    def treeSelectionChanged(self):
        try:
            currCountry = self.currCountrySelection()
            currItem = currCountry.tree.currentItem()
            self.choicesReset()
            for ea in currItem.possibleChildren:
                self.featureCreateGroup.featureChoices.addItem(ea[0], ea[1])
        except:
            self.choicesReset()

    def connectionSetup(self, switching):
        #Disconnects the double click for opening the descwindow (need to rename those functions later)
        oldSelection = self.currentTab
        self.currentTab = self.currCountrySelection()
        print("Reconnecting...")

        if switching: #If we are switching I need to disconnect the previous double click connections. 
            if self.doubleClickToMove: #We were opening windows, now we are moving.
                try:
                    oldSelection.tree.itemDoubleClicked.disconnect(self.treeItemDblClk)
                    self.notebook.tabBarDoubleClicked.disconnect(self.tabBarDblClk)
                    oldSelection.tree.itemSelectionChanged.disconnect(self.treeSelectionChanged)
                except:
                    pass
                try:
                    oldSelection.tree.itemDoubleClicked.connect(self.moveTreeItem)
                    self.notebook.tabBarDoubleClicked.connect(self.moveCountry)
                    self.currentTab.tree.itemSelectionChanged.connect(self.treeSelectionChanged)
                    return
                except:
                    pass
            if not self.doubleClickToMove: #We were moving, now we are opening windows. 
                try:
                    self.notebook.tabBarDoubleClicked.disconnect(self.moveCountry)
                    oldSelection.tree.itemDoubleClicked.disconnect(self.moveTreeItem)
                    oldSelection.tree.itemSelectionChanged.disconnect(self.treeSelectionChanged)
                except:
                    pass
                try:
                    self.notebook.tabBarDoubleClicked.connect(self.tabBarDblClk)
                    oldSelection.tree.itemDoubleClicked.connect(self.treeItemDblClk)
                    self.currentTab.tree.itemSelectionChanged.connect(self.treeSelectionChanged)
                    return
                except:
                    pass
      
        if self.doubleClickToMove: #We are moving
            try:
                oldSelection.tree.itemDoubleClicked.disconnect(self.moveTreeItem)
                self.notebook.tabBarDoubleClicked.disconnect(self.moveCountry)
            except:
                pass
            try:
                oldSelection.tree.itemDoubleClicked.connect(self.moveTreeItem)
                self.notebook.tabBarDoubleClicked.connect(self.moveCountry)
            except:
                pass
        elif not self.doubleClickToMove: #We are opening desc windows
            try:
                self.currentTab.tree.itemDoubleClicked.disconnect(self.treeItemDblClk)
                self.notebook.tabBarDoubleClicked.disconnect(self.tabBarDblClk)
            except:
                pass
            try:
                self.currentTab.tree.itemDoubleClicked.connect(self.treeItemDblClk)
                self.notebook.tabBarDoubleClicked.connect(self.tabBarDblClk)
            except:
                pass
    
    def changeCountrySelection(self):
        self.choicesReset()
        self.connectionSetup(False)

    def updatePos(self):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()
        currCountryI = self.notebook.indexOf(self.currCountrySelection())
        
        expanderHelper = []
        
        for ea in self.countries:
            for each in ea.ALLchildren:
                expanderHelper.append(each.isExpanded())

        self.reload()
        
        self.notebook.setCurrentIndex(currCountryI)
        i = -1
        for ea in self.countries:
            for each in ea.ALLchildren:
                i += 1
                each.setExpanded(expanderHelper[i])
           
    def reload(self):
        myWindow.myWidgetVar.parentSaveFunc(filePath = 'reload.json', dialog = False)
        myWindow.myWidgetVar.parentLoadFunc(filePath = 'reload.json', dialog = False)

    def getPos(self, item):
        currCountry = self.currCountrySelection()
        if (currCountry is None):
            return
        currItem = currCountry.tree.currentItem() #Get current Widget Selected
        root = self.currCountrySelection().tree.invisibleRootItem()
        endResult = []
        loopItem = item
        if item.type == "c":
            return self.notebook.indexOf(item)
        while True:
            if loopItem.type == "ls":
                endResult.reverse()
                endResult.insert(0, self.notebook.currentIndex())
                endResult.insert(1, root.indexOfChild(loopItem))
                break
            else:
                endResult.append(loopItem.parent().indexOfChild(loopItem))
                loopItem = loopItem.parent()
        print(endResult)
        return endResult

    def deleteTargetedRels(self, item):
        for country in self.countries:
            i = -1
            for rel in country.rels:
                i += 1
                if rel.clas.pos == item.pos:
                    del country.rels[i]
            
            for eaTW in country.ALLchildren:
                i = -1
                for relation in eaTW.rels:
                    i += 1
                    if relation.clas.pos == item.pos:
                        del eaTW.rels[i]
    
    def createWidgetRels(self):
        for country in self.countries: # 1
            for cRel in country.saveRels: # 2
                for eaCountry in self.countries: # 3
                    if eaCountry.pos == cRel[0]:
                        print("Loaded Rel to",cRel[0])
                        country.rels.append(Rela.Target(eaCountry, relDesc = cRel[1]))
                for eaCiC in self.countries: # 4
                    for eaTWiC in eaCiC.ALLchildren: # 5
                        if eaTWiC.pos == cRel[0]:
                            print("Loaded Rel to",cRel[0])
                            country.rels.append(Rela.Target(eaTWiC, relDesc = cRel[1]))
                            
                            
            for eTWidg in country.ALLchildren: # 1
                for tRel in eTWidg.saveRels: # 2
                    for eachCountry in self.countries: # 3
                        if eachCountry.pos == tRel[0]:
                            print("Loaded Rel to",tRel[0])
                            eTWidg.rels.append(Rela.Target(eachCountry, relDesc = tRel[1]))
                    for evCou in self.countries: # 4
                        for eaTWid in evCou.ALLchildren: # 5
                            if eaTWid.pos == tRel[0]:
                                print("Loaded Rel to",tRel[0])
                                eTWidg.rels.append(Rela.Target(eaTWid, relDesc = tRel[1]))

    def createTreeWidgetFunc(self, choiceStr, text, currCountry, parent, climateInfo = [], detail="", relations = None, imageData = ("", False)):
        if parent is not None: #There is a value here
            if isinstance(parent, list): #It is not a LS
                for ea in currCountry.ALLchildren:
                    if ea.pos == parent:
                        parentItem = ea
                        break
            else:
                parentItem = parent
        
        if currCountry is None:
            return #If there's no country break out! We can't make a feature with no home!
        if text.replace(" ", "") == "":
            return #The only thing in the name is spaces, NO FEATURE FOR YOU

        if choiceStr == "ls": #Make a landscape
            if not self.isUniq(text, currCountry.children, typ="ls"):
                return
            c = Landscape(text, detail)
            if climateInfo:
                c.climateInfo = climateInfo
            currCountry.tree.addTopLevelItem(c)
            currCountry.children.append(c)

        elif not self.isUniq(text, parentItem.children):
            return
            
        if choiceStr == "np":
                c = NotablePlace(text, detail)
        elif choiceStr == "t":
            if self.isUniq(text, parentItem.children):
                c = Town(text, detail)
        elif choiceStr == "dw":
            if self.isUniq(text, parentItem.children):
                c = Dwelling(text, detail)
        elif choiceStr == "p":
            if self.isUniq(text, parentItem.children):
                c = Person(text, detail)
        elif choiceStr == "m":
            if self.isUniq(text, parentItem.children):
                c = Monster(text, detail)

        if choiceStr != "ls":
            parentItem.addChild(c)
            parentItem.children.append(c)
        
        currCountry.ALLchildren.append(c)
        c.pos = self.getPos(c)
        c.saveRels = relations
        c.imagePath = imageData[0]
        c.isImageBig = imageData[1]

    def createTreeWidget(self):
        choiceStr = self.featureCreateGroup.featureChoices.currentData() #Get's the string attached to the current choice eg. ls/np
        text = self.featureCreateGroup.featureNameField.text() #Get's the text for the features name
        currCountry = self.currCountrySelection() #Get's the currently selected country so that we make the widget in the right country
        self.createTreeWidgetFunc(choiceStr=choiceStr, text=text, currCountry=currCountry, parent=currCountry.tree.currentItem())

    def deleteTreeWidget(self):
        currCountry = self.currCountrySelection()
        currCountryIndex = self.countries.index(currCountry)
        
        root = currCountry.tree.invisibleRootItem()
        currItem = currCountry.tree.currentItem()
        currItemParent = currItem.parent()
        
        if currItem is None:
            return
            
        self.deleteTargetedRels(currItem)
            
        if not isinstance(currItem, type(Landscape(""))):
            itemsToDown = currItem.parent().children #Everything that needs to be downcremented
            numToDown = len(currItem.pos) -1 #Which pos needs to be downcremented.
            
            u = -1 
            for ea in itemsToDown:   # Start point for the downcrement
                u += 1
                if ea.pos == currItem.pos:
                    break # We have the start point
            
            del itemsToDown[u]
            
            currItem.parent().removeChild(currItem)
            currItem.selfDestruct(currItem)
           
            i = -1
            for ea in itemsToDown:
                i += 1
                if i >= u:
                    ea.downcrement(numToDown)
            
        else: #It's a LS.
        
            u = -1 #This will equal the overall index for the LS to be del'd
            for ea in currCountry.children:
                u += 1
                if ea.type == "ls":
                    if ea.pos == currItem.pos:
                        break #Now have the start point
            
            del currCountry.children[u] #Deletes the LS
            
            root.removeChild(currItem)
            
            i = -1
            for ea in currCountry.children:
                i += 1
                if i >= u:
                    ea.downcrement(1)
        
        self.updatePos()
        print("DELETE FEATURE")

    def createTabFunc(self, text, detail="", relations = None, imageData = ("", False)):
        a = CountryTab(text, self, detail=detail)
        self.currCountry = self.currCountrySelection()
        self.notebook.addTab(a, text)
        self.countries.append(a)
        a.pos = self.getPos(a)
        a.saveRels = relations
        a.imagePath = imageData[0]
        a.isImageBig = imageData[1]
        return a

    def createTab(self):
        text = self.countryCreateGroup.countryName_QLineEdit.text()
        if text.replace(" ", "") == "":
            return
        if self.isUniq(text, self.countries):
            self.createTabFunc(text)

    def deleteTab(self):
        currCountry = self.currCountrySelection()
        if currCountry is None:
            return
        
        currCountryIndex = self.countries.index(currCountry) # (gives us start point for down-crementing)
        self.notebook.removeTab(currCountryIndex)
        del self.countries[currCountryIndex]
        
        a = len(self.countries) # total length
        if currCountryIndex == a:
            pass
        else:
            b = currCountryIndex
            for ea in range(a - currCountryIndex):# (2 - 1)
                for each in self.countries[b].children:
                    if each.type == "ls":
                        each.downcrement(0)
                    else:
                        pass  
                b += 1
        
        currCountry = self.currCountrySelection()
        self.treeSelectionChanged()
        if len(self.countries) == 0:
            return
            
        self.updatePos()

    def __init__(self, parent=None):
        super().__init__()

        self.countries = []
        self.currentTab = "" #Placeholder for future tab classes.
        self.openDescWindows = []
        self.openRelWindows = []
        self.doubleClickToMove = False
        self.notebook = QtWidgets.QTabWidget()
        self.countryCreateGroup = AddCountry()
        self.featureCreateGroup = AddFeature()
        self.moveDescLabel = QtWidgets.QLabel("We Are OPENING : ")
        self.moveVar1 = 0
        self.moveVar2 = 0


        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.countryCreateGroup)
        self.layout.addWidget(self.featureCreateGroup)
        self.layout.addWidget(self.moveDescLabel)
        self.layout.addWidget(self.notebook)

        self.setLayout(self.layout)

        self.countryCreateGroup.countryCreate_QPushButton.released.connect(self.createTab)
        self.featureCreateGroup.featureCreateButton.released.connect(self.createTreeWidget)
        self.notebook.currentChanged.connect(self.changeCountrySelection)

class CountryTab(QtWidgets.QWidget):

    def selfDestruct(self):
        for ea in self.children:
            ea.selfDestruct()
        self.children = []

    def __init__(self, name, countryNB, detail=""):
        super().__init__()

        self.uName = name
        self.detInfo = detail
        self.rels = []
        self.saveRels = []
        self.children = []
        self.ALLchildren = []
        self.type = "c"
        self.cNB = countryNB
        self.pos = []
        self.imagePath = ""
        self.isImageBig = False

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name","Type"])

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

class treeObject(QtWidgets.QTreeWidgetItem):

    def downcrement(self, index):
        for ea in self.children:
            ea.downcrement(index)
        self.pos[index] -= 1

    def changePos(self, index, num):
        for ea in self.children:
            ea.changePos(num)
        self.pos[index] = num

    def parentDownPosUpdate(self, index, country = None):
    
        if country: #If we are provided with a country it is because a landscape was deleted.
            for child in country.children:
                child.parentDownPosUpdate()
        else:
            for child in self.children:
                child.parentDownPosUpdate()
                
    def selfDestruct(self, country = None):
        for ea in self.children:
            ea.selfDestruct()
            
        if isinstance(self, type(Landscape(""))):
            if country is not None:
                i = -1
                for ls in country.children:
                    i += 1
                    if ls.pos == self.pos:
                        del country.children[i]
        else:
            i = -1
            try:
                for ea in self.parent().children:
                    i += 1
                    if ea.pos == self.pos:
                        del self.parent().children[i]
            except: 
                pass
                
        self.children = []

    def __init__(self, Parent=None):
        super().__init__()

        self.uName = ""
        self.detInfo = ""
        self.children = []
        self.rels = []
        self.saveRels = []
        self.relsHelper = []
        self.type = ""
        self.possibleChildren = []
        self.pos = ""
        self.imagePath = ""
        self.isImageBig = False

class Landscape(treeObject):
    def __init__(self, name, detail="", Parent=None):
        super().__init__()

        self.possibleChildren = [["Notable Place", "np"], ["Town", "t"]]
        self.uName = name
        self.type = "ls"
        self.climateInfo = []
        self.detInfo = detail

        self.setText(0, name)
        self.setText(1, "Landscape")

class NotablePlace(treeObject):
    def __init__(self, name, detail="", Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"],["Person", "p"], ["Monster", "m"]]
        self.uName = name
        self.type = "np"
        self.detInfo = detail
        
        self.setText(0, name)
        self.setText(1, "Notable Place")

class Town(treeObject):
    def __init__(self, name, detail="", Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"], ["Notable Place", "np"]]
        self.uName = name
        self.type = "t"
        self.detInfo = detail
        
        self.setText(0, name)
        self.setText(1, "Town")

class Dwelling(treeObject):
    def __init__(self, name, detail="", Parent=None):
        super().__init__()

        self.possibleChildren = [["Person", "p"], ["Monster", "m"]]
        self.uName = name
        self.type = "dw"
        self.detInfo = detail
        
        self.setText(0, name)
        self.setText(1, "Dwelling")

class Person(treeObject):
    def __init__(self, name, detail="", Parent=None):
        super().__init__()

        self.uName = name
        self.type = "p"
        self.detInfo = detail
        
        self.setText(0, name)
        self.setText(1, "Person")

class Monster(treeObject):
    def __init__(self, name, detail="", Parent=None):
        super().__init__()

        self.uName = name
        self.type = "m"
        self.detInfo = detail
        
        self.setText(0, name)
        self.setText(1, "Monster")

class MyWidget(QtWidgets.QWidget):

    def saveCountry(self, country):
        ret = []
        rel = []
        ret.append(country.uName) #0
        ret.append("c") #1
        ret.append(country.detInfo) #2
        for ea in country.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #3
        ret.append((country.imagePath, country.isImageBig)) #4
        return ret 
    def saveLandscape(self, landscape):
        ret = []
        rel = []
        ret.append(landscape.uName) #0
        ret.append("ls") #1
        ret.append(landscape.climateInfo) #2
        ret.append(landscape.detInfo) #3
        for ea in landscape.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #4
        ret.append((landscape.imagePath, landscape.isImageBig)) #5
        return ret
    def saveNotablePlace(self, np):
        ret = []
        rel = []
        ret.append(np.uName) #0
        ret.append("np") #1
        ret.append(np.parent().pos) #2
        ret.append(np.detInfo) #3
        for ea in np.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #4
        ret.append((np.imagePath, np.isImageBig)) #5
        return ret
    def saveTown(self, town):
        ret = []
        rel = []
        ret.append(town.uName) #0
        ret.append("t") #1
        ret.append(town.parent().pos) #2
        ret.append(town.detInfo) #3
        for ea in town.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #4
        ret.append((town.imagePath, town.isImageBig)) #5
        return ret
    def saveDwelling(self, dwelling):
        ret = []
        rel = []
        ret.append(dwelling.uName) #0
        ret.append("dw") #1
        ret.append(dwelling.parent().pos) #2
        ret.append(dwelling.detInfo) #3
        for ea in dwelling.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #4
        ret.append((dwelling.imagePath, dwelling.isImageBig)) #5
        return ret
    def savePerson(self, person):
        ret = []
        rel = []
        ret.append(person.uName) #0
        ret.append("p") #1
        ret.append(person.parent().pos) #2
        ret.append(person.detInfo) #3
        for ea in person.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #4
        ret.append((person.imagePath, person.isImageBig)) #5
        return ret
    def saveMonster(self, monster):
        ret = []
        rel = []
        ret.append(monster.uName) #0
        ret.append("m") #1
        ret.append(monster.parent().pos) #2
        ret.append(monster.detInfo) #3
        for ea in monster.rels:
            rel.append([ea.clas.pos, ea.relDesc])
        ret.append(rel) #4
        ret.append((monster.imagePath, monster.isImageBig)) #5
        return ret

    def parentSaveFunc(self, filePath = "", dialog = True):
        countries = self.notebook.countries
        
        if len(countries) == 0:
            return
# We will be parsing through each country to find landscapes.
        self.parentSaveInfo = {}
        for eaCou in countries:
            self.parentSaveInfo[eaCou.uName] = []
            self.parentSaveInfo[eaCou.uName].append(self.saveCountry(eaCou))

    # And now each landscape to find towns/notable places
            for eaLand in eaCou.children:
                if isinstance(eaLand, type(Landscape(""))):
                    self.parentSaveInfo[eaCou.uName].append(self.saveLandscape(eaLand))
                    for eaTNP in eaLand.children:
                        if isinstance(eaTNP, type(NotablePlace(""))):
                            self.parentSaveInfo[eaCou.uName].append(self.saveNotablePlace(eaTNP))

                            for eaDPMI in eaTNP.children:
                                    if isinstance(eaDPMI, type(Dwelling(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.saveDwelling(eaDPMI))
                                        for eaPMI in eaDPMI.children:
                                            if isinstance(eaPMI, type(Person(""))):
                                                self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaPMI))
                                            elif isinstance(eaPMI, type(Monster(""))):
                                                self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaPMI))

                                    elif isinstance(eaDPMI, type(Person(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaDPMI))
                                    elif isinstance(eaDPMI, type(Monster(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaDPMI))

    # For the TOWNS in LANDSCAPES
                        elif isinstance(eaTNP, type(Town(""))):
                            self.parentSaveInfo[eaCou.uName].append(self.saveTown(eaTNP))

                            for eaDNP in eaTNP.children:
    #For the DWELLINGS in TOWNS
                                if isinstance(eaDNP, type(Dwelling(""))):
                                    self.parentSaveInfo[eaCou.uName].append(self.saveDwelling(eaDNP))

                                    for eaPMI in eaDNP.children:
                                        if isinstance(eaPMI, type(Person(""))):
                                            self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaPMI))
                                        elif isinstance(eaPMI, type(Monster(""))):
                                            self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaPMI))

    #For the NOTABLE PLACES in TOWNS
                                elif isinstance(eaDNP, type(NotablePlace(""))):
                                            self.parentSaveInfo[eaCou.uName].append(self.saveNotablePlace(eaDNP))

                                            for eaPMI in eaDNP.children:
                                                if isinstance(eaPMI, type(Person(""))):
                                                    self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaPMI))
                                                elif isinstance(eaPMI, type(Monster(""))):
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaPMI))
        if dialog:
            filePath = QtWidgets.QFileDialog.getSaveFileName(self, caption = "Where to Save", filter = VERSION_CONTROL)[0]
        if filePath != "":
            with open(filePath, "w") as write_file:
                json.dump(self.parentSaveInfo, write_file, indent=1)
                print(self.parentSaveInfo)
                print("Saved!")
        else:
            print("No save")

    def loadCountry(self, data):
        a = self.notebook.createTabFunc(data[0], detail=data[2], relations = data[3], imageData = data[4])
        self.loadAssist += 1
        self.notebook.notebook.setCurrentIndex(self.loadAssist)
        return a 
    def loadLandscape(self, ls, country):
        self.notebook.createTreeWidgetFunc(ls[1], ls[0], country, parent = None, climateInfo = ls[2], detail=ls[3], relations = ls[4], imageData = ls[5])
        pass
    def loadNotablePlace(self, np, country):
        self.notebook.createTreeWidgetFunc(np[1], np[0], country, parent = np[2], detail=np[3], relations = np[4], imageData = np[5])
        pass
    def loadTown(self, t, country):
        self.notebook.createTreeWidgetFunc(t[1], t[0], country, parent = t[2], detail=t[3], relations = t[4], imageData = t[5])
        pass
    def loadDwelling(self, dw, country):
        self.notebook.createTreeWidgetFunc(dw[1], dw[0], country, parent = dw[2], detail=dw[3], relations = dw[4], imageData = dw[5])
        pass
    def loadPerson(self, p, country):
        self.notebook.createTreeWidgetFunc(p[1], p[0], country, parent = p[2], detail=p[3], relations = p[4], imageData = p[5])
        pass
    def loadMonster(self, m, country):
        self.notebook.createTreeWidgetFunc(m[1], m[0], country, parent = m[2], detail=m[3], relations = m[4], imageData = m[5])
        pass

    def parentLoadFunc(self, filePath = "", dialog = True):
        self.loadAssist = -1
        if dialog:
            filePath = QtWidgets.QFileDialog.getOpenFileName(self, caption = "What to Load", filter = VERSION_CONTROL)[0]
        if filePath == "":
            print("No Load")
            return
            
        with open(filePath, "r") as read_file:
            data = json.load(read_file)
            
        if len(self.notebook.countries) > 0:
            for ea in range(len(self.notebook.countries)):
                self.notebook.notebook.clear()
                self.notebook.selfDestruct()
                
        for key, value in data.items():
            for item in value:
                if item[1] == "c":
                    country = self.loadCountry(item)
                elif item[1] == "ls":
                    self.loadLandscape(item, country)
                elif item[1] == "np":
                    self.loadNotablePlace(item, country)
                elif item[1] =="t":
                    self.loadTown(item, country)
                elif item[1] =="dw":
                    self.loadDwelling(item, country)
                elif item[1] =="p":
                    self.loadPerson(item, country)
                elif item[1] =="m":
                    self.loadMonster(item, country)
                    
        self.notebook.notebook.setCurrentIndex(0)
        
        self.notebook.createWidgetRels()

    def __init__(self, parent=None):
        super().__init__()

        self.notebook = CountryNotebook()
        self.middleLayout = QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.notebook)
        self.parentSaveInfo = {}
        self.loadAssist = -1

        self.parentGridLayout = QtWidgets.QGridLayout()
        self.parentGridLayout.addLayout(self.middleLayout, 0,0)
        
        self.setLayout(self.parentGridLayout)

class MainWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        a = True
        b = len(self.myWidgetVar.notebook.openDescWindows)
        c = 0
        if b != c:
            while a is True:
                for window in self.myWidgetVar.notebook.openDescWindows:
                    window.close()
                c += 1
                if c == b:
                    a = False
                    
        a = True
        b = len(self.myWidgetVar.notebook.openRelWindows)
        c = 0
        if b != c:
            while a is True:
                for window in self.myWidgetVar.notebook.openRelWindows:
                    window.close()
                c += 1
                if c == b:
                    a = False
        event.accept()
        
    def __init__(self, parent=None):
        super().__init__()
        self.myWidgetVar = MyWidget()
        self.setWindowTitle("~ 7heDubz's World Organizer ~ ")

        
        self.setGeometry(300, 300, 300, 600)
        self.setMaximumSize(1000, 1500) #x, y

        self.parentMenu = self.menuBar()
        self.fileMenu = QtWidgets.QMenu("File")
        self.fileMenuSaveAction = self.fileMenu.addAction("Save (e)", self.myWidgetVar.parentSaveFunc)
        self.fileMenuLoadAction = self.fileMenu.addAction("Load (e)", self.myWidgetVar.parentLoadFunc)

        self.deleteMenu = QtWidgets.QMenu("Delete")
        self.deleteCountryAction = self.deleteMenu.addAction("Delete Country", self.myWidgetVar.notebook.deleteTab)
        self.deleteFeatureAction = self.deleteMenu.addAction("Delete Feature", self.myWidgetVar.notebook.deleteTreeWidget)

        self.editMenu = QtWidgets.QMenu("Edit")
        self.moveWidgetAction = self.editMenu.addAction("Move / Open Item", self.myWidgetVar.notebook.changeSwitching)

        self.parentMenu.addMenu(self.fileMenu)
        self.parentMenu.addMenu(self.deleteMenu)
        self.parentMenu.addMenu(self.editMenu)


        self.setCentralWidget(self.myWidgetVar)
        
class RelationShowWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        self.removeVar.relWindow = None
        event.accept()
        
    def deleteRel(self):
        relIndex = self.listW.indexFromItem(self.listW.currentItem()).column()
        if relIndex == -1:
            return
        del self.clas.rels[relIndex]
        self.listW.takeItem(relIndex)
            
    def openRelInfo(self, item):
        
        relIndex = self.listW.indexFromItem(self.listW.currentItem()).column()
        targRel = self.clas.rels[relIndex]
        
        for ea in self.notebook.openDescWindows:
            if targRel.clas.pos == ea.clas.pos:
                print("Already open")
                return
        if targRel.clas.type == "c":
            i = -1
            for ea in self.notebook.countries:
                i += 1
                if targRel.clas.pos == ea.pos:
                    break
            self.notebook.openDescWindows.append(DescWindow(targRel.clas, targRel.clas, i, notebook = self.notebook))
        else:
            for ea in self.notebook.countries:
                if ea.pos == targRel.clas.pos[0]:
                    targCoun = ea
            self.notebook.openDescWindows.append(DescWindow(targRel.clas, targCoun, notebook = self.notebook))

    def __init__(self, removeVar, notebook, clas):
        super().__init__()

        self.setGeometry(350,350, 500,500)
        self.setMaximumSize(400,400)
        self.clas = clas
        self.removeVar = removeVar
        self.notebook = notebook
        self.setWindowTitle("Relationships")
        
        self.relWin = Rela.ShowWindow(clas)
        self.cw = self.setCentralWidget(self.relWin)
        
        self.listW = self.relWin.relList_QListWidget
        
        self.listW.itemDoubleClicked.connect(self.openRelInfo)
        self.relWin.relDel_QPushButton.released.connect(self.deleteRel)
        
        self.show()

class RelationAddWindow(QtWidgets.QMainWindow):

    def backParser(self):
        orgNotebook = self.relWin.orgNotebook
        for eaCo in range(self.relWin.relNotebook.count()):
            curWid = self.relWin.relNotebook.widget(0)
            self.notebook.notebook.addTab(curWid, curWid.uName)
            self.notebook.changeCountrySelection()

    def closeEvent(self, event):
        self.removeVar.relWindow = None
        self.backConnections(self.relWin.relNotebook)
        self.backParser()
        event.accept()
    
    def checkPos(self, item):
        for ea in self.clas.rels:
            if ea.clas. pos == item.pos:
                print("Already have a rel!")
                return False
        if self.clas.pos == item.pos:
            print("Same thing!")
            return False
        else:
            return True
    
    def treeItemDblClk(self, item, desc = ""):
        if not self.checkPos(item):
            return
        else:
            self.clas.rels.append(Rela.Target(item, relDesc = desc))
            self.close()
        
    def tabBarDblClk(self, index):
        if not self.checkPos(self.relWin.relNotebook.widget(index)):
            return
        else:
            self.clas.rels.append(Rela.Target(self.relWin.relNotebook.widget(index)))
            self.close()
        
    def connections(self, relNotebook):
        for eaCo in range(relNotebook.count()):
            relNotebook.widget(eaCo).tree.itemDoubleClicked.connect(self.treeItemDblClk)
        relNotebook.tabBarDoubleClicked.connect(self.tabBarDblClk)
        
    def backConnections(self, relNotebook):
        for eaCo in range(relNotebook.count()):
            relNotebook.widget(eaCo).tree.itemDoubleClicked.disconnect(self.treeItemDblClk)
        relNotebook.tabBarDoubleClicked.disconnect(self.tabBarDblClk)
        
    def __init__(self, removeVar, notebook, clas):
        super().__init__()

        self.setGeometry(350,350, 500,500)
        self.setMaximumSize(400,400)
        self.clas = clas
        self.notebook = notebook
        self.removeVar = removeVar
        self.setWindowTitle("Relationships")
        
        self.relWin = Rela.AddWindow(notebook, clas)
        self.cw = self.setCentralWidget(self.relWin)
        
        self.connections(self.relWin.relNotebook)
        
        self.show()

class DescWindow(QtWidgets.QMainWindow):

    def openRelAddWin(self):
        if self.relWindow is not None:
            return
        self.relWindow = RelationAddWindow(self, self.notebook, self.clas)
        self.notebook.openRelWindows.append(self.relWindow)

    def openRelShowWin(self):
        if self.relWindow is not None:
            return
        self.relWindow = RelationShowWindow(self, self.notebook, self.clas)
        self.notebook.openRelWindows.append(self.relWindow)

    def climateSet(self):
        text = self.descW.climateChoice.climateAdd.climateAddField.text()
        if text.replace(" ", "") == "":
            return
        if self.isUniq(text, self.clas.climateInfo):
            self.descW.climateChoice.listChoices.addItem(text)
            self.clas.climateInfo.append(text)

    def deleteClimate(self, item):
        row = self.descW.climateChoice.listChoices.currentRow()
        self.descW.climateChoice.listChoices.takeItem(row)
        del self.clas.climateInfo[row]

    def closeEvent(self, event):
        w = False
        for openWindow in self.country.cNB.openDescWindows:
            if openWindow == self:
                a = self.country.cNB.openDescWindows.index(openWindow)
                del self.country.cNB.openDescWindows[a]
                w = True
            else:
                pass
        if w == True:
            event.accept()
        else:
            event.ignore()

    def isUniq(self, text, listToSrch):
        for ea in listToSrch:
            try:
                if text == ea.uName:
                    return False
            except:
                if text == ea:
                    return False
        return True

    def genDesc_SavetoVar(self):
        text = self.descW.genDes.genDesc_QPlainTextEdit.toPlainText()
        self.clas.detInfo = text
              
    def uNameChange(self):
        text = self.descW.nameChanger.nameChangeEdit.text()
        if text.replace(" ", "") == "":
            return
        if self.clas.type == "c":
            if self.isUniq(text, self.country.cNB.countries):
                self.country.cNB.notebook.setTabText(self.CI, text)
                self.setWindowTitle("Country - "+self.clas.uName)
                self.clas.uName = text
        elif self.clas.type == "ls":
            if self.isUniq(text, self.country.children):
                self.clas.setText(0, text)
                self.setWindowTitle(self.clas.type+" -> "+self.country.uName+text)
                self.clas.uName = text
        else:
            if self.isUniq(text, self.clas.parent().children):
                self.clas.setText(0, text)
                self.setWindowTitle(self.clas.type+" -> "+self.country.uName+text)
                self.clas.uName = text

    def changeSmallImage(self, b = False):
        if b:
            filepath = self.clas.imagePath
        else:
            filepath = QtWidgets.QFileDialog.getOpenFileName(self, caption = "Image to Load", filter = "Images (*.jpg *.jpeg)")[0]
        try:         
            self.origImage = QtGui.QImage(filepath)
            self.editImage = self.origImage.scaled(QtCore.QSize(200,400))
            pixmap = QtGui.QPixmap()
            self.cw.pixLabel.setPixmap(pixmap.fromImage(self.editImage))
            self.clas.imagePath = filepath
            self.clas.isImageBig = False
        except:
            print("NO LOAD IMAGE")

    def changeLargeImage(self, b = False):
        if b:
            filepath = self.clas.imagePath
        else:
            filepath = QtWidgets.QFileDialog.getOpenFileName(self, caption = "Image to Load", filter = "Images (*.jpg *.jpeg)")[0]
        try:             
            self.origImage = QtGui.QImage(filepath)
            self.editImage = self.origImage.scaled(QtCore.QSize(600,600))
            pixmap = QtGui.QPixmap()
            self.cw.pixLabel.setPixmap(pixmap.fromImage(self.editImage))
            self.clas.imagePath = filepath
            self.clas.isImageBig = True
        except:
            print("NO LOAD IMAGE")

    def deleteImage(self):
        self.origImage = None
        self.editImage = None
        self.cw.pixLabel.setPixmap(QtGui.QPixmap(0,0))
        self.clas.imagePath = ""
        self.clas.isImageBig = True

    def __init__(self, clas, country, countryIndex = -99, notebook = "", image = None):
        super().__init__()


        self.setGeometry(350,350, 500, 300) #Pos followed by minimum
        self.setMaximumSize(1000,600)
        self.clas = clas
        self.country = country
        self.CI = countryIndex
        self.notebook = notebook
        self.relWindow = None
        self.origImage = image
        self.editImage = None
        self.sizeImage = False

        
        self.parentMenu = self.menuBar()
        self.relMenu = QtWidgets.QMenu("Relationship")
        self.relMenu.addAction("Show Relations", self.openRelShowWin)
        self.relMenu.addAction("Add Relation", self.openRelAddWin)
        self.imagesMenu = QtWidgets.QMenu("Images")
        self.imagesMenu.addAction("Add/Change Image - Small", self.changeSmallImage)
        self.imagesMenu.addAction("Add/Change Image - Large", self.changeLargeImage)
        self.imagesMenu.addAction("Delete Image", self.deleteImage)

        self.parentMenu.addMenu(self.relMenu)
        self.parentMenu.addMenu(self.imagesMenu)
        
        if self.CI >= 0:
            self.descW = DescriptorClasses.CountryDesc(self.country)
            self.cw = self.setCentralWidget(self.descW)
            self.clas = self.country
            self.uName = self.clas.uName
            self.type = "c"
            self.pos = self.clas.pos
            self.setWindowTitle("Country - "+self.clas.uName)
            
        else:
            if clas.type == "ls":
                self.descW = DescriptorClasses.LandscapeDesc(self.clas)
                self.type = "ls"
                self.setWindowTitle("ls - "+self.country.uName+" -> "+clas.uName)

                for text in self.clas.climateInfo:
                    self.descW.climateChoice.listChoices.addItem(text)

                self.descW.climateChoice.climateAdd.climateAddField.returnPressed.connect(self.climateSet)
                self.descW.climateChoice.listChoices.itemDoubleClicked.connect(self.deleteClimate)

            elif clas.type == "np":
                self.descW = DescriptorClasses.NotablePlaceDesc(self.clas)
                self.type = "np"
                self.setWindowTitle("np - "+self.country.uName+" -> "+clas.uName)

            elif clas.type == "t":
                self.descW = DescriptorClasses.TownDesc(self.clas)
                self.type = "t"
                self.setWindowTitle("t - "+self.country.uName+" -> "+clas.uName)

            elif clas.type == "dw":
                self.descW = DescriptorClasses.DwellingDesc(self.clas)
                self.type = "dw"
                self.setWindowTitle("dw - "+self.country.uName+" -> "+clas.uName)

            elif clas.type == "p":
                self.descW = DescriptorClasses.PersonDesc(self.clas)
                self.type = "p"
                self.setWindowTitle("p - "+self.country.uName+" -> "+clas.uName)

            elif clas.type == "m":
                self.descW = DescriptorClasses.MonsterDesc(self.clas)
                self.type = "m"
                self.setWindowTitle("m - "+self.country.uName+" -> "+clas.uName)

        self.descW.nameChanger.nameChangeEdit.setPlaceholderText(self.clas.uName)
        self.descW.nameChanger.nameChangeEdit.returnPressed.connect(self.uNameChange)
        self.descW.genDes.genDesc_QPlainTextEdit.setPlainText(self.clas.detInfo)
        self.descW.genDes.genDesc_QPlainTextEdit.textChanged.connect(self.genDesc_SavetoVar)


        self.cw = pictureWid(self.descW)
        self.setCentralWidget(self.cw)
        self.uName = self.clas.uName
        self.pos = self.clas.pos

        if self.clas.imagePath != "":
            if self.clas.isImageBig:
                self.changeLargeImage(True)
            if not self.clas.isImageBig:
                self.changeSmallImage(True)

        self.show()

class MoveWindow(QtWidgets.QMainWindow):

    def changeText(text):
        self.textEdit.setPlaintText(text)

    def __init__(self):
        super().__init__()

        self.setGeometry(350,350, 500, 300) #Pos followed by minimum
        self.setMaximumSize(1000,600)

        self.textEdit = QtWidgets.QPlainTextEdit()
        self.cw = self.setCentralWidget(self.textEdit)

        self.textEdit.setReadOnly(True)

        self.show()

class pictureWid(QtWidgets.QWidget):
    def __init__(self, descW):
        super().__init__()

        self.pixLabel = QtWidgets.QLabel()        

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(descW, alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(self.pixLabel, alignment=QtCore.Qt.AlignTop)

        self.setLayout(self.layout)


app = QtWidgets.QApplication(sys.argv)

myWindow = MainWindow()
myWindow.show()

sys.exit(app.exec_())
