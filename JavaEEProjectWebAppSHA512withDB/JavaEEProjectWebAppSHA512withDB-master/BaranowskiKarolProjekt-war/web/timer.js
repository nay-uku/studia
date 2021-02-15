function odliczanie()
		{
		var dzisiaj = new Date();//tworzenie nowego obiektu
		
		var godzina = dzisiaj.getHours();
		if(godzina<10) godzina="0"+godzina;
		var minuta = dzisiaj.getMinutes();
		if(minuta<10) minuta="0"+minuta;
		var sekunda = dzisiaj.getSeconds();
		if(sekunda<10) sekunda="0"+sekunda;
		document.getElementById("timer").innerHTML=godzina+"."+minuta+"."+sekunda;
		setTimeout("odliczanie()",1000);// do diva z htmla o id "zegar" wrzucamy zawartosc tegpo co chcemy wewrzucic wewnatrz tego htmla (inner)
		}

