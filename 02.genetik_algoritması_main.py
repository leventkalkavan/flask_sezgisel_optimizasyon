from flask import Flask,render_template
import random
from typing import List

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
kromozomSayisi=30
#Baslangıç Popülasyonu Oluşturma
populasyon = []
for i in range(0,kromozomSayisi):
  rota= random.sample(SehirListesi, len(SehirListesi))
  populasyon.append(rota)

kureselEnIyicozum= []
kureselEnIyirota=[]
jenerasyon=0
while jenerasyon  <= 100:

 populasyonMesafe = []
 toplam = 0
 toplamMesafe = []
 # Her bir kromozomun toplam mesafesi hesaplama.
 for i in range(0,kromozomSayisi):
   for j in range(1,len(SehirListesi)):
     a= (populasyon [i][j-1])
     b= (populasyon [i][j])
     populasyonMesafe.append([])
     populasyonMesafe[i].append(SehirMatrisi[a][b])
     toplam+=populasyonMesafe[i][j-1]
   toplamMesafe.append(toplam)
   toplam=0

 # Amac fonksiyonuna göre her bir kromozomun uygunluk değeri hesaplama.
 uygunlukDegeri= []
 c = 0.0
 for i in range(len(toplamMesafe)):
    c = 1 / float(toplamMesafe[i])
    uygunlukDegeri.append(c)

 # Secme işlemi için Rulet Tekerleğinden yararlandım.
 toplamUygunluk=0
 for i in range (len(uygunlukDegeri)):
    toplamUygunluk+=uygunlukDegeri[i]
  #Her bir kromozomun olasılığını hesaplama.
 d=0.0
 olasilikUygunluk= []
 for i in range(len(uygunlukDegeri)):
     d= float(uygunlukDegeri[i]/toplamUygunluk)
     olasilikUygunluk.append(d)

 # Her bir kromozomun kümülatif ihtimalini hesaplama.
 kumulatifIhtimal=[]
 e=0.0
 for i in range(len(olasilikUygunluk)):
      e+=olasilikUygunluk[i]
      kumulatifIhtimal.append(e)

  #Hesapladığım bu ihtimale göre seçme işlemi.
 secilim=[]
 for i in range(0, kromozomSayisi):
        secme = random.random()

        for j in range(0, len(olasilikUygunluk)):
            if secme <= kumulatifIhtimal[j]:
                secilim.append(olasilikUygunluk[j])
                break
 temp_hiz=[]
 parcacik=[]
 k=[]
 for takas_operator in temp_hiz:
   if random.random() <= takas_operator[2]:

       aux = parcacik[k][takas_operator[0]]
       parcacik[k][takas_operator[0]] = parcacik[k][takas_operator[1]]
       parcacik[k][takas_operator[1]] = aux
 
 #Bu secme işleminden bir gen havuzu oluşturma.
 genHavuzu = []
 for i in range(0, len(secilim)):
    for j in range(0,len(secilim)):
         if secilim[i] == olasilikUygunluk[j]:
          genHavuzu.append(populasyon[j])

  #Bu havuzdan seçtiğim iki kromozomu çaprazlama.
 Cocuklar = []
 length = len(genHavuzu)
 havuz = random.sample(genHavuzu, len(genHavuzu))


 for i in range(0, length):
    cocuk = []
    cocukP1 = []
    cocukP2 = []
    Ebeveyn1= havuz[i]
    Ebeveyn2= havuz[len(genHavuzu) - i - 1]
    genA = int(random.random() * len(Ebeveyn1))
    genB = int(random.random() * len(Ebeveyn1))


    baslangicGen = min(genA, genB)
    bitisGen = max(genA, genB)


    for j in range(baslangicGen, bitisGen):
        cocukP1.append(Ebeveyn1[j])
    cocukP2 = [item for item in Ebeveyn2 if item not in cocukP1]


    cocuk = cocukP1 + cocukP2
    Cocuklar.append(cocuk)
  # Çaprazladığım kromozomlardan oluşan cocuk popülasyonu üzerinde mutasyon işlemi .Bu işlemi 0.01 olasılıkla gerçekleştirme
 mutasyonPop = []

 for ind in range(0, len(Cocuklar)):
    bireysel=Cocuklar[ind]

    for takas in range(len(bireysel)):
     if random.random() < 0.01:
        kromozomNo = int(random.random() * len(bireysel))

        Sehir1 = bireysel[takas]
        Sehir2 = bireysel[kromozomNo]

        bireysel[takas] = Sehir2
        bireysel[kromozomNo] = Sehir1
     mutasyon= bireysel
     mutasyonPop.append(mutasyon)
 populasyon=[]
 #Olusan yeni nesil bir sonraki iterasyonun ebeveyni
 for i in range(0, len(mutasyonPop)):
    populasyon.append(mutasyonPop[i])


 # Her neslin en iyi uygunluk degerine sahip kromozomunun bulma işlemi
 enIyiuygunluk=max(uygunlukDegeri)
 for i in range(len(uygunlukDegeri)):
  if enIyiuygunluk == uygunlukDegeri[i]:
    kureselEnIyicozum.append(enIyiuygunluk)
    enIyiuygunluk = 0
 jenerasyon=jenerasyon+1

#Her neslin en iyi kromozomları arasındaki en iyi uygunluk degerine sahip kromozomu bulma
enIyiyol=[]
enIyimesafe=[]
kureselEniyi= max(kureselEnIyicozum)
for i in range (len(kureselEnIyicozum)):
    if kureselEniyi == kureselEnIyicozum[i]:
      enIyiyol.append(populasyon[i])
      break

enIyiyolMesafe=[]
mesafeToplam=0

for i in range(0, len(enIyiyol)):
  for j in range (1,len(SehirListesi)):
        a = (enIyiyol[i][j - 1])
        b = (enIyiyol[i][j])
        enIyiyolMesafe.append([])
        enIyiyolMesafe[i].append(SehirMatrisi[a][b])
        mesafeToplam += enIyiyolMesafe [i][j - 1]

print(enIyiyol)
print(mesafeToplam)

app = Flask(__name__)


@app.route("/genetik_algoritma")
def genetik_algoritma():
    return  render_template ("genetik_algoritma.htm",enIyiyol=enIyiyol,mesafeToplam=mesafeToplam )

if __name__ =="__main__":

    app.run(debug=True)
