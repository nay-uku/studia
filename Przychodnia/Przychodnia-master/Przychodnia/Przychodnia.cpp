#include "Przychodnia.h"



Przychodnia::Przychodnia()
{
}


Przychodnia::~Przychodnia()
{
}

bool Przychodnia::zalogujPracownika(string login, string haslo)
{
	for (vector<Pracownik*>::iterator it = pracownicy.begin(); it != pracownicy.end(); it++)
	{
		Pracownik* pracownik = *it;
		if (pracownik->login == login && pracownik->haslo == haslo)
		{
			return true;
		}
	}
	return false;
}

bool Przychodnia::zalogujLekarza(string login, string haslo)
{
	for (vector<Lekarz*>::iterator it = lekarze.begin(); it != lekarze.end(); it++)
	{
		Lekarz* lekarz = *it;
		if (lekarz->login == login && lekarz->haslo == haslo)
		{
			return true;
		}
	}
	return false;
}

bool Przychodnia::zalogujPacjenta(string login, string haslo)
{
	for (vector<Pacjent*>::iterator it = pacjenci.begin(); it != pacjenci.end(); it++)
	{
		Pacjent* pacjent = *it;
		if (pacjent->login == login && pacjent->haslo == haslo)
		{
			return true;
		}
	}
	return false;
}

int Przychodnia::wybierzPracownika()
{
	int i = 1;
	cout << "Wybierz pracownika:\n";
	for (vector<Pracownik*>::iterator it = pracownicy.begin(); it != pracownicy.end(); it++)
	{
		Pracownik* pracownik = *it;
		cout << (i++) << ". " << *pracownik << "\n";

	}
	int wybor;
	cin >> wybor;

	return wybor - 1;
}

int Przychodnia::wybierzLekarza()
{
	int i = 1;
	cout << "Wybierz lekarza:\n";
	for (vector<Lekarz*>::iterator it = lekarze.begin(); it != lekarze.end(); it++)
	{
		Lekarz* lekarz = *it;
		cout << (i++) << ". " << *lekarz << "\n";

	}
	int wybor;
	cin >> wybor;

	return wybor - 1;
}

int Przychodnia::wybierzPacjenta()
{
	int i = 1;
	cout << "Wybierz pacjenta:\n";
	for (vector<Pacjent*>::iterator it = pacjenci.begin(); it != pacjenci.end(); it++)
	{
		Pacjent* pacjent = *it;
		cout << (i++) << ". " << *pacjent << "\n";

	}
	int wybor;
	cin >> wybor;

	return wybor - 1;
}

int Przychodnia::wybierzWizyte()
{
	int i = 1;
	cout << "Wybierz wizyte:\n";
	for (vector<Wizyta*>::iterator it = wizyty.begin(); it != wizyty.end(); it++)
	{
		Wizyta* wizyta = *it;
		cout << (i++) <<
			". Lekarz: " << *wizyta->lekarz <<
			", pacjent: " << *wizyta->pacjent <<
			", termin:" << wizyta->data << " " << wizyta->godzina << "\n";

	}
	int wybor;
	cin >> wybor;

	return wybor - 1;
}

void Przychodnia::dodajPacjenta()
{
	string imie, nazwisko, login, haslo;
	cout << "Podaj imie: ";
	cin >> imie;
	cout << "Podaj nazwisko: ";
	cin >> nazwisko;
	cout << "Podaj login: ";
	cin >> login;
	cout << "Podaj haslo: ";
	cin >> haslo;

	dodajPacjenta(imie, nazwisko, login, haslo);
}

void Przychodnia::dodajPacjenta(string imie, string nazwisko, string login, string haslo)
{
	Pacjent* pacjent = new Pacjent(imie, nazwisko, login, haslo);
	pacjenci.push_back(pacjent);
}

void Przychodnia::usunPacjenta()
{
	int wybor = wybierzPacjenta();
	pacjenci.erase(pacjenci.begin() + wybor);
}

void Przychodnia::edytujPacjenta()
{
	int wybor = wybierzPacjenta();

	string imie, nazwisko, login, haslo;
	cout << "Podaj imie: ";
	cin >> imie;
	cout << "Podaj nazwisko: ";
	cin >> nazwisko;
	cout << "Podaj login: ";
	cin >> login;
	cout << "Podaj haslo: ";
	cin >> haslo;

	pacjenci[wybor]->ustaw(imie, nazwisko, login, haslo);
}

void Przychodnia::dodajLekarza()
{
	string imie, nazwisko, login, haslo;
	cout << "Podaj imie: ";
	cin >> imie;
	cout << "Podaj nazwisko: ";
	cin >> nazwisko;
	cout << "Podaj login: ";
	cin >> login;
	cout << "Podaj haslo: ";
	cin >> haslo;

	dodajLekarza(imie, nazwisko, login, haslo);
}

