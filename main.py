import sys
import time
from PyQt4.Qt import *
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

def print_color(string, color):
    print(string+" color: "+str(color.red())+" "+str(color.green())+" "+str(color.blue()))

class ColorPanel():
    def nextnum(self, current):
        if current < len(self.colorList) - 1:
            return current + 1
        else:
            return 0

    def setColor(self, color):
        #palette = self.label.palette()
        #palette.setColor(palette.Base, color)
        #self.label.setPalette(palette)
        colorstr = "{r}, {g}, {b}, 255".format(r = color.red(), g = color.green(), b = color.blue())
        print("color string: "+colorstr)
        print_color("setting to", color)
        self.label.setStyleSheet("QLabel { background-color: rgba(%s); }" % colorstr)
        #print("color set to "+str(color.red())+" "+str(color.green())+" "+str(color.blue()))
        #self.label.setText("color set to "+str(color.red())+" "+str(color.green())+" "+str(color.blue()))
        self.label.setText(str(self.lastTime))

    def update(self):
        newTime = self.timefunc()
        if newTime != self.lastTime:
            self.step = 0
        self.lastTime = newTime
        self.step+=1
        print("time: " + str(self.lastTime))
        print("step: " + str(self.step))
        print_color("origin:", self.colorList[self.lastTime])
        print_color("target:", self.colorList[self.nextnum(self.lastTime)])
        print(" ")
        ccolor = QColorInterpolator.interpolate(self.colorList[self.nextnum(self.lastTime)], self.colorList[self.lastTime], self.steps, self.step)
        self.setColor(ccolor)
        #self.label.setText(str(self.lastTime))
        #print(Times.msecs())

    def __init__(self, label, timefunc, timertime, steps, startstep, colorList):
        self.step = startstep
        self.steps = steps
        self.label = label
        font = QFont( "Arial", 20, QFont.Bold);
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        self.colorList = colorList
        self.timefunc = timefunc
        self.lastTime = timefunc()
        ccolor = QColorInterpolator.interpolate(colorList[self.nextnum(self.lastTime)], colorList[self.lastTime], steps, startstep)
        self.setColor(ccolor)

        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.update)
        self.timer.start(timertime)

class ColorTime(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args)
        layout = QHBoxLayout()
        self.panels = []

        tenscolors = [QColor(0, 0, 255), QColor(0, 255, 0),
                        QColor(255, 0, 0), QColor(255, 0, 255),
                        QColor(255, 255, 0), QColor(0, 255, 255),
                        QColor(255, 255, 255), QColor(0, 0, 0),
                        QColor(128, 0, 0), QColor(0, 0, 128)]

        # starting step is not currently set

        tmplabel = QLabel(" ")
        self.panels.append(ColorPanel(tmplabel, Times.hourTens, 6*1000, 10*60, 0, tenscolors[0:3]))
        layout.addWidget(tmplabel)
        tmplabel = QLabel(" ")
        self.panels.append(ColorPanel(tmplabel, Times.hourOnes, 10*1000, 6*60, 0, tenscolors))
        layout.addWidget(tmplabel)

        tmplabel = QLabel(" ")
        self.panels.append(ColorPanel(tmplabel, Times.minuteTens, 1000, 600, 0, tenscolors[0:6]))
        layout.addWidget(tmplabel)
        tmplabel = QLabel(" ")
        self.panels.append(ColorPanel(tmplabel, Times.minuteOnes, 500, 120, 0, tenscolors))
        layout.addWidget(tmplabel)

        tmplabel = QLabel(" ")
        self.panels.append(ColorPanel(tmplabel, Times.secondTens, 200, 50, 0, tenscolors[0:6]))
        layout.addWidget(tmplabel)
        tmplabel = QLabel(" ")
        self.panels.append(ColorPanel(tmplabel, Times.secondOnes, 100, 10, 0, tenscolors))
        layout.addWidget(tmplabel)

        self.setLayout(layout)
        self.resize(600,100)

class NumberInterpolator():
    @staticmethod
    def interpolate(target, origin, totalSteps, step):
        if (step >= totalSteps):
            return target 

        val = (((target - origin)/float(totalSteps)) * (step)) + origin
        if (target > origin):
            assert val >= origin
        if (target < origin):
            assert val <= origin
        return val

class QColorInterpolator():
    @staticmethod
    def interpolate(target, origin, totalSteps, step):
        return QColor(
            NumberInterpolator.interpolate(target.red(), origin.red(), totalSteps, step),
            NumberInterpolator.interpolate(target.green(), origin.green(), totalSteps, step),
            NumberInterpolator.interpolate(target.blue(), origin.blue(), totalSteps, step)
        )

class Times():
    @staticmethod
    def hourTens():
        return QDateTime.currentDateTime().time().hour() // 10
    
    @staticmethod
    def hourOnes():
        return QDateTime.currentDateTime().time().hour() % 10

    @staticmethod
    def minuteTens():
        return QDateTime.currentDateTime().time().minute() // 10

    @staticmethod
    def minuteOnes():
        return QDateTime.currentDateTime().time().minute() % 10

    @staticmethod
    def secondTens():
        return QDateTime.currentDateTime().time().second() // 10

    @staticmethod
    def secondOnes():
        return QDateTime.currentDateTime().time().second() % 10

    @staticmethod
    def msecs():
        return QDateTime.currentDateTime().time().msec()

if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    w = ColorTime() 
    w.show() 
    sys.exit(app.exec_())
