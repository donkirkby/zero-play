# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout,
    QWidget)

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
        self.action_strength_test = QAction(MainWindow)
        self.action_strength_test.setObjectName(u"action_strength_test")
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
        self.humans_page = QWidget()
        self.humans_page.setObjectName(u"humans_page")
        self.gridLayout = QGridLayout(self.humans_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.close_humans = QPushButton(self.humans_page)
        self.close_humans.setObjectName(u"close_humans")
        sizePolicy4.setHeightForWidth(self.close_humans.sizePolicy().hasHeightForWidth())
        self.close_humans.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.close_humans, 1, 1, 1, 1)

        self.players_label = QLabel(self.humans_page)
        self.players_label.setObjectName(u"players_label")

        self.gridLayout.addWidget(self.players_label, 0, 0, 1, 1)

        self.new_human = QPushButton(self.humans_page)
        self.new_human.setObjectName(u"new_human")
        sizePolicy4.setHeightForWidth(self.new_human.sizePolicy().hasHeightForWidth())
        self.new_human.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.new_human, 1, 3, 1, 1)

        self.players_table = QTableWidget(self.humans_page)
        self.players_table.setObjectName(u"players_table")

        self.gridLayout.addWidget(self.players_table, 0, 1, 1, 3)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.spacer, 1, 2, 1, 1)

        self.stacked_widget.addWidget(self.humans_page)
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

        self.gridLayout_2.addWidget(self.toggle_review, 3, 2, 1, 1)

        self.move_history = QComboBox(self.display_page)
        self.move_history.setObjectName(u"move_history")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.move_history.sizePolicy().hasHeightForWidth())
        self.move_history.setSizePolicy(sizePolicy6)

        self.gridLayout_2.addWidget(self.move_history, 3, 1, 1, 1)

        self.choices = QTableWidget(self.display_page)
        self.choices.setObjectName(u"choices")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.choices.sizePolicy().hasHeightForWidth())
        self.choices.setSizePolicy(sizePolicy7)

        self.gridLayout_2.addWidget(self.choices, 1, 0, 1, 3)

        self.resume_here = QPushButton(self.display_page)
        self.resume_here.setObjectName(u"resume_here")
        sizePolicy5.setHeightForWidth(self.resume_here.sizePolicy().hasHeightForWidth())
        self.resume_here.setSizePolicy(sizePolicy5)

        self.gridLayout_2.addWidget(self.resume_here, 3, 0, 1, 1)

        self.game_display = QLabel(self.display_page)
        self.game_display.setObjectName(u"game_display")

        self.gridLayout_2.addWidget(self.game_display, 0, 0, 1, 3)

        self.stacked_widget.addWidget(self.display_page)
        self.plot_strength_page = QWidget()
        self.plot_strength_page.setObjectName(u"plot_strength_page")
        self.gridLayout_5 = QGridLayout(self.plot_strength_page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.strength_count_label = QLabel(self.plot_strength_page)
        self.strength_count_label.setObjectName(u"strength_count_label")

        self.gridLayout_5.addWidget(self.strength_count_label, 6, 0, 1, 1)

        self.label_2 = QLabel(self.plot_strength_page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 3, 0, 1, 1)

        self.strength_test_game = QComboBox(self.plot_strength_page)
        self.strength_test_game.setObjectName(u"strength_test_game")

        self.gridLayout_5.addWidget(self.strength_test_game, 0, 1, 1, 2)

        self.reset_strength_test = QPushButton(self.plot_strength_page)
        self.reset_strength_test.setObjectName(u"reset_strength_test")

        self.gridLayout_5.addWidget(self.reset_strength_test, 6, 2, 1, 1)

        self.label = QLabel(self.plot_strength_page)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.strength_test_min = QSpinBox(self.plot_strength_page)
        self.strength_test_min.setObjectName(u"strength_test_min")
        self.strength_test_min.setMinimum(1)
        self.strength_test_min.setMaximum(1000000)

        self.gridLayout_5.addWidget(self.strength_test_min, 3, 1, 1, 2)

        self.start_strength_test = QPushButton(self.plot_strength_page)
        self.start_strength_test.setObjectName(u"start_strength_test")

        self.gridLayout_5.addWidget(self.start_strength_test, 6, 1, 1, 1)

        self.strengths_label = QLabel(self.plot_strength_page)
        self.strengths_label.setObjectName(u"strengths_label")

        self.gridLayout_5.addWidget(self.strengths_label, 2, 0, 1, 1)

        self.label_3 = QLabel(self.plot_strength_page)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_5.addWidget(self.label_3, 4, 0, 1, 1)

        self.strength_test_strengths = QLineEdit(self.plot_strength_page)
        self.strength_test_strengths.setObjectName(u"strength_test_strengths")

        self.gridLayout_5.addWidget(self.strength_test_strengths, 2, 1, 1, 2)

        self.strength_test_max = QSpinBox(self.plot_strength_page)
        self.strength_test_max.setObjectName(u"strength_test_max")
        self.strength_test_max.setMinimum(1)
        self.strength_test_max.setMaximum(1000000)
        self.strength_test_max.setValue(512)

        self.gridLayout_5.addWidget(self.strength_test_max, 4, 1, 1, 2)

        self.stacked_widget.addWidget(self.plot_strength_page)
        self.plot_strength_display_page = QWidget()
        self.plot_strength_display_page.setObjectName(u"plot_strength_display_page")
        self.gridLayout_7 = QGridLayout(self.plot_strength_display_page)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.stacked_widget.addWidget(self.plot_strength_display_page)
        self.plot_history_page = QWidget()
        self.plot_history_page.setObjectName(u"plot_history_page")
        self.gridLayout_6 = QGridLayout(self.plot_history_page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_4 = QLabel(self.plot_history_page)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)

        self.history_game = QComboBox(self.plot_history_page)
        self.history_game.setObjectName(u"history_game")

        self.gridLayout_6.addWidget(self.history_game, 0, 1, 1, 1)

        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 8)
        self.stacked_widget.addWidget(self.plot_history_page)

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
        self.menu_new.addAction(self.action_strength_test)
        self.menu_view.addAction(self.action_coordinates)
        self.menu_help.addAction(self.action_about)
        self.menu_help.addAction(self.menu_rules.menuAction())

        self.retranslateUi(MainWindow)

        self.stacked_widget.setCurrentIndex(5)


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
        self.action_save_log.setText(QCoreApplication.translate("MainWindow", u"Save &Log...", None))
        self.action_coordinates.setText(QCoreApplication.translate("MainWindow", u"Coordinates", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"&About...", None))
        self.action_new_db.setText(QCoreApplication.translate("MainWindow", u"New Player &Database...", None))
        self.action_open_db.setText(QCoreApplication.translate("MainWindow", u"&Open Player Database...", None))
        self.action_strength_test.setText(QCoreApplication.translate("MainWindow", u"&Strength Test", None))
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
        self.game_display.setText(QCoreApplication.translate("MainWindow", u"Game Display", None))
        self.strength_count_label.setText(QCoreApplication.translate("MainWindow", u"0 games recorded", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Opponent min:", None))
        self.reset_strength_test.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Game:", None))
        self.strength_test_min.setSuffix(QCoreApplication.translate("MainWindow", u" iteration(s)", None))
        self.start_strength_test.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.strengths_label.setText(QCoreApplication.translate("MainWindow", u"Player strengths:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Opponent max:", None))
#if QT_CONFIG(tooltip)
        self.strength_test_strengths.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.strength_test_strengths.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.strength_test_max.setSuffix(QCoreApplication.translate("MainWindow", u" iteration(s)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Game:", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_new.setTitle(QCoreApplication.translate("MainWindow", u"&New", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menu_rules.setTitle(QCoreApplication.translate("MainWindow", u"&Rules", None))
    # retranslateUi

