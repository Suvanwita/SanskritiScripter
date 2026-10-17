# SanskritiScripter 📖

> *"Stories that bring your culture to life."*

An AI-powered children's storybook generator celebrating Indian festivals, folklore, regional traditions and languages — powered by Ollama for local, private AI generation.

---

## ✨ Features

- 🎨 Storybook-style Streamlit UI with Indian cultural aesthetics
- 📝 Story creation form: child name, age, region, festival, language, story idea, moral
- 🤖 **Real AI story generation** via Ollama (local LLM, no API key needed)
- 🌿 **Cultural grounding** — rich authentic context for 13+ region/festival combinations
- 📖 4-chapter storybook reader with cover panel and chapter navigation
- 🌐 English / Regional language toggle per chapter (Bengali, Hindi, Tamil, and more)
- 📏 Age-adaptive vocabulary (5–7, 8–10, 11–13 year olds)
- 🎭 **Demo Mode** — preview the full UI without Ollama running
- ⚙️ Sidebar configuration panel with live Ollama status indicator
- 🔁 Robust JSON parsing — handles malformed LLM output gracefully

---

## 🚀 Quick Start

### 1. Install Python dependencies

```bash
cd SanskritiScripter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up Ollama

**Install Ollama** (if not already installed):

```bash
# Linux / macOS
curl -fsSL https://ollama.com/install.sh | sh
```

Or download from [https://ollama.com](https://ollama.com)

**Start the Ollama server:**

```bash
ollama serve
```

**Pull a model** (choose one):

```bash
# Recommended — good quality, reasonable speed
ollama pull qwen2.5:7b

# Faster / lighter alternative
ollama pull llama3.2:3b

# Higher quality, slower
ollama pull gemma2:9b
```

### 3. Run SanskritiScripter

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## ⚙️ Configuration

### Change the default model

**Option 1 — Environment variable:**
```bash
OLLAMA_MODEL=llama3.2:3b streamlit run app.py
```

**Option 2 — In the sidebar:**
Type any model name in the "Model" field in the sidebar (model must be pulled first).

### Change Ollama host (e.g. remote server)

```bash
OLLAMA_HOST=http://192.168.1.10:11434 streamlit run app.py
```

### Change generation timeout

```bash
OLLAMA_TIMEOUT=300 streamlit run app.py
```

---

## 🎭 Demo Mode

If Ollama isn't available, enable **Demo Mode** in the sidebar to preview the full storybook UI using the built-in sample story "Ananya and the Dancing Flame" (Durga Puja, West Bengal, Bengali/English).

---

## 📁 Project Structure

```
SanskritiScripter/
│
├── app.py               # Main Streamlit UI
├── story_generator.py   # AI pipeline: cultural context + prompt + Ollama + parsing
├── cultural_data.json   # Rich cultural grounding data for 13+ region/festival pairs
├── story_cover.png      # AI-generated cover illustration
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🌍 Supported Regions & Festivals

| Region | Festival |
|--------|----------|
| West Bengal | Durga Puja, Diwali (Kali Puja) |
| Kerala | Onam, Vishu |
| Punjab | Lohri, Baisakhi |
| Assam | Bihu |
| Tamil Nadu | Pongal |
| Maharashtra | Ganesh Chaturthi, Diwali |
| Rajasthan | Holi |
| Gujarat | Navratri |
| Bihar | Chhath Puja |
| Odisha | Diwali |
| Uttar Pradesh | Diwali, Holi |
| Himachal Pradesh | Diwali |
| Goa | Christmas, Eid |

---

## 🗣️ Supported Languages

English · Bengali · Hindi · Tamil · Telugu · Malayalam · Marathi · Punjabi · Assamese

> **Note:** Bengali and English are the best-tested regional languages in the MVP. Other languages follow the same architecture — quality depends on the LLM's multilingual capabilities.

---

## 🛣️ Roadmap

- [ ] Streaming text output (display story as it generates)
- [ ] Illustration generation per chapter
- [ ] Audio narration in regional languages
- [ ] PDF storybook export
- [ ] More regional languages (Odia, Kannada, Gujarati, Urdu)
- [ ] Save and revisit past stories

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Ollama is not available" | Run `ollama serve` in a terminal |
| "Model not found" | Run `ollama pull <model-name>` |
| Generation times out | Use a smaller model or increase `OLLAMA_TIMEOUT` |
| Malformed JSON from LLM | Click "Generate Story" again — LLMs occasionally produce imperfect output |
| App shows blank story | Try a different model (some smaller models struggle with JSON output) |

---

*Built with ❤️ using Python, Streamlit and Ollama*
