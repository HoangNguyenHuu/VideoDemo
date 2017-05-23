import cv2
import numpy as np
import os
from scipy.signal import argrelextrema


class VideoDemo:
    def __init__(self, link):
        self.link = link

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
            # Luu y: tham so thu 3 cua ham compareHist nhan 4 gia tri 0,1,2,3 tuong ung voi cac cach tinh khoang cach
            # O day dung 0, tuong ung voi cach tinh do tuong dong correlation, lay 1 - do tuong dong => khoang cach
            d = 1 - cv2.compareHist(hist_new, hist_old, 0)

            # Them vao ket qua so sanh histogram
            list_distance[i - 1] = d

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
        arr_distance = np.array(list_distance.items(), dtype='float')
        temp = arr_distance[:, 1]
        total = np.nansum(temp)
        higher = 2* total / len(temp)
        return higher

    def calcBoundary(self, list_distance, list_threshold):
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
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        dirname = '/home/hoangnh/boundary/' + name + '_boundary/'
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
        print i
        cap.release()
