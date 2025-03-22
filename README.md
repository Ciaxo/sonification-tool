# Simple Sonification Tool

To better understand sonification, I created a tool with a simple graphical interface for sonifying numerical data.  

## Project Description

![App Example](link)

The application consists of two main panels: **the settings panel** and **the chart panel**, allowing intuitive management of input data and customization of the musical piece's parameters. If incorrect data is provided, an error message is displayed with appropriate guidance.  

![Panel Ustawień](link)      
![Panel Wykresu](link)

### Input Data Handling
- **Loading CSV files** – done via the **Load CSV** button and selecting a `.csv` file.  
- **Column selection menu** – dynamically generated based on the columns in the selected `.csv` file.  

### Data Visualization
- Ability to select a column defining the size of the dots on the chart.  
- Option to flip the chart along the X and Y axes for better view adjustment. 

### Normalizacja i stopień swobody
- Normalizacja danych wzdłuż wybranej osi.  
- Skalowanie nieliniowe z regulacją stopnia swobody, co pozwala na kompresję lub ekspansję danych.  

### Właściwości utworu
- Określenie długości utworu w bitach poprzez znacznik konwersji.  
- Regulacja wysokości nuty w zależności od wartości:
  - **Rosnące** – wyższa wartość = niższy dźwięk.  
  - **Malejące** – wyższa wartość = wyższy dźwięk.  
- Regulacja głośności nuty:
  - **Rosnące** – wyższa wartość = głośniejsza nuta.  
  - **Malejące** – wyższa wartość = cichsza nuta.  
  - **Stały poziom** – głośność niezależna od wartości.  
- Możliwość ręcznego ustawienia **BPM** (domyślnie 60).  
- Definiowanie zakresu nut oraz minimalnej i maksymalnej głośności (0-127, format MIDI).  

### Generowanie i odtwarzanie pliku MIDI
- **Zapis do MIDI** – przycisk **Zapisz jako MIDI** wyświetla okienko dla podania nazwy pliku, po czym zapisuje wynik.  
- **Odtwarzanie** – przycisk **Odtwórz utwór** wyświetla okienko do wyboru pliku MIDI po czym go odtwarza.  

## Struktura plików i biblioteki

Aplikacja wykorzystuje następujące biblioteki:

- **Interfejs użytkownika**: `Tkinter`
- **Przetwarzanie danych**: `Pandas`
- **Wizualizacja**: `Matplotlib`
- **Praca z dźwiękiem**: `MIDIUtil`, `Pygame`

### Struktura plików

- **`mapping.py`** – funkcje do mapowania wartości:
  - `map_range` – przekształca wartości wejściowe na nowy zakres.
  - `map_data` – oblicza minimalną i maksymalną wartość w liście wejściowej.

- **`mid.py`** – konwersja nut:
  - `str2midi` – konwertuje nazwę nuty na numer MIDI.
  - `midi2str` – konwertuje numer MIDI na nazwę nuty.

### Główne funkcje aplikacji

#### **Ładowanie i przetwarzanie danych**
- `load_csv()` – wczytuje dane z pliku CSV.
- `update_choice(axis, value)` – wybiera kolumnę danych dla osi X, Y lub wartości odpowiadającej wielkości dźwięku.
- `apply_axis_reversal()` – odwraca wartości na osiach X i Y.
- `apply_normalization()` – normalizuje wartości do przedziału `[0,1]`.
- `apply_power()` – transformuje wartości z użyciem stopnia swobody.
- `calculate_bit_data()` – przelicza długość dźwięków na podstawie wybranej kolumny.

#### **Interfejs użytkownika**
- `create_widgets()` – tworzy elementy interfejsu, takie jak przyciski i menu.
- `configure_grid()` – dynamicznie skaluje okno i dostosowuje je do zawartości.

#### **Generowanie dźwięku i plików MIDI**
- `save_midi()` – zapisuje dane do pliku MIDI.
- `play_midi()` – odtwarza plik MIDI za pomocą `pygame`.

#### **Wizualizacja danych**
- `update_plot()` – rysuje wykres z uwzględnieniem normalizacji i transformacji.

## Przykład zastosowania narzędzia

### Sonifikacja danych dotyczących rytmu serca

Celem tego przykładu jest przekształcenie danych sekwencyjnych opisujących rytm serca w dźwięk, tak aby anomalie były łatwe do usłyszenia.  

Założenia sonifikacji:  
- **Czas pomiaru** → odpowiada długości generowanego utworu.  
- **Interwał tętna (czas między kolejnymi uderzeniami serca)** → determinuje wysokość dźwięku:  
  - Większe interwały → **wyższe dźwięki**,  
  - Mniejsze interwały → **niższe dźwięki**.  
- **Stała głośność** → aby zachować czytelność brzmienia.  

W ten sposób **zarówno zbyt duże, jak i zbyt małe interwały** będą słyszalne jako odchylenia od normy.  

**Rysunek 7**: Panel ustawień po zaimportowaniu danych.  
![Rysunek 7 - Panel ustawień](placeholder.png)  

**Rysunek 8**: Panel wykresu po zaimportowaniu danych.  
![Rysunek 8 - Panel wykresu](placeholder.png)  

---

### 1. Skalowanie danych
Ponieważ dane są już w odpowiednim zakresie i nie wymagają dodatkowej obróbki, **nie stosujemy**:  
- **Odwracania wartości na osiach X i Y**,  
- **Rozciągania wartości**,  
- **Modyfikacji zakresu poprzez stopień swobody**.  

Zostawiamy wszystkie **checkboxy odznaczone**, a pole **Stopień swobody** puste.

---

### 2. Ustawienia muzyczne
Aby uzyskać naturalne odwzorowanie rytmu serca w dźwięku, stosujemy:   
- **Tempo = 180 BPM** → taki **BPM** skraca odstępy między nutami i pozwala na szybszą i łatwiejszą analizę danych.

---

### 3. Zakres nut i głośność
Określamy ramy głośności i wybieramy **zakres nut** (zakres może być dowolny, ale w moim przypadku wybrałem taki):  
 
`C1, E2, F2, A2, C3, D3, G3, B3, D4, F4, A4, B4, D5, G5, A5, C6, D6, E6, F#6, G6, A6`  

Zakres ten obejmuje dźwięki w szerokim spektrum wysokości, co pozwala dobrze oddać różnice w rytmie serca.

Głośność jest **stała**, co ułatwia wychwycenie zmian w tonacji dźwięków bez wpływu natężenia dźwięku.

---

### 4. Zapis i odsłuchanie utworu
Po ustawieniu wszystkich parametrów:  
1. **Zapisujemy wynik** do pliku MIDI, aby móc go później przeanalizować.  
2. **Odtwarzamy utwór** ręcznie lub poprzez przycisk.

<p align="center">
  <img src="placeholder.png" alt="Rysunek 9 - Panel ustawień" width="45%">
  <img src="placeholder.png" alt="Rysunek 10 - Panel wykresu" width="45%">
</p>

