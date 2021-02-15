#include <iostream>
#include <fstream>
#include <vector>

#include "Administrator.h"

using namespace std;

int main()
{
	Administrator* administrator = new Administrator("admin", "123");
	vector<Biegacz*> biegacze;
	vector<Bieg*> biegi;
	vector<Rezultat*> rezultaty;

	int wybor;



	while (true)
	{
		cout << "\nZaloguj jako\n";
		cout << "1 - Administrator\n";
		cout << "2 - Biegacz\n";

		cin >> wybor;

		string login;
		string haslo;

		if (wybor == 1)
		{
			while (true)
			{
				cout << "Login: ";
				cin >> login;
				cout << "Haslo: ";
				cin >> haslo;
				if (administrator->zaloguj(login, haslo))
				{
					break;
				}
			}

			while (true)
			{
				cout << "\nWybierz akcje:\n";
				cout << "1 - Dodaj biegacza\n";
				cout << "2 - Dodaj bieg\n";
				cout << "3 - Dodaj rezultat biegu\n";
				cout << "4 - Wyswietl biegaczy\n";
				cout << "5 - Wyswietl biegi\n";
				cout << "6 - Wyloguj\n";

				cin >> wybor;

				if (wybor == 1)
				{
					administrator->dodajBiegacza(biegacze);
				}
				else if (wybor == 2)
				{
					administrator->dodajBieg(biegi);
				}
				else if (wybor == 3)
				{
					administrator->dodajRezultat(biegacze, biegi);
				}
				else if (wybor == 4)
				{
					administrator->wyswietlBiegaczy(biegacze);
				}
				else if (wybor == 5)
				{
					administrator->wyswietlBiegi(biegi);
				}
				else if (wybor == 6)
				{
					break;
				}
			}
		}
		else if (wybor == 2)
		{
			Biegacz* biegacz = nullptr;

			while (true)
			{
				cout << "Login: ";
				cin >> login;
				cout << "Haslo: ";
				cin >> haslo;

				bool zalogowano = false;

				for (Biegacz* b : biegacze)
				{
					if (b->zaloguj(login, haslo))
					{
						biegacz = b;
						zalogowano = true;
						break;
					}
				}

				if (zalogowano)
				{
					break;
				}
			}

			while (true)
			{
				cout << "\nWybierz akcje:\n";
				cout << "1 - Wyswietl rezultaty\n";
				cout << "2 - Oblicz srednia predkosc wybranego biegacza\n";
				cout << "3 - Oblicz pokonany dystans wybranego biegacza\n";
				cout << "4 - Wyloguj\n";

				cin >> wybor;

				if (wybor == 1)
				{
					biegacz->wyswietlRezultaty();
				}
				else if (wybor == 2)
				{
					biegacz->obliczSredniaPredkosc();
				}
				else if (wybor == 3)
				{
					biegacz->obliczPokonanyDystans();
				}
				else if (wybor == 4)
				{
					break;
				}
			}
		}
	}


	ofstream fAdministrator;
	fAdministrator.open("administrator.txt");
	fAdministrator << *administrator << "\n";
	fAdministrator.close();

	ofstream fBiegacze;
	fBiegacze.open("biegacze.txt");
	for (Biegacz* biegacz : biegacze) fBiegacze << *biegacz << "\n";
	fBiegacze.close();

	ofstream fBiegi;
	fBiegi.open("biegi.txt");
	for (Bieg* bieg : biegi) fBiegi << *bieg << "\n";
	fBiegi.close();

	ofstream fRezultaty;
	fRezultaty.open("rezultaty.txt");
	for (Rezultat* rezultat : rezultaty) fRezultaty << *rezultat << "\n";
	fRezultaty.close();
	
	return 0;
}