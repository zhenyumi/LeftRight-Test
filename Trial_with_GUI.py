import pygame
import os
import sys
import time
import pandas as pd
from pygame.locals import *
from random import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# Functions
# Wait, record the answer, analyse the accuracy
def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if current_round == 0:
                return
            if event.type == KEYDOWN and event.key == K_LEFT:
                directions.append("Left")
                if numofright < numofleft:
                    accuracy.append("Correct")
                else:
                    accuracy.append("Wrong")
                return
            if event.type == KEYDOWN and event.key == K_RIGHT:
                directions.append("Right")
                if numofright > numofleft:
                    accuracy.append("Correct")
                else:
                    accuracy.append("Wrong")
                return

# Re_set all the game variables
def restart():
    global T_StoR, T_TtoS, directions, accuracy, y_coor, x_coor, T_right, T_left, T_onset, T_response, filepath
    T_StoR = []
    T_TtoS = []
    T_onset = []
    T_response = []
    T_right = []
    T_left = []
    directions = []
    accuracy = []
    y_coor = []
    x_coor = []
    filepath = os.path.abspath(__file__)
    filepath = os.path.dirname(filepath)

# If the trial is ended, then save the result and restart the trial
def savecsv():
    Subjectid = [SubjectID_text]*round
    Trialid = []
    for i in range(0, round):
        Trialid.append("{0}_{1}".format(i, TrialID_text))
    global T_StoR,T_TtoS, T_onset, T_response
    dataframe = []
    dataframe = pd.DataFrame({'Subject ID': Subjectid, 'Trial ID': Trialid, 'Time: Time: onset of stimulus (s)': T_onset,
                              'Time: response is made (s)': T_response, 'The number of \\ in the trial': T_right,
                              'The number of / in the trial': T_left, 'The response: left or right': directions,
                              'Response time (ms)': T_StoR
                              })
    global filepath
    print(T_StoR)
    print(dataframe)
    print(filepath)
    filepath = "{0}\\{1}_{2}.csv".format(filepath, SubjectID_text.replace(':',"-"), time.strftime('%Y%m%d_%H-%M-%S'))
    print(filepath)
    filepath = filepath.replace('\\','/')
    print(filepath)
    file = open(filepath, mode='w+')
    file = dataframe.to_csv(file)
    return

