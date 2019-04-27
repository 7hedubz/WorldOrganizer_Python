import sys, json, DescriptorClasses
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

    def isUniq(self, text, listToSrch):
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

    @QtCore.Slot()
    def tabBarDblClk(self, index):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()
        if self.isUniq(currCountry.uName, self.openDescWindows):
            self.openDescWindows.append(DescWindow(currItem, currCountry, index))

    @QtCore.Slot()
    def treeItemDblClk(self):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()
        if self.isUniq(currItem.uName, self.openDescWindows):
            self.openDescWindows.append(DescWindow(currItem, currCountry, -1))
            if currCountry.tree.isItemExpanded(currItem):
                currCountry.tree.setItemExpanded(currItem, False)
            else:
                try:
                    currCountry.tree.setItemExpanded(currItem, True)
                except:
                    pass

    @QtCore.Slot()
    def treeSelectionChanged(self):
        try:
            currCountry = self.currCountrySelection()
            currItem = currCountry.tree.currentItem()
            self.choicesReset()
            for ea in currItem.possibleChildren:
                self.featureCreateGroup.featureChoices.addItem(ea[0], ea[1])
        except:
            self.choicesReset()

    @QtCore.Slot()
    def changeCountrySelection(self):
        try:
            oldSelection = self.currentTab
            self.currentTab = self.currCountrySelection()
            try:
                oldSelection.tree.itemSelectionChanged.disconnect(self.treeSelectionChanged)
                oldSelection.tree.itemDoubleClicked.disconnect(self.treeItemDblClk)
                self.notebook.tabBarDoubleClicked.disconnect(self.treeItemDblClk)
            except:
                pass
            self.currentTab.tree.itemSelectionChanged.connect(self.treeSelectionChanged)
            self.currentTab.tree.itemDoubleClicked.connect(self.tabBarDblClk)
            self.notebook.tabBarDoubleClicked.connect(self.tabBarDblClk)
        except:
            pass

    @QtCore.Slot()
    def saveDetInfo(self):
        currCountry = self.currCountrySelection()
        if (currCountry is None):
            return
        currItem = currCountry.tree.currentItem() #Get current Widget Selected

    @QtCore.Slot()
    def createTreeWidget(self):
        choiceStr = self.featureCreateGroup.featureChoices.currentData() #Get's the string attached to the current choice eg. ls/np
        text = self.featureCreateGroup.featureNameField.text() #Get's the text for the features name
        currCountry = self.currCountrySelection() #Get's the currently selected country so that we make the widget in the right country
        if currCountry is None:
            return #If there's no country break out! We can't make a feature with no home!
        currItem = currCountry.tree.currentItem() #Get current Widget Selected
        if text.replace(" ", "") is "":
            return #The only thing in the name is spaces, NO FEATURE FOR YOU
        if choiceStr == "ls": #Make a landscape
            if self.isUniq(text, currCountry.children):
                c = Landscape(text)
                currCountry.tree.addTopLevelItem(c)
                currCountry.childrenHelper.append(text)
                currCountry.children.append(c)
        if choiceStr == "np":
            if self.isUniq(text, currItem.children):
                c = NotablePlace(text)
                currItem.addChild(c)
                currItem.childrenHelper.append(text)
                currItem.children.append(c)
        if choiceStr == "t":
            if self.isUniq(text, currItem.children):
                c = Town(text)
                currItem.addChild(c)
                currItem.childrenHelper.append(text)
                currItem.children.append(c)
        if choiceStr == "dw":
            if self.isUniq(text, currItem.children):
                c = Dwelling(text)
                currItem.addChild(c)
                currItem.childrenHelper.append(text)
                currItem.children.append(c)
        if choiceStr == "p":
            if self.isUniq(text, currItem.children):
                c = Person(text)
                currItem.addChild(c)
                currItem.childrenHelper.append(text)
                currItem.children.append(c)
        if choiceStr == "m":
            if self.isUniq(text, currItem.children):
                c = Monster(text)
                currItem.addChild(c)
                currItem.childrenHelper.append(text)
                currItem.children.append(c)
        if choiceStr == "i":
            if self.isUniq(text, currItem.children):
                c = Item(text)
                currItem.addChild(c)
                currItem.childrenHelper.append(text)
                currItem.children.append(c)

    def deleteTreeWidget(self):
        try:
            currCountry = self.currCountrySelection()
            currItem = currCountry.tree.currentItem() #Get current Widget Selected
            root = currCountry.tree.invisibleRootItem()

            if isinstance(currItem, type(Landscape(""))):
                a = currCountry.childrenHelper.index(currItem.uName)
                del currCountry.childrenHelper[a]
                del currCountry.children[a]
            else:
                a = currItem.parent().childrenHelper.index(currItem.uName)
                del currItem.parent().childrenHelper[a]
                del currItem.parent().children[a]
            (currItem.parent() or root).removeChild(currItem)
            self.treeSelectionChanged()
        except:
            pass

    @QtCore.Slot()
    def createTab(self):
        text = self.countryCreateGroup.countryNameField.text()
        if text.replace(" ", "") is "":
            return
        if self.isUniq(text, self.countries):
            a = CountryTab(text, self)
            currCountry = self.currCountrySelection()
            self.notebook.addTab(a, text)
            self.countries.append(a)

    @QtCore.Slot()
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

    @QtCore.Slot()
    def saveDetInfo(self):
        currItem = self.tree.currentItem()
        # currItem.detInfo = self.detInfoField.toPlainText()

    def __init__(self, name, countryNB):
        super().__init__()

        self.uName = name
        self.children = []
        self.childrenHelper = []
        self.type = "c"
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
        self.detInfo = ""
        self.children = []
        self.type = ""
        self.childrenHelper = []
        self.possibleChildren = []


