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
	from urllib2 import quote
elif sys.version.startswith('3'):
	from urllib.parse import quote
	from urllib.request import urlopen

from util import popraw_file_url, wybierz_ramke, makedir_quiet

class Rozklad:
	def przetworz_kolumne_rozkladu(self,godziny,minuty,i):
		"""
		Przetwarza pojedynczą kolumnę rozkładu - tą 'W dni robocze
		oprócz sobót', 'W soboty', 'W niedziela i święta', 'Dnia x'
		itp.
		"""
		nowy_katalog = "%s/%d" % (self.nazwa_katalogu, i)
		makedir_quiet(nowy_katalog)
		plik = open("%s/rozklad.csv" % nowy_katalog, 'w')
		tr_godziny = godziny.xpath('.//tr')
		tr_minuty = minuty.xpath('.//tr')
		assert(len(tr_godziny)==len(tr_minuty))
		for i in range(len(tr_godziny)):
			godzina = tr_godziny[i].text_content()
			godzina = int(godzina)
			wiersz_minut = tr_minuty[i]
			for td_minuta in tr_minuty[i].xpath('.//td'):
				#TODO: poprawne przetwarzanie x,y na końcu.
				minuta = td_minuta.text_content()
				#gdybym wiedział, jak ten kod się rozrośnie,
				#rozwiązałbym to inaczej.
				for litera in ('x','y','A','B','C','N','D',
						'd','a','s','T','R','z'):
					minuta = minuta.rstrip(litera)
				if minuta=='-':
					continue
				minuta = int(minuta)
				assert(godzina<24 and minuta<60)
				czas = '%d:%02d' % (godzina,minuta)
				print(czas,file=plik)

	@staticmethod
	def przetworz_rozklad(url,base_url,stary_base_url,nazwa_linii):
		"""
		Pobieramy rozkład i przetwarzamy go. Do odczytania ramek
		potrzebne było czary_mary z base_url i stary_base_url.

		Wynika to ze sposobu, w jaki pliki z rozkładami są zapisane
		w pliku .zip na stronie. Poza znakiem zapytaniem w treści,
		trzeba było jeszcze jakoś rozwiązać "../" w adresach.
		"""
		zwracany_rozklad = Rozklad()

		docelowy_url = popraw_file_url(base_url+url)
		kod_html_rozklad = urlopen(docelowy_url).read()
		tree = html.fromstring(kod_html_rozklad.decode('windows-1250'))
		if url.find('ramka.html?l=')!=-1: #wersja z ZIPa
			par = re.findall('\?l=(.*?)&p=(.*?)&k',url)[0]
			nowy_url = "%s/%s/%s.htm" % (stary_base_url,par[0],par[1])
			print(nowy_url) #USUNĄĆ PO TESTACH
			try: #USUNĄĆ PO TESTACH
				nowy_html = urlopen(nowy_url).read()
			except:
				print("tłumię błąd pobierania: %s" % nowy_url)
				return
			tree = html.fromstring(nowy_html.decode('windows-1250'))
		else: #wersja ze strony
			tree = wybierz_ramke(tree,'T',base_url)

		glowne_tabele = tree.xpath('//td [@valign="TOP"]')
		assert(len(glowne_tabele)==2)

		tabela_z_czasami = glowne_tabele[0]
		tabela_z_rozkladem = glowne_tabele[1].xpath('./table')[0]
		assert(len(tabela_z_rozkladem.xpath('./tr'))==4)

		id_przystanku_td = tree.xpath(
				'//td [@align="CENTER"] [@colspan="2"] ')[0]
		id_przystanku_tekst = id_przystanku_td.text_content()
		id_przystanku = re.findall('.*\((.*?)\)$',id_przystanku_tekst)[0]
		zwracany_rozklad.id_przystanku = id_przystanku
	
		nazwa_katalogu = 'przetworzone/rozklady/%s/%s' % (nazwa_linii, id_przystanku)
		makedir_quiet(nazwa_katalogu)

		zwracany_rozklad.nazwa_katalogu = nazwa_katalogu
		wiersze_tabeli_z_rozkladem = tabela_z_rozkladem.xpath('./tr')
		rozklad = wiersze_tabeli_z_rozkladem[2]
		naglowki = wiersze_tabeli_z_rozkladem[0]
		kolumny_rozkladu = rozklad.xpath('./td')
		plik_naglowki = open('%s/naglowki.csv' % nazwa_katalogu ,'w')
		for i in range(int(len(kolumny_rozkladu)/2)):
			print(i) #USUNĄĆ PO TESTACH
			nazwa_naglowka = naglowki[i].text_content()
			print("%s,%s" % (i,nazwa_naglowka),file=plik_naglowki)
			zwracany_rozklad.przetworz_kolumne_rozkladu(
					kolumny_rozkladu[i*2],kolumny_rozkladu[i*2+1],i)
		return zwracany_rozklad

if __name__=='__main__':
	"""
	Kod testujący.
	"""
	pass #TODO: może jakiś by się przydał? :>
