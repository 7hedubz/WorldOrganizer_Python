# Country, Landscape, NotablePlace, Town, Dwelling, Person, Monster, Item
from PySide2 import QtGui, QtCore, QtWidgets


class MasterDesc(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__()

            self.nameChangeEdit = QtWidgets.QLineEdit()

            self.layout = QtWidgets.QGridLayout()
            self.layout.addWidget(QtWidgets.QLabel("Name : "), 0, 0)
            self.layout.addWidget(self.nameChangeEdit, 0, 1)

            self.setLayout(self.layout)

class CountryDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class LandscapeDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class NotablePlaceDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class TownDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class DwellingDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class PersonDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class MonsterDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()

class ItemDesc(MasterDesc):
        def __init__(self, parent=None):
            super().__init__()
