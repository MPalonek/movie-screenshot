from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QIcon, QPixmap
from argparse import ArgumentParser
import logging
import sys
import worker
from datetime import date
from PyQt5.QtCore import QThreadPool
import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QLabel
from random import randint
import cv2
from math import floor

# TODO

g_directory = ""
g_video_list = []
g_selected_video_path = []
g_video_progress = []
g_images_list = []

class ViewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("detailviewerwindow.ui", self)

        self.ui.show1Button.clicked.connect(self.on_clicked_show1Button)
        self.ui.show2Button.clicked.connect(self.on_clicked_show2Button)
        self.ui.show3Button.clicked.connect(self.on_clicked_show3Button)
        self.ui.show4Button.clicked.connect(self.on_clicked_show4Button)
        self.ui.show5Button.clicked.connect(self.on_clicked_show5Button)
        self.ui.prevImgButton.clicked.connect(self.on_clicked_prevImgButton)
        self.ui.nextImgButton.clicked.connect(self.on_clicked_nextImgButton)

        self.ui.playButton.clicked.connect(self.play_movie)

        self.cur_selected_img_set = 0
        self.img_state = [0, 0, 0, 0, 0]

    def on_clicked_show1Button(self):
        self.cur_selected_img_set = 0
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data, g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1], g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1,
                                                       len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText("{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def on_clicked_show2Button(self):
        self.cur_selected_img_set = 1
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data, g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1], g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1,
                                                       len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText(
            "{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def on_clicked_show3Button(self):
        self.cur_selected_img_set = 2
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data, g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1], g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1,
                                                       len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText(
            "{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def on_clicked_show4Button(self):
        self.cur_selected_img_set = 3
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data, g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1], g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1,
                                                       len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText(
            "{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def on_clicked_show5Button(self):
        self.cur_selected_img_set = 4
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data, g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1], g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1,
                                                       len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText(
            "{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def on_clicked_prevImgButton(self):
        # if we are at first picture do nothing
        if self.img_state[self.cur_selected_img_set] == 0:
            return

        # decrement img_state and show next picture
        self.img_state[self.cur_selected_img_set] = self.img_state[self.cur_selected_img_set] - 1
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data,
                              g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1],
                              g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1, len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText(
            "{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def on_clicked_nextImgButton(self):
        # if we are at last picture do nothing
        if self.img_state[self.cur_selected_img_set] == (len(g_images_list[self.cur_selected_img_set]) - 1):
            return

        # increment img_state and show next picture
        self.img_state[self.cur_selected_img_set] = self.img_state[self.cur_selected_img_set] + 1
        pixmap = QtGui.QImage(g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].data,
                              g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[1],
                              g_images_list[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]].shape[0],
                              QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.ui.imageCountLabel.setText("{}/{}".format(self.img_state[self.cur_selected_img_set] + 1, len(g_images_list[self.cur_selected_img_set])))
        self.ui.timeLabel.setText(
            "{}%".format(g_video_progress[self.cur_selected_img_set][self.img_state[self.cur_selected_img_set]]))

    def play_movie(self):
        # works only on windows, use subprocess for linux
        os.startfile(g_selected_video_path[self.cur_selected_img_set])



