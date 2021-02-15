#include "Lekarz.h"


Lekarz::Lekarz()
{
}

Lekarz::Lekarz(string imie, string nazwisko, string login, string haslo)
	: Osoba(imie, nazwisko, login, haslo)
{
}


Lekarz::~Lekarz()
{
}

void Lekarz::ustawSpecjalizacje(string specjalizacja)
{
	this->specjalizacja = specjalizacja;
}
