# Simple Sonification Tool

To better understand sonification, I created a somewhat universal tool with a simple graphical interface for sonifying numerical data.  

## Project Description

![App Example](link)

Aplikacja składa się z dwóch głównych paneli: **panelu ustawień** i **panelu wykresu**, umożliwiając intuicyjne zarządzanie danymi wejściowymi oraz dostosowywanie parametrów utworu muzycznego. W przypadku podania niepoprawnych danych, wyświetlany jest komunikat o błędzie z odpowiednimi wskazówkami.  

![Panel Ustawień](link)      
![Panel Wykresu](link)

### Obsługa danych wejściowych
- **Wczytywanie plików CSV** – odbywa się poprzez przycisk **Wczytaj CSV** i wybór pliku `.csv`.  
- **Menu wyboru kolumn** – generowane dynamicznie na podstawie zawartości pliku.  

### Wizualizacja danych
- Możliwość wyboru kolumny określającej rozmiar kropek na wykresie.  
- Opcja odwrócenia wykresu wzdłuż osi X i Y dla lepszego dopasowania widoku.  

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

