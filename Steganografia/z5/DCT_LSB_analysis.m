% Czyszczenie ekranu
clear all;
clc;
im_nums = 4; % liczba par obrazów (orginał i stegoobraz)
% Założenie odnośnie plików:
% Obrazy muszą znajdować się folderze z skryptem. Każdy orginalny obraz
% musi nazywać się img<numer>.jpg, a korespondujący mu stegoobraz
% img<numer>stego.jpg
% Jako wynik programu wyswietli się <im_nums> popup'ów wyglądających jak
% przykładowy_wynik.png
for im_num = 1 : im_nums % pętla przez każdy obraz
    % Tytuł popup'u - numer obrazu
    figure('NumberTitle', 'off', 'Name', strcat('Obraz:',num2str(im_num)));
    % Pokrycie popupem całego ekranu
    set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
    % Wczytanie i wyświetlenie orginalego obrazu
    org_img = imread(strcat('img',num2str(im_num),'.jpg'));
    subplot(2, 4, 1), imshow(org_img), title('orgIMG');
    % Wczytanie i wyświetlenie stegoobrazu
    stg_img = imread(strcat('img',num2str(im_num),'steg.jpg'));
    subplot(2, 4, 5), imshow(stg_img), title('stegoIMG'); 
    % dyskretna transformata cosinusowa - DCT
    x = -20:0.25:20; % zakres osi poziomej 
    org_dct = dct(double(org_img));
    subplot(2, 4, 2)
    org_dct = histogram(org_dct, x);
    title('orgDCT');
    stg_dct = dct(double(stg_img));
    subplot(2, 4, 3);
    stg_dct=histogram(stg_dct, x);
    title('stgDCT');
    % Różnica bezwzględna wysokości histogramów DCT
    diff_dct = abs(stg_dct.BinCounts-org_dct.BinCounts);
    subplot(2, 4, 4), histogram('BinCounts', diff_dct, 'BinEdges', x);
    title('diffDCT');
    % Last Significatn Bit - LSB
    h = size(org_img, 1); % wysokość macierzy - liczba wierszy
    w = size(org_img, 2); % szerokość macierzy - liczba kolumn
    % Iteracja przez kolory (1-czerwony, 2-zielony, 3-niebieski)
    for n_col = 1 : 3
        % LSB każdego koloru
        n_bit = 8;
            org_layer = zeros(h,w); % macierz bitów orginalnego obrazu
            stg_layer = zeros(h,w); % macierz bitów stego obrazu
            for i = 1 : h % iteracja po wysokości obrazu
                for j = 1 : w % iteracja po szerokości obrazu
                    % Konwersja na 8-bitową liczbę binarną wartości
                    % na zadanych współrzędnych pikseli obrazów na
                    % iterowanym kolorze
                    org_byte = fliplr(de2bi(org_img(i,j,n_col),8));
                    stg_byte = fliplr(de2bi(stg_img(i,j,n_col),8));
                    % Wyodrębnienie iterowanego bitu
                    org_bit = org_byte(n_bit);
                    stg_bit = stg_byte(n_bit);
                    % Uzupełnienie macierzy warstw
                    org_layer(i,j) = org_bit;
                    stg_layer(i,j) = stg_bit;
                end
            end
            % Wyliczenie xor obu warstw
            xor_layer = xor(org_layer, stg_layer);
            % Wybór koloru do wyświetlenia w  tytule
            if n_col == 1
                col = 'r';
            elseif n_col == 2
                col = 'g';
            else
                col = 'b';
            end
            % obraz warstwy LSB koloru
            subplot(2, 4, n_col+5), imshow(xor_layer, []), title(strcat(...
                'xoredLSB-',col), 'Color',col);  
    end
end