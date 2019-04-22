import sys, json
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

    @QtCore.Slot()
    def treeSelectionChanged(self):
        try:
            currCountry = self.currCountrySelection()
            currItem = currCountry.tree.currentItem()
            # currCountry.detInfoField.setPlainText(currItem.detInfo)

            # if currItem:
                # currCountry.detInfoField.setReadOnly(False)
            self.featureCreateGroup.featureChoices.removeItem(1)
            self.featureCreateGroup.featureChoices.removeItem(1)
            self.featureCreateGroup.featureChoices.removeItem(1)
            for ea in currItem.possibleChildren:
                self.featureCreateGroup.featureChoices.addItem(ea[0], ea[1])
        except:
            self.featureCreateGroup.featureChoices.removeItem(1)
            self.featureCreateGroup.featureChoices.removeItem(1)
            self.featureCreateGroup.featureChoices.removeItem(1)

    @QtCore.Slot()
    def changeCountrySelection(self):
        try:
            oldSelection = self.currentTab
            self.currentTab = self.currCountrySelection()
            try:
                oldSelection.tree.itemSelectionChanged.disconnect(self.treeSelectionChanged)
            except:
                pass
            self.currentTab.tree.itemSelectionChanged.connect(self.treeSelectionChanged)
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
        currItem = currCountry.tree.currentItem() #Get current Widget Selected
        if currCountry is None:
            return #If there's no country break out! We can't make a feature with no home!
        if text.replace(" ", "") is "":
            return #The only thing in the name is spaces, NO FEATURE FOR YOU
        if choiceStr == "ls": #Make a landscape
            if self.isUniq(text, currCountry.landscapes):
                c = Landscape(text)
                currCountry.tree.addTopLevelItem(c)
                currCountry.landscapesHelper.append(text)
                currCountry.landscapes.append(c)
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
                a = currCountry.landscapesHelper.index(currItem.uName)
                del currCountry.landscapesHelper[a]
                del currCountry.landscapes[a]
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
            a = CountryTab(text)
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

    def __init__(self, name, parent=None):
        super().__init__()

        self.uName = name
        self.landscapes = []
        self.landscapesHelper = []

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name","Type"])
        # self.detInfoField = QtWidgets.QPlainTextEdit()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tree)
        # self.layout.addWidget(self.detInfoField)
        # self.detInfoField.setReadOnly(True)
        self.setLayout(self.layout)

        # self.detInfoField.textChanged.connect(self.saveDetInfo)

class treeObject(QtWidgets.QTreeWidgetItem):
    def __init__(self, Parent=None):
        super().__init__()

        self.uName = ""
        self.detInfo = ""
        self.children = []
        self.childrenHelper = []
        self.possibleChildren = []

