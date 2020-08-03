# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(911, 607)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        self.action_comparison = QAction(MainWindow)
        self.action_comparison.setObjectName(u"action_comparison")
        self.action_plot = QAction(MainWindow)
        self.action_plot.setObjectName(u"action_plot")
        self.action_training_session = QAction(MainWindow)
        self.action_training_session.setObjectName(u"action_training_session")
        self.action_game = QAction(MainWindow)
        self.action_game.setObjectName(u"action_game")
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stacked_widget = QStackedWidget(self.centralwidget)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.game_page = QWidget()
        self.game_page.setObjectName(u"game_page")
        self.tic_tac_toe = QPushButton(self.game_page)
        self.tic_tac_toe.setObjectName(u"tic_tac_toe")
        self.tic_tac_toe.setGeometry(QRect(10, 10, 141, 101))
        self.connect4 = QPushButton(self.game_page)
        self.connect4.setObjectName(u"connect4")
        self.connect4.setGeometry(QRect(170, 10, 141, 101))
        self.othello = QPushButton(self.game_page)
        self.othello.setObjectName(u"othello")
        self.othello.setGeometry(QRect(330, 10, 141, 101))
        self.stacked_widget.addWidget(self.game_page)
        self.players_page = QWidget()
        self.players_page.setObjectName(u"players_page")
        self.verticalLayout = QVBoxLayout(self.players_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.network1 = QPushButton(self.players_page)
        self.network1.setObjectName(u"network1")

        self.gridLayout.addWidget(self.network1, 3, 1, 1, 1)

        self.start = QPushButton(self.players_page)
        self.start.setObjectName(u"start")

        self.gridLayout.addWidget(self.start, 6, 1, 1, 1)

        self.label = QLabel(self.players_page)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.player1 = QComboBox(self.players_page)
        self.player1.setObjectName(u"player1")

        self.gridLayout.addWidget(self.player1, 2, 1, 1, 1)

        self.cancel = QPushButton(self.players_page)
        self.cancel.setObjectName(u"cancel")

        self.gridLayout.addWidget(self.cancel, 6, 0, 1, 1)

        self.game_label_2 = QLabel(self.players_page)
        self.game_label_2.setObjectName(u"game_label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_label_2.sizePolicy().hasHeightForWidth())
        self.game_label_2.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.game_label_2, 2, 0, 1, 1)

        self.game_name = QLabel(self.players_page)
        self.game_name.setObjectName(u"game_name")

        self.gridLayout.addWidget(self.game_name, 0, 1, 1, 1)

        self.label_2 = QLabel(self.players_page)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.player2 = QComboBox(self.players_page)
        self.player2.setObjectName(u"player2")

        self.gridLayout.addWidget(self.player2, 4, 1, 1, 1)

        self.lineEdit = QLineEdit(self.players_page)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.game_label = QLabel(self.players_page)
        self.game_label.setObjectName(u"game_label")
        sizePolicy.setHeightForWidth(self.game_label.sizePolicy().hasHeightForWidth())
        self.game_label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.game_label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.players_page)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.network2 = QPushButton(self.players_page)
        self.network2.setObjectName(u"network2")

        self.gridLayout.addWidget(self.network2, 5, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.stacked_widget.addWidget(self.players_page)
        self.display_page = QWidget()
        self.display_page.setObjectName(u"display_page")
        self.display_layout = QVBoxLayout(self.display_page)
        self.display_layout.setObjectName(u"display_layout")
        self.display_view = QGraphicsView(self.display_page)
        self.display_view.setObjectName(u"display_view")

        self.display_layout.addWidget(self.display_view)

        self.stacked_widget.addWidget(self.display_page)
        self.plot_page = QWidget()
        self.plot_page.setObjectName(u"plot_page")
        self.plot_layout = QVBoxLayout(self.plot_page)
        self.plot_layout.setObjectName(u"plot_layout")
        self.stacked_widget.addWidget(self.plot_page)

        self.verticalLayout_2.addWidget(self.stacked_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 911, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_new = QMenu(self.menu_file)
        self.menu_new.setObjectName(u"menu_new")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.menu_new.menuAction())
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_Save)
        self.menu_new.addAction(self.action_game)
        self.menu_new.addAction(self.action_comparison)
        self.menu_new.addAction(self.action_plot)
        self.menu_new.addAction(self.action_training_session)

        self.retranslateUi(MainWindow)

        self.stacked_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"&Open...", None))
        self.action_comparison.setText(QCoreApplication.translate("MainWindow", u"&Comparison", None))
        self.action_plot.setText(QCoreApplication.translate("MainWindow", u"&Plot", None))
        self.action_training_session.setText(QCoreApplication.translate("MainWindow", u"&Training Session", None))
        self.action_game.setText(QCoreApplication.translate("MainWindow", u"&Game", None))
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"&Save...", None))
        self.tic_tac_toe.setText(QCoreApplication.translate("MainWindow", u"Tic Tac Toe", None))
        self.connect4.setText(QCoreApplication.translate("MainWindow", u"Connect 4", None))
        self.othello.setText(QCoreApplication.translate("MainWindow", u"Othello", None))
        self.network1.setText(QCoreApplication.translate("MainWindow", u"Network 1...", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Player 2:", None))
        self.cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.game_label_2.setText(QCoreApplication.translate("MainWindow", u"Player 1:", None))
        self.game_name.setText(QCoreApplication.translate("MainWindow", u"Chosen Game's Name", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Description:", None))
        self.game_label.setText(QCoreApplication.translate("MainWindow", u"Game:", None))
        self.label_3.setText("")
        self.network2.setText(QCoreApplication.translate("MainWindow", u"Network 2...", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_new.setTitle(QCoreApplication.translate("MainWindow", u"&New", None))
    # retranslateUi

