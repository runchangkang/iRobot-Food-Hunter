# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'irobotView.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from controller.foodManager import FetchContentThread
class Ui_MainWindow(object):

	def setModel(self,model):
		self.model = model

	def setupUi(self, MainWindow):
		self.MainWindow = MainWindow
		self.MainWindow.setObjectName("FoodHunter")
		self.MainWindow.resize(632, 530)
		self.centralwidget = QtWidgets.QWidget(self.MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
		self.lineEdit.setGeometry(QtCore.QRect(30, 40, 201, 31))
		self.lineEdit.setClearButtonEnabled(True)
		self.lineEdit.setObjectName("lineEdit")
		self.lineEdit.returnPressed.connect(self.addAction)


		self.resultLabel = QtWidgets.QLabel(self.centralwidget)
		self.resultLabel.setGeometry(QtCore.QRect(430, 30, 57, 16))
		self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.resultLabel.setObjectName("resultLabel")

		self.inputHintLabel = QtWidgets.QLabel(self.centralwidget)
		self.inputHintLabel.setGeometry(QtCore.QRect(30, 20, 261, 16))
		self.inputHintLabel.setObjectName("inputHintLabel")

		self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
		self.textBrowser.setGeometry(QtCore.QRect(320, 50, 281, 391))
		self.textBrowser.setObjectName("textBrowser")


		self.listWidget = QtWidgets.QListWidget(self.centralwidget)
		self.listWidget.setAlternatingRowColors(True)
		self.listWidget.setGeometry(QtCore.QRect(30, 80, 261, 311))
		self.listWidget.setProperty("isWrapping", False)
		self.listWidget.setObjectName("listWidget")


		self.addBtn = QtWidgets.QPushButton(self.centralwidget)
		self.addBtn.setObjectName("addBtn")
		self.addBtn.setGeometry(QtCore.QRect(236, 35, 61, 41))
		self.addBtn.clicked.connect(self.addAction)

		self.searchBtn = QtWidgets.QPushButton(self.centralwidget)
		self.searchBtn.setObjectName("searchBtn")
		self.searchBtn.setGeometry(QtCore.QRect(25, 415, 281, 31))
		self.searchBtn.clicked.connect(self.searchAction)

		self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
		self.clearBtn.setObjectName("clearBtn")
		self.clearBtn.setGeometry(QtCore.QRect(26, 391, 111, 32))
		self.clearBtn.clicked.connect(self.clearAction)


		self.removeBtn = QtWidgets.QPushButton(self.centralwidget)
		self.removeBtn.setObjectName("removeBtn")
		self.removeBtn.setGeometry(QtCore.QRect(128, 391, 41, 32))


		self.removeBtn.clicked.connect(self.removeAction)

		self.MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self.MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 22))
		self.menubar.setObjectName("menubar")
		self.MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
		self.statusbar.setObjectName("statusbar")
		self.MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)

		self.thread = FetchContentThread(self.model)
		self.thread.result.connect(self.setFetchResult)
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

	def addAction(self):
		userInput = self.lineEdit.text()
		if userInput != "":
			self.model.addUserIngredients(userInput)

			self.reloadTable()
			self.lineEdit.clear()
			self.lineEdit.repaint()




	def reloadTable(self):
		self.listWidget.clear()
		for item in self.model.userInputIngredient:
			listItem = QtWidgets.QListWidgetItem(item,self.listWidget)

	def searchAction(self):
		self.textBrowser.setText("Processing..........")
		self.textBrowser.repaint()
		self.thread.start()

	def setFetchResult(self,isSuccess, existing,missing, message):
		if isSuccess:
			self.textBrowser.setText(message)
			self.textBrowser.append("Food Name: "+ self.model.recipe.title)
			self.textBrowser.append("=============================")
			self.textBrowser.append("The ingredients you've already have: ")
			self.textBrowser.append("=============================")
			self.textBrowser.append(existing)
			self.textBrowser.append("=============================")
			self.textBrowser.append("The ingredients you still need: ")
			self.textBrowser.append("=============================")
			self.textBrowser.append(missing)
		else:
			self.textBrowser.setText(message)



	def clearAction(self):
		self.model.clear()
		self.reloadTable()

	def removeAction(self):
		item = self.listWidget.takeItem(self.listWidget.currentRow())
		if not item:
			return
		itemName = item.text()
		self.model.remove(itemName)
		self.reloadTable()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		self.lineEdit.setPlaceholderText(_translate("FoodHunter", "ingredient name"))
		self.resultLabel.setText(_translate("FoodHunter", "Result"))
		self.inputHintLabel.setText(_translate("FoodHunter", "Please add ingredients, one at a time!"))
		self.textBrowser.setText(_translate("FoodHunter","please search!"))
		self.addBtn.setText(_translate("FoodHunter", "Add"))
		self.searchBtn.setText(_translate("FoodHunter", "Search"))
		self.clearBtn.setText(_translate("FoodHunter", "Clear"))
		self.removeBtn.setText(_translate("FoodHunter","-"))

