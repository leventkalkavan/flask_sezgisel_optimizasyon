from random import sample, uniform , randint
import math
from flask import Flask, render_template

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

def calculateDistance(path):
       index = path[0]             #Düğümler arası uzaklık hesabı
       distance = 0
       for nextIndex in path[1:]:
               distance += distanceMatrix[index][nextIndex]
               index = nextIndex
       return distance;

def swap(sequence,i,j):
       temp = sequence[i]     #Düğüm yer değiştirme fonksiyonu
       sequence[i]=sequence[j]
       sequence[j]=temp
def elimination(bacteria,a,b,c,d):
   bacteria = bacteria[0][:]              #Eliminasyon süreci
   swap(bacteria,a,b)
   swap(bacteria,b,c)
   swap(bacteria,c,d)
   swap(bacteria,a,d)
   return (bacteria,calculateDistance(bacteria))

def kemotaxis(bacteria,a,b):
  bacteria = bacteria[0][:]       #Kemotaksis süreci
  swap(bacteria,a,b)
  return (bacteria,calculateDistance(bacteria))

numBacteria = 10   #Bakteri sayısı
worstBacteria = int(0.5*numBacteria) #Değersiz bakteriler

maxGen = 20  #Bakteri jenerasyon sayısı

n = len(distanceMatrix)  #Düğümlerin sayısı

bacteria = []   #Bakteriler için array

initPath=list(range(0,n)) #Rota
index = 0
for i in range(numBacteria):
   rota = sample(initPath, n)
   bacteria.append((rota,calculateDistance(rota)))  #Bakteri sayısı kadar rastgele rota oluşturup yuvalara atanması işlemi

bacteria.sort(key=lambda x: x[1])    #Bakterilerin maliyete göre sıralanması
for i in range(maxGen):
   bestBacterium = bacteria[0]    #Düşük maliyetli bakteriyi göç için seç

   for j in range (n):
       copyBestBacterium=kemotaxis(bestBacterium,randint(0,n-1),randint(0,n-1))    #kemotaksis

       if (bacteria[j][1] > copyBestBacterium[1]):   #Bir sonraki bakteri maliyeti daha yüksekse bakterileri değiştir.
           bacteria[j] = copyBestBacterium
   bacteria.sort(key=lambda x: x[1])

   for k in range(numBacteria - worstBacteria, numBacteria):        #Kötü değerli bakterileriler yeniden işleniyor
       bacteria[k] = kemotaxis(bacteria[k], randint(0, n - 1),randint(0, n - 1)) #Üreme
   bacteria.sort(key=lambda x: x[1])

   if(randint(0,10000)==0):
       for j in range(n):    #Eliminasyon işlemi  %0.01 ihtimalle
                    bacteria[j] = elimination(bestBacterium,randint(0, n - 1),randint(0, n - 1),randint(0, n - 1),randint(0, n - 1))
       bacteria.sort(key=lambda x: x[1])

print ("Çözüm Kümesi") #Bulduğu en iyi çözümü yazdır.
print(bacteria[0])

app = Flask(__name__)

@app.route("/bakteri")
def bakteri():
    return render_template ("bakteri.htm", bacteria=bacteria)

if __name__ =="__main__":

    app.run(debug=True)
