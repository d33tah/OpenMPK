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

import sys #exit(), version
import os #do sprawdzania czy katalog istnieje

if not sys.version.startswith('3'):
	print("""
	Ten program zosta� przeznaczony do uruchamiania pod interpreterem
	Pythona w wersji 3.x W teorii wszystko powinno dzia�a�, ale na wszelki
	wypadek przerywam dzia�anie programu.
	""")
	sys.exit(1) #zakomentuj t� linijk�, je�li czujesz si� odwa�ny :P
	print("Program kontynuuje prac�...")

from Linia import Linia
from downloader import pobierz_paczki

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	#pobierz_paczki()
	z_paczki = Linia.listuj_linie('file://%s/' % os.path.realpath('rozpakowane'))
	ze_strony = Linia.listuj_linie('http://www.mpk.lodz.pl/rozklady/')
	assert(z_paczki==ze_strony)
	przetworzonych = 0
	z_bledami = 0
	for i in range(len(z_paczki)):
		przetworzonych += 1
		print("Porownuje %s i %s..." % (
			z_paczki[i].nazwa, ze_strony[i].nazwa))
		przystanki_z_paczki = z_paczki[i].pobierz_przystanki()
		print("Teraz b�dzie ze strony.")
		przystanki_ze_strony = ze_strony[i].pobierz_przystanki()
		if(przystanki_z_paczki!=przystanki_ze_strony):
			print("R�nica!")
			z_bledami += 1
			#print(przystanki_z_paczki,przystanki_ze_strony)
		#assert(przystanki_z_paczki==przystanki_ze_strony)
		sys.exit(0) #USUN�� PO TESTACH
	print("Przetworzonych: %d, z b��dami: %d" % (
		przetworzonych, z_bledami))

