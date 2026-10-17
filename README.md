# SanskritiScripter 📖

> *"Stories that bring your culture to life."*

An AI-powered children's storybook generator celebrating Indian festivals, folklore, regional traditions and languages.

---

## ✨ Features (MVP)

- 🎨 Beautiful storybook-style Streamlit UI
- 📝 Story creation form with child name, age, region, festival, language, story idea and moral
- 📖 4-chapter storybook reader with cover, chapter titles and rich narrative text
- 🌐 English / Regional language toggle per chapter
- ◀ ▶ Chapter navigation with progress dots
- 🖼️ Illustration placeholders with AI-prompt descriptions
- 🔄 Mock story generation (AI via Ollama — coming soon)

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## 📁 Project Structure

```
SanskritiScripter/
│
├── app.py                # Main Streamlit application
├── story_generator.py    # Story generation logic (mock + future Ollama)
├── cultural_data.json    # Regions, festivals, languages, mock story data
├── story_cover.png       # Sample story cover illustration
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🛣️ Roadmap

- [ ] **Ollama integration** — Real AI story generation using local LLM
- [ ] **Multi-story library** — Multiple mock stories for different festivals
- [ ] **Illustration generation** — AI-generated chapter illustrations
- [ ] **Audio narration** — Text-to-speech in regional languages
- [ ] **PDF export** — Download the storybook as a PDF
- [ ] **More languages** — Odia, Kannada, Gujarati, Urdu

---

## 🎉 Supported Festivals

Durga Puja · Diwali · Holi · Onam · Pongal · Bihu · Lohri · Ganesh Chaturthi · Eid · Christmas · Navratri · Baisakhi · Ugadi · Vishu · Chhath Puja

## 🗣️ Supported Languages

English · Bengali · Hindi · Tamil · Telugu · Malayalam · Marathi · Punjabi · Assamese

---

*Built with ❤️ using Python & Streamlit*
