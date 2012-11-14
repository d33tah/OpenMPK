#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
Rozklad.py

Plik zawiera klasę rozkład, która posiada metody związane z parsowaniem
danych o pojedynczym rozkładzie należącym do danego przystanku.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
import os #error, makedirs
from lxml import html #parsowanie HTML
import re #wyrażenia regularne

#załaduj biblioteki z Pythona 2/3 ze spójnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
elif sys.version.startswith('3'):
	from urllib.request import urlopen

from util import popraw_file_url, wybierz_ramke, makedir_quiet

class Rozklad:
	def przetworz_kolumne_rozkladu(self,godziny,minuty,i):
		"""
		Przetwarza pojedynczą kolumnę rozkładu - tą 'W dni robocze
		oprócz sobót', 'W soboty', 'W niedziela i święta', 'Dnia x'
		itp.
		"""

		#Z założenia, nazwę katalogu mamy ustawioną przez klasę Linia.
		#Tworzymy go i otwieramy rozklad.csv dla danego podkatalogu i.
		nowy_katalog = "%s/%d" % (self.nazwa_katalogu, i)
		makedir_quiet(nowy_katalog)
		plik = open("%s/rozklad.csv" % nowy_katalog, 'w')

		#Wybieramy tr'ki z godzinami i minutami. Ma być ich tyle samo.
		tr_godziny = godziny.xpath('.//tr')
		tr_minuty = minuty.xpath('.//tr')
		assert(len(tr_godziny)==len(tr_minuty))

		#Przechodzimy przez każdą godzinę.
		for i in range(len(tr_godziny)):
			godzina = tr_godziny[i].text_content()
			godzina = int(godzina)
			wiersz_minut = tr_minuty[i]
			#Przechodzimy przez każdą minutę.
			for td_minuta in wiersz_minut.xpath('.//td'):
				minuta = td_minuta.text_content()
				#TODO: poprawne przetwarzanie liter na końcu.
				#Gdybym wiedział, jak ten kod się rozrośnie,
				#rozwiązałbym to inaczej...
				for litera in ('x','y','A','B','C','N','D',
						'd','a','s','T','R','z','P',
						'f','n','J'):
					#Obetnij literkę na końcu.
					minuta = minuta.rstrip(litera)
				if minuta=='-':
					#Się znaczy - w tej kolumnie pod tą 
					#godziną nic nie ma.
					continue
				minuta = int(minuta)
				assert(godzina<24 and minuta<60)
				czas = '%d:%02d' % (godzina,minuta)
				print(czas,file=plik)

	@staticmethod
	def przetworz_rozklad(url,base_url,stary_base_url,nazwa_linii,i):
		"""
		Pobieramy rozkład i przetwarzamy go. Do odczytania ramek
		potrzebne było czary_mary z base_url i stary_base_url.

		Wynika to ze sposobu, w jaki pliki z rozkładami są zapisane
		w pliku .zip na stronie. Poza znakiem zapytaniem w treści,
		trzeba było jeszcze jakoś rozwiązać "../" w adresach.
		"""
		zwracany_rozklad = Rozklad()

		docelowy_url = popraw_file_url(base_url+url)
		tree = html.parse(docelowy_url)
		if url.find('ramka.html?l=')!=-1: #wersja z ZIPa
			#wybieramy l= oraz p= z URL'a i symulujemy działanie
			#kodu JS w ZIPach - ładujemy odpowiedni plik.
			par = re.findall('\?l=(.*?)&p=(.*?)&k',url)[0]
			nowy_url = "%s/%s/%s.htm" % (
					stary_base_url,par[0],par[1])
			try: #USUNĄĆ PO TESTACH
				tree = html.parse(nowy_url)
			except:
				print("tłumię błąd pobierania: %s" % nowy_url)
				return
			#tree = html.fromstring(
			#		nowy_html.decode('windows-1250'))
		else: #wersja ze strony
			tree = wybierz_ramke(tree,'T',base_url)

		#Wybieramy dwie główne tabele.
		glowne_tabele = tree.xpath('//td [@valign="TOP"]')
		assert(len(glowne_tabele)==2)

		#Następnie, wyciągamy tabelę z czasami oraz rozkładem.
		tabela_z_czasami = glowne_tabele[0]
		tabela_z_rozkladem = glowne_tabele[1].xpath('./table')[0]
		assert(len(tabela_z_rozkladem.xpath('./tr'))==4)

		#ID przystanku jest w takim TD, który nie ma ustawionej klasy
		#a jednocześnie ma colspan=2 i align=center.
		id_przystanku_td = tree.xpath('//td[not(@class="naglczas") \
				and @align="CENTER" and @colspan="2"]')
		assert(len(id_przystanku_td)==1)
		#TODO: Może to jest lepsze miejsce do wyciągania nazw 
		#przystanków?
		id_przystanku_tekst = id_przystanku_td[0].text_content()
		#Wzorzec - cośtam, cośtam w nawiasie, koniec. Interesuje nas
		#to drugie cośtam.
		id_przystanku = re.findall('(.*)\((.*?)\)$',
				id_przystanku_tekst)[0]
		#Ustawiamy to zwracanemu obiektowi.
		zwracany_rozklad.id_przystanku = id_przystanku[1]

		#utwórz na wszelki wypadek katalog na listy przystanków,
		#a następnie otwórz plik_lista, gdzie dopiszemy i-ty kierunek
		nazwa_katalogu = 'przetworzone/lista_przystankow/'+nazwa_linii
		makedir_quiet(nazwa_katalogu)
		plik_lista = open("%s/%d.csv" % (nazwa_katalogu,i),'a')
		print("%s" % id_przystanku[1], file=plik_lista)
		plik_lista.close()

	
		#Tworzymy katalog dla tego konkretnego rozkładu.
		nazwa_katalogu = 'przetworzone/rozklady/%s/%s' % (nazwa_linii,
				id_przystanku[1])
		makedir_quiet(nazwa_katalogu)

		#To też ustawiamy zwracanemu obiektowi.
		zwracany_rozklad.nazwa_katalogu = nazwa_katalogu
		
		#Wybieramy tr'ki z tabeli z rozkładem. Rozkład to drugi tr,
		#nagłówek ('W niedziele/dni robocze' itp) jest w pierwszym.
		wiersze_tabeli_z_rozkladem = tabela_z_rozkladem.xpath('./tr')
		rozklad = wiersze_tabeli_z_rozkladem[2]
		naglowki = wiersze_tabeli_z_rozkladem[0]

		#Otwieramy plik na nagłówki.
		plik_naglowki = open('%s/naglowki.csv' % nazwa_katalogu ,'w')

		#Wyciągamy z rozkładu kolumny i iterujemy od 0 do połowy ich 
		#liczby.
		kolumny_rozkladu = rozklad.xpath('./td')
		for i in range(int(len(kolumny_rozkladu)/2)):
			#Zczytujemy nazwę nagłówka i zapisujemy ją.
			nazwa_naglowka = naglowki[i].text_content()
			print("%s,%s" % (i,nazwa_naglowka),file=plik_naglowki)
			#Przetwarzamy parę kolumn rozkładu - godziny i minuty.
			zwracany_rozklad.przetworz_kolumne_rozkladu(
					kolumny_rozkladu[i*2],
					kolumny_rozkladu[i*2+1],i)
		return zwracany_rozklad

if __name__=='__main__':
	"""
	Kod testujący.
	"""
	pass #TODO: może jakiś by się przydał? :>
