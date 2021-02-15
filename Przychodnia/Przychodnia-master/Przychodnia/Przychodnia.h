#pragma once

#include <iostream>
#include <vector>

#include "Pracownik.h"
#include "Lekarz.h"
#include "Pacjent.h"
#include "Wizyta.h"

using namespace std;

class Przychodnia
{
private:

	// kompozycja - Przychodnia zawiera pracownikow, lekarzy, pacjentow, wizyty
	vector<Pracownik*> pracownicy;
	vector<Lekarz*> lekarze;
	vector<Pacjent*> pacjenci;
	vector<Wizyta*> wizyty;

public:
	Przychodnia();
	~Przychodnia();

	bool zalogujPracownika(string login, string haslo);
	bool zalogujLekarza(string login, string haslo);
	bool zalogujPacjenta(string login, string haslo);
	int wybierzPracownika();
	int wybierzLekarza();
	int wybierzPacjenta();
	int wybierzWizyte();
	void dodajPacjenta();
	void dodajPacjenta(string imie, string nazwisko, string login, string haslo);
	void usunPacjenta();
	void edytujPacjenta();
	void dodajLekarza();
	void dodajLekarza(string imie, string nazwisko, string login, string haslo);
	void usunLekarza();
	void edytujLekarza();
	void dodajPracownika();
	void dodajPracownika(string imie, string nazwisko, string login, string haslo);
	void ustawSpecjalizacjeLekarza();
	void zarejestrujPacjenta();
	void ustawStatusWizyty();
	void przegladajWizyty();
	void przegladajWizytyLekarza(string login);
	void przegladajLekarzy();
	void przegladajWizytyPacjenta(string login);
};

