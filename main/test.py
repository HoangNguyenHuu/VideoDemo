from MyVideo import VideoDemo
import numpy as np
import matplotlib.pyplot as plt


video = VideoDemo("/home/hoangnh/OpenCVJupyter/kungfupanda3.mov")
list_distance = video.calcDifferent();

# Chuyen ve dang numpy.array de ve do thi tren matplotlib
array_distance = np.array(list_distance.items(), dtype='float') # khoang cach
# # Ve do thi the hien su chenh lech histogram theo thu tu cac frame, o day chi lay 200 frame tu 0 den 200
# plt.plot(array_distance[0:300, 0], array_distance[0:300, 1])
# plt.ylabel('distance')
# plt.show()
#
# list_second = video.calcSecondDerivative(list_distance)
# array_second = np.array(list_second.items(), dtype='float') # dao ham bac 2
# # lay dao ham bac 2, o day se co nhung diem local maximum rat cao, co the lay nguong de hon
# plt.plot(array_second[0:300, 0], array_second[0:300, 1])
# plt.ylabel('distance')
# plt.show()


higher = video.calcHigherDegree(list_distance)
list_threshold = video.calcAdaptiveThreshold(list_distance, 1, higher)
print higher
arr_threshold = np.array(list_threshold.items(), dtype='float') # nguong adaptive
# lay nguong theo apdaptive, cac diem cao hon nguong moi lay lam bien.
# duong mau xanh la so sanh histogram, duong mau do la adptive threshold

list_boundary = video.calcBoundary(list_distance, list_threshold)
print list_boundary

video.getBoundary(list_boundary)
plt.plot(arr_threshold[0:200, 0], arr_threshold[0:200, 1], 'red', array_distance[0:200, 0], array_distance[0:200, 1], 'blue')
plt.ylabel('distance')
plt.show()



