#include "Rezultat.h"

Rezultat::Rezultat()
{
}

Rezultat::Rezultat(Bieg * bieg, double czas)
{
	this->bieg = bieg;
	this->czas = czas;
}

Rezultat::~Rezultat()
{
}

double Rezultat::Czas()
{
	return czas;
}

double Rezultat::Dystans()
{
	return bieg->dystans;
}

string Rezultat::opis()
{
	return bieg->opis() + ", " + to_string(czas) + "s";
}
