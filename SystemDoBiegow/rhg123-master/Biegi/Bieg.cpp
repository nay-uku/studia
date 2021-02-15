#include "Bieg.h"



Bieg::Bieg()
{
}

Bieg::Bieg(string nazwa, double dystans)
{
	this->nazwa = nazwa;
	this->dystans = dystans;
}


Bieg::~Bieg()
{
}

string Bieg::opis()
{
	return nazwa + ", " + to_string(dystans) + "km";
}
