import cv2
import numpy as np
import os
import operator


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

    def calcHigherDegree(self, list_distance):
        arr_distance = np.array(list_distance.items(), dtype='float')
        temp = arr_distance[:, 1]
        total = np.nansum(temp)
        higher = 3 * total / len(temp)
        return higher

    def calcBoundary(self, list_distance, list_threshold):
        list_bounary = {}
        j = 0
        for i in range(0, len(list_distance)):
            if (list_distance[i] > list_threshold[i]):
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
        list_distance_sort = reversed(sorted(list_distance.items(), key=operator.itemgetter(1)))
        max_distance = max(list_distance, key=list_distance.get)
        min_distance = min(list_distance, key=list_distance.get)
        print "###########max_distance"
        print max_distance
        print "###########min_distance"
        print min_distance
        print "##############"
        print list_distance_sort
        for item in list_distance_sort:
            if self.isChangeShot(item[0], 10):
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

    def isChangeShot(self, position, threshold):
        if position < 1 or position > (len(list_distance)-2):
            return False
        if list_distance[position] == 0:
            return False
        # if (position < len(list_distance) - 1) and list_distance[position+1] == 0 :
        if list_distance[position-1] != 0 and list_distance[position+1] != 0 and \
                (list_distance[position]/list_distance[position-1] > threshold) and \
                (list_distance[position]/list_distance[position+1] > threshold):
            return True
        return False

