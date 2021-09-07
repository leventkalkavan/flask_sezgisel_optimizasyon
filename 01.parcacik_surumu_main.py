from __future__ import division
import  random
from flask import Flask , render_template
#Gerekli kütüphaneleri ekliyoruz.
SehirMatrisi = [[0 , 29 , 20 , 21 , 16 , 31 , 100 ,12 , 4  , 31 ],
[29 , 0  , 15 , 29 , 28 , 40 , 72 , 21 , 29 , 41 ],
[20 , 15 , 0  , 15 , 14 , 25 , 81 , 9  , 23 , 27 ],
[21 , 29 , 15 , 0  , 4 ,  12 , 92 , 12 , 25 , 13 ],
[16 , 28 , 14 , 4  , 0 ,  16 , 94 , 9  , 20 , 16 ],                               
[31 , 40 , 25 , 12 , 16 , 0 ,  95 , 24 , 36 , 3 ],
[100 ,72 , 81 , 92 , 94 , 95 , 0 ,  90 , 101 ,99 ],
[12 , 21 , 9 ,  12 , 9  , 24 , 90 , 0  , 15 , 25 ],
[4  , 29 , 23 , 25 , 20 , 36 , 101 ,15 , 0 ,  35,],
[31 , 41 , 27 , 13 , 16 , 3 ,  99,  25,  35,  0 ]]

SehirListesi=list(range(0,len(SehirMatrisi)))
parcacikSayisi=30
iterasyon=100
parcacik = []
hiz=[]
pBestonceki = []
parcacikOnceki=[]
beta = 0.8
alfa =0.8

for i in range(0,parcacikSayisi):
 rota= random.sample(SehirListesi, len(SehirListesi))
 parcacik.append(rota)

for i in range(parcacikSayisi):
   pBestonceki.append(1000)
gBestOnceki=1000

parcacikOnceki.extend(parcacik)
hiz=[]

for t in range(iterasyon):
 pozisyon = []
parcacikMesafe = []
toplam = 0

for i in range(0, parcacikSayisi):
      for j in range(1, len(SehirListesi)):
          a = (parcacik[i][j - 1])
          b = (parcacik[i][j])
          parcacikMesafe.append([])
          parcacikMesafe[i].append(SehirMatrisi[a][b])
          toplam += parcacikMesafe[i][j - 1]
      pozisyon.append(toplam)
      toplam = 0

pBest = []
pBestyol = []
#Her bir parçacığın önceki pbest değeri ile karşılaştırıp kişisel en iyi pozisyonunu bulma ve güncelleme
for i in range(len(parcacik)):
      if pBestonceki[i] <= pozisyon[i]:
          pBest.append(pBestonceki[i])
          pBestyol.append(parcacikOnceki[i])
      elif pBestonceki[i] > pozisyon[i]:
          pBest.append(pozisyon[i])
          pBestyol.append(parcacik[i])

          gBestyol = []
gBest = min(pBest)
if gBest <= gBestOnceki:
 for i in range(len(pBestyol)):
      if gBest == pBest[i]:
          gBestyol.append(pBestyol[i])
          break
elif gBest > gBestOnceki:
    if gBest == pBestonceki[i]:
        gBestyol.append(parcacikOnceki[i])
del parcacikOnceki[:]
parcacikOnceki.extend(parcacik)
for k in range(len(parcacik)):
 del hiz[:]
 temp_hiz = []
for i in range(len(parcacik)):
   for j in range(len(SehirListesi)):
      if  parcacik[i][j] != pBestyol[i][j]:
       takas_operator = (j, pBestyol[i].index(parcacik[i][j]), alfa)
       temp_hiz.append(takas_operator)
    
       aux = pBestyol[i][takas_operator[0]]
       pBestyol[i][takas_operator[0]] = pBestyol[i][takas_operator[1]]
       pBestyol[i][takas_operator[1]] = aux

for i in range(len(parcacik)):
   for j in range(len(SehirListesi)):
    if parcacik[i][j] != gBestyol[0][j]:
     
       takas_operator=(j, gBestyol[0].index(parcacik[i][j]), beta)
    
       temp_hiz.append(takas_operator)
    
       aux = gBestyol[0][takas_operator[0]]
       gBestyol[0][takas_operator[0]] = gBestyol[0][takas_operator[1]]
       gBestyol[0][takas_operator[1]] = aux
hiz.append(temp_hiz)
for takas_operator in temp_hiz:
   if random.random() <= takas_operator[2]:

       aux = parcacik[k][takas_operator[0]]
       parcacik[k][takas_operator[0]] = parcacik[k][takas_operator[1]]
       parcacik[k][takas_operator[1]] = aux
del pBestonceki[:]
pBestonceki.extend(pBest)
gBestOnceki=gBest

print("EN İYİ YOL")
print(gBestyol)
print(gBest)

app = Flask(__name__)

@app.route('/parcaciksuru')
def parcaciksurusu():
    return render_template("parcaciksuru.htm",gBestyol=gBestyol,gBest=gBest)
   
if __name__ == "__main__":
    app.run(debug=True)
 
