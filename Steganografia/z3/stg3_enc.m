% UKRYWANIE DANYCH
function stg3_enc(key, img, wav)
% key - klucz liczba integer
% img - ścieżka do obrazka, który ma zostać ukryty
% wav - ścieżka do pliku audio.wav, w którym zostanie ukryty obrazek
% Przykładowe użycie: 
% w command window: stg3_enc 5 secret.bmp boat.wav

% Obraz
input = imread(img); % Wczytanie bitmapy z pliku do macierzy
h = size(input, 1); % wysokość macierzy - liczba wierszy
w = size(input, 2); % szerokość macierzy - liczba kolumn
len_img = h * w * 8; % ilość bitów do ukrycia
bin_m = transpose(dec2bin(input,8)); % reprezentacja binarna
bin_m = bin_m(:); % transformacja na 1 kolumnę

% Audio
[y,Fs] = audioread(wav); % wczytanie pliku .wav
n = length(y); % długość .wav

% Losowanie ze stałym ziarnem
seed = str2num(key); % ziarno - klucz
rng(seed);
% Losowanie miejsc bez powtórzeń do osadzenia bitów obrazka
places = randperm(n, len_img);

output = y; % przygotowanie macierzty wynikowej
for i = 1 : len_img % iteracja przez bity obrazka
    num = float2bin(y(places(i))); % losowy element .wav zamieniony na bin 
    lsb = num(end); % najmniej znaczący bit (ostatni)
    % jeżeli lsb dźwięku i bit obrazka różnią się - należy lsb zmienić
    % na bit obrazka i podstawić do macierzy wynikowej w postaci liczby
    % zmiennoprzecinkowej
    if lsb == '0' && bin_m(i) == '1'
        num(end) = '1'; 
        output(places(i)) = bin2float(num);
    elseif lsb == '1' && bin_m(i) == '0'
        num(end) = '0';
        output(places(i)) = bin2float(a);
    end
end
% Przy zapisie należy zwiększyć bits per sample do 64, gdyż domyślnie
% funkcja audiowrite oczekuje macierzy z 32 bitowymi liczbami
audiowrite('stego_boat.wav', output, Fs, 'BitsPerSample', 64);