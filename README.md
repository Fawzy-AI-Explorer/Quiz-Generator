# Quiz Generator 📝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/) [![CrewAI](https://img.shields.io/badge/CrewAI-Powered-green.svg)](https://github.com/joaomdmoura/crewAI) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/gallery) [![PyPDF2](https://img.shields.io/badge/PyPDF2-Enabled-blue)](https://pypdf2.readthedocs.io/) [![LangChain](https://img.shields.io/badge/LangChain-Integrated-orange)](https://langchain.com/) [![AI Generated](https://img.shields.io/badge/AI-Generated_Content-purple.svg)](https://github.com/Fawzy-AI-Explorer/Quiz-Generator) [![GitHub stars](https://img.shields.io/github/stars/Fawzy-AI-Explorer/Quiz-Generator?style=social)](https://github.com/Fawzy-AI-Explorer/Quiz-Generator/stargazers) [![GitHub forks](https://img.shields.io/github/forks/Fawzy-AI-Explorer/Quiz-Generator?style=social)](https://github.com/Fawzy-AI-Explorer/Quiz-Generator/network/members) [![GitHub watchers](https://img.shields.io/github/watchers/Fawzy-AI-Explorer/Quiz-Generator?style=social)](https://github.com/Fawzy-AI-Explorer/Quiz-Generator/watchers) [![GitHub](https://img.shields.io/badge/GitHub-View_Project-blue?logo=GitHub)](https://github.com/Fawzy-AI-Explorer/Quiz-Generator)

> Generate intelligent quizzes from any PDF document using AI Agents

A sophisticated quiz generation system that transforms PDF documents into educational assessments, leveraging AI agents to create high-quality multiple-choice and true/false questions with detailed explanations.

## 📋 Introduction

Quiz Generator is an AI-powered application built using CrewAI that automatically creates educational quizzes from PDF documents. The system employs specialized AI agents working together to extract content, generate questions, and provide comprehensive answer explanations. Perfect for educators, content creators, and students looking to create assessment materials or test their understanding of technical content.

## 🎥 Live Demo

![Live Demo](assets/live_demo.mkv)

## ✨ Features

- 🤖 **AI Agent-Powered**: Utilizes specialized CrewAI agents for different aspects of quiz generation
- 📄 **PDF Processing**: Extracts and processes text from PDF documents
- 🧠 **Multiple Question Types**: Generates both multiple-choice and true/false questions
- 📊 **Quiz Analysis**: Provides detailed explanations for correct and incorrect answers
- 🔍 **Quality Control**: Ensures questions are relevant and pedagogically sound
- 🖥️ **User-Friendly Interface**: Clean Streamlit web interface for easy interaction
- 📱 **Responsive Design**: Works across different screen sizes and devices

## Project Structure

```tree
Quiz-Generator/
├── __init__.py
├── app.py                  # Streamlit web application
├── requirements.txt        # Project dependencies
├── .gitignore             # Git ignore file
├── assets/                # Static assets
│   └── live_demo.mkv      # Demo video
├── config/                # Configuration files
│   ├── __init__.py
│   ├── agents.yaml        # Agent definitions
│   ├── config.py          # Global settings
│   └── tasks.yaml         # Task definitions
├── data/                  # Sample PDF documents
├── output/                 # Generated quiz JSON files
│   ├── mcq_quiz.json       # Multiple-choice questions
│   ├── quiz_analysis.json  # Detailed explanations
│   └── tf_quiz.json        # True/false questions
├── src/                   # Core application code
│   ├── __init__.py
│   ├── crew.py            # CrewAI agent setup
│   ├── pydantic_models.py # Data models
│   ├── quiz_pipeline.py   # Main processing pipeline
│   └── utils.py           # Helper functions
├── .devcontainer/         # Development container config
└── .vscode/              # VS Code settings
```

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Fawzy-AI-Explorer/Quiz-Generator.git
   cd Quiz-Generator
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv .venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/Scripts/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root with:

   ```.env
   PROVIDER=your_llm_provider
   MODEL=your_model_name
   BASE_URL=your_base_url
   TEMPERATURE=0.7
   ```

## 💻 Usage

1. **Start the Streamlit application**

   ```bash
   streamlit run app.py
   ```

2. **Using the application**
   - Upload a PDF document through the web interface
   - Click the "Generate Quiz" button
   - Review generated multiple-choice and true/false questions
   - Explore detailed explanations for each question

3. **Running the pipeline directly**

   ```bash
   cd "Quiz generator"
   python -c "from src.quiz_pipeline import run_pipeline; run_pipeline('path/to/your/file.pdf')"
   ```

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit your changes**

   ```bash
   git commit -m 'Add some amazing feature'
   ```

4. **Push to the branch**

   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open a Pull Request**

Please ensure your code follows the project's coding style and includes appropriate tests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

Thanks to all the amazing people who have contributed to this project!

<a href="https://github.com/Fawzy-AI-Explorer/Quiz-Generator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Fawzy-AI-Explorer/Quiz-Generator" />
</a>

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework for orchestrating role-playing autonomous AI agents
- [Streamlit](https://streamlit.io/) - Framework for building the web interface
- [LangChain](https://langchain.com/) - Framework for language model applications
- [PyPDF](https://pypdf.readthedocs.io/) - Library for PDF processing
