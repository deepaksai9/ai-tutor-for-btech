# 🧠 AI Genius Tutor

An intelligent, adaptive coding tutor built with **LangChain**, **Streamlit**, and **Groq 70B**. This application creates personalized learning paths, generates daily lessons, creates dynamic quizzes, and tracks your progress for any programming language.

## ✨ Features

- **Personalized Curriculum**: Generates a 30-day learning roadmap based on your current skill level.
- **Language Agnostic**: Learn **Python, JavaScript, Rust, Go**, or any other language you choose.
- **AI-Powered Lessons**: Daily lessons generated on-the-fly using Llama-3-70b (via Groq) for high-speed, high-quality explanations.
- **Smart Assessment**: Initial quiz determines if you are a Beginner, Intermediate, or Advanced learner.
- **Interactive Quizzes**: Generates Multiple Choice Questions (MCQs) and Coding Challenges for every topic.
- **Persistent Progress**: Keeps track of your completed days, quiz scores, and streak.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM Orchestration**: [LangChain](https://python.langchain.com/)
- **Model**: Llama-3-70b-versatile (via [Groq](https://groq.com/))
- **Data Handling**: Pydantic & JsonOutputParser for structured AI responses

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [Groq API Key](https://console.groq.com/keys) (Free to generate)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-genius-tutor.git
   cd ai-genius-tutor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r ai_tutor/requirements.txt
   ```

4. **Set up Environment Variables:**
   Create a `.env` file in the `ai_tutor` directory (or root) and add your API key:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the Application:**
   ```bash
   streamlit run ai_tutor/app.py
   ```

## 📂 Project Structure

```
ai_tutor/
├── app.py                  # Main Streamlit application entry point
├── chains/                 # LangChain logic definitions
│   ├── assessment_chain.py
│   ├── learning_path_chain.py
│   ├── lesson_chain.py
│   ├── quiz_chain.py
│   └── evaluation_chain.py
├── prompts/                # Prompt templates for the LLM
├── memory/                 # JSON-based progress storage
└── requirements.txt        # Python dependencies
```

## 🛡️ Deployment

This app is ready to deploy on **Streamlit Community Cloud**.

1. Push your code to GitHub.
2. Connect your repo on share.streamlit.io.
3. In the "Advanced Settings" of your deployment, add your **Secrets**:
   ```toml
   GROQ_API_KEY = "your_actual_api_key"
   ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
