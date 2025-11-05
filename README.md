# Resume Bot

An AI-powered terminal user interface (TUI) application that helps automate the job application process by generating tailored resumes and cover letters based on job descriptions.

## Features

- **Interactive TUI**: Built with `prompt_toolkit` for a smooth command-line interface experience
- **Job Scraping**: Automatically scrapes job listings from configured job sites using Crawl4AI
- **AI-Powered Tailoring**: Uses LangChain and various LLMs to:
  - Parse job descriptions
  - Extract relevant skills and experience
  - Generate customized resumes
  - Create personalized cover letters
- **Job Database**: SQLite-based job tracking system to manage applications
- **Company Research**: Integrates Tavily API for company information lookup
- **Multiple Screens**:
  - Landing screen with navigation
  - Find jobs screen for automated job discovery
  - Manual apply for custom applications
  - Configuration management
  - Relint functionality for resume optimization
  - Job description viewer
  - Application management

## Prerequisites

- Python 3.8+
- Pandoc (for PDF generation)
- Virtual environment recommended

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd resume-bot
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the root directory following the `.env.example` template:

5. Prepare your data:

- Add your personal information in the `data/` directory
- Include an example cover letter in `data/example_cover_letter.md`
- Configure your skills, projects, and experience data

## Usage

### Running the Application

```bash
python main.py
```

Or use the provided script:

```bash
./run.sh
```

### Navigation

- **Vim binds**: Navigate menu options
- **Enter**: Select option
- **q**: Quit application
- **Esc**: Go back to previous screen

### Main Features

#### Find Jobs

Automatically scrapes job listings from configured websites and stores them in the local database.

#### Manual Apply

Manually enter a job description URL or details to generate tailored application materials.

#### Generate Resume

Creates a customized markdown resume that is:

- Tailored to the specific job description
- ATS-friendly
- Converted to PDF format
- Highlights relevant skills and experiences

#### Generate Cover Letter

Produces a personalized cover letter that:

- Matches the job requirements
- Includes company research
- Follows professional formatting
- References your relevant projects and experience
- Includes extra details that you tell the AI

## Key Technologies

- **prompt_toolkit**: Terminal UI framework
- **LangChain**: LLM orchestration
- **Crawl4AI**: Web scraping with Playwright
- **Pandoc**: Document conversion (Markdown to PDF)
- **SQLite**: Local job database
- **OpenAI/Groq**: AI model providers
- **Tavily**: Company research API
- **sentence-transformers**: Semantic similarity matching

## Configuration

The application supports customization through:

- Font settings and formatting options in `models/format_settings.py`
- LLM configuration in `ai/llm_config.py`
- Job scraping parameters in `job_scraping.py`

## Output

Generated documents are saved as:

- **Resumes**: `resume-{company-name}.pdf`
- **Cover Letters**: `cover-letter-{company-name}.pdf`
- Optional markdown versions can be retained

## Contributing

[Add contribution guidelines if applicable]
