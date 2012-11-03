#!/usr/bin/python3
# -*- coding: windows-1250 -*-

"""
scraper.py

Ten kod z założenia ma pobierać dane z pobranych z mpk.lodz.pl paczek 
z rozkładami, a także samodzielnie pobierać stamtąd surowe dane i przetwarzać
je. Po przetworzeniu na wyjściu ma pojawiać się łatwiejsza do przetworzenia
struktura danych.

Kod na dzień dzisiejszy wygląda przeokropnie - uparłem się na Pythona 3, a że
nie byłem w stanie znaleźć dla niego żadnej biblioteki dla scrapingu, użyłem
urllib+własnych hacków. Drugim powodem jest sposób, w jaki zbudowana jest
strona MPK - jest kilka ciekawych kwiatków, opisane w komentarzach poniżej.
Trzeci powód jest taki, że na każdym z kroków nie miałem pojęcia, czego będę
potrzebował za chwilę i tak powstał hack na hacku. Kiedyś pewnie będzie trzeba
to przepisać.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit()
import os #do sprawdzania czy katalog istnieje
import shutil #wygodne usuwanie katalogu
import zipfile #pliki .zip
from lxml import html #parsowanie HTML
import re #wyrażenia regularne

if not sys.version.startswith('3'):
	print("""
	Ten program został przeznaczony do uruchamiania pod interpreterem
	Pythona w wersji 3.x W teorii wszystko powinno działać, ale na wszelki
	wypadek przerywam działanie programu.
	""")
	sys.exit(1) #zakomentuj tą linijkę, jeśli czujesz się odważny :P
	print("Program kontynuuje pracę...")

#załaduj biblioteki z Pythona 2/3 ze spójnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
	from urllib2 import quote
elif sys.version.startswith('3'):
	from urllib.parse import quote
	from urllib.request import urlopen


def popraw_file_url(url):
	"""
	HACK.

	Powodem jest sposób, w jaki zorganizowane są strony w pliczkach
	zip z mpk.lodz.pl. Rozkłady są tam ładowane do linie.htm?p1=w1&p2=w2.
	Oczywiście taki plik nie istnieje, więc musi zostać załadowany 
	linie.htm, a reszta tekstu obcięta. Zwracany jest poprawiony URL.
	"""
	if url.startswith('file://'):
		#weź A/B i zapisz A w podzielony[0] i B w podzielony[1]
		podzielony = re.findall('^(.*)/(.*)$',url)[0]
		#poszukaj znaku zapytania
		indeks = podzielony[1].find('?')
		#jeśli znalazłeś
		if indeks!=-1:
			#zwróć A/B do tego znaku
			return podzielony[0]+'/'+podzielony[1][:indeks]
		else: #w przeciwnych wypadkach zwróć URL nienaruszony
			return url
	else:
		return url

def wybierz_ramke(tree,nazwa_ramki,base_url):
	"""
	Jako, że mamy XXI wiek, strona jest oczywiście napisana na ramkach
	i tabelkach. Skrypt musi być tego świadomy i pozwolić na wybór 
	odpowiedniej ramki.

	Ta funkcja pobiera obiekt lxml.html, nazwę wyciętej ramki oraz
	bazowy adres URL, który ma być doklejony do wybranego z src ramki.
	Zwracany jest nowy (albo i nie, jeśli ramek nie ma) obiekt lxml.html,
	który ma już załadowaną zawartość ramki.
	"""
	ramka = tree.xpath('//frame [@name="%s"]' % nazwa_ramki)
	if(len(ramka)==1): #znaleziono ramkę
		href = ramka[0].attrib['src']
		"""
		HACK: jeżeli w linku jest ?r=, to dalej będzie tekst 
		wyświetlany żywcem na stronie. Trzeba go przepuścić przez
		quote, ale tylko część po ?r=.
		"""
		if href.find('?r=')!=-1:
			podzielone = href.split('?r=')
			href = podzielone[0]+'?r='+quote(podzielone[1])
		nowy_url = base_url + href
		nowy_kod_html = urlopen(nowy_url).read()
		nowy_tree = html.fromstring(
				nowy_kod_html.decode('windows-1250'))
		return nowy_tree
	else:
		return tree

def przetworz_rozklad(url,base_url,stary_base_url):
	"""
	Pobieramy rozkład i przetwarzamy go. Do odczytania ramek
	potrzebne było czary_mary z base_url i stary_base_url.

	Wynika to ze sposobu, w jaki pliki z rozkładami są zapisane
	w pliku .zip na stronie. Poza znakiem zapytaniem w treści,
	trzeba było jeszcze jakoś rozwiązać "../" w adresach.
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
	print(tree.text_content())
	input() #USUNĄĆ PO TESTACH

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

	def przetworz_kierunek(self,kierunek):
		"""
		Przetwarzamy pojedynczy kierunek jazdy z listy przystanków.
		"""
		for wpis in kierunek.xpath('.//tr')[1:]: #[1:] = bez nagłówka
			ulica_glowna = wpis[0].text_content().strip()
			link = wpis[2].xpath('a')
			if link: #przystanek może nie mieć linka, zwykle pętla.
				nazwa_przystanku = link[0].text_content()
				url_rozkladu = link[0].attrib['href']
				base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'
				#przetwarzamy rozkład jazdy, w celach testowych
				przetworz_rozklad(url_rozkladu,
						base_url_rozkladu,
						self.base_url)
				break #USUNĄĆ PO TESTACH
			else:
				nazwa_przystanku = wpis[2].text_content()
			"""
			Na razie pojedynczy przystanek reprezentowany jest
			wyłącznie przez jego nazwę, która na dzień dzisiejszy
			jest kiepsko formatowana. Jak już zerknę, co powinno
			być w klasie, utworzę takową.
			"""
			self.przystanki += ["%s - %s" % (
				ulica_glowna,nazwa_przystanku)]

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
		
			for kierunek in tree.xpath('//td [@class="przyst"]'):
				self.przetworz_kierunek(kierunek)
				break #USUNĄĆ PO TESTACH

		return self.przystanki

