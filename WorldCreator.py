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

        self.featureChoices.addItem("Landscape")

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

    def currSelection(self):
        return self.notebook.currentWidget()

    def isUniq(self, text):
        for clas in self.countries:
            if text == clas.uName:
                return False
        return True

    @QtCore.Slot()
    def changeSelection(self):
        a = self.currSelection()
        try:
            self.countryDetInfoField.setPlainText(a.countryDetInfo)
            print("New Selection :"+a.uName)
        except AttributeError:
            print("Nothing to select")

    @QtCore.Slot()
    def saveDetInfo(self):
        a = self.currSelection()
        if a == None:
            return
        a.countryDetInfo = self.countryDetInfoField.toPlainText()

    @QtCore.Slot()
    def createTreeWidget(self):
        print("User wants to create a TreeWidget!")

    def deleteTreeWidget(self):
        print("User wants to delete a TreeWidget!")

    @QtCore.Slot()
    def createTab(self):
        text = self.countryCreateGroup.countryNameField.text()
        isTextUniq = self.isUniq(text.lower())
        if text.replace(" ", "") is "":
            return
        if isTextUniq == False:
            return
        a = CountryTab(text.lower())
        b = self.currSelection()
        self.notebook.addTab(a, text)
        self.countries.append(a)
        if b == None:
            self.countryDetInfoField.setReadOnly(False)

    @QtCore.Slot()
    def deleteTab(self):
        a = self.currSelection()
        if a == None:
            return
        b = self.countries.index(a)
        self.notebook.removeTab(b)
        del self.countries[b]
        a = self.currSelection()
        if a == None:
            self.countryDetInfoField.setReadOnly(True)
            self.countryDetInfoField.clear()

    def __init__(self, parent=None):
        super().__init__()

        self.countries = []
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

        self.connect(self.countryCreateGroup.countryCreateButton, QtCore.SIGNAL("released()"), self.createTab)
        self.connect(self.countryCreateGroup.countryDeleteButton, QtCore.SIGNAL("released()"), self.deleteTab)
        self.connect(self.featureCreateGroup.featureCreateButton, QtCore.SIGNAL("released()"), self.createTreeWidget)
        self.connect(self.featureCreateGroup.featureDeleteButton, QtCore.SIGNAL("released()"), self.deleteTreeWidget)
        self.connect(self.notebook, QtCore.SIGNAL("currentChanged(int)"), self.changeSelection)
        self.connect(self.countryDetInfoField, QtCore.SIGNAL("textChanged()"), self.saveDetInfo)

class CountryTab(QtWidgets.QWidget):
    def __init__(self, name, parent=None):
        super().__init__()

        self.uName = name
        self.countryDetInfo = ""

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name","Type"])

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)


class Landscape(QtWidgets.QTreeWidgetItem):
    def __init__(self, uName, Parent=None):
        super().__init__()

        self.uName = ""
        self.detInfo = ""
        self.children = []


class BaseInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

class BuildingInfo(BaseInfo):
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

        # self.connect(self.notebook.notebook, QtCore.SIGNAL("currentChanged(int)"), self.changeSelection)


app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()
widget.setGeometry(300, 300, 500, 750)
widget.setMaximumSize(500, 750) #x, y
widget.show()

sys.exit(app.exec_())
