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

import sys #exit(), version
import os #do sprawdzania czy katalog istnieje

if not sys.version.startswith('3'):
	print("""
	Ten program został przeznaczony do uruchamiania pod interpreterem
	Pythona w wersji 3.x W teorii wszystko powinno działać, ale na wszelki
	wypadek przerywam działanie programu.
	""")
	sys.exit(1) #zakomentuj tą linijkę, jeśli czujesz się odważny :P
	print("Program kontynuuje pracę...")

from Linia import Linia
from downloader import pobierz_paczki

if __name__=='__main__':
	"""
	Kod testujący.
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
		print("Teraz będzie ze strony.")
		przystanki_ze_strony = ze_strony[i].pobierz_przystanki()
		if(przystanki_z_paczki!=przystanki_ze_strony):
			print("Różnica!")
			z_bledami += 1
			#print(przystanki_z_paczki,przystanki_ze_strony)
		#assert(przystanki_z_paczki==przystanki_ze_strony)
		sys.exit(0) #USUNĄĆ PO TESTACH
	print("Przetworzonych: %d, z błędami: %d" % (
		przetworzonych, z_bledami))