class Landscape(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Notable Place", "np"], ["Town", "t"]]
        self.uName = name
        self.type = "ls"
        temperate = ""
        self.desc = ""
        self.setText(0, name)
        self.setText(1, "Landscape")

class NotablePlace(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"],["Person", "p"], ["Monster", "m"], ["Item", "i"]]
        self.uName = name
        self.type = "np"
        self.setText(0, name)
        self.setText(1, "Notable Place")

class Town(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"], ["Notable Place", "np"]]
        self.uName = name
        self.type = "t"
        self.setText(0, name)
        self.setText(1, "Town")

class Dwelling(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Person", "p"], ["Monster", "m"], ["Item", "i"]]
        self.uName = name
        self.type = "dw"
        self.setText(0, name)
        self.setText(1, "Dwelling")

class Person(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.type = "p"
        self.setText(0, name)
        self.setText(1, "Person")

class Monster(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.type = "m"
        self.setText(0, name)
        self.setText(1, "Monster")

class Item(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.type = "i"
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
        ret.append(landscape.uName)
        ret.append("ls")
        ret.append(len(landscape.children))
        return ret
    def saveNotablePlace(self, np):
        ret = []
        ret.append(np.uName)
        ret.append("np")
        ret.append(len(np.children))
        return ret
    def saveTown(self, town):
        ret = []
        ret.append(town.uName)
        ret.append("t")
        ret.append(len(town.children))
        return ret
    def saveDwelling(self, dwelling):
        ret = []
        ret.append(dwelling.uName)
        ret.append("dw")
        ret.append(len(dwelling.children))
        return ret
    def savePerson(self, person):
        ret = []
        ret.append(person.uName)
        ret.append("p")
        return ret
    def saveMonster(self, monster):
        ret = []
        ret.append(monster.uName)
        ret.append("m")
        return ret
    def saveItem(self, item):
        ret = []
        ret.append(item.uName)
        ret.append("i")
        return ret


    @QtCore.Slot()
    def parentSaveFunc(self):
        print("Trying to save")
        countries = self.notebook.countries
        if len(countries) == 0:
            print("Nothing to save!")
            return
# We will be parsing through each country to find landscapes.
        for eaCou in countries:
            self.parentSaveInfo = {eaCou.uName : []}
            self.parentSaveInfo[eaCou.uName].append(self.saveCountry(eaCou))
            # Example of a save would be {'America': [['Virginia', 0]]}
            # The first piece (the key) is the country name, whereas the data is a list of lists.
            # The number at the end of a list indicates how many lists after that are childed underneath it.
            # The following list beyond that number is a new piece (whether that be a Dwelling or Country)
            if len(eaCou.children) == 0:
                #print("There are no landscapes in this country.")
                pass
    # And now each landscape to find towns/notable places
            else:
                for eaLand in eaCou.children:
                    self.parentSaveInfo[eaCou.uName].append(self.saveLandscape(eaLand))
                    if len(eaLand.children) == 0:
                        #print("There are no children in this landscape.")
                        pass
        # And now each child of the landscape, to see if it's a notable place
                    else:
                        for eaTNP in eaLand.children:
                            if isinstance(eaTNP, type(NotablePlace(""))):
                                #print("This is a Notable Place!")
                                self.parentSaveInfo[eaCou.uName].append(self.saveNotablePlace(eaTNP))
            # And now each child of the notable place to see if it has children.
                                if len(eaTNP.children) == 0:
                                    # print("There are no children in this Notable Place.")
                                    pass
                                else:
                    # And now each child of the notable place to see if it has children.
                                    for eaChil in eaTNP.children:
                                        if isinstance(eaChil, type(Person(""))):
                                            # print("There is a Person in this Notable place!")
                                            self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaChil))
                    # And now save the Person info.
                                        elif isinstance(eaChil, type(Monster(""))):
                                            # print("There is a Monster in this Notable place!")
                                            self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaChil))
                    # And now save the Monster info
                                        elif isinstance(eaChil, type(Item(""))):
                                            # print("There is an Item in this Notable place!")
                                            self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaChil))
                    # And now save the Item info
        # And now each child of the landscape, to see if it's a town
                            elif isinstance(eaTNP, type(Town(""))):
                                # print("This is a town!")
                                self.parentSaveInfo[eaCou.uName].append(self.saveTown(eaTNP))
            # And now each child of the town to see if it has children
                                if len(eaTNP.children) == 0:
                                    # print("There are no children in this Town.")
                                    pass
                                for eaChil in eaTNP.children:
                                    if isinstance(eaChil, type(Dwelling(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.saveDwelling(eaChil))
                                        if len(eaChil.children) == 0:
                                            # print("There are no children in this Dwelling.")
                                            pass
                                        else:
                                            for eaUnit in eaChil.children:
                                                if isinstance(eaUnit, type(Person(""))):
                                                    # print("There is a Person in this Dwelling!")
                                                    self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaUnit))
                            # And now save the Person info.
                                                elif isinstance(eaUnit, type(Monster(""))):
                                                    # print("There is a Monster in this Dwelling!")
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaUnit))
                            # And now save the Monster info
                                                elif isinstance(eaUnit, type(Item(""))):
                                                    # print("There is an Item in this Dwelling!")
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaUnit))
                            # And now save the Item info

                                    elif isinstance(eaChil, type(NotablePlace(""))):
                                        self.parentSaveInfo[eaCou.uName].append(self.saveNotablePlace(eaChil))
                                        if len(eaChil.children) == 0:
                                            # print("There are no children in this NotablePlace")
                                            pass
                                        else:
                                            for eaUnit in eaChil.children:
                                                if isinstance(eaUnit, type(Person(""))):
                                                    # print("There is a Person in this Dwelling!")
                                                    self.parentSaveInfo[eaCou.uName].append(self.savePerson(eaUnit))
                            # And now save the Person info.
                                                elif isinstance(eaUnit, type(Monster(""))):
                                                    # print("There is a Monster in this Dwelling!")
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveMonster(eaUnit))
                            # And now save the Monster info
                                                elif isinstance(eaUnit, type(Item(""))):
                                                    #  print("There is an Item in this Dwelling!")
                                                    self.parentSaveInfo[eaCou.uName].append(self.saveItem(eaUnit))
                                # And now save the Item info
        print(self.parentSaveInfo)


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

    def __init__(self, parent=None):
        super().__init__()
        myWidgetVar = MyWidget()

        self.setGeometry(300, 300, 500, 800)
        self.setMaximumSize(500, 800) #x, y

        parentMenu = self.menuBar()
        fileMenu = QtWidgets.QMenu("File")
        fileMenuAction = fileMenu.addAction("Save (e)", myWidgetVar.parentSaveFunc)
        fileMenuAction = fileMenu.addAction("Load (e)")

        deleteMenu = QtWidgets.QMenu("Delete")
        deleteCountryAction = deleteMenu.addAction("Delete Country", myWidgetVar.notebook.deleteTab)
        deleteFeatureAction = deleteMenu.addAction("Delete Feature", myWidgetVar.notebook.deleteTreeWidget)

        parentMenu.addMenu(fileMenu)
        parentMenu.addMenu(deleteMenu)

        self.setCentralWidget(myWidgetVar)

