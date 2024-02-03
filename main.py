
from streamlit_option_menu import option_menu
from PIL import Image
import os
import replicate
from streamlit_tags import st_tags
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import streamlit as st
import streamlit as st
import base64
from pyresparser import ResumeParser
import streamlit as st
import spacy
import google.generativeai as genai
from google.ai import generativelanguage as glm
from google.ai.generativelanguage_v1beta.types import model

spacy.load('en_core_web_sm')

api_key = 'AIzaSyAYMQSmPWKCJM7C5Pc_eYzLybRyRDwJ-jA'

client = glm.DiscussServiceClient(
    client_options={'api_key':api_key})


def get_gemini_response(input, pdf_content, prompt):
    input_str = str(input).replace('\n', ' ')
    print(glm.Part(text=input_str))
    
    message_prompt = glm.MessagePrompt(
    
    context=glm.Message(
    content=glm.Content(
      parts=[
            glm.Part(text="Please help me to fit my resume with the job description"),
            glm.Part(text=prompt),
            glm.Part(text=input),
            glm.Part(image_uri=pdf_content)
           ]
        )
        ),
    examples=[],
    messages=[]
    )

    request = glm.GenerateMessageRequest(
        model='models/chat-bison-001',
        prompt=message_prompt
        )

    response = client.generate_message(request)

    print(response)
    # message_str = input_str+prompt_str
    # print(input_str+prompt_str)
#     # Create Message instances for examples
#     message_prompt = glm.MessagePrompt(
#     context=glm.Message(content=glm.Content(parts=[glm.Part(message_str)])),  # Provide any context if needed
#     examples=[],  # Add examples if needed
#     messages=[glm.Message(content=glm.Content(parts=[glm.Blog(text=pdf_content_str)]))]
# )

    
    # message_prompt = glm.MessagePrompt(
    #     context=glm.Message(content=glm.Content(parts=[glm.Part(text=prompt_str), glm.Part(text=input_str)])),  # Provide any context if needed
    #     examples=[],  # Add examples if needed
    #     messages=glm.Part(pdf_content_str)
    # )
    

    # Create MessagePrompt instance
    # request = glm.GenerateMessageRequest(
    #     model='models/chat-bison-001',
    #     prompt=message_prompt
    # )
    # request = glm.GenerateMessageRequest(
    # model='models/chat-bison-001',
    # prompt=glm.MessagePrompt(
    #     messages=[glm.Message(content='Hello!')]))

    # print(client.generate_message(request))
    return client.generate_message(request)
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

input_text=st.text_area("Job Description: ",key="input")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description.Please share your professional evaluation on whether the candidate's profile aligns with the role.Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
if pdf_file is not None:
    os.makedirs('./Uploaded_Resumes', exist_ok=True)
    save_image_path = os.path.join('./Uploaded_Resumes', pdf_file.name)
    print("Attempting to open file:", save_image_path)
    with open(save_image_path, "wb") as f:
        f.write(pdf_file.getbuffer())
    show_pdf(save_image_path)
    resume_data = ResumeParser(save_image_path).get_extracted_data()
    resume_text = pdf_reader(save_image_path)
    if resume_text:



        st.header("**Resume Analysis**")
        st.write(
            f'####    :black[ Hey how are you doing , {resume_data["name"]}]')
        st.write(f'###### :blue[ Email: {resume_data["email"]}]')
        st.write(f'###### :blue[ Number: {resume_data["mobile_number"]}]')
        st.write(f'###### :blue[ Education: {resume_data["degree"]}]')
        st.write(
            f'###### :blue[ Designation: {resume_data["designation"]}]')
        st.write(f'###### :blue[ Experience: {resume_data["experience"]}]')
        st.write(
            f'###### :blue[ company_names: {resume_data["company_names"]}]')

        # Skill shows
        keywords = st_tags(
            label='# Your Skills 💡:',
            text='Analysed skills',
            value=resume_data['skills'], 
            maxtags=-1, 
            key='1'
            )
    submit1 = st.button("Tell Me About the Resume")   
    if submit1:
        if pdf_file is not None:
            response=get_gemini_response(input_prompt1,save_image_path,input_text)
            st.subheader("The Repsonse is")
            st.write(response)
        else:
            st.write("Please uplaod the resume") 
    # get_gemini_response(input_prompt1,resume_text,input_text)
