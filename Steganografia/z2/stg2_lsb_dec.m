% ODCZYTYWANIE UKRYTYCH DANYCH
function stg2_lsb_dec(message_length, key, img)
% message_length - długość wiadomości (liczba znaków)
% key - klucz liczba integer
% img - ścieżka do obrazka z ukrytą wiadomością
% Przykładowe użycie: 
% w command window: stg2_lsb_dec 10 5 stego_img.bmp

% Wczytanie bitmapy z ukrytą wiadomością
input = imread(img);

% Liczba znaków wiadomości
m_len = str2num(message_length);
% Liczba bitów do odebrania
n = m_len * 8;

% Wymiary
h = size(input, 1); % wysokość macierzy - liczba wierszy
w = size(input, 2); % szerokość macierzy - liczba kolumn

% Wczytanie klucza jako ziarno
seed = str2num(key);
rng(seed);

% Dzięki znanemu ziarnu - wygenerowanie współrzędnych x i y  
% pikseli, których ostatnie bity koloru czerwonego tworzą
% wiadomość 
pix_h = randperm(h,n);
pix_w = randperm(w,n);

% Iteracja po bitach do odczytania wiadomości
for i = 1 : n
    % zapis lsb każdego bajtu z wiadomością do wektora wszystkich lsb
    bits(i, 1) = mod(double(input(pix_h(i), pix_w(i), 1)), 2);
end

% Potęgi 2 do odczytania ASCII z wartości binarnych 
bin_vals = [ 128 64 32 16 8 4 2 1 ]; 

% Każda kolumna macierzy to znak wyrażony binarnie
% n/8 - liczba znaków (liczba kolumn macierzy)
bin_m = reshape(bits, 8, (n/8));

% Mnożenie macierzy potęg 2 z bitami znaku zwróći 
% znak ASCII. char() zamieni na znak.
m = char(bin_vals*bin_m); 
fprintf('Otrzymana wiadomość: %s\n', m);
end