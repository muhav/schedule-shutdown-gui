from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QGroupBox, QLabel,
                             QCheckBox, QAction, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLineEdit, QTextEdit, QShortcut, QMessageBox)
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QCursor
from PyQt5.QtCore import pyqtSlot, Qt

import os
import sys
import threading


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Schedule Shutdown'

        self.left = 360
        self.top = 240
        self.width = 640
        self.height = 480
        self.setFixedSize(self.width, self.height)

        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut.activated.connect(self.close)

        self.statusBar().showMessage(' Hibernation command: "shutdown -h"')

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.table_widget.countdown(60, new=True)

        self.show()

    def closeEvent(self, event):
        self.table_widget.label.setText(' 1:00')  # stop countdown
        event.accept()  # let the window close
        # event.ignore()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # self.tabs.resize(300, 200)
        tab_font = QFont("Frutiger Next LT CE", 9, QFont.Light)
        self.tabs.setFont(tab_font)

        # Add tabs
        self.tabs.addTab(self.tab1, "Settings")
        self.tabs.addTab(self.tab2, "Help")

        self.set_tab_1()
        self.set_tab_2()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def set_tab_1(self):
        # Create first tab
        frutiger = QFont("Frutiger Next LT CE", 11, QFont.Light)
        frutiger_light = QFont("Frutiger Next LT CE", 34, QFont.Light)
        frutiger_small = QFont("Frutiger Next LT CE", 22)
        frutiger_select = QFont("Frutiger Next LT CE", 18, QFont.Normal)
        monaco = QFont("monaco", 15, QFont.Normal)
        monaco_big = QFont("monaco", 34, QFont.Normal)
        monaco_small = QFont("monaco", 24, QFont.Normal)

        self.tab1.layout = QVBoxLayout(self)

        self.horizontalGroupBox1 = QGroupBox("Set a Schedule")
        self.horizontalGroupBox1.setFont(frutiger)
        self.horizontalGroupBox1.setStyleSheet("padding: 15px; border: 1px solid lightgray; border-radius: 0")
        layout = QGridLayout()
        layout.setSpacing(10)

        label1 = QLabel('Shutdown after', self)
        label1.setFont(frutiger_light)
        label1.setStyleSheet("padding: 0; border: 0; padding-right: 0;")
        layout.addWidget(label1, 1, 0, 1, 1)

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText('1')
        self.textbox.setFocusPolicy(Qt.StrongFocus)

        self.textbox.setFont(monaco_big)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setStyleSheet("padding: 0; border: 0; border-bottom: 2px solid black; border-radius: 0")
        self.textbox.returnPressed.connect(self.set_schedule)
        layout.addWidget(self.textbox, 1, 1, 1, 1)

        label2 = QLabel('minutes.', self)
        label2.setFont(frutiger_light)
        label2.setStyleSheet("padding: 0; border: 0; padding-right: 0;")
        layout.addWidget(label2, 1, 2, 1, 1)

        button_shutdown = QPushButton('[ confirm ]', self)
        button_shutdown.clicked.connect(self.set_schedule)
        button_shutdown.setFont(frutiger)
        button_shutdown.setStyleSheet("padding: 0; margin-left: 80px; margin-right: 10px; "
                                      "border: 0; border-bottom: 0px solid lightgray; ")
        button_shutdown.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(button_shutdown, 2, 2, 1, 1)

        self.box = QCheckBox("hibernate instead of performing a full shutdown")
        self.box.setStyleSheet("padding: 0; margin:0; padding-top: 5px; border: 0")
        self.box.setFont(frutiger)
        self.box.setChecked(True)
        layout.addWidget(self.box, 2, 0, 1, 2)

        self.horizontalGroupBox1.setLayout(layout)
        self.tab1.layout.addWidget(self.horizontalGroupBox1)

        self.horizontalGroupBox2 = QGroupBox("Select a Command")
        self.horizontalGroupBox2.setFont(frutiger)
        self.horizontalGroupBox2.setStyleSheet("padding: 15px; border: 1px solid lightgray; border-radius: 0")
        buttons = QGridLayout()
        buttons.setSpacing(10)

        label_shutdown = QLabel('Shutdown:', self)
        label_shutdown.setFont(frutiger_select)
        label_shutdown.setStyleSheet("padding: 0; border: 0; padding-right: 0;")
        buttons.addWidget(label_shutdown, 0, 0, 1, 1)

        self.textbox_shutdown = QLineEdit(self)
        self.textbox_shutdown.setText('shutdown -s -f -t 60')
        self.textbox_shutdown.setFocusPolicy(Qt.StrongFocus)

        self.textbox_shutdown.setFont(monaco)
        self.textbox_shutdown.setStyleSheet("padding: 0; border: 0; margin-left: 30px; margin-right: 20px;"
                                            "border-bottom: 1px solid black; border-radius: 0")
        self.textbox_shutdown.returnPressed.connect(self.shutdown)
        buttons.addWidget(self.textbox_shutdown, 0, 1, 1, 1)

        button_shutdown = QPushButton('[ confirm ]', self)
        button_shutdown.clicked.connect(self.shutdown)
        button_shutdown.setFont(frutiger)
        button_shutdown.setStyleSheet("padding: 0; margin-left: 25px; margin-right: 10px; border: 0")
        button_shutdown.setCursor(QCursor(Qt.PointingHandCursor))
        buttons.addWidget(button_shutdown, 0, 2, 1, 1)

        label_restart = QLabel('Restart:', self)
        label_restart.setFont(frutiger_select)
        label_restart.setStyleSheet("padding: 0; border: 0; padding-right: 0;")
        buttons.addWidget(label_restart, 1, 0, 1, 1)

        self.textbox_restart = QLineEdit(self)
        self.textbox_restart.setText('shutdown -r -f -t 60')
        self.textbox_restart.setFocusPolicy(Qt.StrongFocus)

        self.textbox_restart.setFont(monaco)
        self.textbox_restart.setStyleSheet("padding: 0; border: 0; margin-left: 30px; margin-right: 20px;"
                                           "border-bottom: 1px solid black; border-radius: 0")
        self.textbox_restart.returnPressed.connect(self.restart)
        buttons.addWidget(self.textbox_restart, 1, 1, 1, 1)

        button_restart = QPushButton('[ confirm ]', self)
        button_restart.clicked.connect(self.restart)
        button_restart.setFont(frutiger)
        button_restart.setStyleSheet("padding: 0; margin-left: 25px; margin-right: 10px; border: 0")
        button_restart.setCursor(QCursor(Qt.PointingHandCursor))
        buttons.addWidget(button_restart, 1, 2, 1, 1)

        label_cancel = QLabel('Abort:', self)
        label_cancel.setFont(frutiger_select)
        label_cancel.setStyleSheet("padding: 0; border: 0; padding-right: 0;")
        buttons.addWidget(label_cancel, 2, 0, 1, 1)

        self.textbox_cancel = QLineEdit(self)
        self.textbox_cancel.setText('shutdown -a')
        self.textbox_cancel.setFocusPolicy(Qt.StrongFocus)

        self.textbox_cancel.setFont(monaco)
        self.textbox_cancel.setStyleSheet("padding: 0; border: 0; margin-left: 30px; margin-right: 20px;"
                                          "border-bottom: 1px solid black; border-radius: 0")
        self.textbox_cancel.returnPressed.connect(self.cancel)
        buttons.addWidget(self.textbox_cancel, 2, 1, 1, 1)

        button_cancel = QPushButton('[ confirm ]', self)
        button_cancel.clicked.connect(self.cancel)
        button_cancel.setFont(frutiger)
        button_cancel.setStyleSheet("padding: 0; margin-left: 25px; margin-right: 10px; border: 0")
        button_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        buttons.addWidget(button_cancel, 2, 2, 1, 1)

        self.horizontalGroupBox2.setLayout(buttons)
        self.tab1.layout.addWidget(self.horizontalGroupBox2)

        self.horizontalGroupBox3 = QGroupBox("Countdown Timer")
        self.horizontalGroupBox3.setFont(frutiger)
        self.horizontalGroupBox3.setStyleSheet("padding: 15px; border: 1px solid lightgray; border-radius: 0")
        cd = QGridLayout()
        cd.setSpacing(10)

        label3 = QLabel('Remaining time until Shutdown:', self)
        label3.setAlignment(Qt.AlignLeft)
        label3.setFont(frutiger_small)
        label3.setStyleSheet("padding: 0; padding-top: 10px; border: 0")
        cd.addWidget(label3, 2, 0, 1, 2)

        self.label = QLabel(' 1:00', self)
        self.label.setAlignment(Qt.AlignRight)
        self.label.setFont(monaco_small)
        self.label.setStyleSheet("padding: 0; padding-top: 5px; border: 0")
        cd.addWidget(self.label, 2, 2, 1, 1)

        abort = QPushButton()
        abort.clicked.connect(self.abort)
        abort.setCursor(QCursor(Qt.PointingHandCursor))
        abort.setStyleSheet("margin-left: 30px; margin-top: 3px; border: 0")
        cd.addWidget(abort, 2, 2, 1, 1)

        self.horizontalGroupBox3.setLayout(cd)
        self.tab1.layout.addWidget(self.horizontalGroupBox3)

        self.tab1.setLayout(self.tab1.layout)

    @pyqtSlot()
    def on_click(self):
        print("on_click")

    @pyqtSlot()
    def shutdown(self):
        text = self.textbox_shutdown.text()
        button_reply = QMessageBox.question(self, 'PyQt5 message', "Shut down?\n> {}".format(text),
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if button_reply == QMessageBox.Yes:
            # print('Yes clicked.')
            os.popen(text)
            exit(0)

    @pyqtSlot()
    def restart(self):
        text = self.textbox_restart.text()
        button_reply = QMessageBox.question(self, 'PyQt5 message', "Restart?\n> {}".format(text),
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if button_reply == QMessageBox.Yes:
            os.popen(text)
            exit(0)

    @pyqtSlot()
    def cancel(self):
        text = self.textbox_cancel.text()
        self.textbox_cancel.setText('shutdown -a')
        os.popen(text)

    @pyqtSlot()
    def abort(self):
        text = self.label.text()
        self.label.setText(' ' + text)

    @pyqtSlot()
    def set_schedule(self):
        if not self.textbox.text():
            self.textbox.setText('1')
        textbox_value = self.textbox.text()
        if textbox_value.isdigit():
            seconds = max(int(textbox_value) * 60, 20)
            self.countdown(seconds, new=True)

    def countdown(self, remaining, new=False):
        if not new and self.label.text() != '{}:{:02}'.format(*divmod(remaining + 1, 60)):
            return  # updated somewhere else

        self.label.setText('{}:{:02}'.format(*divmod(remaining, 60)))

        if remaining <= 0:
            if self.box.isChecked():
                # Process(target=os.system, args=('ping 127.0.0.1 -n 6 > nul & shutdown -h',)).start()
                os.popen('ping 127.0.0.1 -n 16 > nul & shutdown -h')
                os._exit(0)
            else:
                os.popen('ping 127.0.0.1 -n 6 > nul & shutdown /s /f /t 30')
                os._exit(0)
            return

        t = threading.Timer(1, self.countdown, (remaining - 1,))
        t.start()

    def set_tab_2(self):
        # Create first tab
        frutiger = QFont("Frutiger Next LT CE", 11, QFont.Light)
        monaco = QFont("monaco", 11, QFont.Normal)

        self.tab2.layout = QVBoxLayout(self)

        self.horizontalGroupBox = QGroupBox("Commands")
        self.horizontalGroupBox.setFont(frutiger)
        self.horizontalGroupBox.setStyleSheet("padding: 15px; border: 1px solid lightgray; border-radius: 0")
        cmd = QGridLayout()
        cmd.setSpacing(10)

        c = "> shutdown /s /f /t 0&nbsp;&nbsp;" \
            "# Shutdown the computer<br/>" \
            "> shutdown /s /hybrid&nbsp;&nbsp;" \
            "# Shutdown (for fast startup)<br/>" \
            "> shutdown /h&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" \
            "# Hibernate the local computer<br/>" \
            "> shutdown /r&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" \
            "# Full shutdown and restart<br/>" \
            "> shutdown /r /o&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" \
            "# Advanced Boot Options Menu<br/>" \
            "> shutdown /a&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" \
            "# Abort a system shutdown"

        tx = QTextEdit(c, self)
        tx.setAlignment(Qt.AlignLeft)
        tx.setFont(monaco)
        tx.setStyleSheet("padding: 0; border: 0;")
        tx.setReadOnly(True)
        tx.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cmd.addWidget(tx)

        self.horizontalGroupBox.setLayout(cmd)
        self.tab2.layout.addWidget(self.horizontalGroupBox)

        self.horizontalGroupBox = QGroupBox("Copyright")
        self.horizontalGroupBox.setFont(frutiger)
        self.horizontalGroupBox.setStyleSheet("padding: 20px; border: 1px solid lightgray; border-radius: 0")
        cd = QGridLayout()
        cd.setSpacing(10)

        with open('LICENSE') as f:
            c = f.read()

        ls = QTextEdit(c.replace('\n\n', '<br/>').replace('Permission', '<br/>Permission'), self)
        ls.setAlignment(Qt.AlignLeft)
        ls.setFont(monaco)
        ls.setStyleSheet("padding: 0; border: 0;")
        ls.setReadOnly(True)
        ls.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cd.addWidget(ls)

        self.horizontalGroupBox.setLayout(cd)
        self.tab2.layout.addWidget(self.horizontalGroupBox)

        self.horizontalGroupBox = QGroupBox("About")
        self.horizontalGroupBox.setFont(frutiger)
        self.horizontalGroupBox.setStyleSheet("padding: 15px; border: 1px solid lightgray; border-radius: 0")
        info = QGridLayout()
        info.setSpacing(10)

        label4 = QLabel('Version: 0.1.0', self)
        label4.setAlignment(Qt.AlignCenter)
        label4.setFont(monaco)
        label4.setStyleSheet("padding: 0; border: 0")
        info.addWidget(label4, 0, 0, 1, 1)

        label5 = QLabel('GitHub: <a href="https://github.com/bugstop/schedule-shutdown-gui" '
                        'style="color: black !important; text-decoration: none">bugstop</a>', self)
        label5.setAlignment(Qt.AlignCenter)
        label5.setFont(monaco)
        label5.setStyleSheet("padding: 0; border: 0;")

        label5.setOpenExternalLinks(True)
        info.addWidget(label5, 0, 1, 1, 1)

        self.horizontalGroupBox.setLayout(info)
        self.tab2.layout.addWidget(self.horizontalGroupBox)

        self.tab2.setLayout(self.tab2.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.table_widget.textbox.setFocus()
    sys.exit(app.exec_())
