# Cover Letter Generator

An intelligent application that generates tailored resumes and cover letters using AI. The application analyzes job descriptions and your existing resume to create customized documents that highlight your most relevant experience and skills.

## Features

- **Resume Tailoring**: Automatically optimizes your resume for specific job descriptions
- **Cover Letter Generation**: Creates compelling, personalized cover letters
- **Multiple LLM Support**: Works with both OpenAI and GitHub's AI models
- **User-Friendly Interface**: Simple Streamlit-based UI for easy interaction
- **Document Processing**: Supports both PDF and DOCX formats
- **Copy & Download**: Easy copying and downloading of generated documents

## Prerequisites

- Python 3.8 or higher
- OpenAI API key or GitHub API token
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OGFatmitch/CoverLetterResumeGenerator.git
   cd CoverLetterResumeGenerator
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_API_KEY=your_github_api_key
   ```

## Usage

1. Start the application:
   ```bash
   ./run.sh
   ```
   This will start both the backend and frontend servers.

2. Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

3. In the application:
   - Upload your current resume (PDF or DOCX)
   - Paste the job description
   - Choose your preferred AI model
   - Click "Generate Documents"
   - Use the copy or download buttons to save your generated documents

## Project Structure
CoverLetterGenerator/
├── frontend/ # Streamlit frontend application
├── src/ # Backend services and API
├── requirements.txt # Python dependencies
├── run.sh # Script to start both servers
└── .env # Environment variables (not tracked in git)

## Features in Detail

### Resume Tailoring
- Analyzes job description for key requirements
- Identifies relevant experience and skills
- Optimizes bullet points for impact
- Maintains original format while enhancing content

### Cover Letter Generation
- Creates engaging, personalized cover letters
- Aligns experience with job requirements
- Demonstrates cultural fit
- Uses natural, professional language

### Document Processing
- Supports PDF and DOCX formats
- Preserves original formatting
- Handles complex layouts
- Maintains document structure

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for their GPT models
- GitHub for their AI models
- Streamlit for the frontend framework
- FastAPI for the backend framework
