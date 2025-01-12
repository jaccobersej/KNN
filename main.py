import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import math
# import time

# st = time.time()
learning_data = []
k_values = []
bestKValue = []
BestEucTestpoints = []
BestMinkTestpoints = []
BestCosTestpoints = []

accuracyEuc = []
accuracyMink = []
accuracyCos = []
colors = ['cornflowerblue', 'lightcoral', 'springgreen']
for qwerty in range(0, 300):
    data = np.array(pd.read_excel("C:/Users/Marcu/Downloads/Iris_data.xlsx", nrows=150))  # Indlæs data som pandas dataframe og transformer den til et numpy array
    np.random.shuffle(data)  # bland dataen så vi kan have tilfældig trænings- og testdata
    data[data == 'setosa'] = 0
    data[data == 'versicolor'] = 1  # Omdan de tre labels til tal eftersom det er nemmere at håndtere
    data[data == 'virginica'] = 2
    learning_data, test_data = data[0:100], data[100:150]  # split datasættet op i træning- og testdata ved at splice de første 100 til træningsdata og de sidste 50 til testdata
      # definer farver til når vi skal visualisere vores data.
    k_values = []  #
    originalData = data.copy()
    for value in range(1, 49, 2):
        k_values.append(value)


    def EucDist(test_point, learning_point):
        return np.sqrt(np.sum((test_point[0:4] - learning_point[0:4]) ** 2))


    def MinkDist(test_point, learning_point):
        return np.sqrt(np.sum(abs((test_point[0:4] - learning_point[0:4])) ** 3) ** 1 / 3)


    def CosDist(test_point, learning_point):
        return math.cos(-((np.dot(test_point[0:4], learning_point[0:4]) / (
                    (np.sum(test_point[0:4]) ** 2) * (np.sum(learning_point[0:4]) ** 2)))))


    def sortAndLabel(Distances, k):
        arr = np.array(Distances)
        k_sorted = np.argsort(arr)[:k]
        labels = learning_data[k_sorted]
        predLabel = stats.mode(labels)[0][0][4]
        return predLabel


    def accuracy(Tested_points):
        right = 0
        for index, point in enumerate(Tested_points):
            if (point[4] == originalData[100 + index][4]):
                right += 1
        accuracyPercent = right / len(test_data)
        return accuracyPercent


    BestEucTestpoints = []
    BestMinkTestpoints = []
    BestCosTestpoints = []

    accuracyEuc = []
    accuracyMink = []
    accuracyCos = []

    for k in k_values:
        EucTestpoints = []
        MinkTestpoints = []
        CosTestpoints = []
        for test_point in test_data:
            EucDistances = []
            MinkDistances = []
            CosDistances = []
            for learning_point in learning_data:
                EucDistances.append(EucDist(test_point, learning_point))
                MinkDistances.append(MinkDist(test_point, learning_point))
                CosDistances.append(CosDist(test_point, learning_point))
            EucTestpoints.append(
                [test_point[0], test_point[1], test_point[2], test_point[3], sortAndLabel(EucDistances, k)])
            MinkTestpoints.append(
                [test_point[0], test_point[1], test_point[2], test_point[3], sortAndLabel(MinkDistances, k)])
            CosTestpoints.append(
                [test_point[0], test_point[1], test_point[2], test_point[3], sortAndLabel(CosDistances, k)])

        if k == 1:
            BestEucTestpoints = EucTestpoints, accuracy(EucTestpoints)
            BestMinkTestpoints = MinkTestpoints, accuracy(MinkTestpoints)
            BestCosTestpoints = CosTestpoints, accuracy(CosTestpoints)
        if BestEucTestpoints[1] < accuracy(EucTestpoints):
            BestEucTestpoints = EucTestpoints, accuracy(EucTestpoints)
        if BestMinkTestpoints[1] < accuracy(MinkTestpoints):
            BestMinkTestpoints = MinkTestpoints, accuracy(MinkTestpoints)
        if BestCosTestpoints[1] < accuracy(CosTestpoints):
            BestCosTestpoints = CosTestpoints, accuracy(CosTestpoints)
        accuracyEuc.append(accuracy(EucTestpoints))
        accuracyMink.append(accuracy(MinkTestpoints))
        accuracyCos.append(accuracy(CosTestpoints))

    bestIndex = None
    for index, curAccu in enumerate(accuracyEuc):
        if bestIndex != None and accuracyEuc[bestIndex]+0.001 < curAccu:
            bestIndex = index
        if bestIndex == None:
            bestIndex = index
    bestKValue.append(k_values[bestIndex])
    print(k_values[bestIndex])

figure, axis = plt.subplots(3, 3)
figure.set_figheight(12)
figure.set_figwidth(12)

for point in learning_data:
    axis[0, 0].scatter(point[2], point[3], c=colors[point[4]])
    axis[1, 0].scatter(point[2], point[3], c=colors[point[4]])
    axis[2, 0].scatter(point[2], point[3], c=colors[point[4]])

    axis[0, 1].scatter(point[0], point[1], c=colors[point[4]])
    axis[1, 1].scatter(point[0], point[1], c=colors[point[4]])
    axis[2, 1].scatter(point[0], point[1], c=colors[point[4]])

axis[0, 0].set_title('Euclidean Distance')
axis[1, 0].set_title('Minkowski Distance P = 1/3')
axis[2, 0].set_title('Cosine similarity')

for Eucpoint in BestEucTestpoints[0]:
    axis[0, 0].scatter(Eucpoint[2], Eucpoint[3], c=colors[Eucpoint[4]], edgecolors='black')
    axis[0, 1].scatter(Eucpoint[0], Eucpoint[1], c=colors[Eucpoint[4]], edgecolors='black')

for Minkpoint in BestMinkTestpoints[0]:
    axis[1, 0].scatter(Minkpoint[2], Minkpoint[3], c=colors[Minkpoint[4]], edgecolors='black')
    axis[1, 1].scatter(Minkpoint[0], Minkpoint[1], c=colors[Minkpoint[4]], edgecolors='black')

for Cospoint in BestCosTestpoints[0]:
    axis[2, 0].scatter(Cospoint[2], Cospoint[3], c=colors[Cospoint[4]], edgecolors='black')
    axis[2, 1].scatter(Cospoint[0], Cospoint[1], c=colors[Cospoint[4]], edgecolors='black')

axis[0, 2].plot(k_values, accuracyEuc)
axis[1, 2].plot(k_values, accuracyMink)
axis[2, 2].plot(k_values, accuracyCos)

print(bestKValue)
valueArray = np.array(bestKValue)
print(valueArray)
average = np.sum(valueArray) / len(valueArray)
bestKValue = average
print(bestKValue)

axis[0, 2].set_title('ED accuracy')
axis[1, 2].set_title('MD, P=1/3 accuracy')
axis[2, 2].set_title('CS accuracy')

plt.show()

