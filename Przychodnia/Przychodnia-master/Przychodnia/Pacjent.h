#pragma once

#include "Osoba.h"

class Pacjent : public Osoba
{
public:
	Pacjent();
	Pacjent(string imie, string nazwisko, string login, string haslo);
	~Pacjent();

	friend ostream& operator<< (ostream& out, const Pacjent& pacjent)
	{
		out << pacjent.imie << " " << pacjent.nazwisko;
		return out;
	}
};

