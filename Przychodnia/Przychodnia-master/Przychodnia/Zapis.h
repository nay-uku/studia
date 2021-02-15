#pragma once
#include <fstream>

// szablon klasy
// za T moze byc podstawiony dowolny obiekt
template <class T>
class Zapis
{
public:
	Zapis() {} // konstruktor
	~Zapis() {} // destruktor

	// szablon metody
	// jak widac metoda przyjmuje jako parametr wektor obiektow typu T
	template <class T>
	void zapiszDoPliku(vector<T*>& t, string nazwaPliku)
	{
		ofstream file;
		// otwieramy plik
		file.open(nazwaPliku);
		// wpisujemy zawartosc obiektu t
		// (czyli klasa T musi miec przeciazony operator strumieniowy)
		for (vector<T*>::iterator it = t.begin(); it != t.end(); it++)
		{
			file << t << "\n";
		}	
		// zamykamy plik
		file.close();
	}
};

