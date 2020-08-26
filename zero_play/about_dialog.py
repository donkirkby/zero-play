# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 400)
        Dialog.setSizeGripEnabled(False)
        self.main_layout = QVBoxLayout(Dialog)
        self.main_layout.setObjectName(u"main_layout")
        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.credits_list = QWidget()
        self.credits_list.setObjectName(u"credits_list")
        self.credits_list.setGeometry(QRect(0, 0, 480, 349))
        self.credits_layout = QGridLayout(self.credits_list)
        self.credits_layout.setObjectName(u"credits_layout")
        self.version_label = QLabel(self.credits_list)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.credits_layout.addWidget(self.version_label, 0, 0, 1, 1)

        self.version = QLabel(self.credits_list)
        self.version.setObjectName(u"version")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.version.sizePolicy().hasHeightForWidth())
        self.version.setSizePolicy(sizePolicy)

        self.credits_layout.addWidget(self.version, 0, 1, 1, 1)

        self.scrollArea.setWidget(self.credits_list)

        self.main_layout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.main_layout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About Zero Play", None))
        self.version_label.setText(QCoreApplication.translate("Dialog", u"Version:", None))
        self.version.setText(QCoreApplication.translate("Dialog", u"0.0", None))
    # retranslateUi

