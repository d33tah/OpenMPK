#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
downloader.py

Zadaniem tego modu�u jest pobieranie plik�w .zip ze strony MPK oraz 
rozpakowanie ich.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
import os #do sprawdzania czy katalog istnieje
import shutil #wygodne usuwanie katalogu
import zipfile #pliki .zip

#za�aduj biblioteki z Pythona 2/3 ze sp�jnymi nazwami
if sys.version.startswith('2'):
      from urllib2 import urlopen
elif sys.version.startswith('3'):
      from urllib.request import urlopen

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

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	pobierz_paczki()

