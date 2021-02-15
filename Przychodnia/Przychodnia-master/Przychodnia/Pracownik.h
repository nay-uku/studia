#pragma once

#include "Osoba.h"

class Pracownik : public Osoba
{
public:
	Pracownik();
	Pracownik(string imie, string nazwisko, string login, string haslo);
	~Pracownik();

	friend ostream& operator<< (ostream& out, const Pracownik& pracownik)
	{
		out << pracownik.imie << " " << pracownik.nazwisko;
	}
};

