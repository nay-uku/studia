#include "Osoba.h"



Osoba::Osoba()
{
}

Osoba::Osoba(string imie, string nazwisko, string login, string haslo)
{
	this->imie = imie;
	this->nazwisko = nazwisko;
	this->login = login;
	this->haslo = haslo;
}

void Osoba::ustaw(string imie, string nazwisko, string login, string haslo)
{
	this->imie = imie;
	this->nazwisko = nazwisko;
	this->login = login;
	this->haslo = haslo;
}


Osoba::~Osoba()
{
}