class MovieScreenshot(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create the main window
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.setup_ui()

        # Start Thread pool
        self.threadpool = QThreadPool()
        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.temp_worker = None

        self.w = None

    def setup_ui(self):
        self.setWindowTitle('MovieScreenshot')
        self.setWindowIcon(QtGui.QIcon('icons//favicon.ico'))

        self.ui.rollButton.setDisabled(True)

        self.setup_ui_logic()

    def setup_ui_logic(self):
        self.ui.directoryPushButton.clicked.connect(self.on_directory_label_clicked)
        self.ui.recursiveCheckBox.clicked.connect(self.on_recursive_checkbox_clicked)
        self.ui.rollButton.clicked.connect(self.on_roll_button_clicked)


    def on_directory_label_clicked(self):
        global g_directory
        g_directory = self.getDir()

        if self.ui.recursiveCheckBox.isChecked():
            self.get_recursive_video_list_from_dir(g_directory)
        else:
            self.get_video_list_from_dir(g_directory)

        logging.info('Selected directory: {} - found {} movies'.format(g_directory, len(g_video_list)))
        self.ui.directoryPushButton.setText(g_directory)
        self.ui.foundMoviesLabel.setText("Found {} movies".format(len(g_video_list)))
        self.ui.rollButton.setDisabled(False)

    def getDir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        return dialog.getExistingDirectory(self, 'Choose Directory', os.path.curdir)

    def get_video_list_from_dir(self, directory):
        global g_video_list
        g_video_list = []
        for file in os.listdir(directory):
            if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                g_video_list.append(directory + "//" + file)

    def get_recursive_video_list_from_dir(self, directory):
        global g_video_list
        g_video_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                    g_video_list.append(root + "//" + file)

    def on_recursive_checkbox_clicked(self):
        logging.info("Clicked on recursive check box. State: {}".format(self.ui.recursiveCheckBox.isChecked()))
        if g_directory == "":
            return
        if self.ui.recursiveCheckBox.isChecked():
            self.get_recursive_video_list_from_dir(g_directory)
            self.ui.foundMoviesLabel.setText("Found {} movies".format(len(g_video_list)))
        else:
            self.get_video_list_from_dir(g_directory)
            self.ui.foundMoviesLabel.setText("Found {} movies".format(len(g_video_list)))
        logging.info('Selected directory: {} - found {} movies'.format(g_directory, len(g_video_list)))

    def on_roll_button_clicked(self):
        global g_images_list, g_selected_video_path, g_video_progress
        g_video_progress = []
        g_images_list = []
        g_selected_video_path = []
        video_list = g_video_list
        for i in range(5):
            temp = randint(0, len(video_list) - 1)
            video = video_list[temp]
            logging.info("Drawn movie {}: {}".format(i+1, video))
            g_images_list.append(self.get_video_frames(video, 10))
            g_selected_video_path.append(video)
            video_list.remove(video)
        # To display an OpenCV image, you have to convert the image into a QImage then into a QPixmap where you can
        # display the image with a QLabel
        # pixmap = self.images_list[0][0]
        pixmap = QtGui.QImage(g_images_list[0][0].data, g_images_list[0][0].shape[1], g_images_list[0][0].shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        # pixmap = QPixmap(QtGui.QImage(self.images_list[0][0].data, self.images_list[0][0].shape[1], self.images_list[0][0].shape[0], QtGui.QImage.Format_RGB888).rgbSwapped())

        self.w = ViewWindow()
        self.w.imageLabel.setPixmap(QPixmap.fromImage(pixmap))
        self.w.imageCountLabel.setText("1/{}".format(len(g_images_list[0])))
        self.w.show()

    def get_video_frames(self, video_path, number_of_frames):
        global g_video_progress
        frames = []
        procent_progress = []
        cap = cv2.VideoCapture(video_path)
        total_frames = cap.get(7)

        # take frame from beginning (0.05-0.1)
        # take frame from ending (0.9 - 0.95)
        # take rest of the frames in the middle (0.1 - 0.9) and sort
        frame_number = [randint(floor(0.05 * total_frames), floor(0.1 * total_frames)),
                        randint(floor(0.9 * total_frames), floor(0.95 * total_frames))]
        for i in range(number_of_frames - 2):
            frame_number.append(randint(floor(0.1 * total_frames), floor(0.9 * total_frames)))
        frame_number.sort()
        logging.info("Drawn frames: {}".format(frame_number))
        for el in frame_number:
            procent_progress.append(floor(el / total_frames * 100))

        g_video_progress.append(procent_progress)
        for i in range(len(frame_number)):
            cap.set(1, frame_number[i])
            ret, frame = cap.read()
            # cv2.imwrite('D:\\Repo\\movie-screenshot\\test\\frame_{}.jpg'.format(i), frame)
            frames.append(frame)
        return frames

    def play_movie(self, video_path):
        # works only on windows, use subprocess for linux
        os.startfile(video_path)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", '--DEBUG', action='store_true', help="set logging to be debug")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    log_filename = "ms_log_0.log"
    logging.basicConfig(filename=log_filename, format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=loglevel)
    if os.path.isfile(log_filename):
        f = open(log_filename, "a")
        f.write("\n-----------------------------------------------------------------\n\n")
        f.close()
    logging.info('Starting MovieScreenshot. Current date is: {}'.format(date.today()))

    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Fusion')
    window = MovieScreenshot()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
