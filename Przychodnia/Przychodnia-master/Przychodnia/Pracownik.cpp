#include "Pracownik.h"



Pracownik::Pracownik()
{
}

Pracownik::Pracownik(string imie, string nazwisko, string login, string haslo)
	: Osoba(imie, nazwisko, login, haslo)
{
}


Pracownik::~Pracownik()
{
}
