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
        self.action_open.setVisible(False)
        self.action_comparison = QAction(MainWindow)
        self.action_comparison.setObjectName(u"action_comparison")
        self.action_comparison.setVisible(False)
        self.action_plot = QAction(MainWindow)
        self.action_plot.setObjectName(u"action_plot")
        self.action_training_session = QAction(MainWindow)
        self.action_training_session.setObjectName(u"action_training_session")
        self.action_training_session.setVisible(False)
        self.action_game = QAction(MainWindow)
        self.action_game.setObjectName(u"action_game")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save.setVisible(False)
        self.action_view_game = QAction(MainWindow)
        self.action_view_game.setObjectName(u"action_view_game")
        self.action_view_game.setCheckable(True)
        self.action_view_game.setChecked(True)
        self.action_view_log = QAction(MainWindow)
        self.action_view_log.setObjectName(u"action_view_log")
        self.action_view_log.setCheckable(True)
        self.action_save_log = QAction(MainWindow)
        self.action_save_log.setObjectName(u"action_save_log")
        self.action_save_log.setVisible(False)
        self.action_coordinates = QAction(MainWindow)
        self.action_coordinates.setObjectName(u"action_coordinates")
        self.action_coordinates.setCheckable(True)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_new_db = QAction(MainWindow)
        self.action_new_db.setObjectName(u"action_new_db")
        self.action_open_db = QAction(MainWindow)
        self.action_open_db.setObjectName(u"action_open_db")
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
        self.player_layout = QGridLayout()
        self.player_layout.setObjectName(u"player_layout")
        self.searches_lock2 = QCheckBox(self.players_page)
        self.searches_lock2.setObjectName(u"searches_lock2")

        self.player_layout.addWidget(self.searches_lock2, 2, 4, 1, 1)

        self.player1 = QComboBox(self.players_page)
        self.player1.setObjectName(u"player1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.player1.sizePolicy().hasHeightForWidth())
        self.player1.setSizePolicy(sizePolicy2)

        self.player_layout.addWidget(self.player1, 1, 1, 1, 1)

        self.cancel = QPushButton(self.players_page)
        self.cancel.setObjectName(u"cancel")

        self.player_layout.addWidget(self.cancel, 4, 0, 1, 1)

        self.searches_label1 = QLabel(self.players_page)
        self.searches_label1.setObjectName(u"searches_label1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.searches_label1.sizePolicy().hasHeightForWidth())
        self.searches_label1.setSizePolicy(sizePolicy3)

        self.player_layout.addWidget(self.searches_label1, 1, 3, 1, 1)

        self.player2 = QComboBox(self.players_page)
        self.player2.setObjectName(u"player2")
        sizePolicy2.setHeightForWidth(self.player2.sizePolicy().hasHeightForWidth())
        self.player2.setSizePolicy(sizePolicy2)

        self.player_layout.addWidget(self.player2, 2, 1, 1, 1)

        self.searches_lock1 = QCheckBox(self.players_page)
        self.searches_lock1.setObjectName(u"searches_lock1")

        self.player_layout.addWidget(self.searches_lock1, 1, 4, 1, 1)

        self.game_label = QLabel(self.players_page)
        self.game_label.setObjectName(u"game_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.game_label.sizePolicy().hasHeightForWidth())
        self.game_label.setSizePolicy(sizePolicy4)

        self.player_layout.addWidget(self.game_label, 0, 0, 1, 1)

        self.game_name = QLabel(self.players_page)
        self.game_name.setObjectName(u"game_name")

        self.player_layout.addWidget(self.game_name, 0, 1, 1, 4)

        self.searches_label2 = QLabel(self.players_page)
        self.searches_label2.setObjectName(u"searches_label2")

        self.player_layout.addWidget(self.searches_label2, 2, 3, 1, 1)

        self.player_label1 = QLabel(self.players_page)
        self.player_label1.setObjectName(u"player_label1")
        sizePolicy4.setHeightForWidth(self.player_label1.sizePolicy().hasHeightForWidth())
        self.player_label1.setSizePolicy(sizePolicy4)

        self.player_layout.addWidget(self.player_label1, 1, 0, 1, 1)

        self.searches1 = QSpinBox(self.players_page)
        self.searches1.setObjectName(u"searches1")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.searches1.sizePolicy().hasHeightForWidth())
        self.searches1.setSizePolicy(sizePolicy5)
        self.searches1.setMaximum(1000000)

        self.player_layout.addWidget(self.searches1, 1, 2, 1, 1)

        self.player_label2 = QLabel(self.players_page)
        self.player_label2.setObjectName(u"player_label2")

        self.player_layout.addWidget(self.player_label2, 2, 0, 1, 1)

        self.shuffle_players = QCheckBox(self.players_page)
        self.shuffle_players.setObjectName(u"shuffle_players")

        self.player_layout.addWidget(self.shuffle_players, 3, 1, 1, 4)

        self.searches2 = QSpinBox(self.players_page)
        self.searches2.setObjectName(u"searches2")
        sizePolicy5.setHeightForWidth(self.searches2.sizePolicy().hasHeightForWidth())
        self.searches2.setSizePolicy(sizePolicy5)
        self.searches2.setMaximum(1000000)

        self.player_layout.addWidget(self.searches2, 2, 2, 1, 1)

        self.start = QPushButton(self.players_page)
        self.start.setObjectName(u"start")

        self.player_layout.addWidget(self.start, 4, 1, 1, 4)

        self.player_layout.setColumnStretch(1, 10)
        self.player_layout.setColumnStretch(2, 1)

        self.verticalLayout.addLayout(self.player_layout)

        self.stacked_widget.addWidget(self.players_page)
        self.history_page = QWidget()
        self.history_page.setObjectName(u"history_page")
        self.gridLayout = QGridLayout(self.history_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.close_humans = QPushButton(self.history_page)
        self.close_humans.setObjectName(u"close_humans")
        sizePolicy4.setHeightForWidth(self.close_humans.sizePolicy().hasHeightForWidth())
        self.close_humans.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.close_humans, 1, 1, 1, 1)

        self.players_label = QLabel(self.history_page)
        self.players_label.setObjectName(u"players_label")

        self.gridLayout.addWidget(self.players_label, 0, 0, 1, 1)

        self.new_human = QPushButton(self.history_page)
        self.new_human.setObjectName(u"new_human")
        sizePolicy4.setHeightForWidth(self.new_human.sizePolicy().hasHeightForWidth())
        self.new_human.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.new_human, 1, 3, 1, 1)

        self.tableWidget = QTableWidget(self.history_page)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 0, 1, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.stacked_widget.addWidget(self.history_page)
        self.rules_page = QWidget()
        self.rules_page.setObjectName(u"rules_page")
        self.gridLayout_4 = QGridLayout(self.rules_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.rules_text = QTextBrowser(self.rules_page)
        self.rules_text.setObjectName(u"rules_text")

        self.gridLayout_4.addWidget(self.rules_text, 0, 0, 1, 1)

        self.rules_close = QPushButton(self.rules_page)
        self.rules_close.setObjectName(u"rules_close")
        sizePolicy4.setHeightForWidth(self.rules_close.sizePolicy().hasHeightForWidth())
        self.rules_close.setSizePolicy(sizePolicy4)

        self.gridLayout_4.addWidget(self.rules_close, 1, 0, 1, 1)

        self.stacked_widget.addWidget(self.rules_page)
        self.display_page = QWidget()
        self.display_page.setObjectName(u"display_page")
        self.gridLayout_2 = QGridLayout(self.display_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.toggle_review = QPushButton(self.display_page)
        self.toggle_review.setObjectName(u"toggle_review")
        sizePolicy4.setHeightForWidth(self.toggle_review.sizePolicy().hasHeightForWidth())
        self.toggle_review.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.toggle_review, 4, 2, 1, 1)

        self.resume_here = QPushButton(self.display_page)
        self.resume_here.setObjectName(u"resume_here")
        sizePolicy5.setHeightForWidth(self.resume_here.sizePolicy().hasHeightForWidth())
        self.resume_here.setSizePolicy(sizePolicy5)

        self.gridLayout_2.addWidget(self.resume_here, 4, 0, 1, 1)

        self.choices = QTableWidget(self.display_page)
        self.choices.setObjectName(u"choices")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.choices.sizePolicy().hasHeightForWidth())
        self.choices.setSizePolicy(sizePolicy6)

        self.gridLayout_2.addWidget(self.choices, 2, 0, 1, 3)

        self.display_view = QGraphicsView(self.display_page)
        self.display_view.setObjectName(u"display_view")

        self.gridLayout_2.addWidget(self.display_view, 1, 0, 1, 3)

        self.move_history = QComboBox(self.display_page)
        self.move_history.setObjectName(u"move_history")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.move_history.sizePolicy().hasHeightForWidth())
        self.move_history.setSizePolicy(sizePolicy7)

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
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_rules = QMenu(self.menu_help)
        self.menu_rules.setObjectName(u"menu_rules")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.menu_new.menuAction())
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_log)
        self.menu_file.addAction(self.action_new_db)
        self.menu_file.addAction(self.action_open_db)
        self.menu_new.addAction(self.action_game)
        self.menu_new.addAction(self.action_comparison)
        self.menu_new.addAction(self.action_plot)
        self.menu_new.addAction(self.action_training_session)
        self.menu_view.addAction(self.action_coordinates)
        self.menu_help.addAction(self.action_about)
        self.menu_help.addAction(self.menu_rules.menuAction())

        self.retranslateUi(MainWindow)

        self.stacked_widget.setCurrentIndex(0)


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
        self.action_new_db.setText(QCoreApplication.translate("MainWindow", u"New Player &Database...", None))
        self.action_open_db.setText(QCoreApplication.translate("MainWindow", u"&Open Player Database...", None))
        self.connect4.setText(QCoreApplication.translate("MainWindow", u"Connect 4", None))
        self.tic_tac_toe.setText(QCoreApplication.translate("MainWindow", u"Tic Tac Toe", None))
        self.othello.setText(QCoreApplication.translate("MainWindow", u"Othello", None))
        self.searches_lock2.setText(QCoreApplication.translate("MainWindow", u"Lock", None))
        self.cancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.searches_label1.setText(QCoreApplication.translate("MainWindow", u"searches", None))
        self.searches_lock1.setText(QCoreApplication.translate("MainWindow", u"Lock", None))
        self.game_label.setText(QCoreApplication.translate("MainWindow", u"Game:", None))
        self.game_name.setText(QCoreApplication.translate("MainWindow", u"Chosen Game's Name", None))
        self.searches_label2.setText(QCoreApplication.translate("MainWindow", u"searches", None))
        self.player_label1.setText(QCoreApplication.translate("MainWindow", u"Player 1:", None))
        self.player_label2.setText(QCoreApplication.translate("MainWindow", u"Player 2:", None))
        self.shuffle_players.setText(QCoreApplication.translate("MainWindow", u"Shuffle Player Order", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.close_humans.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.players_label.setText(QCoreApplication.translate("MainWindow", u"Players", None))
        self.new_human.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.rules_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.toggle_review.setText(QCoreApplication.translate("MainWindow", u"Review / Resume", None))
        self.resume_here.setText(QCoreApplication.translate("MainWindow", u"Resume Here", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_new.setTitle(QCoreApplication.translate("MainWindow", u"&New", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menu_rules.setTitle(QCoreApplication.translate("MainWindow", u"&Rules", None))
    # retranslateUi

