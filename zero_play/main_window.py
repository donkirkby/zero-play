# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui',
# licensing of 'main_window.ui' applies.
#
# Created: Thu Nov 28 21:58:53 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(911, 607)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget.setObjectName("stacked_widget")
        self.game_page = QtWidgets.QWidget()
        self.game_page.setObjectName("game_page")
        self.tic_tac_toe = QtWidgets.QPushButton(self.game_page)
        self.tic_tac_toe.setGeometry(QtCore.QRect(10, 10, 141, 101))
        self.tic_tac_toe.setObjectName("tic_tac_toe")
        self.connect4 = QtWidgets.QPushButton(self.game_page)
        self.connect4.setGeometry(QtCore.QRect(170, 10, 141, 101))
        self.connect4.setObjectName("connect4")
        self.othello = QtWidgets.QPushButton(self.game_page)
        self.othello.setGeometry(QtCore.QRect(330, 10, 141, 101))
        self.othello.setObjectName("othello")
        self.stacked_widget.addWidget(self.game_page)
        self.players_page = QtWidgets.QWidget()
        self.players_page.setObjectName("players_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.players_page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.network1 = QtWidgets.QPushButton(self.players_page)
        self.network1.setObjectName("network1")
        self.gridLayout.addWidget(self.network1, 3, 1, 1, 1)
        self.start = QtWidgets.QPushButton(self.players_page)
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.players_page)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.player1 = QtWidgets.QComboBox(self.players_page)
        self.player1.setObjectName("player1")
        self.gridLayout.addWidget(self.player1, 2, 1, 1, 1)
        self.cancel = QtWidgets.QPushButton(self.players_page)
        self.cancel.setObjectName("cancel")
        self.gridLayout.addWidget(self.cancel, 6, 0, 1, 1)
        self.game_label_2 = QtWidgets.QLabel(self.players_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_label_2.sizePolicy().hasHeightForWidth())
        self.game_label_2.setSizePolicy(sizePolicy)
        self.game_label_2.setObjectName("game_label_2")
        self.gridLayout.addWidget(self.game_label_2, 2, 0, 1, 1)
        self.game_name = QtWidgets.QLabel(self.players_page)
        self.game_name.setObjectName("game_name")
        self.gridLayout.addWidget(self.game_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.players_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.player2 = QtWidgets.QComboBox(self.players_page)
        self.player2.setObjectName("player2")
        self.gridLayout.addWidget(self.player2, 4, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.players_page)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.game_label = QtWidgets.QLabel(self.players_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_label.sizePolicy().hasHeightForWidth())
        self.game_label.setSizePolicy(sizePolicy)
        self.game_label.setObjectName("game_label")
        self.gridLayout.addWidget(self.game_label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.players_page)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.network2 = QtWidgets.QPushButton(self.players_page)
        self.network2.setObjectName("network2")
        self.gridLayout.addWidget(self.network2, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.stacked_widget.addWidget(self.players_page)
        self.display_page = QtWidgets.QWidget()
        self.display_page.setObjectName("display_page")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.display_page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 801, 581))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.display_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        self.display_layout.setObjectName("display_layout")
        self.stacked_widget.addWidget(self.display_page)
        self.verticalLayout_2.addWidget(self.stacked_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 911, 22))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_new = QtWidgets.QMenu(self.menu_file)
        self.menu_new.setObjectName("menu_new")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_comparison = QtWidgets.QAction(MainWindow)
        self.action_comparison.setObjectName("action_comparison")
        self.action_plot = QtWidgets.QAction(MainWindow)
        self.action_plot.setObjectName("action_plot")
        self.action_training_session = QtWidgets.QAction(MainWindow)
        self.action_training_session.setObjectName("action_training_session")
        self.action_game = QtWidgets.QAction(MainWindow)
        self.action_game.setObjectName("action_game")
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.menu_new.addAction(self.action_game)
        self.menu_new.addAction(self.action_comparison)
        self.menu_new.addAction(self.action_plot)
        self.menu_new.addAction(self.action_training_session)
        self.menu_file.addAction(self.menu_new.menuAction())
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_Save)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        self.stacked_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.tic_tac_toe.setText(QtWidgets.QApplication.translate("MainWindow", "Tic Tac Toe", None, -1))
        self.connect4.setText(QtWidgets.QApplication.translate("MainWindow", "Connect 4", None, -1))
        self.othello.setText(QtWidgets.QApplication.translate("MainWindow", "Othello", None, -1))
        self.network1.setText(QtWidgets.QApplication.translate("MainWindow", "Network 1...", None, -1))
        self.start.setText(QtWidgets.QApplication.translate("MainWindow", "Start", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Player 2:", None, -1))
        self.cancel.setText(QtWidgets.QApplication.translate("MainWindow", "Cancel", None, -1))
        self.game_label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Player 1:", None, -1))
        self.game_name.setText(QtWidgets.QApplication.translate("MainWindow", "Chosen Game\'s Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Description:", None, -1))
        self.game_label.setText(QtWidgets.QApplication.translate("MainWindow", "Game:", None, -1))
        self.network2.setText(QtWidgets.QApplication.translate("MainWindow", "Network 2...", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("MainWindow", "&File", None, -1))
        self.menu_new.setTitle(QtWidgets.QApplication.translate("MainWindow", "&New", None, -1))
        self.action_open.setText(QtWidgets.QApplication.translate("MainWindow", "&Open...", None, -1))
        self.action_comparison.setText(QtWidgets.QApplication.translate("MainWindow", "&Comparison", None, -1))
        self.action_plot.setText(QtWidgets.QApplication.translate("MainWindow", "&Plot", None, -1))
        self.action_training_session.setText(QtWidgets.QApplication.translate("MainWindow", "&Training Session", None, -1))
        self.action_game.setText(QtWidgets.QApplication.translate("MainWindow", "&Game", None, -1))
        self.action_Save.setText(QtWidgets.QApplication.translate("MainWindow", "&Save...", None, -1))

