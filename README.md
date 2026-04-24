# 🚀 Quiz Leaderboard API (FastAPI)

## 📌 Project Overview

This project implements a backend system for generating a **quiz leaderboard** by integrating with an external validator API.
It processes multiple API responses, removes duplicate records, aggregates scores, and produces a final ranked leaderboard.

This assignment simulates a **real-world backend integration problem** involving API polling, data consistency, and fault handling. 

---

## 🎯 Objective

* Poll API **10 times**
* Collect all responses
* Remove duplicate records using `(roundId + participant)`
* Aggregate total scores per participant
* Generate a sorted leaderboard
* Submit final result to validation API

---

## ⚙️ Tech Stack

* **Backend:** FastAPI (Python)
* **HTTP Client:** requests
* **Server:** Uvicorn

FastAPI is a modern high-performance framework for building APIs efficiently with Python. ([Wikipedia][1])

---

## 🔁 Workflow Logic

```
Poll API (0–9) → Collect Data → Deduplicate → Aggregate Scores → 
Sort Leaderboard → Submit → Validate Result
```

---

## 🧠 Core Logic

### ✅ Deduplication

```python
key = (roundId, participant)
```

### ✅ Aggregation

```python
scores[participant] += score
```

### ✅ Sorting

```python
leaderboard.sort(key=lambda x: x["totalScore"], reverse=True)
```

---

## 🚨 Error Handling (Important)

This project handles real-world API failures:

### ✔ If API works:

```json
"isCorrect": true
```

### ❌ If API fails:

```json
{
  "status": "API_FAILED",
  "message": "Server not responding"
}
```

👉 This ensures:

* No crashes
* Clear debugging
* Proper backend behavior

---

## 🧪 How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/run
```

---

## 📊 Sample Output

### ✅ Success Case

```json
{
  "isCorrect": true,
  "submittedTotal": 220,
  "expectedTotal": 220
}
```

### ❌ Server Failure Case

```json
{
  "status": "API_FAILED",
  "message": "Server not responding"
}
```

---

## ⚠️ Important Notes

* Exactly **10 polls (0–9)** must be executed
* Duplicate records must be ignored
* Submission must be done **once**
* API may return repeated data (handled correctly) 

---

## 🧩 Challenges Faced

* External API returning **503 (Server Unavailable)**
* Handling duplicate event data
* Ensuring idempotent submission

---

## ✅ Solution Approach

* Implemented **robust polling mechanism**
* Used **set-based deduplication**
* Added **safe API handling (no crash)**
* Provided **clear logs for debugging**

---

## 📁 Project Structure

```
quiz-leaderboard-api-fastapi/
│── main.py
│── requirements.txt
│── .gitignore
│── README.md
```

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 👨‍💻 Author

**Shourish Paul**  
B.Tech Student – SRM Institute of Science and Technology  
📧 Email: sp7179@srmist.edu.in  
🆔 Registration No: RA2311003030036

---

## 🏁 Final Note

This project demonstrates:

* API Integration
* Data Processing
* Error Handling
* Backend Engineering Skills

👉 **If API is active → system returns correct leaderboard**
👉 **If API fails → system clearly indicates server-side issue**

---

[1]: https://en.wikipedia.org/wiki/FastAPI?utm_source=chatgpt.com "FastAPI"
