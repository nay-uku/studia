% ODCZYTYWANIE UKRYTYCH DANYCH
function stg3_dec(key, w, h, wav)
% key - klucz liczba integer
% w - szerokość obrazu wynikowego (ilość pikseli)
% h - wysokość obrazu wynikowego
% wav - ścieżka do pliku audio .wav z ukrytym obrazem
% Przykładowe użycie: 
% w command window: stg3_dec 5 128 128 stego_boat.wav

% Audio
[y,Fs] = audioread(wav); % Wczytanie piku audio z ukrytą wiadomością
n = length(y); % Długość .wav

% Obraz
h = str2num(h); % wysokość macierzy - liczba wierszy
w = str2num(w); % szerokość macierzy - liczba kolumn
output = uint8(zeros(h, w)); % Macierz wynikowa obrazu inicjalizowana zerami
len_img = h * w * 8; % ilość bitów do odczytania

seed = str2num(key); % Wczytanie klucza jako ziarno do losowani
rng(seed);

% Dzięki znanemu ziarnu - wygenerowanie pozycji bajtów  
% pliku dźwiękowego, których ostatnie bity tworzą obraz 
places = randperm(n, len_img);
bits = zeros(len_img, 1); % wektor bitów obrazu

for i = 1 : len_img % Iteracja po bitach do odczytania wiadomości
    num = float2bin(y(places(i))); % liczba, w której ukryty jest bit obrazu
    bits(i,1) = double(str2num(num(end))); %uzupełnianie wektora obrazu
end

% Każda kolumna macierzy to znak wyrażony binarnie
% len_img/8 - liczba znaków (liczba kolumn macierzy)
output = reshape(bits, 8, (len_img/8));
% Potęgi 2 do odczytania ASCII z wartości binarnych 
bin_vals = [ 128 64 32 16 8 4 2 1 ];

% Mnożenie macierzy potęg 2 z bitami znaku zwróći 
% znak ASCII , który jest konwertowany na 8 bitowy uint
output = uint8(bin_vals*output);
output = reshape(output, h, w); % zmiana wymiaru macierzy
imwrite(output, 'dec_secret.bmp'); % zapis outputu do podanego pliku
