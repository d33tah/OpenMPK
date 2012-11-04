#!/usr/bin/python3
# -*- coding: windows-1250 -*-

"""
Rozklad.py

Plik zawiera klas� rozk�ad, kt�ra posiada metody zwi�zane z parsowaniem
danych o pojedynczym rozk�adzie nale��cym do danego przystanku.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
from lxml import html #parsowanie HTML
import re #wyra�enia regularne

if not sys.version.startswith('3'):
	print("""
	Ten program zosta� przeznaczony do uruchamiania pod interpreterem
	Pythona w wersji 3.x W teorii wszystko powinno dzia�a�, ale na wszelki
	wypadek przerywam dzia�anie programu.
	""")
	sys.exit(1) #zakomentuj t� linijk�, je�li czujesz si� odwa�ny :P
	print("Program kontynuuje prac�...")

#za�aduj biblioteki z Pythona 2/3 ze sp�jnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
	from urllib2 import quote
elif sys.version.startswith('3'):
	from urllib.parse import quote
	from urllib.request import urlopen

from util import popraw_file_url, wybierz_ramke

class Rozklad:
	def przetworz_kolumne_rozkladu(godziny,minuty):
		"""
		Przetwarza pojedyncz� kolumn� rozk�adu - t� 'W dni robocze
		opr�cz sob�t', 'W soboty', 'W niedziela i �wi�ta', 'Dnia x'
		itp.
		"""
		tr_godziny = godziny.xpath('.//tr')
		tr_minuty = minuty.xpath('.//tr')
		assert(len(tr_godziny)==len(tr_minuty))
		for i in range(len(tr_godziny)):
			godzina = tr_godziny[i].text_content()
			godzina = int(godzina)
			wiersz_minut = tr_minuty[i]
			for td_minuta in tr_minuty[i].xpath('.//td'):
				#TODO: poprawne przetwarzanie 'x' na ko�cu.
				minuta = td_minuta.text_content().rstrip('x')
				minuta = int(minuta)
				czas = '%d:%02d' % (godzina,minuta)

	def przetworz_rozklad(url,base_url,stary_base_url):
		"""
		Pobieramy rozk�ad i przetwarzamy go. Do odczytania ramek
		potrzebne by�o czary_mary z base_url i stary_base_url.

		Wynika to ze sposobu, w jaki pliki z rozk�adami s� zapisane
		w pliku .zip na stronie. Poza znakiem zapytaniem w tre�ci,
		trzeba by�o jeszcze jako� rozwi�za� "../" w adresach.
		"""
		docelowy_url = popraw_file_url(base_url+url)
		kod_html_rozklad = urlopen(docelowy_url).read()
		tree = html.fromstring(kod_html_rozklad.decode('windows-1250'))
		if url.find('ramka.html?l=')!=-1: #wersja z ZIPa
			par = re.findall('\?l=(.*?)&p=(.*?)&k',url)[0]
			nowy_url = "%s/%s/%s.htm" % (stary_base_url,par[0],par[1])
			nowy_html = urlopen(nowy_url).read()
			tree = html.fromstring(nowy_html.decode('windows-1250'))
		else: #wersja ze strony
			tree = wybierz_ramke(tree,'T',base_url)

		glowne_tabele = tree.xpath('//td [@valign="TOP"]')
		assert(len(glowne_tabele)==2)

		tabela_z_czasami = glowne_tabele[0]
		tabela_z_rozkladem = glowne_tabele[1].xpath('./table')[0]
		assert(len(tabela_z_rozkladem.xpath('./tr'))==4)

		rozklad = tabela_z_rozkladem.xpath('./tr')[2]
		kolumny_rozkladu = rozklad.xpath('./td')
		for i in range(int(len(kolumny_rozkladu)/2)):
			Rozklad.przetworz_kolumne_rozkladu(
					kolumny_rozkladu[i],kolumny_rozkladu[i+1])

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	pass #TODO: mo�e jaki� by si� przyda�? :>
