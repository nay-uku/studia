#pragma once

#include "Osoba.h"

class Lekarz : public Osoba
{
private:
	string specjalizacja;

public:
	Lekarz();
	Lekarz(string imie, string nazwisko, string login, string haslo);
	~Lekarz();
	void ustawSpecjalizacje(string specjalizacja);

	friend ostream& operator<< (ostream& out, const Lekarz& lekarz)
	{
		out << lekarz.imie << " " << lekarz.nazwisko << ", specjalizacja: " << lekarz.specjalizacja;
		return out;
	}
};

