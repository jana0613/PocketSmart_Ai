# 🪙 PocketSmart AI

PocketSmart AI is a GenAI-powered budget and recommendation assistant for **Home Interior, Party, and Jewelry planning**.

## ✨ Features
- User registration and JWT authentication
- 🏠 Home Interior Planner
- 🎉 Party Planner
- 💎 Jewelry Planner with optional outfit image analysis
- Budget-aware recommendations
- Recommendation history stored in SQLite
- Google Gemini integration using the current `google-genai` SDK
- Deterministic fallback recommendations when Gemini is unavailable
- FastAPI REST API with Swagger docs
- Responsive Jinja2 + HTML/CSS/JavaScript frontend
- Pytest test suite

## 🏗️ Architecture

```text
Browser → FastAPI → Auth/Validation → Recommendation Service
                              ↓              ↓
                           SQLite       Gemini AI
                              ↓              ↓
                         History       AI/Fallback Result
```

## 📁 Project Structure

```text
PocketSmart_Ai/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── dependencies.py
│   ├── security.py
│   ├── models/
│   ├── routes/
│   └── services/
├── templates/
├── static/
├── tests/
├── data/
├── .env.example
├── .gitignore
└── requirements.txt
```

## 🚀 Windows / VS Code Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Put your Gemini API key in `.env` if you want live AI responses:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Then run:

```powershell
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000**.

Swagger API docs: **http://127.0.0.1:8000/docs**

## 🧪 Testing

```powershell
pytest -q
```

The tests work without a Gemini key because the recommendation service has a fallback mode.

## 🔐 Security

Never commit `.env` or a real Gemini API key. The repository's `.gitignore` excludes `.env`, virtual environments, SQLite databases, and uploads.

## 🔮 Future Enhancements
- Live product/retailer integrations
- Real-time price comparison
- More planner categories
- Cloud deployment
- Mobile application
- Advanced personalization

**PocketSmart AI — Smart recommendations. Smarter budgeting.**
