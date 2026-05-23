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
## **6. Opis użytych metod**
## **7. Opis wdrożenia metod/modelu**
## **8. Wyniki**
## **9. Wnioski**