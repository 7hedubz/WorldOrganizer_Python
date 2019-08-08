# Country, Landscape, NotablePlace, Town, Dwelling, Person, Monster, Item
from PySide2 import QtGui, QtCore, QtWidgets

class ClimateAddChoice(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.climateAddField = QtWidgets.QLineEdit()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Add Climate Attribute : "))
        self.layout.addWidget(self.climateAddField)
        self.setLayout(self.layout)

class ClimateChoices(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.listChoices = QtWidgets.QListWidget()
        self.climateAdd = ClimateAddChoice()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Climate : "))
        self.layout.addWidget(self.listChoices)

        self.layout.addWidget(self.climateAdd)

        self.setLayout(self.layout)

class NameChange(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.nameChangeLabel = QtWidgets.QLabel("Name : ")
		self.nameChangeEdit = QtWidgets.QLineEdit()

		self.layout = QtWidgets.QHBoxLayout()
		self.layout.addWidget(self.nameChangeLabel)
		self.layout.addWidget(self.nameChangeEdit)
		#self.layout.addSpacing(175)

		self.setLayout(self.layout)

class genericDesc(QtWidgets.QWidget):
    def __init__(self):
       super().__init__()
       
       self.genDesc_QLabel = QtWidgets.QLabel("Description")
       self.genDesc_QPlainTextEdit = QtWidgets.QPlainTextEdit()
       
       self.layout = QtWidgets.QHBoxLayout()
       self.layout.addWidget(self.genDesc_QLabel)
       self.layout.addWidget(self.genDesc_QPlainTextEdit)
       
       self.setLayout(self.layout)
       
       
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
class MasterDesc(QtWidgets.QWidget):
        def __init__(self, flags="WA_DeleteOnClose()"):
            super().__init__()
            self.nameChanger = NameChange()
            self.genDes = genericDesc()

            self.layout = QtWidgets.QVBoxLayout()
            self.layout.addWidget(self.nameChanger)
            self.layout.addWidget(self.genDes)
            self.setLayout(self.layout)

class CountryDesc(MasterDesc):
        def __init__(self, country):
            super().__init__()

class LandscapeDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

            self.climateChoice = ClimateChoices()
            self.layout.addWidget(self.climateChoice)
            self.layout.addSpacing(500)

class NotablePlaceDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

class TownDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

class DwellingDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

class PersonDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

class MonsterDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

class ItemDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()
