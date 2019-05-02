import sys, json, DescriptorClasses, Reputations, random, string
from PySide2 import QtGui, QtCore, QtWidgets

class AddCountry(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.countryNameField = QtWidgets.QLineEdit()
        self.countryCreateButton = QtWidgets.QPushButton("Create Country")

        #Set the layout var, add the widgets, apply the layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Country Name"))
        self.layout.addWidget(self.countryNameField)
        self.layout.addWidget(self.countryCreateButton)
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
        self.layout.addSpacing(200)
        self.setLayout(self.layout)

class CountryNotebook(QtWidgets.QWidget):

    def currCountrySelection(self):
        return self.notebook.currentWidget()

    def isUniq(self, text, listToSrch, typ = None):
        if typ == "ls":
            for ea in listToSrch:
                if ea.Type == "ls":
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
            if currCountry.Type == ea.Type:
                if currCountry.uName == ea.uName:
                    return

        self.openDescWindows.append(DescWindow(currItem, currCountry, index))


    def treeItemDblClk(self):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()

        for ea in self.openDescWindows:
            if currItem.id == ea.id:
                return

        a = DescWindow(currItem, currCountry)
        self.openDescWindows.append(a)


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


    def changeCountrySelection(self):
        try:
            oldSelection = self.currentTab
            self.currentTab = self.currCountrySelection()
            try:
                oldSelection.tree.itemSelectionChanged.disconnect(self.treeSelectionChanged)
                oldSelection.tree.itemDoubleClicked.disconnect(self.treeItemDblClk)
                self.notebook.tabBarDoubleClicked.disconnect(self.tabBarDblClk)
            except:
                pass
            self.currentTab.tree.itemSelectionChanged.connect(self.treeSelectionChanged)
            self.currentTab.tree.itemDoubleClicked.connect(self.treeItemDblClk)
            self.notebook.tabBarDoubleClicked.connect(self.tabBarDblClk)
        except:
            pass


    def saveDetInfo(self):
        currCountry = self.currCountrySelection()
        if (currCountry is None):
            return
        currItem = currCountry.tree.currentItem() #Get current Widget Selected

    def createTreeWidgetFunc(self, choiceStr, text, currCountry, parent, climateInfo = [], itemID = None):
        try:
            parentItem = parent
            parent = parent.id
        except:
            pass

        if itemID:
            for eaItem in currCountry.childrenHelper:
                if itemID == eaItem:
                    i = index(currCountry.countryHelper(itemID))
                    parentItem = currCountry.children[i]

        if currCountry is None:
            return #If there's no country break out! We can't make a feature with no home!
        if text.replace(" ", "") is "":
            return #The only thing in the name is spaces, NO FEATURE FOR YOU

        if choiceStr == "ls": #Make a landscape
            if not self.isUniq(text, currCountry.children, typ="ls"):
                return
            c = Landscape(text)
            if climateInfo:
                c.climateInfo = climateInfo
            currCountry.tree.addTopLevelItem(c)

        elif not self.isUniq(text, parentItem.children):
            return
        if choiceStr == "np":
                c = NotablePlace(text)
        elif choiceStr == "t":
            if self.isUniq(text, parentItem.children):
                c = Town(text)
        elif choiceStr == "dw":
            if self.isUniq(text, parentItem.children):
                c = Dwelling(text)
        elif choiceStr == "p":
            if self.isUniq(text, parentItem.children):
                c = Person(text)
        elif choiceStr == "m":
            if self.isUniq(text, parentItem.children):
                c = Monster(text)
        elif choiceStr == "i":
            if self.isUniq(text, parentItem.children):
                c = Item(text)

        if choiceStr != "ls":
            parentItem.addChild(c)
            parentItem.childrenHelper.append(c.id)
            parentItem.children.append(c)
        currCountry.childrenHelper.append(c.id)
        currCountry.children.append(c)


    def createTreeWidget(self):
        choiceStr = self.featureCreateGroup.featureChoices.currentData() #Get's the string attached to the current choice eg. ls/np
        text = self.featureCreateGroup.featureNameField.text() #Get's the text for the features name
        currCountry = self.currCountrySelection() #Get's the currently selected country so that we make the widget in the right country
        self.createTreeWidgetFunc(choiceStr, text, currCountry, currCountry.tree.currentItem())

    def deleteTreeWidget(self):
        try:
            currCountry = self.currCountrySelection()
            currItem = currCountry.tree.currentItem() #Get current Widget Selected
            root = currCountry.tree.invisibleRootItem()

            if isinstance(currItem, type(Landscape(""))):
                a = currCountry.childrenHelper.index(currItem.id)
                del currCountry.childrenHelper[a]
                del currCountry.children[a]
            else:
                a = currItem.parent().childrenHelper.index(currItem.id)
                del currItem.parent().childrenHelper[a]
                del currItem.parent().children[a]

            (currItem.parent() or root).removeChild(currItem)
            self.treeSelectionChanged()
        except:
            pass

    def createTabFunc(self, text):
        a = CountryTab(text, self)
        self.currCountry = self.currCountrySelection()
        self.notebook.addTab(a, text)
        self.countries.append(a)
        return a


    def createTab(self):
        text = self.countryCreateGroup.countryNameField.text()
        if text.replace(" ", "") is "":
            return
        if self.isUniq(text, self.countries):
            self.createTabFunc(text)


    def deleteTab(self):
        currCountry = self.currCountrySelection()
        if currCountry is None:
            return
        currCountryIndex = self.countries.index(currCountry)
        self.notebook.removeTab(currCountryIndex)
        del self.countries[currCountryIndex]
        currCountry = self.currCountrySelection()
        self.treeSelectionChanged()

    def __init__(self, parent=None):
        super().__init__()

        self.countries = []
        self.currentTab = "" #Placeholder for future tab classes.
        self.openDescWindows = []
        self.notebook = QtWidgets.QTabWidget()
        self.countryCreateGroup = AddCountry()
        self.featureCreateGroup = AddFeature()


        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.countryCreateGroup)
        self.layout.addWidget(self.featureCreateGroup)
        self.layout.addWidget(self.notebook)

        self.setLayout(self.layout)

        #self.Sender(in this case the button WITHIN another class).SIGNAL.connect(func)
        self.countryCreateGroup.countryCreateButton.released.connect(self.createTab)
        self.featureCreateGroup.featureCreateButton.released.connect(self.createTreeWidget)
        self.notebook.currentChanged.connect(self.changeCountrySelection)

