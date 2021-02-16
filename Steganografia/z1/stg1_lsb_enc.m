% Ukrywanie danych

% Czyszczenie ekranu
clear all;
clc;

% Wczytanie bitmapy z pliku do macierzy
input = imread('img.bmp');
% Zainicjalizowanie macierzy wynikowej
output = input;

% Numer albumu
m = 60493;

% Konwersja na liczbę  
bin_m = dec2bin(m); % zwraca napis
bin_m = bin_m(:); % konwersja na wektor
n = length(bin_m); % długość wektora - liczba bitów
bin_m = str2num(bin_m); % konwersja współrzędnych na liczby

h = size(input, 1); % wysokość macierzy - liczba wierszy
w = size(input, 2); % szerokość macierzy - liczba kolumn
counter = 1; % licznik długości wiadomości

% Iteracaja od dolnego prawego rogu wierszami w lewo
for i = h:-1:1
    for j = w:-1:1
        % Rozpatrywane tylko współrzędne mieszczące wiadomość,
        % których indeks modulo 4 jest równy 0
        if counter <= n && mod(j, 4) == 0
            % Modulo 2 z liczby zwraca jej ostatni bit.
            % Trzecia współrzędna w macierzy określa bajt koloru RGB
            % np. input(i,j,1) - czerwony
            lsb = mod(input(i, j, 1), 2);
            % Podmiana ostatniego bitu macierzy wynikowej.
            % W zależności od wartości ostatniego bitu i ukrywanego bitu
            % zmiana bitu z 0 na 1 poprzez dodanie 1 do 
            % liczby na danym indeksie lub zmiana bitu z 1 na 0 poprzez 
            % odjęcie 1 od liczby na danym indeksie. Gdy bit się zgadza
            % - pozostawienie bez zmiany
            if lsb == 0 && bin_m(counter) == 1
                output(i, j, 1) = input(i, j, 1) + 1;
            % Zmiana bitu z 1 na 0 poprzez odjęcie 1 od 
            % liczby na danym indeksie
            elseif lsb == 1 && bin_m(counter) == 0
                output(i, j, 1) = input(i, j, 1) - 1;   
            end
             counter = counter + 1;
        else
            % Wyjście z drugiej pętli gdy wiadomość została ukryta
            break
        end
        % Wyjście z pierwszej pętli gdy wiadomość została ukryta 
        if counter == n
            break
        end
        
    end
end
% Zapis do pliku .bmp
imwrite(output, 'stego_img.bmp');
fprintf('Dane zapisano. Liczba bitów: %d\n', n)















