#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
Linia.py

Tutaj parsujemy informacje o pojedynczej linii - na ten moment, lista 
przystanków. Dla każdego z przystanków można potem pobrać rozkład i przesiadki.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
from lxml import html #parsowanie HTML
import re #wyrażenia regularne
import os #path.exists

#załaduj biblioteki z Pythona 2/3 ze spójnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
	from urllib2 import quote
elif sys.version.startswith('3'):
	from urllib.parse import quote
	from urllib.request import urlopen

from util import wybierz_ramke, makedir_quiet
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
		Porównywanie dwóch obiektów klasy Linia - porównujemy tylko 
		nazwy. Domyślnie obiekty są równe tylko gdy jest to ten sam 
		obiekt w dwóch referencjach.
		"""
		return isinstance(prawy,Linia) and (lewy.nazwa)==(prawy.nazwa)

	def obsluz_przesiadki(self,link):
		"""
		Wstępny kod obsługi przesiadek. Klika w link "przesiadki" dla
		danego przystanku i listuje, jakie linie są na danym 
		przystanku.
		"""
		url = link.attrib['href']
		base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'
		docelowy_url = base_url_rozkladu+url 
		try:
			kod_html_przesiadki = urlopen(docelowy_url).read()
		except:
			print("tłumię błąd pobierania: %s" % docelowy_url)
			return

			
		tree = html.fromstring(kod_html_przesiadki. \
					decode('windows-1250'))

		dane_przystanku_el = tree.xpath(
				'//*[self::font or self::div]')
		assert(len(dane_przystanku_el)==1)
		dane_przystanku_tekst=dane_przystanku_el[0].text_content()
		dane_przystanku = re.findall('(.*)\((.*?)\)$',
				dane_przystanku_tekst)[0]
		nazwa_przystanku = dane_przystanku[0]
		id_przystanku = dane_przystanku[1]
		
		nazwa_pliku_przesiadki = 'przetworzone/przesiadki/%s.txt' % \
				id_przystanku
		if not os.path.exists(nazwa_pliku_przesiadki):
			makedir_quiet('przetworzone/przesiadki')
			plik = open(nazwa_pliku_przesiadki,'a')
			plik_przystanki = open('przetworzone/nazwy_przystankow.txt','a')
			print("%s,%s" % (id_przystanku,nazwa_przystanku),file=plik_przystanki)
			plik_przystanki.close()
		else:
			plik = None
		
		for p in tree.xpath('//p'):
			if p.text_content().endswith('na mapie'):
				continue
			nast_el = p.getnext()
			if(nast_el.tag=='ul'):
				for el in nast_el.xpath('li'):
					#uwaga na link! znowu będzie problem
					#z ramka.html w ZIPie
					link = el.xpath('a')[0]
					nazwa_linii = link.text_content().strip()
					if plik:
						print('"%s"' % nazwa_linii, 
								file=plik)
				break #chyba, że nas interesują linie w pobliżu?

	def przetworz_kierunek(self,kierunek,i):
		"""
		Przetwarzamy pojedynczy kierunek jazdy z listy przystanków.
		"""
		nazwa_katalogu = 'przetworzone/lista_przystankow/%s' % self.nazwa
		makedir_quiet(nazwa_katalogu)
		plik_lista = open("%s/%d.csv" % (nazwa_katalogu,i),'w')

		for wpis in kierunek.xpath('.//tr')[1:]: #[1:] = bez nagłówka
			ulica_glowna = wpis[0].text_content().strip()
			link = wpis[2].xpath('a')
			if link: #przystanek może nie mieć linka, zwykle pętla.
				nazwa_przystanku = link[0].text_content()
				url_rozkladu = link[0].attrib['href']
				base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'
				#przetwarzamy rozkład jazdy, w celach testowych
				Rozklad.przetworz_rozklad(url_rozkladu,
						base_url_rozkladu,
						self.base_url,self.nazwa)
			else:
				nazwa_przystanku = wpis[2].text_content()

			if wpis[3].xpath('.//a'):
				self.obsluz_przesiadki(
						wpis[3].xpath('.//a')[0])
			"""
			Na razie pojedynczy przystanek reprezentowany jest
			wyłącznie przez jego nazwę, która na dzień dzisiejszy
			jest kiepsko formatowana. Jak już zerknę, co powinno
			być w klasie, utworzę takową.
			"""
			pelna_nazwa = "%s - %s" % (
					ulica_glowna,nazwa_przystanku)
			print(pelna_nazwa,file=plik_lista)
			self.przystanki += [pelna_nazwa]

	def pobierz_przystanki(self):
		"""
		Jeśli już mamy przystanki, zwróć je. W przeciwnym razie
		wejdź na linka z obiektu, przeskocz ramki i dla każdego
		z kierunków, przetwórz go.
		"""
		if not self.przystanki:

			kod_html_przystanki = urlopen(self.url).read()
			tree = html.fromstring(kod_html_przystanki. \
					decode('windows-1250'))

			tree = wybierz_ramke(tree,'rozklad',self.base_url)
			tree = wybierz_ramke(tree,'D',self.base_url)
		
			kierunki = tree.xpath('//td [@class="przyst"]')
			for i in range(len(kierunki)):
				self.przetworz_kierunek(kierunki[i],i)
				break #USUNĄĆ PO TESTACH

		return self.przystanki

	@staticmethod
	def listuj_linie(url):
		"""
		Funkcja wchodzi na podanego URL'a (w przypadku strony MPK, musi
		nastąpić przekierowanie, bo mamy index.jsp, a nie .html) i pobiera
		listę linii.

		TODO: rozróżniać autobusy dzienne/nocne i tramwaje? Na tej podstronie
		jest taka możliwość.
		"""
		kod_html = urlopen(url+'/index.html').read()
		tree = html.fromstring(kod_html.decode('windows-1250'))
		przekierowanie = tree.xpath('//meta [@http-equiv="refresh"]')
		if przekierowanie:
			"""
			Wybierz pierwszy element z tej tablicy i weź tekst na prawo od 
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
		
		makedir_quiet('przetworzone')
		f = open('przetworzone/lista_linii.txt','w')

		for linia in linie_td:
			link = linia.xpath('a')[0]
			nazwa_linii = link.text_content().lstrip("Linia: ")
			print(nazwa_linii,file=f)
			url_linii = url+link.attrib['href']
			ret += [Linia(nazwa_linii,url_linii,url)]
		return ret

if __name__=='__main__':
	"""
	Kod testujący.
	"""
	pass #niespodzianka, brak!

