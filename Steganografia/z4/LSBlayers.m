% Czyszczenie ekranu
clear all;
clc;
% Wczytanie bitmapy z pliku do macierzy
org_img = imread('img2.jpg');
stg_img = imread('img2steg.jpg');
h = size(org_img, 1); % wysokość macierzy - liczba wierszy
w = size(org_img, 2); % szerokość macierzy - liczba kolumn
% Iteracja przez 24 warstwy:
    % Iteracja przez kolory (1-czerwony, 2-zielony, 3-niebieski)
for n_col = 1 : 3
    % Iteracja przez każdy bit
    for n_bit = 1 : 8
        org_layer = zeros(h,w); % macierz bitów pierwszego obrazu
        stg_layer = zeros(h,w); % macierz bitów drugiego obrazu
        pixels = strings(h,w); % macierz współrzędnych
        for i = 1 : h % iteracja po wysokości obrazu
            for j = 1 : w % iteracja po szerokości obrazu
                % Konwersja na 8-bitową liczbę binarną wartości
                % na zadanych współrzędnych pikseli obrazów i na
                % iterowanym kolorze
                org_byte = fliplr(de2bi(org_img(i,j,n_col),8));
                stg_byte = fliplr(de2bi(stg_img(i,j,n_col),8));
                % Wyodrębnienie iterowanego bitu
                org_bit = org_byte(n_bit);
                stg_bit = stg_byte(n_bit);
                % Uzupełnienie macierzy warstw
                org_layer(i,j) = org_bit;
                stg_layer(i,j) = stg_bit;
                % Złączenie współrzędnych pixela w string
                pix = strcat(num2str(i),':',num2str(j));
                pixels(i,j) = pix; % uzupełnienie macierzy współrzędnych
            end
        end
        % Jeżeli wszystkie bity warstwy są takie same w obydwu obrazkach,
        % mamy pewność, że nie ma ukrytej wiadomości, więc
        % wizualizacja nie jest przeprowadzona, aby nie wyświetlać 24 razy.
        % Wizualizacja przeprowadzana jest tylko dla różniących się warstw.
        % Aby otrzymać wszystkie 24 wizualizacje wystarczy zakomentować
        % poniższy if i kończący go end
         if ~isequal(org_layer, stg_layer)
            % Wyliczenie xor obu warstw
            xor_layer = xor(org_layer, stg_layer);
            % Wybór koloru do wyświetlenia w  tytule
            if n_col == 1
                col = 'red';
            elseif n_col == 2
                col = 'green';
            else
                col = 'blue';
            end
            % Tytuł popup'u - wskazanie warstwy (kolor i bit)
            figure('NumberTitle', 'off', 'Name', strcat('Layer - color: ',...
                col,', bit: ',num2str(n_bit)));
            % Pokrycie popupem całego ekranu
            set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
            % 3 obrazy warstw na jednym popup'ie
            subplot(1, 3, 1), imshow(org_layer, []), title("Orginal layer");
            subplot(1, 3, 2), imshow(stg_layer, []), title("Modified layer");
            subplot(1, 3, 3), imshow(xor_layer, []), title("Xored layer");
            % Tabela ze współrzędnymi
            org_layer = reshape(org_layer,1,[]); % reshape na wektor
            stg_layer = reshape(stg_layer,1,[]);
            xor_layer = reshape(xor_layer,1,[]);
            pixels = reshape(pixels,1,[]);
            t = uitable('RowName', {'orginal','modified','xor'},...
                        'Data', [org_layer; stg_layer; xor_layer],...
                        'ColumnName', pixels,...
                        'Position',[10 10 1900 200]);         
         end
    end
end