# GUI configuration: Login
class Ui_Dialog(object):
    ## The function for clicking 'cancel' button
    def cancel_clicked(self):
        sys.exit()
        sys.exit(app.exec_())
    ## The function for clicking 'ok' button
    def ok_clicked(self):
        global SubjectID_text
        global TrialID_text
        if self.SubjectID.text() == "":
            pass
        else:
            SubjectID_text = self.SubjectID.text()
        if self.TrialID.text() == "":
            pass
        else:
            TrialID_text = self.TrialID.text()
        print(SubjectID_text)
        print(TrialID_text)
        widget.close()

    def setupUi(self, Dialog):
        # The main window
        Dialog.setObjectName("Dialog")
        Dialog.resize(573, 300)
        # The labels
        self.Setsubjectid = QtWidgets.QLabel(Dialog)
        self.Setsubjectid.setGeometry(QtCore.QRect(30, 140, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Setsubjectid.setFont(font)
        self.Setsubjectid.setObjectName("Setsubjectid")
        self.SettrialID = QtWidgets.QLabel(Dialog)
        self.SettrialID.setGeometry(QtCore.QRect(60, 200, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.SettrialID.setFont(font)
        self.SettrialID.setObjectName("SettrialID")
        self.SubjectID = QtWidgets.QLineEdit(Dialog)
        self.SubjectID.setGeometry(QtCore.QRect(180, 130, 381, 31))
        # The ID input
        self.SubjectID.setObjectName("SubjectID")
        self.TrialID = QtWidgets.QLineEdit(Dialog)
        self.TrialID.setGeometry(QtCore.QRect(180, 190, 381, 31))
        self.TrialID.setObjectName("TrialID")
        # The OK button
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(350, 250, 93, 28))
        self.ok.setObjectName("ok")
        self.ok.clicked.connect(self.ok_clicked)
        # The explain text
        self.Explain = QtWidgets.QLabel(Dialog)
        self.Explain.setGeometry(QtCore.QRect(30, 30, 521, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Explain.setFont(font)
        self.Explain.setWordWrap(True)
        self.Explain.setObjectName("Explain")
        # The cancel button
        self.cancel = QtWidgets.QPushButton(Dialog)
        self.cancel.setGeometry(QtCore.QRect(460, 250, 93, 28))
        self.cancel.setObjectName("cancel")
        ## If click the cancel button, then close the whole program
        self.cancel.clicked.connect(self.cancel_clicked)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Config"))
        self.Setsubjectid.setText(_translate("Dialog", "Set Subject ID"))
        self.SettrialID.setText(_translate("Dialog", "Set Trial ID"))
        self.ok.setText(_translate("Dialog", "OK"))
        self.Explain.setText(_translate("Dialog", "Before the trial, you can set the sbject ID and trial ID freely. If you do not want to config this, you can just click \"OK\" and will use default setting."))
        self.cancel.setText(_translate("Dialog", "Cancel"))

# GUI configuration: Save and restart panel
class Ui_save_restart(object):
    def finish_clicked(self):
        savecsv()
        widget2.close()
        pygame.quit()
        sys.exit()

    def ok_clicked(self):
        savecsv()
        global current_round
        current_round = 0
        print(current_round)
        global TrialID_text
        if self.TrialID.text() == "":
            TrialID_text = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        global SubjectID_text
        if self.SubjectID.text() == "":
            pass
        else:
            SubjectID_text = self.SubjectID.text()
        # Update the placeholder in the save window
        self.SubjectID.setPlaceholderText(SubjectID_text)
        self.TrialID.setPlaceholderText(TrialID_text)
        widget2.close()

    def filepath_clicked(self):
        global filepath
        filepath = QFileDialog.getExistingDirectory(None)
        print(filepath)
        self.Filepath.setText(filepath)
        return

    def setup_save_restart(self, Dialog):
        # The tips
        Dialog.setObjectName("Dialog")
        Dialog.resize(746, 612)
        font = QtGui.QFont()
        font.setKerning(True)
        Dialog.setFont(font)
        self.Tip1 = QtWidgets.QLabel(Dialog)
        self.Tip1.setGeometry(QtCore.QRect(20, 20, 701, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Tip1.setFont(font)
        self.Tip1.setWordWrap(True)
        self.Tip1.setObjectName("Tip1")
        self.Tip2 = QtWidgets.QLabel(Dialog)
        self.Tip2.setGeometry(QtCore.QRect(20, 90, 701, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Tip2.setFont(font)
        self.Tip2.setWordWrap(True)
        self.Tip2.setObjectName("Tip2")
        self.Tip3 = QtWidgets.QLabel(Dialog)
        self.Tip3.setGeometry(QtCore.QRect(20, 170, 701, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Tip3.setFont(font)
        self.Tip3.setWordWrap(True)
        self.Tip3.setObjectName("Tip3")
        self.Tip4 = QtWidgets.QLabel(Dialog)
        self.Tip4.setGeometry(QtCore.QRect(20, 260, 701, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Tip4.setFont(font)
        self.Tip4.setWordWrap(True)
        self.Tip4.setObjectName("Tip4")
        # The subject ID
        self.SettrialID_2 = QtWidgets.QLabel(Dialog)
        self.SettrialID_2.setGeometry(QtCore.QRect(100, 500, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.SettrialID_2.setFont(font)
        self.SettrialID_2.setObjectName("SettrialID_2")
        self.SubjectID = QtWidgets.QLineEdit(Dialog)
        self.SubjectID.setGeometry(QtCore.QRect(230, 370, 381, 31))
        self.SubjectID.setObjectName("SubjectID")
        global SubjectID_text
        self.SubjectID.setPlaceholderText(SubjectID_text)
        self.Setsubjectid = QtWidgets.QLabel(Dialog)
        self.Setsubjectid.setGeometry(QtCore.QRect(80, 380, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Setsubjectid.setFont(font)
        self.Setsubjectid.setObjectName("Setsubjectid")
        # Trial ID
        self.SettrialID = QtWidgets.QLabel(Dialog)
        self.SettrialID.setGeometry(QtCore.QRect(110, 440, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.SettrialID.setFont(font)
        self.SettrialID.setObjectName("SettrialID")
        self.TrialID = QtWidgets.QLineEdit(Dialog)
        self.TrialID.setGeometry(QtCore.QRect(230, 430, 381, 31))
        self.TrialID.setObjectName("TrialID")
        global TrialID_text
        self.TrialID.setPlaceholderText(TrialID_text)
        # Finish button
        self.finish = QtWidgets.QPushButton(Dialog)
        self.finish.setGeometry(QtCore.QRect(450, 550, 131, 31))
        self.finish.setObjectName("finish")
        self.finish.clicked.connect(self.finish_clicked)
        # Ok button
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(180, 550, 131, 31))
        self.ok.setObjectName("ok")
        self.ok.clicked.connect(self.ok_clicked)
        # The filepath input
        self.Filepath = QtWidgets.QLineEdit(Dialog)
        self.Filepath.setGeometry(QtCore.QRect(230, 490, 381, 31))
        self.Filepath.setObjectName("Filepath")
        self.Filepath.setPlaceholderText(filepath)
        # The ... filepath setting button
        self.set_file_path = QtWidgets.QPushButton(Dialog)
        self.set_file_path.setGeometry(QtCore.QRect(620, 490, 51, 28))
        self.set_file_path.setObjectName("set_file_path")
        self.set_file_path.clicked.connect(self.filepath_clicked)

        self.retranslateUi_save_restart(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi_save_restart(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Next Trial？"))
        self.Tip1.setText(_translate("Dialog",
                                     "You have completed all the rounds and this is the end of this trial. If you want to quit, then click the \'Finish\' button or just close this window."))
        self.Tip2.setText(_translate("Dialog",
                                     "You can reset your Subject ID and Trial ID if necessary. If you do not need to change your Subject ID, just click the \'OK\' button."))
        self.Tip3.setText(_translate("Dialog",
                                     "If you want to begin a new trial, you must change your Trial ID. You can just click the \'OK\' button to use the default setting."))
        self.Setsubjectid.setText(_translate("Dialog", "Set Subject ID"))
        self.SettrialID.setText(_translate("Dialog", "Set Trial ID"))
        self.finish.setText(_translate("Dialog", "Finish"))
        self.ok.setText(_translate("Dialog", "OK"))
        self.SettrialID_2.setText(_translate("Dialog", "Set file path: "))
        self.set_file_path.setText(_translate("Dialog", "..."))
        self.Tip4.setText(_translate("Dialog",
                                     "The experiment result will be saved to a .csv file, you can set the filepath. Or the .csv file will be saved to the same path as the .py file. The file will be named as 'Subject ID-Date.csv'"))

# Construct Pygame GUI and Initiation of Variables
pygame.init()
## Set the screen size
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
## Set the title of the windows
pygame.display.set_caption("Trial")
background = pygame.Surface(screen.get_size())
background.fill([255, 255, 255])
## Record the number of \ and / in each round
global T_right, T_left
T_right = []
T_left = []
## Record the respond
directions = []
## Time gap between onset and stimuli
time_to_wait = 2000
## Round of trials. How much trials in one experiment
global round
round = 60
## Distance separate
separate_distance = 100
## Record the accuracy
accuracy = []
## Setup time calculation
clock = pygame.time.Clock()
## Time record
### Time period from onset of the trial to onset of the stimuli
T_TtoS = []
### Time period from onset of the stimuli to response
T_StoR = []
### Time of onset
global T_onset
T_onset = []
### Time of response
global T_response
T_response = []
## IDs
global SubjectID_text
SubjectID_text = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
global TrialID_text
TrialID_text = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
## Current round num
global current_round
current_round = 0
## The final path saved csv
global filepath
filepath = os.path.abspath(__file__)
filepath = os.path.dirname(filepath)

# The main loop of the Game
running = True

## Open Login Panel
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(widget)
    widget.show()
## Open save window
if __name__ == "__main__":
    app2 = QtWidgets.QApplication(sys.argv)
    widget2 = QtWidgets.QWidget()
    ui2 = Ui_save_restart()
    ui2.setup_save_restart(widget2)
    widget2.show()
    widget2.close()

# Waiting for trail start and display some tips:
start = False
while not start:
    background.fill([255, 255, 255])
    font = pygame.font.Font(None, 50)
    ## Tips content
    tips1 = font.render("Hi. This is a program to test something.", 1, (0, 0, 0))
    tips2 = font.render("There are {0} trials in total. ".format(round), 1, (0, 0, 0))
    tips3 = font.render("You have {:.1f}s to get ready before each trial.".format(time_to_wait/1000), 1, (0, 0, 0))
    tips4 = font.render("If you get ready, press 'F' to start.", 1, (0, 0, 0))
    ## Tips position
    center1 = (screen_width/2, screen_height/2-200)
    center2 = (screen_width/2, screen_height/2-50)
    center3 = (screen_width/2, screen_height/2+50)
    center4 = (screen_width/2, screen_height/2+200)
    ## Insert the tips
    tipspos = tips1.get_rect(center=center1)
    background.blit(tips1, tipspos)
    tipspos = tips2.get_rect(center=center2)
    background.blit(tips2, tipspos)
    tipspos = tips3.get_rect(center=center3)
    background.blit(tips3, tipspos)
    tipspos = tips4.get_rect(center=center4)
    background.blit(tips4, tipspos)
    ## Update the screen
    screen.blit(background, (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == pygame.K_f:
            start = True
            break

# Beginning of the main loop
while running:
    ## Trial onset
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        ## Construct a random number and determine the number of / and \
        ### Make sure / and \ do not have equal numbers
        while True:
            numofright = randint(20, 40)
            numofleft = 60 - numofright
            if numofright != numofleft:
                T_left.append(numofleft)
                T_right.append(numofright)
                break
        background.fill([255, 255, 255])
        ## Wait for a while before response: The gap screen
        background.fill([255, 255, 255])
        font = pygame.font.Font(None, 50)
        ### The gap info
        tips1 = font.render("Please wait for the next trial.", 1, (0, 0, 0))
        tips2 = font.render("The gap is {:.1f}s".format(time_to_wait/1000), 1, (0, 0, 0))
        center1 = (screen_width / 2, screen_height / 2 - 50)
        center2 = (screen_width / 2, screen_height / 2 + 50)
        tipspos = tips1.get_rect(center=center1)
        background.blit(tips1, tipspos)
        tipspos = tips2.get_rect(center=center2)
        background.blit(tips2, tipspos)
        ### update the screen
        screen.blit(background, (0, 0))
        pygame.display.update()
        pygame.time.wait(time_to_wait)
        ### Reupdate the screen to blank
        background.fill([255, 255, 255])
        screen.blit(background, (0, 0))
        pygame.display.update()
        ## Display / and \
        # Creat \ and / objects
        font = pygame.font.Font(None, 50)
        textright = font.render("\\", 1, (255, 10, 10))  # Color
        textleft = font.render("/", 1, (255, 10, 10))  # Color
        # Randomly put / and \
        ## Record of the center of / and \
        x_coor = [0]
        y_coor = [0]
        for i in range(0, numofright):
            ## Seperate the \
            xNotS = True
            while xNotS:
                x = randint(50, 750)
                for j in x_coor:
                    if abs(x - j) < separate_distance:
                        xNotS = True
                    else:
                        xNotS = False
            x_coor.append(x)
            yNotS = True
            while yNotS:
                y = randint(100, 750)
                for j in y_coor:
                    if abs(y - j) < separate_distance:
                        yNotS = True
                    else:
                        yNotS = False
            y_coor.append(y)
            ## Put the \ into position
            center = (x, y)  # Position
            textpos = textright.get_rect(center=center)
            ## Insert \ into background
            background.blit(textright, textpos)
        for i in range(0, numofleft):
            # Seperate the /
            xNotS = True
            while xNotS:
                x = randint(50, 750)
                for j in x_coor:
                    if abs(x - j) < separate_distance:
                        xNotS = True
                    else:
                        xNotS = False
            x_coor.append(x)
            yNotS = True
            while yNotS:
                y = randint(100, 750)
                for j in y_coor:
                    if abs(y - j) < separate_distance:
                        yNotS = True
                    else:
                        yNotS = False
            y_coor.append(y)
            ## Put the \ into position
            center = (x, y)  # Position
            textpos = textleft.get_rect(center=center)
            ## Insert \ into background
            background.blit(textleft, textpos)
        # Insert information of each trial
        ## re-calculate/update current round
        current_round = current_round + 1
        font_info = pygame.font.Font(None, 25)
        round_info = font_info.render("Round No.{0}".format(current_round), 1, (0, 0, 0))
        center_info_round = (30, 10)
        infopos = round_info.get_rect(center=center_info_round)
        background.blit(round_info, center_info_round)
        ## subject ID info
        subject_info = font_info.render("Subject ID: {0}".format(SubjectID_text), 1, (0, 0, 0))
        center_info_subjectID = (30, 40)
        infopos = subject_info.get_rect(center=center_info_subjectID)
        background.blit(subject_info, center_info_subjectID)
        ## trial ID info
        trial_info = font_info.render("Trial ID: {0}_{1}".format(current_round, TrialID_text), 1, (0, 0, 0))
        center_info_trialID = (30, 70)
        infopos = trial_info.get_rect(center=center_info_trialID)
        background.blit(trial_info, center_info_trialID)
        # Insert background into the screen
        screen.blit(background, (0, 0))
        # Update background.
        # Stimuli onset
        ## Time Calculation Begins: update clock time to 0 and record the time from trial onset to stimili onset
        T_TtoS.append(clock.tick())
        T_onset.append(time.perf_counter())
        pygame.display.update()
        ## Waiting for response
        wait()
        ## Record the respond time
        T_StoR.append(clock.tick())
        T_response.append(time.perf_counter())
        print(directions)
        print(accuracy)
        print(numofleft)
        print(numofright)
        print(T_TtoS)
        print(T_StoR)
        if current_round == round:
            print("end")
            current_round = 0
            # show the save window
            widget2.show()
            # Waiting for next trail start and display some tips:
            start = False
            while not start:
                background.fill([255, 255, 255])
                font = pygame.font.Font(None, 50)
                ## Tips content
                tips1 = font.render("Hi. This is the end of one experiment.", 1, (0, 0, 0))
                tips2 = font.render("There are {0} trials in next experiment. ".format(round), 1, (0, 0, 0))
                tips3 = font.render("You have {:.1f}s to get ready before each trial.".format(time_to_wait / 1000), 1,
                                    (0, 0, 0))
                tips4 = font.render("If you get ready, press 'F' to start.", 1, (0, 0, 0))
                ## Tips position
                center1 = (screen_width / 2, screen_height / 2 - 200)
                center2 = (screen_width / 2, screen_height / 2 - 50)
                center3 = (screen_width / 2, screen_height / 2 + 50)
                center4 = (screen_width / 2, screen_height / 2 + 200)
                ## Insert the tips
                tipspos = tips1.get_rect(center=center1)
                background.blit(tips1, tipspos)
                tipspos = tips2.get_rect(center=center2)
                background.blit(tips2, tipspos)
                tipspos = tips3.get_rect(center=center3)
                background.blit(tips3, tipspos)
                tipspos = tips4.get_rect(center=center4)
                background.blit(tips4, tipspos)
                ## Update the screen
                screen.blit(background, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and event.key == pygame.K_f:
                        start = True
                        # restart all the variables
                        restart()
                        break