class Landscape(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Notable Place", "np"], ["Town", "t"]]
        self.uName = name
        self.setText(0, name)
        self.setText(1, "Landscape")

class NotablePlace(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Person", "p"], ["Monster", "m"], ["Item", "i"]]
        self.uName = name
        self.setText(0, name)
        self.setText(1, "Notable Place")

class Town(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Dwelling", "dw"], ["Notable Place", "np"]]
        self.uName = name
        self.setText(0, name)
        self.setText(1, "Town")

class Dwelling(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Person", "p"], ["Monster", "m"], ["Item", "i"]]
        self.uName = name
        self.setText(0, name)
        self.setText(1, "Dwelling")

class Person(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.setText(0, name)
        self.setText(1, "Person")

class Monster(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.setText(0, name)
        self.setText(1, "Monster")

class Item(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.uName = name
        self.setText(0, name)
        self.setText(1, "Item")

class MyWidget(QtWidgets.QWidget):

    def saveCountry(self, country):
        ret = []
        ret.append(country.uName)
        ret.append(len(country.landscapes))
        print(ret)

    def saveNotablePlace(np):
        pass
    def saveTown(town):
        pass
    def saveDwelling(dwelling):
        pass
    def savePerson(person):
        pass
    def saveMonster(monster):
        pass
    def saveItem(item):
        pass


    @QtCore.Slot()
    def parentSaveFunc(self):
        print("Trying to save")
        countries = self.notebook.countries
        if len(countries) == 0:
            print("Nothing to save!")
            return
# We will be parsing through each country to find landscapes.
        for eaCou in countries:
            parentSaveInfo = {eaCou.uName : []}
            self.saveCountry(eaCou)
            if len(eaCou.landscapes) == 0:
                print("There are no landscapes in this country.")
    # And now each landscape to find towns/notable places
            else:
                for eaLand in eaCou.landscapes:
                    if len(eaLand.children) == 0:
                        print("There are no children in this landscape.")
        # And now each child of the landscape, to see if it's a notable place
                    else:
                        for eaTNP in eaLand.children:
                            if isinstance(eaTNP, type(NotablePlace(""))):
                                print("This is a Notable Place!")
            # And now each child of the notable place to see if it has children.
                                if len(eaTNP.children) == 0:
                                    print("There are no children in this Notable Place.")
                                else:
                    # And now each child of the notable place to see if it has children.
                                    for eaChil in eaTNP.children:
                                        if isinstance(eaChil, type(Person(""))):
                                            print("There is a Person in this Notable place!")
                    # And now save the Person info.
                                        elif isinstance(eaChil, type(Monster(""))):
                                            print("There is a Monster in this Notable place!")
                    # And now save the Monster info
                                        elif isinstance(eaChil, type(Item(""))):
                                            print("There is an Item in this Notable place!")
                    # And now save the Item info
        # And now each child of the landscape, to see if it's a town
                            elif isinstance(eaTNP, type(Town(""))):
                                print("This is a town!")
            # And now each child of the town to see if it has children
                                if len(eaTNP.children) == 0:
                                    print("There are no children in this Town.")

                                    for eaChil in eaTNP.children:
                                        if isinstance(eaChil, type(Dwelling(""))):
                                            if len(eaChil.children) == 0:
                                                print("There are no children in this town.")
                                            else:
                                                for eaDw in eaChil.children:
                                                    if isinstance(eaChil, type(Person(""))):
                                                        print("There is a Person in this Notable place!")
                                                        # And now save the Person info.
                                                    elif isinstance(eaChil, type(Monster(""))):
                                                        print("There is a Monster in this Notable place!")
                                                        # And now save the Monster info
                                                    elif isinstance(eaChil, type(Item(""))):
                                                        print("There is an Item in this Notable place!")
                                                        # And now save the Item info

                                        elif isinstance(eaChil, type(NotablePlace(""))):
                                            if len(eaChil.children) == 0:
                                                print("There are no children in this NotablePlace")
                                            else:
                                                for eaNP in eaChil.children:
                                                    if isinstance(eaChil, type(Person(""))):
                                                        print("There is a Person in this Town!")
                                                        # And now save the Person info.
                                                    elif isinstance(eaChil, type(Monster(""))):
                                                        print("There is a Monster in this Town!")
                                                        # And now save the Monster info
                                                    elif isinstance(eaChil, type(Item(""))):
                                                        print("There is an Item in this Town!")
                                                        # And now save the Item info


    def __init__(self, parent=None):
        super().__init__()

        self.notebook = CountryNotebook()
        self.middleLayout = QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.notebook)

        self.parentGridLayout = QtWidgets.QGridLayout()
        self.parentGridLayout.addLayout(self.middleLayout, 0,0)
        self.setLayout(self.parentGridLayout)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        myWidgetVar = MyWidget()

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


app = QtWidgets.QApplication(sys.argv)

myWindow = MainWindow()
myWindow.setGeometry(300, 300, 500, 750)
myWindow.setMaximumSize(1920, 1080) #x, y
myWindow.show()

sys.exit(app.exec_())
