# LIGHT SQUARE!
## Technologie
* Python 3.7
* FastAPI 
* OpenCV
* JavaScript
* HTML
* CSS


## Paczka zawiera foldery:
* tracklib - zawierajacy algorytmy sledzenia oraz rozpoznawania gestów
* resources - zawierajacy logo projektu
* html - zawierajacy strone odbierana przez klienta
* configs - zawierajacy pliki konfiguracyjne do poprawnej konfiguracji kamery na buildroocie
* tests - zawierajacy testy implementacji
oraz pliki:
* main.py - zawierajacy program serwerowy wraz z endpointami
* requirements.txt - zawierajacy zaleznosci potrzebne do uruchomienia projektu

## Sposób uruchomienia
Przed uruchomieniem, nalezy sie upewnic, ze ma sie zainstalowaego Python’a minimalnie w wersji 3.7.3. Podczas pierwszego uruchomienia nalezy pobrac wymagane pakiety znajdujace sie w pliku
requirements.txt, mozna do tego uzyc komendy:
```
pip install -r requirements.txt
```
Nastepnie na komputerze serwerowym nalezy odpowiednio zmodyfikowac plik index.html i umiescic
w nim adres ip swojej maszyny lub adres domeny pod którym bedzie dostepny serwer. Ostatecznie
nalezy uruchomic serwer przy pomocy jednej z podanych nizej komend
```
uvicorn main:app --host 0.0.0.0 --port 8000
python3 main.py
```
Dodatkowo podczas lokalnego debuggowania aplikacji przydatna moze sie okazac flaga -d
```
python3 main.py -d
```
Jednak do uzycia tej flagi, nalezy miec zainstalowana pełna wersje biblioteki OpenCV, najlepiej w
wersji 4.5.1.48
```
pip install opencv-python==4.5.1.48
```