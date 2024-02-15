import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject,QRunnable, Signal
from former import former
import logging
import pyperclip
import threading
from pyqt_loading_progressbar.loadingProgressBar import LoadingProgressBar
from time import sleep
from ui_form import Ui_Widget
from openai_api import Qtype, questioner
from PySide6.QtCore import QThread
from PySide6.QtCore import QRunnable, Qt, QThreadPool
import sys, os
basedir = os.path.dirname(__file__)
try:
    from ctypes import windll
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
class Worker(QObject):
    finished = Signal()
    def __init__(self, him):
        super().__init__()
        self.form = him.form
        self.him=him
        logging.error("Created")
    def run(self):
        logging.error(self.form)
        Jackie=questioner("gpt-4-1106-preview")
        self.him.text=Jackie.writeText(self.form.getText(), self.form.getTypes()) #TODO: Add usage of TEXT:
        self.finished.emit()
class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.form=former()
        self.text=""
        uiFileQt = QFile(os.path.join(basedir, "form.ui"))
        uiFileQt.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(uiFileQt, parentWidget=self)
        uiFileQt.close()
        self.ui.pushButton.setEnabled(False)
        self.ui.setParent(self)
        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.resize(self.ui.size())
        self.setLayout(layout)
        self.ui.pushButton.clicked.connect(self.runLongTask)
        self.ui.plainTextEdit.textChanged.connect(self.setText)
        self.ui.spinBox_4.valueChanged.connect(self.setTrueFalse)
        self.ui.spinBox.valueChanged.connect(self.setMultipleChoice)
        self.ui.spinBox_2.valueChanged.connect(self.setFillInTheBlank)
        self.ui.spinBox_3.valueChanged.connect(self.setOpenQuestion)
        self.threads=[]
        self.show()
    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.start()
        self.widgetProgress=WidgetProgress()
        self.widgetProgress.setWindowTitle("Jackie")
        self.widgetProgress.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'Jackie7X.ico')))
        self.widgetProgress.resize(300, 70)
        self.widgetProgress.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.widgetProgress.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.widgetProgress.show()
        self.setEnabled(False)
    def on_thread_finished(self):
        self.widgetAnswer = WidgetAnswer(None, self.text)
        self.widgetAnswer.setWindowTitle("Jackie Вопросы")
        self.widgetAnswer.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'Jackie7X.ico')))
        self.widgetAnswer.show()
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.setEnabled(True)
        self.widgetProgress.close()
        self.thread.deleteLater()
    def setText(self):
        self.form.setText(self.ui.plainTextEdit.toPlainText())
        if self.form.text!="" and sum([int(i.get()[0]) for i in self.form.types])!=0:
            self.ui.pushButton.setEnabled(True)

        if self.form.text=="" or sum([int(i.get()[0]) for i in self.form.types])==0:
            self.ui.pushButton.setEnabled(False)
    def setTrueFalse(self,value):
        type=Qtype("True/False Question*", value)
        self.form.appendType(type,1)
        if self.form.text!="" and sum([int(i.get()[0]) for i in self.form.types])!=0:
            self.ui.pushButton.setEnabled(True)
        if self.form.text=="" or sum([int(i.get()[0]) for i in self.form.types])==0:
            self.ui.pushButton.setEnabled(False)
    def setMultipleChoice(self,value):
        type=Qtype("Multiple-Choice Question*", value)
        self.form.appendType(type,2)
        if self.form.text!="" and sum([int(i.get()[0]) for i in self.form.types])!=0:
            self.ui.pushButton.setEnabled(True)
        if self.form.text=="" or sum([int(i.get()[0]) for i in self.form.types])==0:
            self.ui.pushButton.setEnabled(False)
    def setFillInTheBlank(self,value):
        type=Qtype("Fill-in-the-Blank Question*", value)
        self.form.appendType(type,3)
        if self.form.text!="" and sum([int(i.get()[0]) for i in self.form.types])!=0:
            self.ui.pushButton.setEnabled(True)
        if self.form.text=="" or sum([int(i.get()[0]) for i in self.form.types])==0:
           self.ui.pushButton.setEnabled(False)
    def setOpenQuestion(self,value):
        type=Qtype("Question* with open answer", value)
        self.form.appendType(type,4)
        if self.form.text!="" and sum([int(i.get()[0]) for i in self.form.types])!=0:
            self.ui.pushButton.setEnabled(True)
        if self.form.text=="" or sum([int(i.get()[0]) for i in self.form.types])==0:
            self.ui.pushButton.setEnabled(False)
class WidgetProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        uiFileQt = QFile(os.path.join(basedir, "progress.ui"))
        uiFileQt.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(uiFileQt, parentWidget=self)
        uiFileQt.close()
        layout = QVBoxLayout()
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setMinimum(0)
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'Jackie7X.ico')))
        self.setLayout(layout)
        self.show()
class WidgetAnswer(QWidget):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.form=former()
        uiFileQt = QFile(os.path.join(basedir, "displayer.ui"))
        uiFileQt.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(uiFileQt, parentWidget=self)
        uiFileQt.close()
        self.ui.setParent(self)
        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.resize(self.ui.size())
        self.setLayout(layout)
        self.show()
        self.ui.textEdit.setText(text)
        self.ui.pushButton_2.clicked.connect(self.copyText)
        self.ui.pushButton.clicked.connect(self.destroyME)
    def copyText(self):
        pyperclip.copy(self.ui.textEdit.toPlainText())
    def destroyME(self):
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.setWindowTitle("Jackie")
    widget.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'Jackie7X.ico')))
    widget.show()
    sys.exit(app.exec())