class CountryTab(QtWidgets.QWidget):


    def saveDetInfo(self):
        currItem = self.tree.currentItem()
        # currItem.detInfo = self.detInfoField.toPlainText()

    def __init__(self, name, countryNB):
        super().__init__()

        self.uName = name
        self.children = []
        self.childrenHelper = []
        self.Type = "c"
        self.cNB = countryNB

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name","Type"])
        # self.detInfoField = QtWidgets.QPlainTextEdit()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tree)
        # self.layout.addWidget(self.detInfoField)
        # self.detInfoField.setReadOnly(True)
        self.setLayout(self.layout)

class treeObject(QtWidgets.QTreeWidgetItem):
    def __init__(self, Parent=None):
        super().__init__()

        self.uName = ""
        self.id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        self.detInfo = ""
        self.children = []
        self.Type = ""
        self.childrenHelper = []
        self.possibleChildren = []
        self.parentCountry = ""

class Landscape(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Notable Place", "np"], ["Town", "t"]]
        self.uName = name
        self.Type = "ls"
        self.climateInfo = []

        self.setText(0, name)
        self.setText(1, "Landscape")

class NotablePlace(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"],["Person", "p"], ["Monster", "m"], ["Item", "i"]]
        self.uName = name
        self.Type = "np"
        self.setText(0, name)
        self.setText(1, "Notable Place")

class Town(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"], ["Notable Place", "np"]]
        self.uName = name
        self.Type = "t"
        self.setText(0, name)
        self.setText(1, "Town")

class Dwelling(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Person", "p"], ["Monster", "m"], ["Item", "i"]]
        self.uName = name
        self.Type = "dw"
        self.setText(0, name)
        self.setText(1, "Dwelling")

class Person(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.Type = "p"
        self.setText(0, name)
        self.setText(1, "Person")

class Monster(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.Type = "m"
        self.setText(0, name)
        self.setText(1, "Monster")

class Item(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.Type = "i"
        self.setText(0, name)
        self.setText(1, "Item")


class MyWidget(QtWidgets.QWidget):

    def saveCountry(self, country):
        ret = []
        ret.append(country.uName)
        ret.append("c")
        ret.append(len(country.children))
        return ret
    def saveLandscape(self, landscape):
        ret = []
        ret.append(landscape.uName) #0
        ret.append("ls") #1
        ret.append(len(landscape.children)) #2
        ret.append(landscape.climateInfo) #3
        ret.append(landscape.id) #4
        return ret
    def saveNotablePlace(self, np):
        ret = []
        ret.append(np.uName) #0
        ret.append("np") #1
        ret.append(np.id)#2
        ret.append(np.parent().id)#3
        return ret
    def saveTown(self, town):
        ret = []
        ret.append(town.uName) #0
        ret.append("t") #1
        ret.append(town.id) #2
        ret.append(town.parent().id) #3
        return ret
    def saveDwelling(self, dwelling):
        ret = []
        ret.append(dwelling.uName) #0
        ret.append("dw") #1
        ret.append(dwelling.id) #2
        ret.append(dwelling.parent().id) #3
        return ret
    def savePerson(self, person):
        ret = []
        ret.append(person.uName) #0
        ret.append("p") #1
        ret.append(person.id) #2
        ret.append(person.parent().id) #3
        return ret
    def saveMonster(self, monster):
        ret = []
        ret.append(monster.uName) #0
        ret.append("m") #1
        ret.append(monster.id) #2
        ret.append(monster.parent().id) #3
        return ret
    def saveItem(self, item):
        ret = []
        ret.append(item.uName) #0
        ret.append("i") #1
        ret.append(item.id) #2
        ret.append(item.parent().id) #3
        return ret

    def parentSaveFunc(self):
        print("Trying to save")
        countries = self.notebook.countries
        if len(countries) == 0:
            print("Nothing to save!")
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
                                            elif isinstance(eaPMI, type(Item(""))):
                                                self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaPMI))

                                    elif isinstance(eaDPMI, type(Person(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaDPMI))
                                    elif isinstance(eaDPMI, type(Monster(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaDPMI))
                                    elif isinstance(eaDPMI, type(Item(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaDPMI))

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
                                        elif isinstance(eaPMI, type(Item(""))):
                                            self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaPMI))

    #For the NOTABLE PLACES in TOWNS
                                elif isinstance(eaDNP, type(NotablePlace(""))):
                                            self.parentSaveInfo[eaCou.uName].append(self.saveNotablePlace(eaDNP))

                                            for eaPMI in eaDNP.children:
                                                if isinstance(eaPMI, type(Person(""))):
                                                    self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaPMI))
                                                elif isinstance(eaPMI, type(Monster(""))):
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaPMI))
                                                elif isinstance(eaPMI, type(Item(""))):
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaPMI))
        print(self.parentSaveInfo)
        with open("data_file1.json", "w") as write_file:
            json.dump(self.parentSaveInfo, write_file, indent=4)
            print("Saved!")

    def loadCountry(self, text):
        a = self.notebook.createTabFunc(text)
        return a
    def loadLandscape(self, ls, country):
        self.notebook.createTreeWidgetFunc(ls[1], ls[0], country, parent = None, climateInfo = ls[3], itemID = ls[4])
    def loadNotablePlace(self, np, country):
        self.notebook.createTreeWidgetFunc(np[1], np[0], country, parent = np[3], itemID = np[2])
    def loadTown(self, t, country):
        self.notebook.createTreeWidgetFunc(t[1], t[0], country, parent = t[3], itemID = t[2])
    def loadDwelling(self, dw, country):
        self.notebook.createTreeWidgetFunc(dw[1], dw[0], country, parent = dw[3], itemID = dw[2])
    def loadPerson(self, p, country):
        self.notebook.createTreeWidgetFunc(p[1], p[0], country, parent = p[3], itemID = p[2])
    def loadMonster(self, m, country):
        self.notebook.createTreeWidgetFunc(m[1], m[0], country, parent = m[3], itemID = m[2])
    def loadItem(self, i, country):
        self.notebook.createTreeWidgetFunc(i[1], i[0], country, parent = i[3], itemID = i[2])

    def parentLoadFunc(self):
        with open("data_file1.json", "r") as read_file:
            data = json.load(read_file)
        if len(self.notebook.countries) > 0:
            return
        for key, value in data.items():
            self.fullList = value
            for item in value:
                if item[1] == "c":
                    country = self.loadCountry(item[0])
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
                elif item[1] =="i":
                    self.loadItem(item, country)


    def __init__(self, parent=None):
        super().__init__()

        self.notebook = CountryNotebook()
        self.middleLayout = QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.notebook)
        self.parentSaveInfo = {}

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
        event.accept()

    def __init__(self, parent=None):
        super().__init__()
        self.myWidgetVar = MyWidget()

        self.setGeometry(300, 300, 500, 800)
        self.setMaximumSize(500, 800) #x, y

        self.parentMenu = self.menuBar()
        self.fileMenu = QtWidgets.QMenu("File")
        self.fileMenuAction = self.fileMenu.addAction("Save (e)", self.myWidgetVar.parentSaveFunc)
        self.fileMenuAction = self.fileMenu.addAction("Load (e)", self.myWidgetVar.parentLoadFunc)

        self.deleteMenu = QtWidgets.QMenu("Delete")
        self.deleteCountryAction = self.deleteMenu.addAction("Delete Country", self.myWidgetVar.notebook.deleteTab)
        self.deleteFeatureAction = self.deleteMenu.addAction("Delete Feature", self.myWidgetVar.notebook.deleteTreeWidget)

        self.parentMenu.addMenu(self.fileMenu)
        self.parentMenu.addMenu(self.deleteMenu)

        self.setCentralWidget(self.myWidgetVar)

