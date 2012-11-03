#!/usr/bin/python3
# -*- coding: windows-1250 -*-

"""
scraper.py

Ten kod z za�o�enia ma pobiera� dane z pobranych z mpk.lodz.pl paczek 
z rozk�adami, a tak�e samodzielnie pobiera� stamt�d surowe dane i przetwarza�
je. Po przetworzeniu na wyj�ciu ma pojawia� si� �atwiejsza do przetworzenia
struktura danych.

Kod na dzie� dzisiejszy wygl�da przeokropnie - upar�em si� na Pythona 3, a �e
nie by�em w stanie znale�� dla niego �adnej biblioteki dla scrapingu, u�y�em
urllib+w�asnych hack�w. Drugim powodem jest spos�b, w jaki zbudowana jest
strona MPK - jest kilka ciekawych kwiatk�w, opisane w komentarzach poni�ej.
Trzeci pow�d jest taki, �e na ka�dym z krok�w nie mia�em poj�cia, czego b�d�
potrzebowa� za chwil� i tak powsta� hack na hacku. Kiedy� pewnie b�dzie trzeba
to przepisa�.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit()
import os #do sprawdzania czy katalog istnieje
import shutil #wygodne usuwanie katalogu
import zipfile #pliki .zip
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


def popraw_file_url(url):
	"""
	HACK.

	Powodem jest spos�b, w jaki zorganizowane s� strony w pliczkach
	zip z mpk.lodz.pl. Rozk�ady s� tam �adowane do linie.htm?p1=w1&p2=w2.
	Oczywi�cie taki plik nie istnieje, wi�c musi zosta� za�adowany 
	linie.htm, a reszta tekstu obci�ta. Zwracany jest poprawiony URL.
	"""
	if url.startswith('file://'):
		#we� A/B i zapisz A w podzielony[0] i B w podzielony[1]
		podzielony = re.findall('^(.*)/(.*)$',url)[0]
		#poszukaj znaku zapytania
		indeks = podzielony[1].find('?')
		#je�li znalaz�e�
		if indeks!=-1:
			#zwr�� A/B do tego znaku
			return podzielony[0]+'/'+podzielony[1][:indeks]
		else: #w przeciwnych wypadkach zwr�� URL nienaruszony
			return url
	else:
		return url

def wybierz_ramke(tree,nazwa_ramki,base_url):
	"""
	Jako, �e mamy XXI wiek, strona jest oczywi�cie napisana na ramkach
	i tabelkach. Skrypt musi by� tego �wiadomy i pozwoli� na wyb�r 
	odpowiedniej ramki.

	Ta funkcja pobiera obiekt lxml.html, nazw� wyci�tej ramki oraz
	bazowy adres URL, kt�ry ma by� doklejony do wybranego z src ramki.
	Zwracany jest nowy (albo i nie, je�li ramek nie ma) obiekt lxml.html,
	kt�ry ma ju� za�adowan� zawarto�� ramki.
	"""
	ramka = tree.xpath('//frame [@name="%s"]' % nazwa_ramki)
	if(len(ramka)==1): #znaleziono ramk�
		href = ramka[0].attrib['src']
		"""
		HACK: je�eli w linku jest ?r=, to dalej b�dzie tekst 
		wy�wietlany �ywcem na stronie. Trzeba go przepu�ci� przez
		quote, ale tylko cz�� po ?r=.
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
	print(tree.text_content())
	input() #USUN�� PO TESTACH

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
				przetworz_rozklad(url_rozkladu,
						base_url_rozkladu,
						self.base_url)
				break #USUN�� PO TESTACH
			else:
				nazwa_przystanku = wpis[2].text_content()
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

def pobierz_plik(url,nazwa_pliku,rozmiar_bufora=2048):
	"""
	Pobierz plik, bior�c pod uwag�, �e mo�e si� ca�y w pami�ci nie 
	zmie�ci�.
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
	My�la�em, �e b�dzie tu wi�cej kodu. Z drugiej strony, nie testowa�em
	tego pod Windows.
	"""
	plik = zipfile.ZipFile(nazwa_pliku)
	plik.extractall(path=katalog)

def pobierz_paczki():
	"""
	Pobiera paczki z rozk�adami i rozpakowuje je.
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
			print("R�nica!")
			z_bledami += 1
			#print(przystanki_z_paczki,przystanki_ze_strony)
		#assert(przystanki_z_paczki==przystanki_ze_strony)
		sys.exit(0) #USUN�� PO TESTACH
	print("Przetworzonych: %d, z b��dami: %d" % (
		przetworzonych, z_bledami))

