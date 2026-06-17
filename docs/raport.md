# **Ocena formalności tekstu**
*Miłosz Malinowski, Michał Korzeniewski, Piotr Misiejuk*
## Spis treści
1. [Streszczenie](#1-streszczenie)
2. [Wprowadzenie](#2-wprowadzenie)
3. [Cel projektu oraz kontekst](#3-cel-projektu-oraz-kontekst)
4. [Literatura](#4-literatura)
5. [Opis danych](#5-opis-danych)
6. [Opis użytych metod](#6-opis-użytych-metod)
7. [Opis wdrożenia metod/modelu](#7-opis-wdrożenia-metodmodelu)
8. [Wyniki](#8-wyniki)
9. [Wnioski](#9-wnioski)
## **1. Streszczenie**
W ramach projektu "Ocena stopnia formalnośći tekstu" porównano dwie metody: klasyczny klasyfikator wytrenowany własnoręcznie na znalezionych danych, oraz promptowany SLM Qwen2.5-1.5B-Instruct. Do szkolenia klasyfikatora i testowania go oraz slma użyty został zbiór 
## **2. Wprowadzenie**
Skuteczna komunikacja wymaga od nas ciągłego dostosowywania rejestru językowego do sytuacji społecznej. Styl formalny (urzędowy, biznesowy czy akademicki) cechuje się dążeniem do całkowitej niezależności od kontekstu. Jest konstruowany tak, aby był precyzyjny i zrozumiały dla każdego odbiorcy, co w strukturze gramatycznej objawia się dominacją rzeczowników oraz przymiotników. Z kolei styl nieformalny (potoczny) bazuje na współdzielonej wiedzy rozmówców, skrótach myślowych, zaimkach i czasownikach.

W dobie dynamicznego rozwoju sztucznej inteligencji automatyczna ocena formalności tekstu stała się kluczowym, a zarazem bardzo praktycznym wyzwaniem w obszarze przetwarzania języka naturalnego (NLP). Umiejętność ta jest niezbędna do optymalizacji pracy zaawansowanych chatbotów, automatycznych systemów moderacji treści oraz nowoczesnych narzędzi tłumaczenia maszynowego, które muszą zachować odpowiedni ton wypowiedzi. Algorytmiczne podejście do tego problemu ewoluowało na przestrzeni lat – od prostych statystyk gramatycznych, przez klasyczne uczenie maszynowe (takie jak maszyny wektorów nośnych – SVM), aż po współczesne głębokie modele transformerowe.

Realizacja tego zadania w ujęciu dwujęzycznym – dla języka polskiego oraz angielskiego – wiąże się ze zróżnicowanymi wyzwaniami lingwistycznymi. Język angielski opiera swoją formalność głównie na doborze specyficznego słownictwa (np. słów pochodzenia łacińskiego zamiast czasowników frazowych) oraz sztywnej strukturze składniowej. Z kolei język polski cechuje się bogatą fleksją, wolnym szykiem zdania oraz naturalną tendencją do pomijania zaimków osobowych, gdyż informacja o osobie jest zakodowana w końcówkach czasowników. Uwzględnienie obu tych języków wymaga od stosowanych algorytmów nie tylko prostej detekcji słów kluczowych, ale przede wszystkim zdolności do głębokiej interpretacji kontekstu semantycznego i różnic typologicznych między nimi.
## **3. Cel projektu oraz kontekst**
### Cel projektu
Głównym celem niniejszego projektu jest zaprojektowanie, implementacja oraz ewaluacja systemu do automatycznej klasyfikacji i oceny stopnia formalności tekstów w ujęciu dwujęzycznym: dla języka polskiego oraz angielskiego. Projekt ma na celu zbadanie, w jakim stopniu zróżnicowane metody przetwarzania języka naturalnego (NLP) radzą sobie z odmiennymi strukturami gramatycznymi i sposobami wyrażania rejestru oficjalnego w obu tych językach.

W ramach realizacji celu głównego postawiono następujące zadania szczegółowe:

* **Przygotowanie i analiza danych:** Pozyskanie oraz odpowiednie przetworzenie zbalansowanych korpusów tekstowych zawierających próbki o zróżnicowanym stopniu formalności (formalne, nieformalne, neutralne) dla obu języków.

* **Ekstrakcja cech i implementacja modeli:** Porównanie skuteczności klasycznych metod lingwistycznych (takich jak wskaźnik F-score oparty na proporcjach części mowy) oraz tradycyjnych algorytmów uczenia maszynowego z nowoczesnymi podejściami opartymi na architekturze Transformer.

* **Analiza porównawcza:** Zbadanie różnic w efektywności i barierach klasyfikacji dla analitycznego języka angielskiego oraz syntetycznego, bogatego fleksyjnie języka polskiego.

### Kontekst projektu
Projekt wpisuje się w intensywnie rozwijany nurt badań nad kontrolą stylu i atrybutów tekstu w systemach sztucznej inteligencji. Praktycznym kontekstem pracy jest rosnące zapotrzebowanie na narzędzia automatyzujące weryfikację korespondencji biznesowej, wspomagające redakcję tekstów (style-checking) oraz umożliwiające dostosowanie tonu wypowiedzi systemów konwersacyjnych (chatbotów i asystentów AI) do profilu odbiorcy. Badanie realizowane w środowisku dwujęzycznym pozwala na ocenę uniwersalności wybranych architektur modeli i sprawdzenie, czy narzędzia rozwijane pierwotnie dla języka angielskiego zachowują swoją skuteczność po adaptacji do specyfiki polszczyzny.

## **4. Literatura**
### **[FAME-MT Dataset: Formality Awareness Made Easy for Machine Translation Purposes](https://arxiv.org/html/2405.11942v1?fbclid=IwY2xjawR-YndleHRuA2FlbQIxMABicmlkETBhbHJTa2V4ZlNKNG83aVdyc3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHiD_lb22AAl6b43zXcVXM4DI5leN8F5xPIoGXigKJ04UkuszThutfxM23Zzz_aem_zN-smMkoeIQrJZ9pQkUuYg)**
***D. Wiśniewski, Z. Rostek, A. Nowakowski***

Praca dotyczy stworzenia zbioru danych FAME-MT – największego obecnie wielojęzycznego zbioru danych (11,2 mln tłumaczeń dla 112 par językowych) przeznaczonego do kontroli poziomu formalności w systemach tłumaczenia maszynowego. Autorzy opisują metodę automatycznej klasyfikacji tekstów na kategorie: formalną, nieformalną oraz neutralną, zwracając szczególną uwagę na wyzwania związane z językiem polskim (np. pomijanie zaimków osobowych).

### **[Formality of Language: definition, measurement and behavioral determinants](https://pespmc1.vub.ac.be/Papers/Formality.pdf)**
***F. Heylighen, J.-M. Dewaele***

Praca wyjaśnia, że formalność to unikanie niejasności poprzez tworzenie wypowiedzi zrozumiałych nawet bez znajomości kontekstu. Autorzy opracowali wskaźnik F, który pozwala zmierzyć ten poziom na podstawie gramatyki: styl formalny opiera się na rzeczownikach i przymiotnikach, a nieformalny na zaimkach i czasownikach. Z badań wynika, że bardziej formalni jesteśmy w piśmie niż w mowie oraz gdy rozmawiamy z obcymi osobami; cecha ta jest też silniejsza u introwertyków i osób z wyższym wykształceniem

### **[Learning to Classify Documents According to Formal and Informal Style](https://doi.org/10.33011/lilt.v8i.1305)**
***F. Abu Sheikha, D. Inkpen***

Praca przenosi klasyfikację stylu do świata uczenia maszynowego. Autorzy stworzyli uniwersalny model, który rozpoznaje stopień formalności zarówno całych dokumentów, jak i pojedynczych zdań na podstawie cech gramatycznych i doboru słownictwa. Do treningu wykorzystano teksty ogólne oraz specjalistyczne (medyczne), co udowodniło, że algorytmy radzą sobie z różną tematyką. W eksperymentach przetestowano Drzewa Decyzyjne, Naiwnego Klasyfikatora Bayesa oraz Maszyny Wektorów Nośnych (SVM) – ten ostatni algorytm osiągnął najwyższą skuteczność.

## **5. Opis danych**
Do trenowania standardowego klasyfikatora a następnie testowania go oraz małego modelu językowego użyto danych z zestawu danych FAME-MT, w którym kawałki tekstu w różnych językach (z których użyte zostały polski i angielski) są pogrupowane na teksty formalne i potoczne.
## **6. Opis użytych metod**

### 6.1. Frontend (GUI)
Interfejs użytkownika zbudowany w oparciu o framework **Streamlit**, umożliwiający interaktywną analizę formalności tekstu:

**Architektura interfejsu:**
- Aplikacja jednostronicowa z podziałem na panel boczny (sidebar) i obszar główny
- Konfiguracja za pomocą zmiennych środowiskowych (.env)
- Responsywny układ z wykorzystaniem kolumn (columns)

**Komponenty interaktywne:**
- Selectboxy do wyboru języka (polski/angielski) i modelu AI
- Pole tekstowe (text_area) do wprowadzania analizowanego tekstu
- Przycisk inicjujący proces klasyfikacji z wizualizacją ładowania (spinner)

**Wizualizacja wyników:**
- Podział na dwie kolumny: ogólna ocena tonu i szczegółowa analiza
- Indeks formalności w formie interaktywnego suwaka z gradientem kolorystycznym
- Kategoryzacja tonu na 5 poziomów (od "Highly Informal" do "Highly Formal")
- Podświetlanie słów z wykorzystaniem kolorów (niebieski → formalne, czerwony → nieformalne)
- Legenda wyjaśniająca znaczenie kolorów i intensywność

### 6.2. Klasyfikator standardowy
Aplikacja wykorzystuje ensemble klasyfikatoror do oceny formalności tekstu:

**Architektura modelu:**

VotingClassifier łączący trzy algorytmy:
  - Stochastic Gradient Descent (SGD) z funkcją straty logistycznej
  - Regresję Logistyczną z solverem liblinear
  - Naiwny klasyfikator Bayesa (MultinomialNB)

Głosowanie miękkie (soft voting) – uśrednianie prawdopodobieństw z wszystkich klasyfikatorów

**Przetwarzanie cech:**

Wektoryzacja TF-IDF z optymalizacją parametrów:
  - Maksymalna częstotliwość dokumentów (`max_df`)
  - Zakres n-gramów (unigramy, bigramy, trigramy)

**Optymalizacja hiperparametrów:**
- GridSearchCV z 3-krotną walidacją krzyżową
- Optymalizacja parametrów dla każdego klasyfikatora składowego
- Kryterium optymalizacji: dokładność (accuracy)

**Wyjaśnialność predykcji:**

Do interpretacji wyników wykorzystano **LIME** (Local Interpretable Model-agnostic Explanations):
- Generowanie lokalnych wyjaśnień dla pojedynczych predykcji
- Identyfikacja słów mających największy wpływ na decyzję klasyfikatora
- Określenie wagi każdego słowa (dodatnia dla formalnych, ujemna dla nieformalnych)

### Mały Model Językowy (SLM)

## **7. Opis wdrożenia metod/modelu**
### 7.1. Frontend (GUI)

**Struktura plików:**
```
├── app.py                 # Główna aplikacja Streamlit
├── utils/
│   └── text_utils.py      # Funkcje pomocnicze
└── assets/
    └── logo.svg           # Zasoby graficzne
```

**Implementacja interfejsu (`app.py`):**

1. **Konfiguracja strony:**
   - Ustawienie tytułu, ikony i układu (wide)
   - Wczytanie zmiennych środowiskowych (tytuł aplikacji, nazwa społeczności)
   - Dodanie niestandardowego CSS dla poprawy wyglądu

2. **Panel boczny (sidebar):**
   - Nagłówek i opis konfiguracji
   - Selectbox dla języka (English/Polish)
   - Selectbox dla modelu (Standard Classifier/SLM)
   - Wyświetlenie docelowej społeczności

3. **Obszar główny:**
   - Wyświetlenie logo i tytułu aplikacji
   - Pole tekstowe z miejscem na wprowadzenie tekstu
   - Przycisk "Classify Tone" z obsługą stanów ładowania

4. **Prezentacja wyników:**
   - Wywołanie funkcji `classify_tone()` z modułu `ai.classifier`
   - Wygenerowanie podświetleń przez `highlight_words()` z `utils.text_utils`
   - Wyświetlenie ogólnej oceny z emoji i etykietą
   - Renderowanie suwaka z pozycją obliczoną na podstawie `formal_prob` (0-100%)
   - Wyświetlenie indeksu formalności i poziomu ufności
   - Prezentacja podświetlonego tekstu z legendą

**Obsługa błędów:**
- Walidacja pustego tekstu przed klasyfikacją
- Komunikaty ostrzegawcze dla użytkownika
- Wyświetlanie statusu ładowania podczas analizy

**Personalizacja:**
- Dostosowanie tytułu i nazwy społeczności przez plik .env
- Możliwość rozszerzenia o dodatkowe języki i modele
- Skalowalna architektuma umożliwiająca dodawanie nowych komponentów

### 7.2. Klasyfikator standardowy

**Trenowanie modelu (`create_classifier`):**
1. Wczytanie danych z plików CSV (osobno dla formalnych i nieformalnych)
2. Próbkowanie danych (do 100 000 przykładów na klasę, dalsze zwiększonie ilości danych nie poprawiało jakości modelu). Podział na zbiory treningowe (70%) i testowe (30%) z zachowaniem stratifikacji
4. Konfiguracja potoku (Pipeline):
   - Wektoryzacja TF-IDF
   - Ensemble klasyfikatorów (VotingClassifier)
5. Przeszukiwanie siatki hiperparametrów (GridSearchCV) z 3-krotną walidacją
6. Ewaluacja na zbiorze testowym (dokładność, raport klasyfikacji)
7. Zapis wytrenowanego modelu za pomocą `joblib`

**Ładowanie i predykcja (`load_model`, `classify_tune`):**
- Ładowanie zapisanego modelu z dysku (ścieżka: `ai/models/{model}_{język}.pkl`)
- Automatyczne trenowanie w przypadku braku pliku modelu
- Zwracanie: kategorii tonu, poziomu ufności i prawdopodobieństwa formalności

**Wizualizacja podświetleń (`get_highlighted_words`):**
1. Inicjalizacja explainera LIME z nazwami klas ["informal", "formal"]
2. Wygenerowanie lokalnego wyjaśnienia dla wprowadzonego tekstu
3. Ograniczenie liczby wyświetlanych słów (uwzględniając długość tekstu)
4. Zwrócenie listy słów z przypisanymi wagami (dodatnie → formalne, ujemne → nieformalne)

**Format zapisu modelu:**
- Główny plik: `{model}_{język}.pkl` (zawiera cały potok Pipeline)
- Plik metadanych: `{model}_{język}_info.txt` (parametry, dokładność, raport)

### 7.3 Mały Model Językowy (SLM)

## **8. Wyniki**
Klasyfikator stanadrdowy: Angielski

Best parameters: {'classifier__Logistic Regression__C': 10.0, 'classifier__Multinomial Naive Bayes__alpha': 1.0, 'classifier__Stochastic Gradient Descent__alpha': 1e-05, 'vectorizer__max_df': 0.9, 'vectorizer__ngram_range': (1, 2)}Model saved: ai/models/Standard_Classifier_English.pkl
Accuracy: 0.7893
Training samples: 140000
Features: 836710
Random State: 2217827989
Classification Report:
              precision    recall  f1-score   support

          -1       0.81      0.76      0.78     30000
           1       0.77      0.82      0.80     30000

    accuracy                           0.79     60000
   macro avg       0.79      0.79      0.79     60000
weighted avg       0.79      0.79      0.79     60000


Klasyfikator standardowy: Polski
Best parameters: {'classifier__Logistic Regression__C': 1.0, 'classifier__Multinomial Naive Bayes__alpha': 1.0, 'classifier__Stochastic Gradient Descent__alpha': 1e-05, 'vectorizer__max_df': 0.8, 'vectorizer__ngram_range': (1, 1)}Model saved: ai/models/Standard_Classifier_Polish.pkl
Accuracy: 0.7930
Training samples: 140000
Features: 131178
Random State: 2225172574
Classification Report:
              precision    recall  f1-score   support

          -1       0.78      0.81      0.80     30000
           1       0.80      0.77      0.79     30000

    accuracy                           0.79     60000
   macro avg       0.79      0.79      0.79     60000
weighted avg       0.79      0.79      0.79     60000

slm: Angielski

Accuracy: 0.6200
Classification Report:
              precision    recall  f1-score   support

          -1       0.54      0.89      0.67        44
           1       0.82      0.41      0.55        56

    accuracy                           0.62       100
   macro avg       0.68      0.65      0.61       100
weighted avg       0.70      0.62      0.60       100

slm: Polski
Accuracy: 0.5000
Classification Report:
              precision    recall  f1-score   support

          -1       0.51      0.85      0.64        52
           1       0.43      0.12      0.19        48

    accuracy                           0.50       100
   macro avg       0.47      0.49      0.42       100
weighted avg       0.47      0.50      0.42       100

## **9. Wnioski**
SLM miał zazwyczaj gorsze wyniki, co nie jest szczególnie zaskakujące, zważywszy na jego ogólny charakter, zwłaszcza że ze względów sprzętowych użyty został relatywnie mały SLM. Powoodowało to więc problemy z konfiguracją i niezawodnym otrzymywaniem wyników w poprawnym formacie, a sam model potrafił przekręcać słowa (np dla  tekstu: "Podjąłem starania mające na celu gromadzenia środków na wsparcie tego niezwykłego przedsięwzięcia."
Odpowiedź SLMa brzmiała:{"formality": 0.6, "important_words": [["podjęłem", 0.7], ["starania", 0.6], ["gromadzenia", 0.6], ["wsparcie", 0.6], ["niezwykłego", 0.5], ["przedsięwzięcia", 0.6]]},
a więc słowo "Podjąłem" zostało przekręcone na (niepoprawne gramatycznie) "podjęłem".), albo zachowywać się ogólnie w sposób nieprzewidywalny (kiedy do komendy dodana została klauzula o wspomnieniu tylko o pięciu najważniejszych słowach (aby cała odpowiedź zmieściła się w limicie tokenów), slm wyróżnił w odpowiedzi dwa słowa, z czego drugie powtarzał w nieskończoność ).
Za to klasyfikator klasyczny radził sobie zazwyczaj lepiej, lecz wymagał najpierw konkretnego treningu i w wypadku tekstów których dziedzina/tematyka nie pokrywa się z podanymi danymi może poradzić sobie gorzej, a same rankingi formalności poszczególnych słów bywają często mniej intuicyjne i zgodne z rzeczywistością niż te slm-a.
Wynikają z tego więć niezbyt zaskakujące wnioski, że narzędzie konkretnie skierowane pod dane zastosowanie i wytrenowane na konkretnych danych radzi sobie lepiej i jest bardziej niezawodne, niż ogólny model językowy który musi na dodatek sam wywnioskować jakie właściwie jest jego zadanie i kryteria jego wykonania (gdzie model klasyfikacyjny nie musi o tym "myśleć" tylko w skutek swojego naturalnego działania daje określone dane w określonym formacie).