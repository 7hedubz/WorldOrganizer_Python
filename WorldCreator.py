import sys
from PySide2 import QtGui, QtCore, QtWidgets



class AddCountry(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.countryNameField = QtWidgets.QLineEdit()
        self.countryCreateButton = QtWidgets.QPushButton("Create Country")
        self.countryDeleteButton = QtWidgets.QPushButton("Delete Country")

        #Set the layout var, add the widgets, apply the layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Country Name"))
        self.layout.addWidget(self.countryNameField)
        self.layout.addWidget(self.countryCreateButton)
        self.layout.addWidget(self.countryDeleteButton)
        self.layout.addSpacing(200)
        self.setLayout(self.layout)

class AddFeature(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.featureChoices = QtWidgets.QComboBox()
        self.featureNameField = QtWidgets.QLineEdit()
        self.featureCreateButton = QtWidgets.QPushButton("Create Feature")
        self.featureDeleteButton = QtWidgets.QPushButton("Delete Feature")

        self.featureChoices.addItem("Landscape", "ls")

        self.layout = QtWidgets.QHBoxLayout()
        # self.layout.addWidget(QtWidgets.QLabel("Feature Type"))
        self.layout.addWidget(self.featureChoices)
        self.layout.addWidget(QtWidgets.QLabel("Feature Name"))
        self.layout.addWidget(self.featureNameField)
        self.layout.addWidget(self.featureCreateButton)
        self.layout.addWidget(self.featureDeleteButton)
        self.layout.addSpacing(200)
        self.setLayout(self.layout)

class CountryNotebook(QtWidgets.QWidget):

    def currCountrySelection(self):
        return self.notebook.currentWidget()

    def isUniq(self, text, listToSrch):
        for clas in listToSrch:
            if text == clas.uName:
                return False
        return True

    @QtCore.Slot()
    def treeSelectionChanged(self):
        currCountry = self.currCountrySelection()
        currItem = currCountry.tree.currentItem()
        currCountry.detInfoField.setPlainText(currItem.detInfo)
        print("Tree selection changed in tab "+currCountry.uName+" to: "+str(currItem))
        if currItem:
            currCountry.detInfoField.setReadOnly(False)

    @QtCore.Slot()
    def changeCountrySelection(self):
        try:
            oldSelection = self.currentTab
            self.currentTab = self.currCountrySelection()
            self.countryDetInfoField.setPlainText(self.currentTab.countryDetInfo)
            try:
                oldSelection.tree.itemSelectionChanged.disconnect(self.treeSelectionChanged)
                print("Tree signal disconnected from previous owner: "+str(oldSelection.uName))
            except:
                pass
            self.currentTab.tree.itemSelectionChanged.connect(self.treeSelectionChanged)

            print("Tree signal connected to",self.currentTab.uName+"'s tree")
        except:
            pass

    @QtCore.Slot()
    def saveDetInfo(self):
        currCountry = self.currCountrySelection()
        if currCountry == None:
            return
        currCountry.countryDetInfo = self.countryDetInfoField.toPlainText()

    @QtCore.Slot()
    def createTreeWidget(self):
        choiceStr = self.featureCreateGroup.featureChoices.currentData() #Get's the string attached to the current choice eg. ls/np
        text = self.featureCreateGroup.featureNameField.text() #Get's the text for the features name
        currCountry = self.currCountrySelection() #Get's the currently selected country so that we make the widget in the right country
        if currCountry == None:
            return #If there's no country break out! We can't make a feature with no home!
        if text.replace(" ", "") is "":
            return #The only thing in the name is spaces, NO FEATURE FOR YOU
        if choiceStr == "ls": #Make a landscape
            if self.isUniq(text, currCountry.landscapes):
                c = Landscape(text)
                currCountry.tree.addTopLevelItem(c)
                currCountry.landscapes.append(c)
                print("created Landscape ",text)
        elif choiceStr == "np":
                print("created Notable Place ",text)
        if choiceStr == "t":
            pass
        if choiceStr == "dw":
            pass
        if choiceStr == "p":
            pass
        if choiceStr == "m":
            pass
        if choiceStr == "i":
            pass

    def deleteTreeWidget(self):
        print("User wants to delete a TreeWidget!")

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
            if currCountry == None:
                self.countryDetInfoField.setReadOnly(False)

    @QtCore.Slot()
    def deleteTab(self):
        currCountry = self.currCountrySelection()
        if currCountry == None:
            return
        currCountryIndex = self.countries.index(currCountry)
        self.notebook.removeTab(currCountryIndex)
        del self.countries[currCountryIndex]
        currCountry = self.currCountrySelection()
        if currCountry == None:
            self.countryDetInfoField.setReadOnly(True)
            self.countryDetInfoField.clear()

    def __init__(self, parent=None):
        super().__init__()

        self.countries = []
        self.currentTab = "" #Placeholder for future tab classes.
        self.notebook = QtWidgets.QTabWidget()
        self.countryDetInfoField = QtWidgets.QPlainTextEdit()
        self.countryCreateGroup = AddCountry()
        self.featureCreateGroup = AddFeature()


        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.countryCreateGroup)
        self.layout.addWidget(self.featureCreateGroup)
        self.layout.addWidget(self.notebook)
        self.layout.addWidget(self.countryDetInfoField)
        self.countryDetInfoField.setReadOnly(True)
        self.layout.addWidget(QtWidgets.QLabel("Country Information PlainTextEdit"))

        self.setLayout(self.layout)

        self.countryCreateGroup.countryCreateButton.released.connect(self.createTab)
        self.countryCreateGroup.countryDeleteButton.released.connect(self.deleteTab)
        self.featureCreateGroup.featureCreateButton.released.connect(self.createTreeWidget)
        self.featureCreateGroup.featureDeleteButton.released.connect(self.deleteTreeWidget)
        self.notebook.currentChanged.connect(self.changeCountrySelection)
        self.countryDetInfoField.textChanged.connect(self.saveDetInfo)

class CountryTab(QtWidgets.QWidget):

    @QtCore.Slot()
    def treeSelectionChanged(self):
        currItem = self.tree.currentItem()
        self.detInfoField.setPlainText(currItem.detInfo)

    @QtCore.Slot()
    def saveDetInfo(self):
        currItem = self.tree.currentItem()
        print(currItem.uName)
        currItem.detInfo = self.detInfoField.toPlainText()


    def __init__(self, name, parent=None):
        super().__init__()

        self.uName = name
        self.countryDetInfo = ""
        self.landscapes = []

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name","Type"])
        self.detInfoField = QtWidgets.QPlainTextEdit()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.detInfoField)
        self.detInfoField.setReadOnly(True)
        self.setLayout(self.layout)

        self.detInfoField.textChanged.connect(self.saveDetInfo)

class treeObject(QtWidgets.QTreeWidgetItem):
    def __init__(self, Parent=None):
        super().__init__()

        self.uName = ""
        self.detInfo = ""
        self.children = []
        self.possibleChildren = []

class Landscape(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possibleChildren = [["Notable Place", "np"], ["Town", "t"]]
        self.uName = name
        self.setText(0, name)
        self.setText(1, "Landscape")

class NotablePlace(treeObject):
    def __init__(self, parent=None):
        super().__init__()

class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.notebook = CountryNotebook()
        self.middleLayout = QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.notebook)

        self.parentGridLayout = QtWidgets.QGridLayout()
        self.parentGridLayout.addLayout(self.middleLayout, 0,0)
        self.setLayout(self.parentGridLayout)



app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()
widget.setGeometry(300, 300, 500, 750)
widget.setMaximumSize(500, 750) #x, y
widget.show()

sys.exit(app.exec_())
