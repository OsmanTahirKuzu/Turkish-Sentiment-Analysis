from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


from snowballstemmer import TurkishStemmer

import pandas as pd
df_cumleler = pd.read_csv("cumleler.csv", encoding="UTF-8", sep=";")

df_kelimeler = pd.read_csv("kelimeler.csv", encoding="UTF-8", sep=";")

# kontrol işlemlerinde kolaylık için ayrılması gerekiyor
kelime_Ol_i_s = []
kelime_Ol_f = []
kelime_Olsuz_i_s = []
kelime_Olsuz_f = []


def main():
    #-------Kelimelerin stemmerdan geçirilmesi----------------------------------------
    #nanları almammak için sayi girdim range içine (istenen türden kaç tane varsa).
    for x in range(339):
        kelime_Ol_i_s.append(kelimeStemmer(df_kelimeler["olumlu isim&sıfat"][x]))
        #print(kelime_Ol_i_s[x])
    for x in range(262):
        kelime_Ol_f.append(kelimeStemmer(df_kelimeler["olumlu fiil"][x]))
        #print(kelime_Ol_f[x])
         
    for x in range(393):
        kelime_Olsuz_i_s.append(kelimeStemmer(df_kelimeler["olumsuz isim&sıfat"][x]))
        #print(kelime_Olsuz_i_s[x])
    for x in range(282):
        kelime_Olsuz_f.append(kelimeStemmer(df_kelimeler["olumsuz fiil"][x])) 
        #print(kelime_Olsuz_f[x])   
    #-----End-------------------------------------------------------------------------    
    DogruSonucArtir = 0 # 1200 cümlede Karar fonksiyonuyla bulduğumuz sonuc ile cumlenin belirtilen sınıfı uyuşuyorsa 1 artırılacak
    
    #cümleler veri setimizdeki hangi cümleyi kontrol edeceğimizin seçilmesi
    for x in range(len(df_cumleler["Cümle"])):

        cumle = df_cumleler["Cümle"][x]
        
        stemmerSonrasi = Stemmer(cumle)#liste halinde cümlenin kelimeleri döner

        kontrol = Karar(stemmerSonrasi)#0,1 veya -1 döner 
        
        # print(stemmerSonrasi)
        # print(df_cumleler["Sınıf"][x])
        # print(kontrol)

        #pozitif = 1,negatif = -1,nötr = 0
        if df_cumleler["Sınıf"][x] =="Pozitif" and kontrol == 1:
            DogruSonucArtir += 1      
        elif df_cumleler["Sınıf"][x] =="Negatif" and kontrol == -1:
            DogruSonucArtir += 1
        elif df_cumleler["Sınıf"][x] =="Nötr" and kontrol == 0:
            DogruSonucArtir +=1

    return ((DogruSonucArtir + 1)/1200)*100 #yüzde kaç doğru hesaplanıyor onu döndürür


import re
# kelimenin kökünü almak için
def kelimeStemmer(kelime):
    kelime = kelime.lower()
    rootWord = kelime
    #mek mak ları giderdik
    x = re.findall("m.k$", rootWord)    
    if x:
        rootWord = rootWord.replace(rootWord[-3:],"")

    ps =TurkishStemmer()
    if len(kelime)>5:
        
        rootWord = ps.stemWord(kelime)   
         
    else:
        rootWord = kelime
    #print(rootWord)

    return rootWord # iki kelime olan kelimelerin ilk kelimesini alıyor. yok olmak -> yok


