#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
util.py

Tutaj będą funkcje użytkowe, których mi brakuje w Pythonie i tych jego 
bibliotekach, które znam. Funkcje będą oczywiście uzbrojone w zbiór hacków
potrzebnych, aby być w stanie dogadać się z tym cudem myśli programistycznej,
jakim są strony MPK.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
import os #makedir
from lxml import html #parsowanie HTML
import re #wyrażenia regularne

#załaduj biblioteki z Pythona 2/3 ze spójnymi nazwami
if sys.version.startswith('2'):
	from urllib2 import urlopen
	from urllib2 import quote
elif sys.version.startswith('3'):
	from urllib.parse import quote
	from urllib.request import urlopen


def makedir_quiet(dirname):
	"""
	Nie chciało mi się tysiąc razy pisać tej samej konstrukcji, więc 
	zrobiłem sobie funkcję, która tworzy katalog i tłumi błąd wynikający
	z tego, że on już istnieje.
	"""
	try:
		os.makedirs(dirname)
	except os.error:
		pass


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

if __name__=='__main__':
	"""
	Kod testujący.
	"""
	pass #na dzień dzisiejszy brak.

