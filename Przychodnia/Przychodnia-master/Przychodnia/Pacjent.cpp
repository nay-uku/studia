#include "Pacjent.h"



Pacjent::Pacjent()
{
}

Pacjent::Pacjent(string imie, string nazwisko, string login, string haslo)
	: Osoba(imie, nazwisko, login, haslo)
{
}


Pacjent::~Pacjent()
{
}
