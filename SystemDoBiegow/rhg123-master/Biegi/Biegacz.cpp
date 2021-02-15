#include "Biegacz.h"

Biegacz::Biegacz()
{
}

Biegacz::Biegacz(string imie, string nazwisko, string login, string haslo)
{
	this->imie = imie;
	this->nazwisko = nazwisko;
	this->login = login;
	this->haslo = haslo;
}

Biegacz::~Biegacz()
{
}

bool Biegacz::zaloguj(string login, string haslo)
{
	return this->login == login && this->haslo == haslo;
}

Bieg * Biegacz::wybierzBieg(vector<Bieg*>& biegi)
{
	cout << "Wybierz bieg:\n";
	int i = 1;
	for (Bieg* bieg : biegi)
	{
		cout << (i++) << ": " << *bieg << "\n";
	}

	int wybor;
	cin >> wybor;
	wybor--;

	if (wybor >= 0 && wybor < biegi.size())
	{
		return biegi[wybor];
	}
	else
	{
		return nullptr;
	}
}

void Biegacz::dodajRezultat(Rezultat * rezultat)
{
	rezultaty.push_back(rezultat);
}

void Biegacz::wyswietlRezultaty()
{
	int i = 1;
	for (Rezultat* rezultat : rezultaty)
	{
		cout << (i++) << ": " << *rezultat << "\n";
	}
}

void Biegacz::obliczSredniaPredkosc()
{
	double dystans = accumulate(
		rezultaty.begin(),
		rezultaty.end(),
		0.0,
		[&](double d, Rezultat* r) -> double { return d + r->Dystans(); }//lambda
	);

	double czas = accumulate(
		rezultaty.begin(),
		rezultaty.end(),
		0.0,
		[&](double d, Rezultat* r) -> double { return d + r->Czas(); }//lambda
	);

	cout << "Srednia predkosc: " << (dystans / (czas / 3600)) << "km/h";
}

void Biegacz::obliczPokonanyDystans()
{
	double dystans = accumulate(
		rezultaty.begin(),
		rezultaty.end(),
		0.0,
		[&](double d, Rezultat* r) -> double { return d + r->Dystans(); }
	);

	cout << "Dystans: " << dystans << "km";
}

string Biegacz::imieNazwisko()
{
	return imie + " " + nazwisko;
}
