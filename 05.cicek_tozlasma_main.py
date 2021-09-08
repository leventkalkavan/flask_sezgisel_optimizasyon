import numpy    # Dizi üretme vb. işlemlerde kolaylık sağlamaktadır.
import math     # Matematiksel işlemler için eklenmiştir.
import random   # Random bazlı üretim işlemleri için eklenmiştir.
from flask import Flask, render_template

#Travelling Salessman Problem (Gezgin Satıcı Problemi, veri setimiz)
distanceMatrix = [[0 , 29 , 20 , 21 , 16 , 31 , 100 ,12 , 4  , 31],
[29 , 0  , 15 , 29 , 28 , 40 , 72 , 21 , 29 , 41],
[20 , 15 , 0  , 15 , 14 , 25 , 81 , 9  , 23 , 27],
[21 , 29 , 15 , 0  , 4 ,  12 , 92 , 12 , 25 , 13],
[16 , 28 , 14 , 4  , 0 ,  16 , 94 , 9  , 20 , 16],
[31 , 40 , 25 , 12 , 16 , 0 ,  95 , 24 , 36 , 3],
[100 ,72 , 81 , 92 , 94 , 95 , 0 ,  90 , 101 ,99],
[12 , 21 , 9 ,  12 , 9  , 24 , 90 , 0  , 15 , 25],
[4  , 29 , 23 , 25 , 20 , 36 , 101 ,15 , 0 ,  35],
[31 , 41 , 27 , 13 , 16 , 3 ,  99,  25,  35,  0]]

#CONSTANTS (Sabitler):
n=10                       # Popülasyon büyüklüğü
dimension=10               # Boyut Sayısı
iterationSize=100000       # İterasyon sayısı
transitionProbability=0.8  # Geçiş olasılığı sabiti

# dimension: Boyut sayısı
# willBeProccessed: Döndürülecek popülasyon

def createRandomSolution(dimension):
    willBeProccessed=list(range(0,n))
    random.shuffle(willBeProccessed)
    return willBeProccessed

# solution: Gelen popülasyon
# total Distance: Toplam mesafe
# index - nextIndex: İndis numaraları

def calculateCost(solution):
    totalDistance = 0
    index = solution[0]

    for nextIndex in solution[1:]:
        totalDistance += distanceMatrix[index][nextIndex]
        index = nextIndex

    return totalDistance

# sequence: Gelen dizi
# i ve j: Değiştirilecek dizi elemanlarının indis numaraları
# temp: Swap işlemlerinde kullanılan geçici değişken.

def swap(sequence, i, j):
    temp = sequence[i]
    sequence[i] = sequence[j]
    sequence[j] = temp

# cloneSolution : Klon popülasyon
# index1, index2, index3, index4 : Random olarak üretilen indisler.

def globalPollination(cloneSolution,n):
    index1=random.randint(0, n-1)
    index2=random.randint(0, n-1)

    index3=random.randint(0, n-1)
    index4=random.randint(0, n-1)

    swap(cloneSolution,index1,index2)
    swap(cloneSolution, index3, index4)

    return cloneSolution

# cloneSolution : Klon popülasyon
# index1, index2 : Random olarak üretilen indisler.

def localPollination(cloneSolution,n):
    index1 = random.randint(0, n-1)
    index2 = random.randint(0, n-1)

    swap(cloneSolution,index1,index2)

    return cloneSolution
# solutions: Popülasyon listesi
# costs: Maliyetler dizisi

solutions = (numpy.ones((n, dimension),dtype=int) * -1).tolist()
costs = numpy.zeros((n, 1), dtype=int)

for i in range(0, n):
    solutions[i] = createRandomSolution(dimension)
    costs[i] = calculateCost(solutions[i])


# minCost: Minimum maliyet
# minFitnessIndex: Minimum maliyetin indis numarası
# bestSolution: En iyi çözüm kümesi
# cloneSolution: Klon çözüm kümesi

minCost = costs.min(0)

minFitnessIndex = (costs.argmin(0))[0]
bestSolution = solutions[minFitnessIndex]
cloneSolution = solutions.copy()

for iterationIndex in range(0, iterationSize):
    for i in range(0, n):
        if numpy.random.random() < transitionProbability:
            # global pollination
            # L = levy(dimension)
            # cloneSolution[i] = solutions[i] + L * (solutions[i] - bestSolution)
            cloneSolution[i]=globalPollination(cloneSolution[i],n)
        else:
            # local pollination
            #epsilon = numpy.random.random_sample()
            #jk = numpy.random.permutation(n)
            # cloneSolution[i] = cloneSolution[i] + epsilon * (solutions[jk[0]] - solutions[jk[1]])
            cloneSolution[i]=localPollination(cloneSolution[i],n)

        newCost = calculateCost(cloneSolution[i]) # Yeni maliyet

        if newCost <= costs[i]:
            solutions[i] = cloneSolution[i]
            costs[i] = newCost
        if newCost <= minCost:
            bestSolution = cloneSolution[i]
            minCost = newCost

print("Best solution:  ", end='')
print(bestSolution)
print("Minimum cost:  ", end='')
print(minCost)

app = Flask(__name__)
@app.route("/cicek")
def cicek():
    return render_template ("cicek.htm", bestSolution=bestSolution, minCost=minCost)

if __name__ =="__main__":

    app.run(debug=True)
