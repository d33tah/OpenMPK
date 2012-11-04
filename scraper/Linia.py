#!/usr/bin/python3
# -*- coding: windows-1250 -*-

"""
Linia.py

Tutaj parsujemy informacje o pojedynczej linii - na ten moment, lista 
przystank�w. Dla ka�dego z przystank�w mo�na potem pobra� rozk�ad i przesiadki.
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

from util import wybierz_ramke
from Rozklad import Rozklad

class Linia:
	def __init__(self,nazwa,url,base_url):
		"""
		Konstruktor klasy Linia. Bierze trzy parametry i zapisuje
		jako swoje atrybuty.
		"""
		self.nazwa = nazwa
		self.url = url
		self.base_url = base_url
		self.przystanki = [] 

	def __str__(self):
		"""
		Rzutowanie obiektu klasy Linia na stringa. Zrobione zgodnie
		z Pythonowymi zwyczajami.
		"""
		return '<Linia id="%s", nazwa="%s", url="%s" />' % (
				id(self), self.nazwa, self.url)

	def __eq__(lewy,prawy):
		"""
		Por�wnywanie dw�ch obiekt�w klasy Linia - por�wnujemy tylko 
		nazwy. Domy�lnie obiekty s� r�wne tylko gdy jest to ten sam 
		obiekt w dw�ch referencjach.
		"""
		return isinstance(prawy,Linia) and (lewy.nazwa)==(prawy.nazwa)

	def obsluz_przesiadki(self,link):
		"""
		Wst�pny kod obs�ugi przesiadek. Klika w link "przesiadki" dla
		danego przystanku i listuje, jakie linie s� na danym 
		przystanku.
		"""
		url = link.attrib['href']
		base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'
		docelowy_url = base_url_rozkladu+url 
		kod_html_przesiadki = urlopen(docelowy_url).read()
		tree = html.fromstring(kod_html_przesiadki. \
					decode('windows-1250'))
		for p in tree.xpath('//p'):
			if p.text_content().endswith('na mapie'):
				next #mapa nas na razie nie interesuje.
			nast_el = p.getnext()
			if(nast_el.tag=='ul'):
				for el in nast_el.xpath('li'):
					#uwaga na link! znowu b�dzie problem
					#z ramka.html w ZIPie
					link = el.xpath('a')[0]
					nazwa_linii = link.text_content().strip()
					print('"%s"' % nazwa_linii)
				break #chyba, �e nas interesuj� linie w pobli�u?

	def przetworz_kierunek(self,kierunek):
		"""
		Przetwarzamy pojedynczy kierunek jazdy z listy przystank�w.
		"""
		for wpis in kierunek.xpath('.//tr')[1:]: #[1:] = bez nag��wka
			ulica_glowna = wpis[0].text_content().strip()
			link = wpis[2].xpath('a')
			if link: #przystanek mo�e nie mie� linka, zwykle p�tla.
				nazwa_przystanku = link[0].text_content()
				url_rozkladu = link[0].attrib['href']
				base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'
				#przetwarzamy rozk�ad jazdy, w celach testowych
				Rozklad.przetworz_rozklad(url_rozkladu,
						base_url_rozkladu,
						self.base_url)
			else:
				nazwa_przystanku = wpis[2].text_content()
			if wpis[3].xpath('.//a'):
				self.obsluz_przesiadki(
						wpis[3].xpath('.//a')[0])
			"""
			Na razie pojedynczy przystanek reprezentowany jest
			wy��cznie przez jego nazw�, kt�ra na dzie� dzisiejszy
			jest kiepsko formatowana. Jak ju� zerkn�, co powinno
			by� w klasie, utworz� takow�.
			"""
			self.przystanki += ["%s - %s" % (
				ulica_glowna,nazwa_przystanku)]

	def pobierz_przystanki(self):
		"""
		Je�li ju� mamy przystanki, zwr�� je. W przeciwnym razie
		wejd� na linka z obiektu, przeskocz ramki i dla ka�dego
		z kierunk�w, przetw�rz go.
		"""
		if not self.przystanki:

			kod_html_przystanki = urlopen(self.url).read()
			tree = html.fromstring(kod_html_przystanki. \
					decode('windows-1250'))

			tree = wybierz_ramke(tree,'rozklad',self.base_url)
			tree = wybierz_ramke(tree,'D',self.base_url)
		
			for kierunek in tree.xpath('//td [@class="przyst"]'):
				self.przetworz_kierunek(kierunek)
				break #USUN�� PO TESTACH

		return self.przystanki

	def listuj_linie(url):
		"""
		Funkcja wchodzi na podanego URL'a (w przypadku strony MPK, musi
		nast�pi� przekierowanie, bo mamy index.jsp, a nie .html) i pobiera
		list� linii.

		TODO: rozr�nia� autobusy dzienne/nocne i tramwaje? Na tej podstronie
		jest taka mo�liwo��.
		"""
		kod_html = urlopen(url+'/index.html').read()
		tree = html.fromstring(kod_html.decode('windows-1250'))
		przekierowanie = tree.xpath('//meta [@http-equiv="refresh"]')
		if przekierowanie:
			"""
			Wybierz pierwszy element z tej tablicy i we� tekst na prawo od 
			URL w jego 'content'.
			"""
			nowy_url = przekierowanie[0].attrib['content'].split(
					'URL=')[-1]
			kod_html = urlopen(nowy_url).read()
			tree = html.fromstring(kod_html.decode('windows-1250'))

		linie_tree = wybierz_ramke(tree,'rozklad',url)
		linie_td = linie_tree.xpath('//div [contains(@id,bx1)]//td \
				[@class="nagl" and not(contains(.,"Aktualny"))]')
		ret = []
		for linia in linie_td:
			link = linia.xpath('a')[0]
			nazwa_linii = link.text_content().lstrip("Linia: ")
			url_linii = url+link.attrib['href']
			ret += [Linia(nazwa_linii,url_linii,url)]
		return ret

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	pass #niespodzianka, brak!

