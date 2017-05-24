import cv2
import numpy as np
import os
import operator
from scipy.signal import argrelextrema
import subprocess as sp

class VideoDemo:
    def __init__(self, link):
        self.link = link

    def validVideo(self):
        cap = cv2.VideoCapture(self.link)
        if not cap.isOpened():
            print "Fatal error - could not open video."
            return False
        else:
            print "Parsing video..."
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print "Video Resolution: %d x %d" % (width, height)
            return True

    def calcDifferent(self):
        cap = cv2.VideoCapture(self.link)
        i = 0
        hist_new = np.array([])
        hist_old = np.array([])
        list_distance = {}

        # tinh histogram cho frame do va tinh khoang cach voi frame phia truoc
        while (cap.isOpened()):
            # Doc cac frame trong video
            ret, frame = cap.read()

            # Neu khong con frame nao thi ket thuc
            if (ret != True):
                break

            # Tinh histogram
            hist_new = cv2.calcHist([frame], [0, 1, 2], None, [32, 32, 32],
                                    [0, 256, 0, 256, 0, 256])

            # Neu la frame dau tien thi chua can so sanh
            if (i == 0):
                i = i + 1
                hist_old = hist_new
                continue

            # Neu khong phai la frame dau tien, so sanh histogram
            list_distance[i - 1] = cv2.compareHist(hist_new, hist_old, 3)

            # Tang i, cho hist_new thanh hist_old de tinh tiep
            i = i + 1
            hist_old = hist_new

        # print i
        cap.release()
        return list_distance

    def calcAdaptiveThreshold(self, list_distance, w, c):
        # lay cua so kich thuoc la 2 * w + 1
        # nguong cao hon gia tri trung binh la c
        list_threshold = {}
        for key in list_distance:
            if (key - w >= 0 and key + w < len(list_distance)):
                total = 0
                for x in range(key - w, key + w + 1):
                    total = total + list_distance[x]
                list_threshold[key] = total / (2 * w + 1) + c
            else:
                list_threshold[key] = list_distance[key] + c
        return list_threshold

    def calcSecondDerivative(self, list_distance):
        # phan nay tinh dao ham bac 2 cho histogram
        list_second = {}
        list_second[0] = list_distance[0]
        list_second[len(list_distance) - 1] = list_distance[len(list_distance) - 1]

        for key in list_distance:
            if (key == 0 or key == (len(list_distance) - 1)):
                continue
            list_second[key] = list_distance[key] - list_distance[key - 1]

        return list_second

    def calcAverageDerivative(self, list_second):
        # Tinh gia tri trung binh cua dao ham bac 2
        list_second_abs = {}
        for i in range(len(list_second)):
            list_second_abs[i] = abs(list_second[i])
        arr_second_abs = np.array(list_second_abs.items(), dtype='float')
        my_arr = arr_second_abs[:, 1]
        index = argrelextrema(my_arr, np.greater)
        total = 0
        for i in index:
            total = total + my_arr[i]
        average = total.sum() / len(index[0])
        return average

    def calcHigherDegree(self, list_distance):
        # Tinh muc chenh lech dua tren gia tri trung binh cua khoang cach
        arr_distance = np.array(list_distance.items(), dtype='float')
        temp = arr_distance[:, 1]
        total = np.nansum(temp)
        higher = total / len(temp)
        return higher

    def calcBoundary(self, list_distance, list_threshold):
        # Tinh cac diem vuot nguong
        list_bounary = {}
        j = 0
        for i in range(0, len(list_distance)):
            if (list_distance[i] > list_threshold[i]):
                list_bounary[j] = i
                j = j + 1
        return list_bounary

    def calcBoundaryConstant(self, list_distance, threshold):
        list_bounary = {}
        j = 0
        for i in range(0, len(list_distance)):
            if (list_distance[i] > threshold):
                list_bounary[j] = i
                j = j + 1
        return list_bounary

    def getBeginEnd(self, list_boundary, length):
        # Lay cac so thu tu frame bat dau va ket thuc cua moi shot
        begin = {}
        end = {}
        begin[0] = 0
        begin_index = 1
        end_index = 0
        for i in range(0, len(list_boundary)):
            end[end_index] = list_boundary[i]
            begin[begin_index] = list_boundary[i] + 1
            begin_index = begin_index + 1
            end_index = end_index + 1

        end[end_index] = length - 1
        return {"begin": begin, "end": end}

    def getShotFrame(self, list_boundary):
        # Lay cac frame dau va cuoi moi shot roi luu vao file
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_boundary/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            for the_file in os.listdir(dirname):
                file_path = os.path.join(dirname, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print (e)

        cap = cv2.VideoCapture(self.link)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # print "Length: " + str(length)
        listShot = self.getBeginEnd(list_boundary, length)

        list_begin = listShot["begin"]
        list_end = listShot["end"]
        i = 0
        begin_index = 0
        end_index = 0
        # tinh histogram cho frame do va tinh khoang cach voi frame phia truoc
        while (cap.isOpened()):
            # Doc cac frame trong video
            ret, frame = cap.read()

            # Neu khong con frame nao thi ket thuc
            if (ret != True):
                break

            if begin_index < len(list_begin):
                # Lay frame dau shot
                if i == list_begin[begin_index]:
                    filename = 'image_begin' + str(begin_index) + '.png'
                    #                     print "Start shot " + str(begin_index) + " at frame: " + str(i)
                    cv2.imwrite(os.path.join(dirname, filename), frame)
                    begin_index = begin_index + 1
            if end_index < len(list_end):
                # Lay frame cuoi shot
                if i == list_end[end_index]:
                    filename = 'image_end' + str(end_index) + '.png'
                    #                     print "End shot " + str(end_index) + " at frame: " + str(i)
                    cv2.imwrite(os.path.join(dirname, filename), frame)
                    end_index = end_index + 1

            i = i + 1
        cap.release()

    def detectThreshold(self):
        global list_distance
        threshold = 0
        list_distance = self.calcDifferent()
        print list_distance
        list_distance_sort = reversed(sorted(list_distance.items(), key=operator.itemgetter(1)))
        print "##############"
        print list_distance_sort
        for item in list_distance_sort:
            if self.isMaximaGraph(item[0], 2):
                print item[0]
                threshold = item[1]
        return threshold

    def detectShot(self, threshold):
        list_bounary = {}
        j = 0
        for i in range(0, len(list_distance)):
            if list_distance[i] >= threshold:
                if i < len(list_distance) - 1:
                    if list_distance[i] < list_distance[i + 1]:
                        continue
                    if list_distance[i + 1] > threshold:
                        continue
                list_bounary[j] = i
                j = j + 1
        return list_bounary

    def isMaximaGraph(self, position, threshold):
        if position < 1 or position > (len(list_distance)-2):
            return False
        if list_distance[position] == 0:
            return False
        if list_distance[position-1] != 0 and list_distance[position + 1] != 0 and \
                ((list_distance[position]/list_distance[position - 1] > threshold) and
                     (list_distance[position]/list_distance[position + 1] > threshold)):
            return True
        return False

    def getKeyFrame(self, list_boundary):
        # lay cac keyframe trong video
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_keyframe/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            for the_file in os.listdir(dirname):
                file_path = os.path.join(dirname, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print (e)

        cap = cv2.VideoCapture(self.link)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # print "Length: " + str(length)
        listShot = self.getBeginEnd(list_boundary, length)

        list_begin = listShot["begin"]
        list_end = listShot["end"]
        list_key = {}
        for i in range(len(list_begin)):
            #             print "Begin: " + str(list_begin[i])
            #             print "End: " + str(list_end[i])
            list_key[i] = int(round((list_begin[i] + list_end[i]) / 2))
        # print "Key: " + str(list_key[i])
        i = 0
        key_index = 0
        # lay key frame
        while (cap.isOpened()):
            # Doc cac frame trong video
            ret, frame = cap.read()

            # Neu khong con frame nao thi ket thuc
            if (ret != True):
                break

            if key_index < len(list_key):
                # Lay frame dau shot
                if i == list_key[key_index]:
                    filename = 'image_key' + str(key_index) + '.png'
                    cv2.imwrite(os.path.join(dirname, filename), frame)
                    key_index = key_index + 1
            i = i + 1
        print i
        cap.release()
        return {"begin": list_begin, "end": list_end}

    def getShotVideo(self, list_begin, list_end):
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_shotvideo/'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            for the_file in os.listdir(dirname):
                file_path = os.path.join(dirname, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print (e)

        FFMPEG_BIN = "ffmpeg"
        for i in range(len(list_begin)):
            file_name = dirname + "shot_" + str(i) + ".mp4"
            command = [FFMPEG_BIN,
                       '-i', self.link,
                       '-vf', 'trim=start_frame=' + str(list_begin[i]) + ':end_frame=' + str(list_end[i]),
                       '-an', file_name]
            pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)

    def calcThresholdConst(self):
        list_maxium_graph = np.array(list_distance.items(), dtype='double')
        arr_maxium_graph = argrelextrema(list_maxium_graph[:, 1], np.greater)
        print arr_maxium_graph;
