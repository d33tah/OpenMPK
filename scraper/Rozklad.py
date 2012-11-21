#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
Rozklad.py

Plik zawiera klas� rozk�ad, kt�ra posiada metody zwi�zane z parsowaniem
danych o pojedynczym rozk�adzie nale��cym do danego przystanku.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
import os #error, makedirs
from lxml import html #parsowanie HTML
import re #wyra�enia regularne

#za�aduj biblioteki z Pythona 2/3 ze sp�jnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
elif sys.version.startswith('3'):
	from urllib.request import urlopen

from util import popraw_file_url, wybierz_ramke, makedir_quiet

class Rozklad:
	def przetworz_kolumne_rozkladu(self,godziny,minuty,i):
		"""
		Przetwarza pojedyncz� kolumn� rozk�adu - t� 'W dni robocze
		opr�cz sob�t', 'W soboty', 'W niedziela i �wi�ta', 'Dnia x'
		itp.
		"""

		#Z za�o�enia, nazw� katalogu mamy ustawion� przez klas� Linia.
		#Tworzymy go i otwieramy rozklad.csv dla danego podkatalogu i.
		nowy_katalog = "%s/%d" % (self.nazwa_katalogu, i)
		makedir_quiet(nowy_katalog)
		plik = open("%s/rozklad.csv" % nowy_katalog, 'w')

		#Wybieramy tr'ki z godzinami i minutami. Ma by� ich tyle samo.
		tr_godziny = godziny.xpath('.//tr')
		tr_minuty = minuty.xpath('.//tr')
		assert(len(tr_godziny)==len(tr_minuty))

		#Przechodzimy przez ka�d� godzin�.
		for i in range(len(tr_godziny)):
			godzina = tr_godziny[i].text_content()
			godzina = int(godzina)
			wiersz_minut = tr_minuty[i]
			#Przechodzimy przez ka�d� minut�.
			for td_minuta in wiersz_minut.xpath('.//td'):
				minuta = td_minuta.text_content()
				#TODO: poprawne przetwarzanie liter na ko�cu.
				#Gdybym wiedzia�, jak ten kod si� rozro�nie,
				#rozwi�za�bym to inaczej...
				for litera in ('x','y','A','B','C','N','D',
						'd','a','s','T','R','z','P',
						'f','n','J'):
					#Obetnij literk� na ko�cu.
					minuta = minuta.rstrip(litera)
				if minuta=='-':
					#Si� znaczy - w tej kolumnie pod t� 
					#godzin� nic nie ma.
					continue
				minuta = int(minuta)
				assert(godzina<24 and minuta<60)
				czas = '%d:%02d' % (godzina,minuta)
				print(czas,file=plik)

	@staticmethod
	def przetworz_rozklad(url,base_url,stary_base_url,nazwa_linii,i):
		"""
		Pobieramy rozk�ad i przetwarzamy go. Do odczytania ramek
		potrzebne by�o czary_mary z base_url i stary_base_url.

		Wynika to ze sposobu, w jaki pliki z rozk�adami s� zapisane
		w pliku .zip na stronie. Poza znakiem zapytaniem w tre�ci,
		trzeba by�o jeszcze jako� rozwi�za� "../" w adresach.
		"""
		zwracany_rozklad = Rozklad()

		docelowy_url = popraw_file_url(base_url+url)
		tree = html.parse(docelowy_url)
		if url.find('ramka.html?l=')!=-1: #wersja z ZIPa
			#wybieramy l= oraz p= z URL'a i symulujemy dzia�anie
			#kodu JS w ZIPach - �adujemy odpowiedni plik.
			par = re.findall('\?l=(.*?)&p=(.*?)&k',url)[0]
			nowy_url = "%s/%s/%s.htm" % (
					stary_base_url,par[0],par[1])
			try: #USUN�� PO TESTACH
				tree = html.parse(nowy_url)
			except:
				print("t�umi� b��d pobierania: %s" % nowy_url)
				return
			#tree = html.fromstring(
			#		nowy_html.decode('windows-1250'))
		else: #wersja ze strony
			tree = wybierz_ramke(tree,'T',base_url)

		#Wybieramy dwie g��wne tabele.
		glowne_tabele = tree.xpath('//td [@valign="TOP"]')
		assert(len(glowne_tabele)==2)

		#Nast�pnie, wyci�gamy tabel� z czasami oraz rozk�adem.
		tabela_z_czasami = glowne_tabele[0]
		tabela_z_rozkladem = glowne_tabele[1].xpath('./table')[0]
		assert(len(tabela_z_rozkladem.xpath('./tr'))==4)

		#ID przystanku jest w takim TD, kt�ry nie ma ustawionej klasy
		#a jednocze�nie ma colspan=2 i align=center.
		id_przystanku_td = tree.xpath('//td[not(@class="naglczas") \
				and @align="CENTER" and @colspan="2"]')
		assert(len(id_przystanku_td)==1)
		#TODO: Mo�e to jest lepsze miejsce do wyci�gania nazw 
		#przystank�w?
		id_przystanku_tekst = id_przystanku_td[0].text_content()
		#Wzorzec - co�tam, co�tam w nawiasie, koniec. Interesuje nas
		#to drugie co�tam.
		id_przystanku = re.findall('(.*)\((.*?)\)$',
				id_przystanku_tekst)[0]
		#Ustawiamy to zwracanemu obiektowi.
		zwracany_rozklad.id_przystanku = id_przystanku[1]

		#utw�rz na wszelki wypadek katalog na listy przystank�w,
		#a nast�pnie otw�rz plik_lista, gdzie dopiszemy i-ty kierunek
		nazwa_katalogu = 'przetworzone/lista_przystankow/'+nazwa_linii
		makedir_quiet(nazwa_katalogu)
		plik_lista = open("%s/%d.csv" % (nazwa_katalogu,i),'a')
		print("%s" % id_przystanku[1], file=plik_lista)
		plik_lista.close()

	
		#Tworzymy katalog dla tego konkretnego rozk�adu.
		nazwa_katalogu = 'przetworzone/rozklady/%s/%s' % (nazwa_linii,
				id_przystanku[1])
		makedir_quiet(nazwa_katalogu)

		#To te� ustawiamy zwracanemu obiektowi.
		zwracany_rozklad.nazwa_katalogu = nazwa_katalogu
		
		#Wybieramy tr'ki z tabeli z rozk�adem. Rozk�ad to drugi tr,
		#nag��wek ('W niedziele/dni robocze' itp) jest w pierwszym.
		wiersze_tabeli_z_rozkladem = tabela_z_rozkladem.xpath('./tr')
		rozklad = wiersze_tabeli_z_rozkladem[2]
		naglowki = wiersze_tabeli_z_rozkladem[0]

		#Otwieramy plik na nag��wki.
		plik_naglowki = open('%s/naglowki.csv' % nazwa_katalogu ,'w')

		#Wyci�gamy z rozk�adu kolumny i iterujemy od 0 do po�owy ich 
		#liczby.
		kolumny_rozkladu = rozklad.xpath('./td')
		for i in range(int(len(kolumny_rozkladu)/2)):
			#Zczytujemy nazw� nag��wka i zapisujemy j�.
			nazwa_naglowka = naglowki[i].text_content()
			print("%s,%s" % (i,nazwa_naglowka),file=plik_naglowki)
			#Przetwarzamy par� kolumn rozk�adu - godziny i minuty.
			zwracany_rozklad.przetworz_kolumne_rozkladu(
					kolumny_rozkladu[i*2],
					kolumny_rozkladu[i*2+1],i)
		return zwracany_rozklad

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	pass #TODO: mo�e jaki� by si� przyda�? :>
