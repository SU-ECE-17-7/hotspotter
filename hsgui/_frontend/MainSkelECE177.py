# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainSkel.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(826, 558)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(25, 25, 70))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.horizontalGroupBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalGroupBox.sizePolicy().hasHeightForWidth())
        self.horizontalGroupBox.setSizePolicy(sizePolicy)
        self.horizontalGroupBox.setMaximumSize(QtCore.QSize(1200, 90))
        self.horizontalGroupBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.horizontalGroupBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.horizontalGroupBox.setObjectName(_fromUtf8("horizontalGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(50, 0, 100, 0)
        self.horizontalLayout.setSpacing(100)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.PantheraLogo = QtGui.QLabel(self.horizontalGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PantheraLogo.sizePolicy().hasHeightForWidth())
        self.PantheraLogo.setSizePolicy(sizePolicy)
        self.PantheraLogo.setMaximumSize(QtCore.QSize(150, 75))
        self.PantheraLogo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.PantheraLogo.setText(_fromUtf8(""))
        self.PantheraLogo.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../Panthera logo & branding_internal only/Panthera Logos/Logo_DarkBackgrounds.png")))
        self.PantheraLogo.setScaledContents(True)
        self.PantheraLogo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PantheraLogo.setWordWrap(True)
        self.PantheraLogo.setObjectName(_fromUtf8("PantheraLogo"))
        self.horizontalLayout.addWidget(self.PantheraLogo)
        self.label = QtGui.QLabel(self.horizontalGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(75, 75))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("hsicon.ico")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.horizontalGroupBox)
        self.label_2.setMaximumSize(QtCore.QSize(175, 60))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../Downloads/SeattleUMain-red-background.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.horizontalGroupBox)
        self.TableTabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TableTabWidget.sizePolicy().hasHeightForWidth())
        self.TableTabWidget.setSizePolicy(sizePolicy)
        self.TableTabWidget.setMaximumSize(QtCore.QSize(16777215, 1200))
        self.TableTabWidget.setTabsClosable(False)
        self.TableTabWidget.setObjectName(_fromUtf8("TableTabWidget"))
        self.imageTab = QtGui.QWidget()
        self.imageTab.setObjectName(_fromUtf8("imageTab"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.imageTab)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.imageView = QtGui.QVBoxLayout()
        self.imageView.setObjectName(_fromUtf8("imageView"))
        self.gxs_TBL = QtGui.QTableWidget(self.imageTab)
        self.gxs_TBL.setObjectName(_fromUtf8("gxs_TBL"))
        self.gxs_TBL.setColumnCount(0)
        self.gxs_TBL.setRowCount(0)
        self.imageView.addWidget(self.gxs_TBL)
        self.verticalLayout_6.addLayout(self.imageView)
        self.horizontalGroupBox1 = QtGui.QGroupBox(self.imageTab)
        self.horizontalGroupBox1.setObjectName(_fromUtf8("horizontalGroupBox1"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalGroupBox1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.pushButton = QtGui.QPushButton(self.horizontalGroupBox1)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.horizontalGroupBox1)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.AutoChip = QtGui.QPushButton(self.horizontalGroupBox1)
        self.AutoChip.setObjectName(_fromUtf8("AutoChip"))
        self.horizontalLayout_4.addWidget(self.AutoChip)
        self.verticalLayout_6.addWidget(self.horizontalGroupBox1)
        self.TableTabWidget.addTab(self.imageTab, _fromUtf8(""))
        self.chipTab = QtGui.QWidget()
        self.chipTab.setObjectName(_fromUtf8("chipTab"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.chipTab)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.chipView = QtGui.QVBoxLayout()
        self.chipView.setObjectName(_fromUtf8("chipView"))
        self.cxs_TBL = QtGui.QTableWidget(self.chipTab)
        self.cxs_TBL.setObjectName(_fromUtf8("cxs_TBL"))
        self.cxs_TBL.setColumnCount(0)
        self.cxs_TBL.setRowCount(0)
        self.chipView.addWidget(self.cxs_TBL)
        self.verticalLayout_7.addLayout(self.chipView)

        
        self.horizontalGroupBox2 = QtGui.QGroupBox(self.chipTab)
        self.horizontalGroupBox2.setObjectName(_fromUtf8("horizontalGroupBox2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalGroupBox2)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pushButton_3 = QtGui.QPushButton(self.horizontalGroupBox2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_5.addWidget(self.pushButton_3)

        
        self.AutoQuery = QtGui.QPushButton(self.horizontalGroupBox2)
        self.AutoQuery.setObjectName(_fromUtf8("AutoQuery"))
        self.horizontalLayout_5.addWidget(self.AutoQuery)
        self.verticalLayout_7.addWidget(self.horizontalGroupBox2)
        self.TableTabWidget.addTab(self.chipTab, _fromUtf8(""))
        self.nameTab = QtGui.QWidget()
        self.nameTab.setObjectName(_fromUtf8("nameTab"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.nameTab)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.nameView = QtGui.QVBoxLayout()
        self.nameView.setObjectName(_fromUtf8("nameView"))
        self.nxs_TBL = QtGui.QTableWidget(self.nameTab)
        self.nxs_TBL.setObjectName(_fromUtf8("nxs_TBL"))
        self.nxs_TBL.setColumnCount(0)
        self.nxs_TBL.setRowCount(0)
        self.nameView.addWidget(self.nxs_TBL)
        self.verticalLayout_8.addLayout(self.nameView)
        self.TableTabWidget.addTab(self.nameTab, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.tab_6)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.queryView = QtGui.QVBoxLayout()
        self.queryView.setObjectName(_fromUtf8("queryView"))
        self.qxs_TBL = QtGui.QTableWidget(self.tab_6)
        self.qxs_TBL.setObjectName(_fromUtf8("qxs_TBL"))
        self.qxs_TBL.setColumnCount(0)
        self.qxs_TBL.setRowCount(0)
        self.queryView.addWidget(self.qxs_TBL)
        self.verticalLayout_9.addLayout(self.queryView)
        self.TableTabWidget.addTab(self.tab_6, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.TableTabWidget)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout_2.addWidget(self.textEdit)
        self.TableTabWidget.raise_()
        self.textEdit.raise_()
        self.horizontalGroupBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuActions = QtGui.QMenu(self.menubar)
        self.menuActions.setObjectName(_fromUtf8("menuActions"))
        self.menuBatch = QtGui.QMenu(self.menubar)
        self.menuBatch.setObjectName(_fromUtf8("menuBatch"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.actionNew_Database = QtGui.QAction(MainWindow)
        self.actionNew_Database.setObjectName(_fromUtf8("actionNew_Database"))
        self.actionOpen_Database = QtGui.QAction(MainWindow)
        self.actionOpen_Database.setObjectName(_fromUtf8("actionOpen_Database"))
        self.actionSave_Database = QtGui.QAction(MainWindow)
        self.actionSave_Database.setObjectName(_fromUtf8("actionSave_Database"))
        self.actionImport_Images_Select_file_s = QtGui.QAction(MainWindow)
        self.actionImport_Images_Select_file_s.setObjectName(_fromUtf8("actionImport_Images_Select_file_s"))
        self.actionImport_Images_Select_Directory = QtGui.QAction(MainWindow)
        self.actionImport_Images_Select_Directory.setObjectName(_fromUtf8("actionImport_Images_Select_Directory"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionAdd_Chip = QtGui.QAction(MainWindow)
        self.actionAdd_Chip.setObjectName(_fromUtf8("actionAdd_Chip"))
        self.actionNew_Chip_Property = QtGui.QAction(MainWindow)
        self.actionNew_Chip_Property.setObjectName(_fromUtf8("actionNew_Chip_Property"))
        self.actionQuery = QtGui.QAction(MainWindow)
        self.actionQuery.setObjectName(_fromUtf8("actionQuery"))
        self.actionReselect_ROI = QtGui.QAction(MainWindow)
        self.actionReselect_ROI.setObjectName(_fromUtf8("actionReselect_ROI"))
        self.actionReselect_Orientation = QtGui.QAction(MainWindow)
        self.actionReselect_Orientation.setObjectName(_fromUtf8("actionReselect_Orientation"))
        self.actionSelect_Next = QtGui.QAction(MainWindow)
        self.actionSelect_Next.setObjectName(_fromUtf8("actionSelect_Next"))
        self.actionDelete_Chip = QtGui.QAction(MainWindow)
        self.actionDelete_Chip.setObjectName(_fromUtf8("actionDelete_Chip"))
        self.actionDelete_Image = QtGui.QAction(MainWindow)
        self.actionDelete_Image.setObjectName(_fromUtf8("actionDelete_Image"))
        self.actionPrecompute_Chips_Features = QtGui.QAction(MainWindow)
        self.actionPrecompute_Chips_Features.setObjectName(_fromUtf8("actionPrecompute_Chips_Features"))
        self.actionPrecompute_Queries = QtGui.QAction(MainWindow)
        self.actionPrecompute_Queries.setObjectName(_fromUtf8("actionPrecompute_Queries"))
        self.actionScale_All_ROIs = QtGui.QAction(MainWindow)
        self.actionScale_All_ROIs.setObjectName(_fromUtf8("actionScale_All_ROIs"))
        self.actionConvert_All_Images_into_Chips = QtGui.QAction(MainWindow)
        self.actionConvert_All_Images_into_Chips.setObjectName(_fromUtf8("actionConvert_All_Images_into_Chips"))
        self.actionLayout_Figures = QtGui.QAction(MainWindow)
        self.actionLayout_Figures.setObjectName(_fromUtf8("actionLayout_Figures"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionView_Documentation = QtGui.QAction(MainWindow)
        self.actionView_Documentation.setObjectName(_fromUtf8("actionView_Documentation"))
        self.actionView_Database_Dir = QtGui.QAction(MainWindow)
        self.actionView_Database_Dir.setObjectName(_fromUtf8("actionView_Database_Dir"))
        self.actionView_Computed_Dir = QtGui.QAction(MainWindow)
        self.actionView_Computed_Dir.setObjectName(_fromUtf8("actionView_Computed_Dir"))
        self.actionView_Global_Dir = QtGui.QAction(MainWindow)
        self.actionView_Global_Dir.setObjectName(_fromUtf8("actionView_Global_Dir"))
        self.actionWrite_Logs = QtGui.QAction(MainWindow)
        self.actionWrite_Logs.setObjectName(_fromUtf8("actionWrite_Logs"))
        self.actionDelete_Cached_Query_Results = QtGui.QAction(MainWindow)
        self.actionDelete_Cached_Query_Results.setObjectName(_fromUtf8("actionDelete_Cached_Query_Results"))
        self.actionDelete_Computed_Directory = QtGui.QAction(MainWindow)
        self.actionDelete_Computed_Directory.setObjectName(_fromUtf8("actionDelete_Computed_Directory"))
        self.actionDelete_Global_Preferences = QtGui.QAction(MainWindow)
        self.actionDelete_Global_Preferences.setObjectName(_fromUtf8("actionDelete_Global_Preferences"))
        self.actionDeveloper_Mode_IPython = QtGui.QAction(MainWindow)
        self.actionDeveloper_Mode_IPython.setObjectName(_fromUtf8("actionDeveloper_Mode_IPython"))
        self.actionDeveloper_Reload = QtGui.QAction(MainWindow)
        self.actionDeveloper_Reload.setObjectName(_fromUtf8("actionDeveloper_Reload"))
        self.menuFile.addAction(self.actionNew_Database)
        self.menuFile.addAction(self.actionOpen_Database)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Database)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_Images_Select_file_s)
        self.menuFile.addAction(self.actionImport_Images_Select_Directory)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuActions.addAction(self.actionAdd_Chip)
        self.menuActions.addAction(self.actionNew_Chip_Property)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionQuery)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionReselect_ROI)
        self.menuActions.addAction(self.actionReselect_Orientation)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionSelect_Next)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionDelete_Chip)
        self.menuActions.addAction(self.actionDelete_Image)
        self.menuBatch.addAction(self.actionPrecompute_Chips_Features)
        self.menuBatch.addAction(self.actionPrecompute_Queries)
        self.menuBatch.addSeparator()
        self.menuBatch.addAction(self.actionScale_All_ROIs)
        self.menuBatch.addSeparator()
        self.menuBatch.addAction(self.actionConvert_All_Images_into_Chips)
        self.menuOptions.addAction(self.actionLayout_Figures)
        self.menuOptions.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionView_Documentation)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionView_Database_Dir)
        self.menuHelp.addAction(self.actionView_Computed_Dir)
        self.menuHelp.addAction(self.actionView_Global_Dir)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionWrite_Logs)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDelete_Cached_Query_Results)
        self.menuHelp.addAction(self.actionDelete_Computed_Directory)
        self.menuHelp.addAction(self.actionDelete_Global_Preferences)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDeveloper_Mode_IPython)
        self.menuHelp.addAction(self.actionDeveloper_Reload)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())
        self.menubar.addAction(self.menuBatch.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.TableTabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Import Image(s)", None))
        self.pushButton_2.setText(_translate("MainWindow", "Save Database", None))
        self.AutoChip.setText(_translate("MainWindow", "AutoChip", None))
        self.TableTabWidget.setTabText(self.TableTabWidget.indexOf(self.imageTab), _translate("MainWindow", "Image Table", None))
        self.pushButton_3.setText(_translate("MainWindow", "Save Database", None))
        self.AutoQuery.setText(_translate("MainWindow", "AutoQuery", None))
        self.TableTabWidget.setTabText(self.TableTabWidget.indexOf(self.chipTab), _translate("MainWindow", "Chip Table", None))
        self.TableTabWidget.setTabText(self.TableTabWidget.indexOf(self.nameTab), _translate("MainWindow", "Name View", None))
        self.TableTabWidget.setTabText(self.TableTabWidget.indexOf(self.tab_6), _translate("MainWindow", "Query Results Table", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuActions.setTitle(_translate("MainWindow", "Actions", None))
        self.menuBatch.setTitle(_translate("MainWindow", "Batch", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionNew_Database.setText(_translate("MainWindow", "New Database", None))
        self.actionOpen_Database.setText(_translate("MainWindow", "Open Database", None))
        self.actionSave_Database.setText(_translate("MainWindow", "Save Database", None))
        self.actionImport_Images_Select_file_s.setText(_translate("MainWindow", "Import Images (Select file(s))", None))
        self.actionImport_Images_Select_Directory.setText(_translate("MainWindow", "Import Images (Select Directory)", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionAdd_Chip.setText(_translate("MainWindow", "Add Chip", None))
        self.actionNew_Chip_Property.setText(_translate("MainWindow", "New Chip Property", None))
        self.actionQuery.setText(_translate("MainWindow", "Query", None))
        self.actionReselect_ROI.setText(_translate("MainWindow", "Reselect ROI", None))
        self.actionReselect_Orientation.setText(_translate("MainWindow", "Reselect Orientation", None))
        self.actionSelect_Next.setText(_translate("MainWindow", "Select Next", None))
        self.actionDelete_Chip.setText(_translate("MainWindow", "Delete Chip", None))
        self.actionDelete_Image.setText(_translate("MainWindow", "Delete Image", None))
        self.actionPrecompute_Chips_Features.setText(_translate("MainWindow", "Precompute Chips/Features", None))
        self.actionPrecompute_Queries.setText(_translate("MainWindow", "Precompute Queries", None))
        self.actionScale_All_ROIs.setText(_translate("MainWindow", "Scale All ROIs", None))
        self.actionConvert_All_Images_into_Chips.setText(_translate("MainWindow", "Convert All Images into Chips", None))
        self.actionLayout_Figures.setText(_translate("MainWindow", "Layout Figures", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionView_Documentation.setText(_translate("MainWindow", "View Documentation", None))
        self.actionView_Database_Dir.setText(_translate("MainWindow", "View Database Dir", None))
        self.actionView_Computed_Dir.setText(_translate("MainWindow", "View Computed Dir", None))
        self.actionView_Global_Dir.setText(_translate("MainWindow", "View Global Dir", None))
        self.actionWrite_Logs.setText(_translate("MainWindow", "Write Logs", None))
        self.actionDelete_Cached_Query_Results.setText(_translate("MainWindow", "Delete Cached Query Results", None))
        self.actionDelete_Computed_Directory.setText(_translate("MainWindow", "Delete Computed Directory", None))
        self.actionDelete_Global_Preferences.setText(_translate("MainWindow", "Delete Global Preferences", None))
        self.actionDeveloper_Mode_IPython.setText(_translate("MainWindow", "Developer Mode (IPython)", None))
        self.actionDeveloper_Reload.setText(_translate("MainWindow", "Developer Reload", None))