class DescWindow(QtWidgets.QMainWindow):

    def isUniq(self, text, listToSrch):
        for ea in listToSrch:
            if text == ea.uName:
                return False
        return True

    @QtCore.Slot()
    def uNameChange(self):
        text = self.w.nameChanger.nameChangeEdit.text()
        if text.replace(" ", "") is "":
            return
        if self.clas.type == "c":
            if self.isUniq(text, self.country.cNB.countries):
                self.country.cNB.notebook.setTabText(self.CI, text)
                self.clas.uName = text
        elif self.clas.type == "ls":
            if self.isUniq(text, self.country.children):
                self.clas.setText(0, text)
                self.setWindowTitle(self.clas.type+" - "+text)
                self.clas.uName = text
        else:
            if self.isUniq(text, self.currItem.parent().children):
                self.clas.setText(0, text)
                self.setWindowTitle(self.clas.type+" - "+text)
                self.clas.uName = text

    def __init__(self, clas, country, countryIndex):
        super().__init__()
        self.setGeometry(350,350, 400,600)
        self.setMaximumSize(400,600)
        self.clas = clas
        self.country = country
        self.CI = countryIndex
        print(clas)

        if countryIndex >= 0:
            self.w = DescriptorClasses.CountryDesc(self.country)
            self.cw = self.setCentralWidget(self.w)
            self.clas = self.country
            self.uName = self.clas.uName
            self.setWindowTitle("Country - "+self.clas.uName)
        else:
            self.currItem = country.tree.currentItem()

            if clas.type == "ls":
                self.w = DescriptorClasses.LandscapeDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("ls - "+clas.uName)
            elif clas.type == "np":
                self.w = DescriptorClasses.NotablePlaceDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("np - "+clas.uName)
            elif clas.type == "t":
                self.w = DescriptorClasses.TownDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("t - "+clas.uName)
            elif clas.type == "dw":
                self.w = DescriptorClasses.DwellingDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("dw - "+clas.uName)
            elif clas.type == "p":
                self.w = DescriptorClasses.PersonDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("p - "+clas.uName)
            elif clas.type == "m":
                self.w = DescriptorClasses.MonsterDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("m - "+clas.uName)
            elif clas.type == "i":
                self.w = DescriptorClasses.ItemDesc(self.clas)
                self.cw = self.setCentralWidget(self.w)
                self.setWindowTitle("i - "+clas.uName)
            self.uName = self.clas.uName

        self.w.nameChanger.nameChangeEdit.setPlaceholderText(self.clas.uName)
        self.w.nameChanger.nameChangeEdit.returnPressed.connect(self.uNameChange)
        self.show()

app = QtWidgets.QApplication(sys.argv)

myWindow = MainWindow()
myWindow.show()

sys.exit(app.exec_())
