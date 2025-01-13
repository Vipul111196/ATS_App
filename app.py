import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import PyPDF2 as pdf
import os

# Streamlit app configuration
st.set_page_config(page_title="Smart ATS", page_icon=":briefcase:", layout="wide")


#####################################################
# # Sidebar for OpenAI API Key Input
# st.sidebar.header("API Key Configuration")
# openai_api_key = st.sidebar.text_input(
#     "Enter OpenAI API Key",
#     type="password",
#     help="Enter your OpenAI API Key to enable the app.",
# )

# # Validate API Key
# if openai_api_key:
#     # Set the OpenAI API key as an environment variable
#     os.environ["OPENAI_API_KEY"] = openai_api_key
#     st.sidebar.success("OpenAI API key set successfully!")
# else:
#     st.sidebar.warning("Please enter your OpenAI API key.")

# # OpenAI Model and Endpoint
# openai_model = "gpt-4o"
# llm = OpenAI(model=openai_model)


###########################################################
# Sidebar for API Key Input
st.sidebar.header("API Key Configuration")
huggingface_token = st.sidebar.text_input(
    "Enter Hugging Face API Token", 
    type="password", 
    help="Enter your Hugging Face API Token to enable the app."
)

# Display instructions in the sidebar
st.sidebar.markdown("""
**Steps**:
1. Obtain your API key from [Hugging Face Tokens](https://huggingface.co/settings/tokens).
2. Paste it in the input box above.
""")

# Validate API Key
if huggingface_token:
    # Set the token as an environment variable
    import os
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_token
    st.sidebar.success("Hugging Face token set successfully!")
else:
    st.sidebar.warning("Please enter your Hugging Face API token.")

# Hugging Face Model and Endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
endpoint_url = f"https://api-inference.huggingface.co/models/{repo_id}"
llm = HuggingFaceEndpoint(endpoint_url=endpoint_url)


###########################################################

# Chat prompt template
# template = """
# You are an advanced and highly skilled Applicant Tracking System (ATS) with expertise in evaluating resumes across various industries. Your task is to review the provided resume in relation to the given job description and provide constructive feedback.

# **Instructions**:
# 1. Start with a brief, natural-language review of the resume's overall quality and effectiveness, focusing on its strengths and weaknesses.
# 2. Provide a structured match assessment, including:
#    {{
#       "JD Match Percentage": "<calculated_percentage>%",
#       "Missing Keywords": ["keyword1", "keyword2", ...],
#       "Profile Enhancement Suggestions": "Your detailed suggestions here."
#    }}
# 3. Conclude with actionable suggestions, including recommended skills to develop, courses to take, or projects to undertake to strengthen the candidate's profile.

# **Inputs**:
# Resume: {resume_text}
# Job Description: {job_description}

# **Response Format**:
# 1. **Resume Review**: Provide a brief natural-language assessment of the resume.
# 2. **Match Assessment**: Provide a structured analysis of the match with the job description.
# 3. **Improvement Suggestions**: Recommend specific courses, certifications, or projects to strengthen the resume and improve job suitability.

# Be constructive, supportive, and detailed in your response.
# """

template = """
As an advanced Applicant Tracking System (ATS) with comprehensive knowledge across various industries, your task is to strictly output a JSON object that evaluates the provided resume against the job description. 

**Instructions**:
1. Calculate a percentage match between the resume and job description.
2. Identify missing critical keywords.
3. Provide enhancement suggestions.

**Inputs**:
Resume: {resume_text}
Job Description: {job_description}

Respond in the following format.

  "**JD Match Percentage**": "<calculated_percentage>%",
  "**Missing Keywords**": ["keyword1", "keyword2", ...],
  "**Profile Enhancement Suggestions**": "Your detailed suggestions here."
  "**Match Assessment**": "Provide a structured analysis of the match with the job description."
  "**Improvement Suggestions**": "Recommend specific courses, certifications, or projects to strengthen the resume and improve job suitability."
"""


prompt = ChatPromptTemplate.from_template(template=template)

# Function to get LLM response
def get_llm_response(input_data):
    try:
        ats_chain = prompt | llm | StrOutputParser()
        response = ats_chain.invoke(input_data)
        return response
    except Exception as e:
        return f"Error invoking the model: {e}"

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = " ".join([page.extract_text() for page in reader.pages])
        if not text.strip():
            raise ValueError("No text could be extracted from the uploaded PDF.")
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

# Streamlit app layout
st.title("Application Tracking System ATS :briefcase:")
st.markdown("**Enhance Your Resume for Applicant Tracking Systems**")

# Inputs
jd = st.text_area("Paste the Job Description", height=200, placeholder="Enter the job description here...")
uploaded_file = st.file_uploader("Upload Your Resume (PDF format)", type="pdf", help="Please upload your resume in PDF format.")
submit = st.button("Submit")

# Process submission
if submit:
    # if not (openai_api_key or huggingface_token):
    #     st.error("Please enter your OpenAI API key in the sidebar.")
    if not huggingface_token:
        st.error("Please enter your huggingface_token in the sidebar.")
    elif not jd:
        st.warning("Please enter the job description.")
    elif uploaded_file is None:
        st.warning("Please upload your resume in PDF format.")
    else:
        with st.spinner("Processing..."):
            resume_text = input_pdf_text(uploaded_file)
            if resume_text:
                input_data = {"job_description": jd, "resume_text": resume_text}
                response = get_llm_response(input_data)
                st.subheader("Recommendations for ATS friendly resume")
                st.write("Most Important: Use basic template as shown here 'https://www.jobscan.co/resume-templates/ats-templates' and focus on below suggestions: ")
                st.write(response)
            else:
                st.error("Failed to extract text from the uploaded PDF. Please check the file and try again.")

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextArea textarea {
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .stFileUploader div {
            border: 1px dashed #ccc;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)