def pobierz_plik(url,nazwa_pliku,rozmiar_bufora=2048):
	"""
	Pobierz plik, biorąc pod uwagę, że może się cały w pamięci nie 
	zmieścić.
	"""
	h = urlopen(url)
	f = open(nazwa_pliku,'wb')
	while True:
		buf = h.read(rozmiar_bufora)
		if len(buf)==0:
			break #EOF
		f.write(buf)
	f.close()

def rozpakuj_plik(nazwa_pliku,katalog='.'):
	"""
	Myślałem, że będzie tu więcej kodu. Z drugiej strony, nie testowałem
	tego pod Windows.
	"""
	plik = zipfile.ZipFile(nazwa_pliku)
	plik.extractall(path=katalog)

def pobierz_paczki():
	"""
	Pobiera paczki z rozkładami i rozpakowuje je.
	"""
	nazwy_plikow = ['autobusy.zip','tramwaje.zip',
			'nocne.zip','przesiadki.zip']
	url = 'http://mpk.lodz.pl/rozklady/skompresowane_rozklady/'
	if not os.path.exists('pliki'):
		os.makedirs('pliki')
	for nazwa_pliku in nazwy_plikow:
		print("Pobieram %s..." % nazwa_pliku)
		pobierz_plik(url+nazwa_pliku,'pliki/'+nazwa_pliku)
	print("OK, teraz je rozpakuje...")
	try:
		shutil.rmtree('rozpakowane')
	except OSError as e:
		"""
		nietestowane pod Windowsem - jesli katalog nie istnieje,
		jest to dopusczalny wyjatek. kazdy inny ponownie wyrzuc.
		"""
		if e.errno==2: 
			pass
		else:
			raise
	os.makedirs('rozpakowane')
	for nazwa_pliku in nazwy_plikow:
		rozpakuj_plik('pliki/'+nazwa_pliku,'rozpakowane')

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
	for linia in linie_td:
		link = linia.xpath('a')[0]
		nazwa_linii = link.text_content().lstrip("Linia: ")
		url_linii = url+link.attrib['href']
		ret += [Linia(nazwa_linii,url_linii,url)]
	return ret

if __name__=='__main__':
	"""
	Kod testujący.
	"""
	#pobierz_paczki()
	z_paczki = listuj_linie('file://%s/' % os.path.realpath('rozpakowane'))
	ze_strony = listuj_linie('http://www.mpk.lodz.pl/rozklady/')
	assert(z_paczki==ze_strony)
	przetworzonych = 0
	z_bledami = 0
	for i in range(len(z_paczki)):
		przetworzonych += 1
		print("Porownuje %s i %s..." % (
			z_paczki[i].nazwa, ze_strony[i].nazwa))
		przystanki_z_paczki = z_paczki[i].pobierz_przystanki()
		przystanki_ze_strony = ze_strony[i].pobierz_przystanki()
		if(przystanki_z_paczki!=przystanki_ze_strony):
			print("Różnica!")
			z_bledami += 1
			#print(przystanki_z_paczki,przystanki_ze_strony)
		#assert(przystanki_z_paczki==przystanki_ze_strony)
		sys.exit(0) #USUNĄĆ PO TESTACH
	print("Przetworzonych: %d, z błędami: %d" % (
		przetworzonych, z_bledami))

