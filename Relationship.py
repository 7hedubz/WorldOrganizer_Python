from PySide2 import QtGui, QtCore, QtWidgets

class ShowWindow(QtWidgets.QWidget):

    def changeRelDesc(self, itemIndex):
        if len(self.clas.rels) != 0:
            self.currentItem = self.clas.rels[itemIndex]
            if self.relDesc_QPlainTextEdit.isReadOnly():
                self.relDesc_QPlainTextEdit.setReadOnly(False)
            self.relDesc_QPlainTextEdit.setPlainText(str(self.currentItem.relDesc))
            return
        self.relDesc_QPlainTextEdit.setPlainText("")
        self.relDesc_QPlainTextEdit.setReadOnly(True)

    def saveRelDesc(self):
        self.currentItem.relDesc = self.relDesc_QPlainTextEdit.toPlainText()

    def delRel(self):
        pass #Placeholder to delete Rels
    
    def showRels(self):
        for x in range(len(self.clas.rels)):
            a = self.relList_QListWidget.addItem(self.clas.rels[x].clas.uName)

    def __init__(self, clas, flags="WA_DeleteOnClose()"):
        super().__init__()
        
        self.clas = clas
        self.currentItem = ""
        
        
        self.relList_QListWidget = QtWidgets.QListWidget()
        self.relDel_QPushButton = QtWidgets.QPushButton("Delete Selection")
        self.relDesc_QPlainTextEdit = QtWidgets.QPlainTextEdit()
        self.relDesc_QPlainTextEdit.setReadOnly(True)
        

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.relDel_QPushButton, alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(self.relList_QListWidget)
        self.layout.addWidget(self.relDesc_QPlainTextEdit)
        
        self.relDesc_QPlainTextEdit.textChanged.connect(self.saveRelDesc)
        self.relList_QListWidget.currentRowChanged.connect(self.changeRelDesc)
        self.showRels()

        self.setLayout(self.layout)

class AddWindow(QtWidgets.QWidget):

    def parser(self, notebook):
        for eaCo in range(notebook.count()):
            curWid = notebook.widget(0)
            self.relNotebook.addTab(curWid, curWid.uName)

    def __init__(self, notebook, clas, flags="WA_DeleteOnClose()"):
        super().__init__()
        self.clas = clas

        self.relLabel_QLabel = QtWidgets.QLabel("Add Relation")
        self.orgNotebook = notebook.notebook
        self.relNotebook = QtWidgets.QTabWidget()

        self.parser(self.orgNotebook)
        
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.relLabel_QLabel)
        self.layout.addWidget(self.relNotebook)

        self.setLayout(self.layout)

class Target(QtWidgets.QListWidgetItem):
    def __init__(self, target, relDesc = ""):
        self.clas = target
        self.relDesc = relDesc
