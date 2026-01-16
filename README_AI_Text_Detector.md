# AI Text Detector  
System detekcji tekstów generowanych przez sztuczną inteligencję

---

## 1. Informacje ogólne

Projekt **AI Text Detector** jest aplikacją webową służącą do analizy tekstu pisanego pod kątem jego pochodzenia — rozróżnienia pomiędzy tekstem napisanym przez człowieka a tekstem wygenerowanym przez model sztucznej inteligencji.

System został zaprojektowany jako rozwiązanie hybrydowe (ML + NLP), łączące:
- klasyfikator statystyczny oparty o **Logistic Regression**,
- model **Transformer (DistilBERT)** do analizy semantycznej,
- silnik decyzyjny typu **weighted ensemble** z obsługą stanu niepewności (`UNCERTAIN`),
- moduł **Explainability (XAI)** dla modelu statystycznego.

Aplikacja została podzielona na niezależny backend (API + ML) oraz frontend (klient webowy).

---

## 2. Wymagania systemowe

### Backend
- Python 3.10+
- Windows / Linux / macOS

### Frontend
- Przeglądarka internetowa
- Python (lokalny serwer HTTP)

---

## 3. Instrukcja uruchomienia lokalnie

### Backend

```bash
cd ai_text_detector
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Swagger: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
python -m http.server 5500
```

http://127.0.0.1:5500/

---

## 4. Struktura projektu

```
app/
 ├── api/
 ├── core/
 ├── ml/
 ├── services/
 ├── experiments/
 └── main.py
frontend/
data/
```

---

## 5. Funkcjonalność

- Detekcja AI / HUMAN / UNCERTAIN
- Ensemble ML
- Explainability (XAI)
- Raporty CSV
- Eksperymenty odporności

---

## 6. Ewaluacja

Metryki:
- Accuracy
- Precision
- Recall
- F1-score

Wyniki zapisywane w CSV.

---

## 7. Ograniczenia

- Krótkie teksty → UNCERTAIN
- Transformer mniej interpretowalny
- Dane spoza zbioru treningowego

---

## 8. Rozwój

- Większe datasety
- Więcej modeli
- Monitoring jakości
- Integracje B2B

---

© Projekt inżynierski – AI Text Detector
