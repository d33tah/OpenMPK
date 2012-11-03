#!/usr/bin/python3
# -*- coding: windows-1250 -*-

from __future__ import print_function

import sys #exit()
import os #do sprawdzania czy katalog istnieje
import shutil #wygodne usuwanie katalogu
import zipfile #pliki .zip
from lxml import html

if not sys.version.startswith('3'):
	print("""
	Ten program został przeznaczony do uruchamiania pod interpreterem
	Pythona w wersji 3.x W teorii wszystko powinno działać, ale na wszelki
	wypadek przerywam działanie programu.
	""")
	#sys.exit(1) #zakomentuj tą linijkę, jeśli czujesz się odważny :P

if sys.version.startswith('2'):
	from urllib2 import urlopen
elif sys.version.startswith('3'):
	from urllib.request import urlopen

def pobierz_plik(url,nazwa_pliku,rozmiar_bufora=2048):
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
	Aktualnie działa tylko pod Linuksem. Nie wiem jak wygląda sprawa
	z 
	"""
	plik = zipfile.ZipFile(nazwa_pliku)
	plik.extractall(path=katalog)

def pobierz_paczki():
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
	kod_html = urlopen(url+'/index.html').read()
	tree = html.fromstring(kod_html.decode('windows-1250'))

	ramka = tree.xpath('//frame [@name="rozklad"]')
	print("len(ramka)=%s" % len(ramka))
	assert(len(ramka)==1)
	ramka = ramka[0]

	kod_html = urlopen(url+ramka.attrib['src'])

	pass

if __name__=='__main__':
	listuj_linie('file://%s/' % os.path.realpath('rozpakowane'))
	listuj_linie('http://www.mpk.lodz.pl/rozklady/')
	#pobierz_paczki()