# cümlelerdeki noktalama ve stopwordslerin cümlelerden kaldırılması + cümledeki bütün kelimelerin kökleri
def Stemmer(cumle):
    cumle= cumle.lower()

    mypunc= [".",":",";",",", "\"","\'","<",">","(",")"]

    #cümlelere ayrılmak istenirse
    #mysentences=sent_tokenize(cumle)
    
    for chk in cumle:
        if chk in mypunc:
            cumle = cumle.replace(chk, "")

    words = word_tokenize(cumle)

    # stop words
    stopWords = set(stopwords.words('turkish'))
    wordsU=[]

    # stopwordsleri ele
    for w in words:
        if w not in stopWords:
            wordsU.append(w)

    all_stem_lists = []
    ps =TurkishStemmer()
    for w in wordsU:
        if len(w) >5 : # iyi i olduğu için 
            rootWord=ps.stemWord(w)
        else:
            rootWord = w

        all_stem_lists.append(rootWord)
        
    
    return all_stem_lists
def Karar(stemmerSonrasi):
    kontrol = 1
    flag = 0# nötr kontrolünü sağlamak için kullanıyorum
    
    j = 0        
    while j < len(stemmerSonrasi):  
    # hem sondaki ikilileri kontrol eder hem de kelimeler olumlu mu olumsuz mu yoksa nötr mü onu belirler
        if flag == 0:
            for k in range(393): 
                if stemmerSonrasi[len(stemmerSonrasi)-1] == ("değil") and (stemmerSonrasi[len(stemmerSonrasi)-2] == kelime_Olsuz_i_s[k]):
                    kontrol*=1
                    flag = 1
                    break 
                #cümlenin kelimelerinin teker teker kontrol edilmesi df_kelimelerde ilgili sınıfın kontrol edilmesi
                elif stemmerSonrasi[j] == kelime_Olsuz_i_s[k]:
                   kontrol *=-1
                   flag=1
                   break
               
               
        if flag == 0: # daha önce bir yere girmiş mi onu kontrol ettirir
            for k in range(282):
                if stemmerSonrasi[len(stemmerSonrasi)-1] == ("değil ") and (stemmerSonrasi[len(stemmerSonrasi)-2] == kelime_Olsuz_f[k] ):
                    kontrol*=1
                    flag = 1
                    break  
                #cümlenin kelimelerinin teker teker kontrol edilmesi df_kelimelerde ilgili sınıfın kontrol edilmesi
                elif stemmerSonrasi[j] == kelime_Olsuz_f[k]:
                   kontrol *=-1
                   flag=1
                   break
               
        if flag == 0:
            for k in range(339):
                if stemmerSonrasi[len(stemmerSonrasi)-1] == ("değil") and (stemmerSonrasi[len(stemmerSonrasi)-2] == kelime_Ol_i_s[k]):
                    kontrol*=-1
                    flag = 1
                    break   
                #cümlenin kelimelerinin teker teker kontrol edilmesi df_kelimelerde ilgili sınıfın kontrol edilmesi
                elif stemmerSonrasi[j] == kelime_Ol_i_s[k] :
                    kontrol*=1
                    flag = 1
                    break
        if flag == 0:
            for k in range(262):
                if stemmerSonrasi[len(stemmerSonrasi)-1] == ("değil") and (stemmerSonrasi[len(stemmerSonrasi)-2] == kelime_Ol_f[k]):
                    kontrol*=-1
                    flag = 1
                    break   
                #cümlenin kelimelerinin teker teker kontrol edilmesi df_kelimelerde ilgili sınıfın kontrol edilmesi
                elif stemmerSonrasi[j] == kelime_Ol_f[k]:
                    kontrol*=1
                    flag = 1
                    break
        
        if stemmerSonrasi[j] == "!":# ünlem varsa terse döndür
            kontrol *= -1
            flag = 1
        if stemmerSonrasi[j] == "?": #soru işareti varsa cümle genelde nötr oluyor  
            kontrol *= 0
            return kontrol
        
        j += 1 #while döngüsü için stemmerdan çıkmış cümledeki kelimeler için stemmerSonrasi[j] 
     
    #nötr belirleme alanı            
    if flag == 0:
        kontrol *= 0

    #cümlenin pozitif mi negatif mi yoksa nötr mü olduğunu döndürür                                
    return kontrol
print(main())           

