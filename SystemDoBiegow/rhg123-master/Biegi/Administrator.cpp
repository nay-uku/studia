#include "Administrator.h"



Administrator::Administrator()
{
}

Administrator::Administrator(string login, string haslo)
{
	this->login = login;
	this->haslo = haslo;
}


Administrator::~Administrator()
{
}

bool Administrator::zaloguj(string login, string haslo)
{
	return this->login == login && this->haslo == haslo;
}

void Administrator::dodajBiegacza(vector<Biegacz*>& biegacze)
{
	string imie;
	string nazwisko;
	string login;
	string haslo;
	cout << "Podaj dane:\n";
	cout << "Imie: ";
	cin >> imie;
	cout << "Nazwisko: ";
	cin >> nazwisko;
	cout << "Login: ";
	cin >> login;
	cout << "Haslo: ";
	cin >> haslo;
	biegacze.push_back(new Biegacz(imie, nazwisko, login, haslo));
}

void Administrator::dodajBieg(vector<Bieg*>& biegi)
{
	string nazwa;
	double dystans;
	cout << "Podaj dane:\n";
	cout << "Nazwa: ";
	cin >> nazwa;
	cout << "Dystans: ";
	cin >> dystans;
	biegi.push_back(new Bieg(nazwa, dystans));
}
Bieg * Administrator::wybierzBieg(vector<Bieg*>& biegi)
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

Biegacz * Administrator::wybierzBiegacza(vector<Biegacz*>& biegacze)
{
	cout << "Wybierz biegacza:\n";
	int i = 1;
	for (Biegacz* biegacz : biegacze)
	{
		cout << (i++) << ": " << biegacz->imieNazwisko() << "\n";
	}
	int wybor;
	cin >> wybor;
	wybor--;

	if (wybor >= 0 && wybor < biegacze.size())
	{
		return biegacze[wybor];
	}
	else
	{
		return nullptr;
	}
}
void Administrator::dodajRezultat(vector<Biegacz*>& biegacze, vector<Bieg*>& biegi)
{
	Biegacz* biegacz = wybierzBiegacza(biegacze);
	Bieg* bieg = wybierzBieg(biegi);
	double czas;

	cout << "Czas (w sekundach):";
	cin >> czas;

	biegacz->dodajRezultat(new Rezultat(bieg, czas));
}

void Administrator::wyswietlBiegaczy(vector<Biegacz*>& biegacze)
{
	int i = 1;
	for (Biegacz* biegacz : biegacze)
	{
		cout << (i++) << ": " << biegacz->imieNazwisko() << "\n";
	}
}

void Administrator::wyswietlBiegi(vector<Bieg*>& biegi)
{
	int i = 1;
	for (Bieg* bieg : biegi)
	{
		cout << (i++) << ": " << bieg->opis() << "\n";
	}
}
