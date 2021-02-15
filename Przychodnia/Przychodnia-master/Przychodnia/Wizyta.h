#pragma once

#include "Lekarz.h"
#include "Pacjent.h"

using namespace std;

class Wizyta
{
public:
	Lekarz* lekarz;
	Pacjent* pacjent;
	string data;
	string godzina;
	string status;

public:
	Wizyta();
	Wizyta(Lekarz* lekarz, Pacjent* pacjent, string data, string godzina)
	{
		this->lekarz = lekarz;
		this->pacjent = pacjent;
		this->data = data;
		this->godzina = godzina;
		this->status = "aktywna";
	}
	~Wizyta();

	void ustawStatus(string status)
	{
		this->status = status;
	}
};

