from flask import Flask, render_template
from random import uniform , randint
import math
distanceMatrix = [[0 , 29 , 20 , 21 , 16 , 31 , 100 ,12 , 4  , 31],
[29 , 0  , 15 , 29 , 28 , 40 , 72 , 21 , 29 , 41],
[20 , 15 , 0  , 15 , 14 , 25 , 81 , 9  , 23 , 27],                    #Gezgin Satıcı Problemi
[21 , 29 , 15 , 0  , 4 ,  12 , 92 , 12 , 25 , 13],
[16 , 28 , 14 , 4  , 0 ,  16 , 94 , 9  , 20 , 16],
[31 , 40 , 25 , 12 , 16 , 0 ,  95 , 24 , 36 , 3],
[100 ,72 , 81 , 92 , 94 , 95 , 0 ,  90 , 101 ,99],
[12 , 21 , 9 ,  12 , 9  , 24 , 90 , 0  , 15 , 25],
[4  , 29 , 23 , 25 , 20 , 36 , 101 ,15 , 0 ,  35],
[31 , 41 , 27 , 13 , 16 , 3 ,  99,  25,  35,  0]]



def levyFlight(u):
	return math.pow(u,-1.0/3.0) #Levy uçuşu formülü

def randF():
	return uniform(0.0001,0.9999)  #0 ile 1 arasında eşit dağılımlı rastgele bir sayı

def calculateDistance(path):
        index = path[0]             #Düğümler arası uzaklık hesabı
        distance = 0
        for nextIndex in path[1:]:
                distance += distanceMatrix[index][nextIndex]
                index = nextIndex
        return distance;

def swap(sequence,i,j):
        temp = sequence[i]    #Düğüm yer değiştirme fonksiyonu
        sequence[i]=sequence[j]
        sequence[j]=temp

def twoOptMove(nest,a,b):
	nest = nest[0][:]       #Düğüm karıştırma fonksiyonu
	swap(nest,a,b)
	return (nest,calculateDistance(nest))
	

def doubleBridgeMove(nest,a,b,c):
	nest = nest[0][:]               #Düğüm karıştırma fonksiyonu
	swap(nest,a,b)
	swap(nest,b,c)
	return (nest , calculateDistance(nest))

numNests = 10                       #Yuva sayısı
worstNests = int(0.2*numNests)      #Yüksek maliyetli yuvalar
bestNests = int(0.6*numNests)       #Düşük maliyetli yuvalar

alfa=5;    #YY için sabit parametreler.
yMax=10;
yMin=0;

maxGen = 100          #Jenerasyon sayısı (Bitirme kriteri)

n = len(distanceMatrix)     #Düğümlerin sayısı

YY=alfa*1/n*(yMax-yMin);  #Yumurtlama yarıçapı

nests = []                  #Yuva için array

initPath=list(range(0,n))   #Rota
index = 0

for i in range(numNests):
	if index == n-1:
		index = 0
	swap(initPath,index,index+1)          #Yuva sayısı kadar rota oluşturulup yuvalara atanması işlemi
	index+=1
	nests.append((initPath[:],calculateDistance(initPath)))

nests.sort(key=lambda x: x[1])            #Yuvaların maliyete göre sıralanması

for t in range(maxGen):

	cuckooNest = nests[randint(0,bestNests)]    #Düşük maliyetli yuvaları göç için seç

	if(levyFlight(randF())>2):      #Levy uçuşundan gelen değer 2 den büyükse Double Bridge hareketini kullanarak düğümleri karıştır.
		cuckooNest = doubleBridgeMove(cuckooNest,randint(0,n-1),randint(0,n-1),randint(0,n-1))
	else:                           #Levy uçuşundan gelen değer 2 den küçüks Two Opt hareketini kullanarak düğümleri karıştır.
		cuckooNest = twoOptMove(cuckooNest,randint(0,n-1),randint(0,n-1))
	randomNestIndex = randint(0,YY) #Yumurtalama yarıçapına göre yuvayı belirle.

	if(nests[randomNestIndex][1]>cuckooNest[1]):  #Bir sonraki yuva maliyeti daha yüksekse yuvaları değiştir.
		nests[randomNestIndex] = cuckooNest

	for i in range(numNests-worstNests,numNests):
		nests[i] = twoOptMove(nests[i],randint(0,n-1),randint(0,n-1))   #Yüksek maliyetli yuvaları Two Opt hareketiyle karıştır.
	nests.sort(key=lambda x: x[1]) #Yuvalarıın maliyetlerini sırala

print ("Çözüm Kümesi") #Bulduğu en iyi çözümü yazdır.
print(nests[0])
  
                                 
app = Flask(__name__)


@app.route('/gugukkusu')
def gugukkusu():
    return render_template ("gugukkusu.htm", nests=nests)


if __name__ =="__main__":

    app.run(debug=True)