class DescWindow(QtWidgets.QMainWindow):


    def climateSet(self):
        text = self.w.climateChoice.climateAdd.climateAddField.text()
        if text.replace(" ", "") is "":
            return
        if self.isUniq(text, self.clas.climateInfo):
            self.w.climateChoice.listChoices.addItem(text)
            self.clas.climateInfo.append(text)
            print(self.clas.climateInfo)

    def deleteClimate(self, item):
        row = self.w.climateChoice.listChoices.currentRow()
        self.w.climateChoice.listChoices.takeItem(row)
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


    def uNameChange(self):
        text = self.w.nameChanger.nameChangeEdit.text()
        if text.replace(" ", "") is "":
            return
        if self.clas.Type == "c":
            print("It's a Country!")
            if self.isUniq(text, self.country.cNB.countries):
                self.country.cNB.notebook.setTabText(self.CI, text)
                self.setWindowTitle("Country - "+self.clas.uName)
                self.clas.uName = text
        elif self.clas.Type == "ls":
            if self.isUniq(text, self.country.children):
                self.clas.setText(0, text)
                self.setWindowTitle(self.clas.Type+" -> "+self.country.uName+text)
                self.clas.uName = text
        else:
            if self.isUniq(text, self.currItem.parent().children):
                self.clas.setText(0, text)
                self.setWindowTitle(self.clas.Type+" -> "+self.country.uName+text)
                self.clas.uName = text

    def __init__(self, clas, country, countryIndex = -99):
        super().__init__()


        self.setGeometry(350,350, 370,600)
        self.setMaximumSize(370,600)
        self.clas = clas
        self.country = country
        self.CI = countryIndex

        if self.CI >= 0:
            self.w = DescriptorClasses.CountryDesc(self.country)
            self.cw = self.setCentralWidget(self.w)
            self.clas = self.country
            self.uName = self.clas.uName
            self.Type = "c"
            self.id = self.clas.id
            self.setWindowTitle("Country - "+self.clas.uName)
        else:
            self.currItem = country.tree.currentItem()

            if clas.Type == "ls":
                self.w = DescriptorClasses.LandscapeDesc(self.clas)
                self.Type = "ls"
                self.setWindowTitle("ls - "+self.country.uName+" -> "+clas.uName)

                for text in self.clas.climateInfo:
                    self.w.climateChoice.listChoices.addItem(text)

                self.w.climateChoice.climateAdd.climateAddField.returnPressed.connect(self.climateSet)
                self.w.climateChoice.listChoices.itemDoubleClicked.connect(self.deleteClimate)

            elif clas.Type == "np":
                self.w = DescriptorClasses.NotablePlaceDesc(self.clas)
                self.Type = "np"
                self.setWindowTitle("np - "+self.country.uName+" -> "+clas.uName)

            elif clas.Type == "t":
                self.w = DescriptorClasses.TownDesc(self.clas)
                self.Type = "t"
                self.setWindowTitle("t - "+self.country.uName+" -> "+clas.uName)

            elif clas.Type == "dw":
                self.w = DescriptorClasses.DwellingDesc(self.clas)
                self.Type = "dw"
                self.setWindowTitle("dw - "+self.country.uName+" -> "+clas.uName)

            elif clas.Type == "p":
                self.w = DescriptorClasses.PersonDesc(self.clas)
                self.Type = "p"
                self.setWindowTitle("p - "+self.country.uName+" -> "+clas.uName)

            elif clas.Type == "m":
                self.w = DescriptorClasses.MonsterDesc(self.clas)
                self.Type = "m"
                self.setWindowTitle("m - "+self.country.uName+" -> "+clas.uName)

            elif clas.Type == "i":
                self.w = DescriptorClasses.ItemDesc(self.clas)
                self.Type = "i"
                self.setWindowTitle("i - "+self.country.uName+" -> "+clas.uName)

        self.w.nameChanger.nameChangeEdit.setPlaceholderText(self.clas.uName)
        self.w.nameChanger.nameChangeEdit.returnPressed.connect(self.uNameChange)
        self.cw = self.setCentralWidget(self.w)
        self.uName = self.clas.uName
        self.id = self.clas.id

        self.show()

app = QtWidgets.QApplication(sys.argv)

myWindow = MainWindow()
myWindow.show()

sys.exit(app.exec_())