void Przychodnia::dodajLekarza(string imie, string nazwisko, string login, string haslo)
{
	Lekarz* lekarz = new Lekarz(imie, nazwisko, login, haslo);
	lekarze.push_back(lekarz);
}

void Przychodnia::usunLekarza()
{
	int wybor = wybierzLekarza();
	lekarze.erase(lekarze.begin() + wybor);
}

void Przychodnia::edytujLekarza()
{
	int wybor = wybierzLekarza();

	string imie, nazwisko, login, haslo;
	cout << "Podaj imie: ";
	cin >> imie;
	cout << "Podaj nazwisko: ";
	cin >> nazwisko;
	cout << "Podaj login: ";
	cin >> login;
	cout << "Podaj haslo: ";
	cin >> haslo;

	lekarze[wybor]->ustaw(imie, nazwisko, login, haslo);
}

void Przychodnia::dodajPracownika()
{
	string imie, nazwisko, login, haslo;
	cout << "Podaj imie: ";
	cin >> imie;
	cout << "Podaj nazwisko: ";
	cin >> nazwisko;
	cout << "Podaj login: ";
	cin >> login;
	cout << "Podaj haslo: ";
	cin >> haslo;

	dodajPracownika(imie, nazwisko, login, haslo);
}

void Przychodnia::dodajPracownika(string imie, string nazwisko, string login, string haslo)
{
	Pracownik* pracownik = new Pracownik(imie, nazwisko, login, haslo);
	pracownicy.push_back(pracownik);
}

void Przychodnia::ustawSpecjalizacjeLekarza()
{
	string specjalizacja;
	int wybor = wybierzLekarza();

	cout << "Podaj specjalizacje: ";
	cin >> specjalizacja;

	lekarze[wybor]->ustawSpecjalizacje(specjalizacja);
}

void Przychodnia::zarejestrujPacjenta()
{
	string data, godzina;
	int wyborLekarza = wybierzLekarza();
	int wyborPacjenta = wybierzPacjenta();

	cout << "Podaj date wizyty: ";
	cin >> data;

	cout << "Podaj godzine wizyty: ";
	cin >> godzina;

	wizyty.push_back(new Wizyta(lekarze[wyborLekarza], pacjenci[wyborPacjenta], data, godzina));
}

void Przychodnia::ustawStatusWizyty()
{
	int wyborWizyty = wybierzWizyte();

	cout << "1 - Ustaw jako zakonczona\n";
	cout << "2 - Ustaw jako anulowana\n";
	cout << "> ";

	int wybor;
	cin >> wybor;

	string status = wybor == 1 ? "zakonczona" : "anulowana";
	wizyty[wyborWizyty]->ustawStatus(status);
}

void Przychodnia::przegladajWizyty()
{
	int i = 1;
	for (vector<Wizyta*>::iterator it = wizyty.begin(); it != wizyty.end(); it++)
	{
		Wizyta* wizyta = *it;
		cout << (i++) << ". Lekarz: " << wizyta->lekarz->imie << " " << wizyta->lekarz->nazwisko <<
			", pacjent: " << wizyta->pacjent->imie << " " << wizyta->pacjent->nazwisko <<
			", termin: " << wizyta->data << " " << wizyta->godzina <<
			", status: " << wizyta->status << "\n";
	}
}

void Przychodnia::przegladajWizytyLekarza(string login)
{
	int i = 1;
	for (vector<Wizyta*>::iterator it = wizyty.begin(); it != wizyty.end(); it++)
	{
		Wizyta* wizyta = *it;

		if (wizyta->lekarz->login == login)
		{
			cout << (i++) << ". Lekarz: " << wizyta->lekarz->imie << " " << wizyta->lekarz->nazwisko <<
				", pacjent: " << wizyta->pacjent->imie << " " << wizyta->pacjent->nazwisko <<
				", termin: " << wizyta->data << " " << wizyta->godzina <<
				", status: " << wizyta->status << "\n";
		}
	}
}

void Przychodnia::przegladajLekarzy()
{
	int i = 1;
	cout << "Wybierz lekarza:\n";
	for (vector<Lekarz*>::iterator it = lekarze.begin(); it != lekarze.end(); it++)
	{
		Lekarz* lekarz = *it;
		cout << (i++) << ". " << *lekarz << "\n";

	}
}

void Przychodnia::przegladajWizytyPacjenta(string login)
{
	int i = 1;
	for (vector<Wizyta*>::iterator it = wizyty.begin(); it != wizyty.end(); it++)
	{
		Wizyta* wizyta = *it;

		if (wizyta->pacjent->login == login)
		{
			cout << (i++) << ". Lekarz: " << wizyta->lekarz->imie << " " << wizyta->lekarz->nazwisko <<
				", pacjent: " << wizyta->pacjent->imie << " " << wizyta->pacjent->nazwisko <<
				", termin: " << wizyta->data << " " << wizyta->godzina <<
				", status: " << wizyta->status << "\n";
		}
	}
}
