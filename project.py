# Resume-Refiner that helps the candidate optimise the resume for a particular job based on the specific keywords and job requirements

import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

st.header('Resume Refiner for the jobs you truly deserve')
job_description = st.text_input('Job Description')
resume = st.file_uploader('upload your resume')

# extracting text page by page from the candidate's resume in the pdf format 

def extract_text_from_resume(resume):
    resume_object = PdfReader(resume)
    resume_as_str = ""
    for page in resume_object.pages :
        resume_as_str+=page.extract_text()
    return resume_as_str

# creating clickable buttons for the front-end application
# One button for comparision b/w resume and job description on job portal/company's website
# Other button for returning the % of match b/w candidate's profile and job role

button1 = st.button('Get a complete comparision')
button2 = st.button('Get the match score')

# prompts for the LLM to perform comparision and return % match

prompt1 = """Act as a well developed Profile Analysing System that is well trained in the 
tasks of extensively,thoroughly learning the job decription & resume of the candidate. 
Use this training to comphrehensively study the below given criterias in both resume and 
job description provided.\criterias for extensive comparision : education, skills, projects, 
experiences, requirements,expectations, job requirements and role descriptions.\n
Based on the study, Write down as points the following\n
important keywords in job description. Measure importance based on repition of keywords 
and/or how they are described. Eg: Must have Python skills is more important than
Python skills preferred.\nkeywords that are common to resume and job description\n
keywords that are present in the job description but absent in resume\nFactors that
make the candidate an ideal fit for the job role based on the thorough study and
rememberance of candidate's resume as well as job role's job description\n
Factors that make the candidate NOT an ideal fit for the job role.
Format the entire body of response using headers, bold fonts etc as 
deemed neat and tidy and appropriate

"""
prompt2 = """Act as a well trained and skillful Match Quantification System that is 
skilled at quantifying how much the
criterias in candidate resume matches with criterias in job description
and express the same as a percentage score.Read/
analyse/study/memorize/evaluate the below criterias from the text of 
the enitre job description and candidate's
resume in its entirety to output an aggregate percentage that tells
how much text from candidate's resume matches with text from the
job description.\ncriterias to read/
analyse/study/memorize/evaluate : skills, requirements, roles,
job descriptions, qualifications, years of 
experience,education, educational background./nThe match score percentage is a
expressed as percentage 
ranging from 0% to 100%  where 0% denotes NO criteria is common/no criterias match
and 100% means all criterias like skills, experience, education.. etc exactly 
match with the corresponding criterias from the resume. The output/response 
from the LLM should be like below\n example of final LLM response/output : 85 %  """


# google's gemini-pro that return responses

model = genai.GenerativeModel(model_name="gemini-pro")

def generate_content(resume, jd, prompt):
    response = model.generate_content(contents = [resume, jd, prompt])
    return response.text

# Implementing the model as an application in front end using streamlit

if button1 :
    if len(job_description)!=0 and resume is not None:
        resume_info = extract_text_from_resume(resume)
        st.write(generate_content(resume_info, job_description,prompt1))
    elif len(job_description)==0 :
        st.error("Please write/paste your job's description and proceed")
    elif resume is None :
        st.error('Upload your resume and proceed')


if button2 :
    if len(job_description)!=0 and resume is not None:
        resume_info = extract_text_from_resume(resume)
        st.write(generate_content(resume_info, job_description,prompt2))
    elif len(job_description)==0 :
        st.error("Please write/paste your job's description and proceed")
    elif resume is None :
        st.error('Upload your resume and proceed')


