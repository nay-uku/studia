% Odczytywanie ukrytych danych

% Czyszczenie ekranu
clear all;
clc;

% Wczytanie bitmapy z ukrytą wiadomością
input = imread('stego_img.bmp');

% Ilość bitów do odebrania
n = 16;

h = size(input, 1); % wysokość macierzy - liczba wierszy
w = size(input, 2); % szerokość macierzy - liczba kolumn
counter = 1; % licznik długości wiadomości

% Iteracaja od dolnego prawego rogu wierszami w lewo
for i = h:-1:1
    for j = w:-1:1
        % Rozpatrywane tylko współrzędne mieszczące wiadomość,
        % których indeks modulo 4 jest równy 0, gdyż odbiorcy znane
        % są pozycje ukrytych bitów i długość wiadomości
        if counter <= n && mod(j, 4) == 0
            % zapis lsb do wektora
            bits(counter, 1) = mod(input(i, j, 1), 2);
            counter = counter + 1;
        else
            % Wyjście z drugiej pętli gdy wiadomość została odczytana
            break
        end
        % Wyjście z pierwszej pętli gdy wiadomość została odczytana 
        if counter == n
            break
        end
        
    end
end
% Transformacja odczytancyh bitów na liczbę
m = bin2dec(transpose(num2str(bits)));
fprintf('Otrzymana wiadomość: %d\n', m);

