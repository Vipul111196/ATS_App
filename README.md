# Smart ATS (Applicant Tracking System) Tracker

Smart ATS is a Streamlit-based tool that uses OpenAI's GPT-4 API to evaluate resumes against job descriptions for better ATS (Applicant Tracking System) compatibility. Built with resume screening in mind, this tool provides feedback on resume match percentage, missing keywords, and a profile summary based on a provided job description, helping users optimize their resumes for competitive job markets in technology and data fields.

## Features
- **Resume Match Scoring**: Calculates the percentage match between a resume and the job description.
- **Missing Keywords Identification**: Lists missing keywords, highlighting essential skills and terms missing from the resume.
- **Profile Summary**: Summarizes the resume's alignment with the job requirements, offering targeted advice for improvement.

## Tech Stack
- **Streamlit**: For the web interface.
- **OpenAI GPT-4 API**: For text processing and analysis.
- **PyPDF2**: For extracting text from PDF resumes.
- **dotenv**: For environment variable management.

## Getting Started

### Prerequisites
- **Python 3.8 or later**
- **OpenAI API Key**: You’ll need an API key from OpenAI to use GPT-4.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Vipul111196/ATS_App.git
   cd ATS_App
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the project root:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Replace `your_openai_api_key_here` with your actual OpenAI API key.

### Running the App
Start the Streamlit app from the project directory:
```bash
streamlit run app.py
```

The app will open in your default web browser.

## Usage

1. **Input the Job Description**: Paste the job description into the provided text area.
2. **Upload Resume**: Upload a PDF version of your resume.
3. **Get Feedback**: Click **Submit** to receive:
   - **Job Description Match (%)**: A percentage match indicating alignment with the job description.
   - **Missing Keywords**: A list of missing keywords crucial to the job role.
   - **Profile Summary**: A high-level summary of the resume’s alignment with job requirements and suggested improvements.

## Project Structure

- **`app.py`**: Main application code, implementing Streamlit UI and ATS functionality.
- **`requirements.txt`**: Lists required Python libraries.
- **`.env`**: Contains environment variables for secure storage of API keys.

## Example Response Format

The response is structured as follows:
```json
{
  "JD Match": "80%",
  "MissingKeywords": ["Python", "Machine Learning", "Data Visualization"],
  "Profile Summary": "The resume aligns well with the job description, but could improve by adding specific tools such as Python, and emphasizing experience in Machine Learning."
}
```

## Future Enhancements
- **Support for Multiple File Formats**: Adding support for DOCX and TXT resumes.
- **Additional Analysis**: Incorporate advanced insights like experience level and domain-specific recommendations.
- **Automated Suggestions**: Generate specific, actionable suggestions for each missing keyword or skill.

## License
This project is open-source and licensed under the MIT License.
