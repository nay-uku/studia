% UKRYWANIE DANYCH
function stg2_lsb_enc(message, key, img)
% message - wiadomość jako łańcuch znaków
% key - klucz liczba integer
% img - ścieżka do obrazka, wktórym zostanie ukryta wiadomość
% Przykładowe użycie: 
% w command window: stg2_lsb_enc 'mój sekret' 5 img.bmp

% Wczytanie bitmapy z pliku do macierzy
input = imread(img);
% Zainicjalizowanie macierzy wynikowej
output = input;

% Wiadomość
m = message;
asci_value = uint8(m); % na ASCII
bin_m = transpose(dec2bin(asci_value, 8)); % reprezentacja binarna
bin_m = bin_m(:); % 1 kolumna
n = length(bin_m); % długość wektora - liczba bitów
bin_m = str2num(bin_m); % wiadomość jako pionowy wektor liczb binarnych

% Wymiary
h = size(input, 1); % wysokość macierzy - liczba wierszy
w = size(input, 2); % szerokość macierzy - liczba kolumn

% Losowanie
seed = str2num(key); % ziarno - klucz
rng(seed);

% Losowanie współrzędnych x i y bez powtórzeń do osadzenia bitów 
% wiadomości
pix_h = randperm(h,n);
pix_w = randperm(w,n);

% Iteracaja po bitach do zapisania wiadomości
for i = 1 : n
    % Modulo 2 z liczby zwraca jej ostatni bit.
    % Trzecia współrzędna w macierzy określa bajt koloru RGB
    % np. input(i,j,1) - czerwony
    lsb = mod(input(pix_h(i), pix_w(i), 1), 2);
    % Podmiana ostatniego bitu macierzy wynikowej.
    % W zależności od wartości ostatniego bitu i ukrywanego bitu
    % zmiana bitu z 0 na 1 poprzez dodanie 1 do 
    % liczby na danym indeksie lub zmiana bitu z 1 na 0 poprzez 
    % odjęcie 1 od liczby na danym indeksie. Gdy bit się zgadza
    % - pozostawienie bez zmiany
    if lsb == 0 && bin_m(i) == 1
        output(pix_h(i), pix_w(i), 1) = input(pix_h(i), pix_w(i), 1) + 1;
    % Zmiana bitu z 1 na 0 poprzez odjęcie 1 od 
    % liczby na danym indeksie
    elseif lsb == 1 && bin_m(i) == 0
        output(pix_h(i), pix_w(i), 1) = input(pix_h(i), pix_w(i), 1) - 1;   
    end
end
    
% Zapis do pliku .bmp
imwrite(output, 'stego_img.bmp');
fprintf('Dane zapisano. Liczba znaków: %d, liczba bitów: %d\n', n/8,n);
end