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
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_view_game = QAction(MainWindow)
        self.action_view_game.setObjectName(u"action_view_game")
        self.action_view_game.setCheckable(True)
        self.action_view_game.setChecked(True)
        self.action_view_log = QAction(MainWindow)
        self.action_view_log.setObjectName(u"action_view_log")
        self.action_view_log.setCheckable(True)
        self.action_save_log = QAction(MainWindow)
        self.action_save_log.setObjectName(u"action_save_log")
        self.action_coordinates = QAction(MainWindow)
        self.action_coordinates.setObjectName(u"action_coordinates")
        self.action_coordinates.setCheckable(True)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stacked_widget = QStackedWidget(self.centralwidget)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.game_page = QWidget()
        self.game_page.setObjectName(u"game_page")
        self.gridLayout_3 = QGridLayout(self.game_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.connect4 = QPushButton(self.game_page)
        self.connect4.setObjectName(u"connect4")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect4.sizePolicy().hasHeightForWidth())
        self.connect4.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.connect4, 0, 1, 1, 1)

        self.tic_tac_toe = QPushButton(self.game_page)
        self.tic_tac_toe.setObjectName(u"tic_tac_toe")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tic_tac_toe.sizePolicy().hasHeightForWidth())
        self.tic_tac_toe.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.tic_tac_toe, 0, 0, 1, 1)

        self.othello = QPushButton(self.game_page)
        self.othello.setObjectName(u"othello")
        sizePolicy.setHeightForWidth(self.othello.sizePolicy().hasHeightForWidth())
        self.othello.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.othello, 1, 0, 1, 1)

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
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.game_label_2.sizePolicy().hasHeightForWidth())
        self.game_label_2.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.game_label_2, 2, 0, 1, 1)

        self.game_name = QLabel(self.players_page)
        self.game_name.setObjectName(u"game_name")

        self.gridLayout.addWidget(self.game_name, 0, 1, 1, 1)

        self.label_2 = QLabel(self.players_page)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.player2 = QComboBox(self.players_page)
        self.player2.setObjectName(u"player2")

        self.gridLayout.addWidget(self.player2, 4, 1, 1, 1)

        self.lineEdit = QLineEdit(self.players_page)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.game_label = QLabel(self.players_page)
        self.game_label.setObjectName(u"game_label")
        sizePolicy2.setHeightForWidth(self.game_label.sizePolicy().hasHeightForWidth())
        self.game_label.setSizePolicy(sizePolicy2)

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
        self.gridLayout_2 = QGridLayout(self.display_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.toggle_review = QPushButton(self.display_page)
        self.toggle_review.setObjectName(u"toggle_review")
        sizePolicy2.setHeightForWidth(self.toggle_review.sizePolicy().hasHeightForWidth())
        self.toggle_review.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.toggle_review, 4, 2, 1, 1)

        self.resume_here = QPushButton(self.display_page)
        self.resume_here.setObjectName(u"resume_here")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.resume_here.sizePolicy().hasHeightForWidth())
        self.resume_here.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.resume_here, 4, 0, 1, 1)

        self.choices = QTableWidget(self.display_page)
        self.choices.setObjectName(u"choices")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.choices.sizePolicy().hasHeightForWidth())
        self.choices.setSizePolicy(sizePolicy5)

        self.gridLayout_2.addWidget(self.choices, 2, 0, 1, 3)

        self.display_view = QGraphicsView(self.display_page)
        self.display_view.setObjectName(u"display_view")

        self.gridLayout_2.addWidget(self.display_view, 1, 0, 1, 3)

        self.move_history = QComboBox(self.display_page)
        self.move_history.setObjectName(u"move_history")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.move_history.sizePolicy().hasHeightForWidth())
        self.move_history.setSizePolicy(sizePolicy6)

        self.gridLayout_2.addWidget(self.move_history, 4, 1, 1, 1)

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
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_file.addAction(self.menu_new.menuAction())
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_log)
        self.menu_new.addAction(self.action_game)
        self.menu_new.addAction(self.action_comparison)
        self.menu_new.addAction(self.action_plot)
        self.menu_new.addAction(self.action_training_session)
        self.menu_view.addAction(self.action_coordinates)
        self.menu_Help.addAction(self.action_about)

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
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"&Save...", None))
        self.action_view_game.setText(QCoreApplication.translate("MainWindow", u"&Game", None))
        self.action_view_log.setText(QCoreApplication.translate("MainWindow", u"&Log", None))
        self.action_save_log.setText(QCoreApplication.translate("MainWindow", u"Save &Log...", None))
        self.action_coordinates.setText(QCoreApplication.translate("MainWindow", u"Coordinates", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"&About...", None))
        self.connect4.setText(QCoreApplication.translate("MainWindow", u"Connect 4", None))
        self.tic_tac_toe.setText(QCoreApplication.translate("MainWindow", u"Tic Tac Toe", None))
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
        self.toggle_review.setText(QCoreApplication.translate("MainWindow", u"Review / Resume", None))
        self.resume_here.setText(QCoreApplication.translate("MainWindow", u"Resume Here", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_new.setTitle(QCoreApplication.translate("MainWindow", u"&New", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
    # retranslateUi

