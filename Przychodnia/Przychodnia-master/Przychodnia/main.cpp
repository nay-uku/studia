
#include <iostream>
#include <fstream>

#include "Przychodnia.h"

int main()
{
	Przychodnia przychodnia;

	cout << "PRZYCHODNIA\n";
	cout << "1 - Zaloguj jako pracownik\n";
	cout << "2 - Zaloguj jako lekarz\n";
	cout << "3 - Zaloguj jako pacjent\n";

	int wybor;
	cin >> wybor;

	przychodnia.dodajPracownika("Jan", "Nowak", "jannowak", "123");

	przychodnia.dodajLekarza("Tomasz", "Kowalski", "tomaszkowalski", "123");
	przychodnia.dodajLekarza("Marcin", "Kot", "marcinkot", "123");

	przychodnia.dodajPacjenta("Adam", "Zajac", "adamzajac", "123");
	przychodnia.dodajPacjenta("Grzegorz", "Lewandowski", "grzegorzlewandowski", "123");

	if (wybor == 1)
	{
		string login, haslo;
		while (true)
		{			
			cout << "Podaj login: ";
			cin >> login;
			cout << "Podaj haslo: ";
			cin >> haslo;
			bool statusLogowania = przychodnia.zalogujPracownika(login, haslo);
			if (!statusLogowania)
			{
				cout << "Nie udalo sie zalogowac!\n";
				continue;
			}
			else
			{
				break;
			}			
		}

		while (true)
		{
			cout << "\nPanel pracownika:\n";
			cout << "1 - Dodaj pacjenta\n";
			cout << "2 - Usun pacjenta\n";
			cout << "3 - Edytuj pacjenta\n";
			cout << "4 - Dodaj lekarza\n";
			cout << "5 - Usun lekarza\n";
			cout << "6 - Edytuj lekarza\n";
			cout << "7 - Ustaw specjalizacje lekarza\n";
			cout << "8 - Zarejestruj pacjenta\n";
			cout << "9 - Ustaw status wizyty\n";
			cout << "10 - Przegladaj wizyty\n";
			cout << "11 - Wyjdz\n";
			cout << "> ";

			cin >> wybor;

			switch (wybor)
			{
			case 1:
				przychodnia.dodajPacjenta();
				break;
			case 2:
				przychodnia.usunPacjenta();
				break;
			case 3:
				przychodnia.edytujPacjenta();
				break;
			case 4:
				przychodnia.dodajLekarza();
				break;
			case 5:
				przychodnia.usunLekarza();
				break;
			case 6:
				przychodnia.edytujLekarza();
				break;
			case 7:
				przychodnia.ustawSpecjalizacjeLekarza();
				break;
			case 8:
				przychodnia.zarejestrujPacjenta();
				break;
			case 9:
				przychodnia.ustawStatusWizyty();
				break;
			case 10:
				przychodnia.przegladajWizyty();
				break;
			case 11:

				return 0;
			}
		}
	}
	else if (wybor == 2)
	{
		string login, haslo;
		while (true)
		{		
			cout << "Podaj login: ";
			cin >> login;
			cout << "Podaj haslo: ";
			cin >> haslo;
			bool statusLogowania = przychodnia.zalogujLekarza(login, haslo);
			if (!statusLogowania)
			{
				cout << "Nie udalo sie zalogowac!\n";
				continue;
			}
			else
			{
				break;
			}
		}

		while (true)
		{
			cout << "\nPanel lekarza:\n";
			cout << "1 - Przegladaj wizyty pacjentow\n";
			cout << "2 - Wyjdz\n";

			cin >> wybor;

			switch (wybor)
			{
			case 1:
				przychodnia.przegladajWizytyLekarza(login);
				break;
			case 2:
				return 0;
			}
		}
	}
	else if (wybor == 3)
	{
		string login, haslo;
		while (true)
		{
			cout << "Podaj login: ";
			cin >> login;
			cout << "Podaj haslo: ";
			cin >> haslo;
			bool statusLogowania = przychodnia.zalogujPacjenta(login, haslo);
			if (!statusLogowania)
			{
				cout << "Nie udalo sie zalogowac!\n";
				continue;
			}
			else
			{
				break;
			}
		}

		while (true)
		{
			cout << "\nPanel pacjenta:\n";
			cout << "1 - Przegladaj lekarzy\n";
			cout << "2 - Przegladaj wizyty\n";
			cout << "3 - Wyjdz\n";

			cin >> wybor;

			switch (wybor)
			{
			case 1:
				przychodnia.przegladajLekarzy();
				break;
			case 2:
				przychodnia.przegladajWizytyPacjenta(login);
				break;
			case 3:
				return 0;
			}
		}
	}
	return 0;
}