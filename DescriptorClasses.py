# Country, Landscape, NotablePlace, Town, Dwelling, Person, Monster, Item
from PySide2 import QtGui, QtCore, QtWidgets

class TempatureChoices(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tempChoices = QtWidgets.QComboBox()

class NameChange(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()

            self.nameChangeLabel = QtWidgets.QLabel("Name : ")
            self.nameChangeEdit = QtWidgets.QLineEdit()

            self.layout = QtWidgets.QHBoxLayout()


class MasterDesc(QtWidgets.QWidget):
        def __init__(self, flags="WA_DeleteOnClose()"):
            super().__init__()
            self.nameChanger = NameChange()

            self.layout = QtWidgets.QVBoxLayout()
            self.layout.addWidget(self.nameChanger)
            self.setLayout(self.layout)


class CountryDesc(MasterDesc):
        def __init__(self, country):
            super().__init__()

class LandscapeDesc(MasterDesc):
        def __init__(self, clas):
            super().__init__()

            self.layout.addWidget(TempatureChoices())

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
