import cv2
import numpy as np
import os


class VideoDemo2:
    def __init__(self, link):
        self.link = link

    def validVideo(self):
        cap = cv2.VideoCapture(self.link)
        if not cap.isOpened():
            # print "Fatal error - could not open video."
            return {"flag": False, "info": "Not Video Format"}
        else:
            # print "Parsing video..."
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # print "Video Resolution: %d x %d" % (width, height)
            start = self.link.rfind('/')
            name = self.link[start + 1: len(self.link)]
            info = name + ": " + str(width) + " x " + str(height)
            return {"flag":True, "info": info}
    def calcDifferent(self):
        cap = cv2.VideoCapture(self.link)
        i = 0
        hist_new = np.array([])
        hist_old = np.array([])
        list_distance = {}
        list_hist = {}

        # tinh histogram cho frame do va tinh khoang cach voi frame phia truoc
        while (cap.isOpened()):
            # Doc cac frame trong video
            ret, frame = cap.read()

            # Neu khong con frame nao thi ket thuc
            if (ret != True):
                break
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #             img = self.histogram_equalize(frame)
            # Tinh histogram
            hist_new = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8],
                                    [0, 256, 0, 256, 0, 256])
            #             cv2.normalize(hist,hist_new).flatten()
            list_hist[i] = hist_new

            # Neu la frame dau tien thi chua can so sanh
            if (i == 0):
                i = i + 1
                hist_old = hist_new
                continue

            # Neu khong phai la frame dau tien, so sanh histogram
            # Luu y: tham so thu 3 cua ham compareHist nhan 4 gia tri 0,1,2,3 tuong ung voi cac cach tinh khoang cach
            d = cv2.compareHist(hist_new, hist_old, 3)

            # if (np.isnan(d)):
            #     print "nan %d", i
            #     d = 1
            # Them vao ket qua so sanh histogram
            list_distance[i - 1] = d
            # Tang i, cho hist_new thanh hist_old de tinh tiep
            i = i + 1
            hist_old = hist_new

        print i
        cap.release()
        return {"list_distance": list_distance, "list_hist": list_hist}

    def getThresholds(self, list_distance):
        x = sorted(list_distance.values(), reverse=True)
        x = np.array(x, dtype='float')
        x = x[np.where(x > 0)]
        len_c = int(len(x) / 50)
        len_s = int(len(x) / 10)
        t_c = x[0:len_c].sum() / len_c
        t_s = x[0:len_s].sum() / len_s
        return {"t_c": t_c, "t_s": t_s}

    def getBoundary(self, t_c, t_s, list_distance, list_hist):
        # Lay cac diem hard cut va co the la soft cut
        list_hardcut = {}
        list_softcut = {}
        index_hard = 0
        index_soft = 0
        for i in range(len(list_distance)):
            if list_distance[i] > t_c:
                list_hardcut[index_hard] = i
                index_hard = index_hard + 1
                continue
            if list_distance[i] > t_s:
                list_softcut[index_soft] = i
                index_soft = index_soft + 1

        # lay cac diem short cut thuc su
        list_softcut_real = {}
        index = 0
        cut_now = 0
        for i in range(len(list_softcut)):
            check = list_softcut[i]
            if check <= cut_now:
                continue
            ref_hist = list_hist[check]
            for j in range(check + 1, check + 71):
                d = cv2.compareHist(list_hist[j], ref_hist, 3)
                if (np.isnan(d)):
                    d = 0
                if d > t_c:
                    list_softcut_real[index] = j - 1
                    cut_now = j - 1
                    print "Check:", check, "Cut:", cut_now
                    index = index + 1
                    break

        index = len(list_hardcut)
        for i in range(len(list_softcut_real)):
            list_hardcut[index] = list_softcut_real[i]
            index = index + 1

        # loai bo cac diem cut bi trung
        list_cut = sorted(list_hardcut.values())
        i = 1
        while (i < len(list_cut)):
            if list_cut[i] <= list_cut[i - 1] + 1:
                del list_cut[i]
                continue
            i = i + 1

        list_boundary = {}
        for i in range(0, len(list_cut)):
            list_boundary[i] = list_cut[i]
        return list_boundary


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
        # dirname = '/home/hoangnh/boundary/' + name + '_boundary/'
        dirname = os.path.expanduser('~') + "/video_database/" + name + "/" + name + '_boundary/'
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

    def getKeyFrame(self, list_boundary):
        # lay cac keyframe trong video
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        # dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_keyframe/'
        dirname = os.path.expanduser('~')+ "/video_database/"+ name +"/" + name + '_keyframe'
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

    def getShotVideo(self, list_end):
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        # dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_shotvideo/'
        dirname = os.path.expanduser('~') + "/video_database/" + name + "/" + name + '_shotvideo/'
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
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        shotpath = dirname + "shot0.avi"
        out2 = cv2.VideoWriter(shotpath, fourcc, fps, (width, height))
        index2 = 0
        # lengthShot = len(list_end) - 1
        # loop through again video then get shot                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ame and shot
        for i in range(length):
            # Capture frame-by-frameOCN
            ret, frame = cap.read()
            # calculate the constrast
            if (ret != True):
                break
            if ((i == int(list_end[index2] + 1))):
                index2 = index2 + 1
                out2.release()
                shotpath = dirname + 'shot%d.avi' % index2
                out2 = cv2.VideoWriter(shotpath, fourcc, fps,
                                       (width, height))
                out2.write(frame)
                # if (index2 >= lengthShot):
                #     break
            else:
                out2.write(frame)