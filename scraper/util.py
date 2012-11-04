#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
util.py

Tutaj b�d� funkcje u�ytkowe, kt�rych mi brakuje w Pythonie i tych jego 
bibliotekach, kt�re znam. Funkcje b�d� oczywi�cie uzbrojone w zbi�r hack�w
potrzebnych, aby by� w stanie dogada� si� z tym cudem my�li programistycznej,
jakim s� strony MPK.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
import os #makedir
from lxml import html #parsowanie HTML
import re #wyra�enia regularne

#za�aduj biblioteki z Pythona 2/3 ze sp�jnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
	from urllib2 import quote
elif sys.version.startswith('3'):
	from urllib.parse import quote
	from urllib.request import urlopen


def makedir_quiet(dirname):
	"""
	Nie chcia�o mi si� tysi�c razy pisa� tej samej konstrukcji, wi�c 
	zrobi�em sobie funkcj�, kt�ra tworzy katalog i t�umi b��d wynikaj�cy
	z tego, �e on ju� istnieje.
	"""
	try:
		os.makedirs(dirname)
	except os.error:
		pass


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

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	pass #na dzie� dzisiejszy brak.

