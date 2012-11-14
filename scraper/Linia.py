#!/usr/bin/python3 -u
# -*- coding: windows-1250 -*-

"""
Linia.py

Tutaj parsujemy informacje o pojedynczej linii - na ten moment, lista 
przystank�w. Dla ka�dego z przystank�w mo�na potem pobra� rozk�ad i przesiadki.
"""

#na wypadek uruchomienia pod Pythonem 2.x - funkcja print() zamiast operatora
from __future__ import print_function

import sys #exit(), version
from lxml import html #parsowanie HTML
import re #wyra�enia regularne
import os #path.exists

#za�aduj biblioteki z Pythona 2/3 ze sp�jnymi nazwami
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
		Por�wnywanie dw�ch obiekt�w klasy Linia - por�wnujemy tylko 
		nazwy. Domy�lnie obiekty s� r�wne tylko gdy jest to ten sam 
		obiekt w dw�ch referencjach.
		"""
		return isinstance(prawy,Linia) and (lewy.nazwa)==(prawy.nazwa)

	def obsluz_przesiadki(self,link):
		"""
		Wst�pny kod obs�ugi przesiadek. Klika w link "przesiadki" dla
		danego przystanku i listuje, jakie linie s� na danym 
		przystanku. UWAGA, du�e.
		"""
		url = link.attrib['href']

		#wyci�gamy tre�� przed ostatnim uko�nikiem jako 
		#base_url_rozkladu.
		base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'

		#B��dy tego typu maj� miejsce w ZIPach MPK. P�niej im to 
		#pewnie zg�osz�.
		docelowy_url = base_url_rozkladu+url 
		try:
			tree = html.parse(docelowy_url)
		except:
			print("t�umi� b��d pobierania: %s" % docelowy_url)
			return
		
		#Dane przystanku s� w jakim� divie albo foncie. Ma by� jeden.
		dane_przystanku_el = tree.xpath(
				'//*[self::font or self::div]')
		assert(len(dane_przystanku_el)==1)
		dane_przystanku_tekst=dane_przystanku_el[0].text_content()
		#Dzielimy to wed�ug wzorca - co�tam, co�tam w nawiasie, koniec.
		dane_przystanku = re.findall('(.*)\((.*?)\)$',
				dane_przystanku_tekst)[0]
		nazwa_przystanku = dane_przystanku[0] #pierwsze co�tam

		#Poni�sze trzy linijki daj� pewne wyobra�enie o tym jakiej 
		#jako�ci s� dane z ZIPa.
		nazwa_przystanku = nazwa_przystanku.lstrip('null')
		nazwa_przystanku = nazwa_przystanku.lstrip()
		nazwa_przystanku = nazwa_przystanku.lstrip('- ')
		nazwa_przystanku = nazwa_przystanku.rstrip()

		id_przystanku = dane_przystanku[1] #drugie co�tam
		
		nazwa_pliku_przesiadki = 'przetworzone/przesiadki/%s.txt' % \
				id_przystanku
		"""
		Je�eli istnieje ju� plik z przesiadkami, ustawiamy plik na 
		None, �eby go nie dopisywa� do bazy przesiadek.	Przy okazji, 
		je�li nie ma go w przesiadkach, dopiszmy go te�	do 
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
		
		#przechodzimy przez ka�dy tag <p>
		for p in tree.xpath('//p'):
			#dotyczy tylko strony WWW
			if p.text_content().endswith('na mapie'):
				continue
			#je�eli potem jest ul, to najprawdopodobniej jest to
			#lista przesiadek.
			nast_el = p.getnext()
			if(nast_el.tag=='ul'):
				for el in nast_el.xpath('li'):
					#uwaga na link! znowu b�dzie problem
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
				break #chyba, �e potrzebujemy linie w pobli�u?

	def przetworz_kierunek(self,kierunek,i):
		"""
		Przetwarzamy pojedynczy kierunek jazdy z listy przystank�w.
		Oznacza to, �e przejdziemy przez wszystkie przystanki w nim,
		ka�dy zapiszemy w li�cie przystank�w danego kierunku, a poza
		tym obs�u�ymy przesiadki i rozk�ad.
		"""
		
			#przejd� przez ka�dy <tr> jako wpis
		for wpis in kierunek.xpath('.//tr')[1:]: #[1:] = bez nag��wka
			ulica_glowna = wpis[0].text_content().strip()
			link = wpis[2].xpath('a')
			if link: #przystanek mo�e nie mie� linka, zwykle p�tla.
				nazwa_przystanku = link[0].text_content()
				url_rozkladu = link[0].attrib['href']
				base_url_rozkladu = re.findall('^(.*)/(.*)$',
						self.url)[0][0]+'/'
				#przetwarzamy rozk�ad jazdy, w celach testowych
				Rozklad.przetworz_rozklad(url_rozkladu,
						base_url_rozkladu,
						self.base_url,self.nazwa,i)
			else:
				nazwa_przystanku = wpis[2].text_content()

			#je�li w trzeciej kolumnie jest link, obs�u� 
			#przesiadki.
			if wpis[3].xpath('.//a'):
				self.obsluz_przesiadki(
						wpis[3].xpath('.//a')[0])
			"""
			Na razie pojedynczy przystanek reprezentowany jest
			wy��cznie przez jego nazw�. Jak ju� zerkn�, co powinno
			by� w klasie, utworz� takow�.
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
		Je�li ju� mamy przystanki, zwr�� je. W przeciwnym razie
		wejd� na linka z obiektu, przeskocz ramki i dla ka�dego
		z kierunk�w, przetw�rz go.
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
		nast�pi� przekierowanie, bo mamy index.jsp, a nie .html) i 
		pobiera list� linii.

		TODO: rozr�nia� autobusy dzienne/nocne i tramwaje? Na tej 
		podstronie jest taka mo�liwo��.
		"""
		tree = html.parse(url+'/index.html')
		przekierowanie = tree.xpath('//meta [@http-equiv="refresh"]')
		if przekierowanie:
			#Wybierz pierwszy element z tej tablicy i we� tekst na 
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
			#wytnij "Linia: " z linka i uznaj to za nazw� linii
			nazwa_linii = link.text_content().lstrip("Linia: ")
			url_linii = url+link.attrib['href']
			ret += [Linia(nazwa_linii,url_linii,url)]
			print(nazwa_linii,file=f)
		return ret

if __name__=='__main__':
	"""
	Kod testuj�cy.
	"""
	pass #niespodzianka, brak!

