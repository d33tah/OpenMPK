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
elif sys.version.startswith('3'):
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
		przystanku. UWAGA, duże.
		"""
		url = link.attrib['href']

		#wyciągamy treść przed ostatnim ukośnikiem jako 
		#base_url_rozkladu.
		base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'

		#Błędy tego typu mają miejsce w ZIPach MPK. Później im to 
		#pewnie zgłoszę.
		docelowy_url = base_url_rozkladu+url 
		try:
			tree = html.parse(docelowy_url)
		except:
			print("tłumię błąd pobierania: %s" % docelowy_url)
			return
		
		#Dane przystanku są w jakimś divie albo foncie. Ma być jeden.
		dane_przystanku_el = tree.xpath(
				'//*[self::font or self::div]')
		assert(len(dane_przystanku_el)==1)
		dane_przystanku_tekst=dane_przystanku_el[0].text_content()
		#Dzielimy to według wzorca - cośtam, cośtam w nawiasie, koniec.
		dane_przystanku = re.findall('(.*)\((.*?)\)$',
				dane_przystanku_tekst)[0]
		nazwa_przystanku = dane_przystanku[0] #pierwsze cośtam

		#Poniższe trzy linijki dają pewne wyobrażenie o tym jakiej 
		#jakości są dane z ZIPa.
		nazwa_przystanku = nazwa_przystanku.lstrip('null')
		nazwa_przystanku = nazwa_przystanku.lstrip()
		nazwa_przystanku = nazwa_przystanku.lstrip('- ')
		nazwa_przystanku = nazwa_przystanku.rstrip()

		id_przystanku = dane_przystanku[1] #drugie cośtam
		
		nazwa_pliku_przesiadki = 'przetworzone/przesiadki/%s.txt' % \
				id_przystanku
		"""
		Jeżeli istnieje już plik z przesiadkami, ustawiamy plik na 
		None, żeby go nie dopisywać do bazy przesiadek.	Przy okazji, 
		jeśli nie ma go w przesiadkach, dopiszmy go też	do 
		nazwy_przystankow.txt.
		"""
		if not os.path.exists(nazwa_pliku_przesiadki):
			makedir_quiet('przetworzone/przesiadki')
			plik = open(nazwa_pliku_przesiadki,'a')

			plik_przystanki = open('przetworzone/'+\
					'nazwy_przystankow.txt','a')
			print("%s,%s" % (id_przystanku,nazwa_przystanku),
					file=plik_przystanki)
			plik_przystanki.close()
		else:
			plik = None
		
		#przechodzimy przez każdy tag <p>
		for p in tree.xpath('//p'):
			#dotyczy tylko strony WWW
			if p.text_content().endswith('na mapie'):
				continue
			#jeżeli potem jest ul, to najprawdopodobniej jest to
			#lista przesiadek.
			nast_el = p.getnext()
			if(nast_el.tag=='ul'):
				for el in nast_el.xpath('li'):
					#uwaga na link! znowu będzie problem
					#z ramka.html w ZIPie
					link = el.xpath('a')[0]
					nazwa_linii = link.text_content()
					nazwa_linii = nazwa_linii.strip()
					kier_tekst = link.tail
					kier_tekst = kier_tekst.split('-->')[1]
					kier_tekst = kier_tekst.strip()
					if plik:
						print('%s,%s' % (nazwa_linii, 
							kier_tekst), file=plik)
				break #chyba, że potrzebujemy linie w pobliżu?

	def przetworz_kierunek(self,kierunek,i):
		"""
		Przetwarzamy pojedynczy kierunek jazdy z listy przystanków.
		Oznacza to, że przejdziemy przez wszystkie przystanki w nim,
		każdy zapiszemy w liście przystanków danego kierunku, a poza
		tym obsłużymy przesiadki i rozkład.
		"""
		
			#przejdź przez każdy <tr> jako wpis
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
						self.base_url,self.nazwa,i)
			else:
				nazwa_przystanku = wpis[2].text_content()

			#jeśli w trzeciej kolumnie jest link, obsłuż 
			#przesiadki.
			if wpis[3].xpath('.//a'):
				self.obsluz_przesiadki(
						wpis[3].xpath('.//a')[0])
			"""
			Na razie pojedynczy przystanek reprezentowany jest
			wyłącznie przez jego nazwę. Jak już zerknę, co powinno
			być w klasie, utworzę takową.
			"""
			if ulica_glowna:
				pelna_nazwa = "%s - %s" % (
					ulica_glowna,nazwa_przystanku)
			else:
				pelna_nazwa = nazwa_przystanku
			#dopisz do listy - w pliku i klasie
			self.przystanki += [pelna_nazwa]

	def pobierz_przystanki(self):
		"""
		Jeśli już mamy przystanki, zwróć je. W przeciwnym razie
		wejdź na linka z obiektu, przeskocz ramki i dla każdego
		z kierunków, przetwórz go.
		"""
		if not self.przystanki:

			tree = html.parse(self.url)

			tree = wybierz_ramke(tree,'rozklad',self.base_url)
			tree = wybierz_ramke(tree,'D',self.base_url)
		
			kat_linia = 'przetworzone/lista_przystankow/%s' % \
					self.nazwa

			kierunki = tree.xpath('//td [@class="przyst"]')
			makedir_quiet(kat_linia)
			plik_ilosc_kier = open(kat_linia+'/il_kier.csv','w')
			print(len(kierunki),file=plik_ilosc_kier)
			plik_ilosc_kier.close()

			for i in range(len(kierunki)):
				self.przetworz_kierunek(kierunki[i],i)

		return self.przystanki

	@staticmethod
	def listuj_linie(url):
		"""
		Funkcja wchodzi na podanego URL'a (w przypadku strony MPK, musi
		nastąpić przekierowanie, bo mamy index.jsp, a nie .html) i 
		pobiera listę linii.

		TODO: rozróżniać autobusy dzienne/nocne i tramwaje? Na tej 
		podstronie jest taka możliwość.
		"""
		tree = html.parse(url+'/index.html')
		przekierowanie = tree.xpath('//meta [@http-equiv="refresh"]')
		if przekierowanie:
			#Wybierz pierwszy element z tej tablicy i weź tekst na 
			#prawo od URL w jego 'content'.
			nowy_url = przekierowanie[0].attrib['content'].split(
					'URL=')[-1]
			tree = html.parse(nowy_url)

		linie_tree = wybierz_ramke(tree,'rozklad',url)
		linie_td = linie_tree.xpath('//div [contains(@id,bx1)]//td \
				[@class="nagl" and not(contains( \
				.,"Aktualny"))]')
		ret = []
		
		makedir_quiet('przetworzone')
		f = open('przetworzone/lista_linii.txt','w')

		for linia in linie_td:
			link = linia.xpath('a')[0]
			#wytnij "Linia: " z linka i uznaj to za nazwę linii
			nazwa_linii = link.text_content().lstrip("Linia: ")
			url_linii = url+link.attrib['href']
			ret += [Linia(nazwa_linii,url_linii,url)]
			print(nazwa_linii,file=f)
		return ret

if __name__=='__main__':
	"""
	Kod testujący.
	"""
	pass #niespodzianka, brak!

