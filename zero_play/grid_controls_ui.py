# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid_controls_ui.ui'
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

from zero_play.scaled_label import ScaledLabel


class Ui_GridControls(object):
    def setupUi(self, GridControls):
        if not GridControls.objectName():
            GridControls.setObjectName(u"GridControls")
        GridControls.resize(400, 300)
        self.grid_layout = QGridLayout(GridControls)
        self.grid_layout.setObjectName(u"grid_layout")
        self.game_display = QGraphicsView(GridControls)
        self.game_display.setObjectName(u"game_display")

        self.grid_layout.addWidget(self.game_display, 0, 0, 5, 1)

        self.black_count = ScaledLabel(GridControls)
        self.black_count.setObjectName(u"black_count")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.black_count.sizePolicy().hasHeightForWidth())
        self.black_count.setSizePolicy(sizePolicy)
        self.black_count.setScaledContents(True)
        self.black_count.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.black_count, 1, 1, 1, 1)

        self.black_count_pixmap = ScaledLabel(GridControls)
        self.black_count_pixmap.setObjectName(u"black_count_pixmap")
        sizePolicy.setHeightForWidth(self.black_count_pixmap.sizePolicy().hasHeightForWidth())
        self.black_count_pixmap.setSizePolicy(sizePolicy)
        self.black_count_pixmap.setScaledContents(True)
        self.black_count_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.black_count_pixmap, 0, 1, 1, 1)

        self.white_count_pixmap = ScaledLabel(GridControls)
        self.white_count_pixmap.setObjectName(u"white_count_pixmap")
        sizePolicy.setHeightForWidth(self.white_count_pixmap.sizePolicy().hasHeightForWidth())
        self.white_count_pixmap.setSizePolicy(sizePolicy)
        self.white_count_pixmap.setScaledContents(True)
        self.white_count_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.white_count_pixmap, 0, 2, 1, 1)

        self.white_count = ScaledLabel(GridControls)
        self.white_count.setObjectName(u"white_count")
        sizePolicy.setHeightForWidth(self.white_count.sizePolicy().hasHeightForWidth())
        self.white_count.setSizePolicy(sizePolicy)
        self.white_count.setScaledContents(True)
        self.white_count.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.white_count, 1, 2, 1, 1)

        self.player_pixmap = ScaledLabel(GridControls)
        self.player_pixmap.setObjectName(u"player_pixmap")
        sizePolicy.setHeightForWidth(self.player_pixmap.sizePolicy().hasHeightForWidth())
        self.player_pixmap.setSizePolicy(sizePolicy)
        self.player_pixmap.setScaledContents(True)
        self.player_pixmap.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)

        self.grid_layout.addWidget(self.player_pixmap, 2, 1, 1, 2)

        self.move_text = ScaledLabel(GridControls)
        self.move_text.setObjectName(u"move_text")
        sizePolicy.setHeightForWidth(self.move_text.sizePolicy().hasHeightForWidth())
        self.move_text.setSizePolicy(sizePolicy)
        self.move_text.setScaledContents(True)
        self.move_text.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.grid_layout.addWidget(self.move_text, 3, 1, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.grid_layout.addItem(self.verticalSpacer, 4, 1, 1, 2)

        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setRowStretch(2, 5)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setRowStretch(4, 5)
        self.grid_layout.setColumnStretch(0, 10)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)

        self.retranslateUi(GridControls)

        QMetaObject.connectSlotsByName(GridControls)
    # setupUi

    def retranslateUi(self, GridControls):
        GridControls.setWindowTitle(QCoreApplication.translate("GridControls", u"Form", None))
        self.black_count.setText(QCoreApplication.translate("GridControls", u"0", None))
        self.black_count_pixmap.setText(QCoreApplication.translate("GridControls", u"B", None))
        self.white_count_pixmap.setText(QCoreApplication.translate("GridControls", u"W", None))
        self.white_count.setText(QCoreApplication.translate("GridControls", u"0", None))
        self.player_pixmap.setText(QCoreApplication.translate("GridControls", u"Player", None))
        self.move_text.setText(QCoreApplication.translate("GridControls", u"to move", None))
    # retranslateUi

