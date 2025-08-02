# Universal Resume Parser: Extract Structured Data from Any Resume

## 📄 Overview

**Universal Resume Parser** is a Python-based tool that intelligently extracts structured data from resumes (PDFs) across any industry — tech, business, healthcare, education, and more. It outputs clean, categorized JSON including skills, experience, projects, contact info, and hyperlinks.

Powered by local LLMs via **Ollama** (Mistral or LLaMA 3), this parser delivers context-aware, accurate extraction.

---

## 🚀 Key Features

- **Multi-Field Support**: Handles resumes from diverse domains — tech, healthcare, business, creative arts, and more.
- **Structured Output**:
  - Personal info: name, contact, social links
  - Skills: auto-categorized by domain
  - Experience: roles, companies, responsibilities, impact
  - Projects: tailored to industry focus
- **Hyperlink Detection**: Pulls GitHub, LinkedIn, portfolios, etc., from resume PDFs
- **LLM-Powered Parsing**: Uses local LLMs through Ollama for intelligent, context-aware parsing

---

## 📦 Installation

### Prerequisites

- Python **3.8+**
- [Ollama](https://ollama.com) installed locally

### Install Required Libraries

```bash
pip install pydantic pdfplumber langchain-ollama PyPDF2
```

### Pull the LLM Model

```bash
ollama pull mistral
```

---

## ▶️ Usage

1. Place your resume PDFs in the `./resumes/` directory.
2. Run the parser:

```bash
python parser.py
```

3. Extracted JSON files will be saved in the `./output/` folder.

---

## 🧾 Output Format

The tool outputs structured JSON data. Below are examples based on different resume types:

### Tech Resume Example

```json
{
  "name": "Alice Smith",
  "contact": {
    "email": "alice@example.com",
    "phone": "+123456789",
    "links": [
      "https://github.com/alicesmith",
      "https://linkedin.com/in/alicesmith"
    ]
  },
  "skills": {
    "languages": ["Python", "JavaScript"],
    "frameworks": ["Django", "React"],
    "tools": ["Docker", "Git"]
  },
  "experience": [
    {
      "role": "Software Engineer",
      "company": "TechCorp",
      "achievements": [
        "Improved API performance by 40%",
        "Led migration to cloud infrastructure"
      ]
    }
  ],
  "projects": [
    {
      "name": "Resume Parser",
      "description": "LLM-powered resume analysis tool",
      "tech_stack": ["Python", "Langchain", "Ollama"]
    }
  ]
}
```

### Business Resume Example

- Skills include stakeholder management, ROI optimization, financial analysis  
- Experience emphasizes team leadership, strategic impact

### Healthcare Resume Example

- Highlights certifications (e.g., RN, CPR), patient systems, EMR/EHR usage  
- Projects include clinical trials, public health outreach

---

## ⚙️ Customization

### Modify Schema

Edit `schema.py` to customize or add new fields in the `ResumeData` model.

### Adjust LLM Prompts

Update `prompts.py` to improve or specialize how the LLM extracts data for specific industries or resume formats.

---

## ⚠️ Limitations

- Works best with clean, text-based PDFs (not scanned images or photos)
- Hyperlinks may be missed if not embedded in PDF text
- Requires local LLM running via Ollama

---

## 🤝 Contributing

We welcome contributions!

- Open issues or suggest improvements via GitHub Issues
- Submit pull requests for additional field adapters (e.g., legal, education, creative writing)


