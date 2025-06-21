# 🎓 University Chatbot

An intelligent, intent-driven chatbot built with Python for assisting users with university-related queries. It supports both a command-line interface and a web-based chat UI via Flask. Trained on custom intents, the chatbot classifies user input and responds with helpful answers for students and website visitors.

---

## 📌 Features

* 🧠 Intent classification using NLP and machine learning
* 💬 CLI-based chatbot via terminal (main.py)
* 🌐 Flask web interface with frontend chat UI (main\_v2.py)
* 📁 Includes preprocessed training data and pickle models
* 🎨 Frontend includes responsive HTML/CSS/JS interface
* 🏫 Designed for academic institutions or university websites

---

## 📁 Project Structure

```
Chatbot_for_university/
├── main.py                         # CLI chatbot interface
├── main_v2.py                      # Flask web chatbot
├── training.py                     # Model training script
├── intents_3.json                  # Intent definitions for NLP model
├── data.pickle                     # Serialized training data
├── static/
│   ├── css/style.css               # Frontend styling
│   └── images/                     # UI images (e.g., logo, background)
├── templates/
│   ├── chat.html                   # Chat UI (Flask)
│   ├── index.html                  # Homepage template
│   └── university-homepage-with-chat.tsx  # Optional React/TypeScript integration
```

---

## 🛠️ Requirements

Install dependencies with:

```bash
pip install flask nltk scikit-learn tensorflow
```

Ensure you also download NLTK tokenizers if needed:

```python
import nltk
nltk.download('punkt')
```

---

## 🚀 Usage

### 🖥️ Command Line Interface (CLI)

Run the terminal-based chatbot:

```bash
python main.py
```

Then start chatting in the terminal.

---

### 🌐 Web-Based Chatbot (Flask)

Run the Flask web app:

```bash
python main_v2.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

Interact with the chatbot via the frontend chat window.

---

## 🧠 Training the Model

To re-train the model or modify intents:

1. Edit intents in intents\_3.json.
2. Run:

```bash
python training.py
```

This will regenerate data.pickle used for prediction.

---

