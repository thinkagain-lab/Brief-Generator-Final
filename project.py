# import openai

# def generate_brief(design_type, industry):
#     openai.api_key = 'sk-proj-k7gQxcTn6LUfJRTStNnLT3BlbkFJP5DZSf9tnyxZ6u5bftPX'
    
#     prompt = (
#         f"Generate a design brief for a {design_type} in the {industry} industry. "
#         f"Include a company name, company description, design requirements, and a deadline."
#     )
    
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=200
#     )
    
#     return response.choices[0].text.strip()

# # Example usage
# brief = generate_brief("Logo", "Technology")
# print(brief)

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from datetime import datetime


os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
chat = ChatGroq(temperature=0.5, model_name="mixtral-8x7b-32768")

def get_current_datetime():
    """
    Get the current date and time.
    
    Returns:
    str: Current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    # Get the current date and time
    current_datetime = datetime.now()
    
    # Format the date and time as 'YYYY-MM-DD HH:MM:SS'
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    return datetime_str

def brief(design_type,industry,current_datetime):
    system=f"Generate a design brief for a {design_type} in the {industry} industry. Include a company name, company description, design requirements, and a deadline(The deadline must be According to the requirement and an experienced person would take to complete in days and it should be  after the current date and time {current_datetime})."
    
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    res = chain.invoke({"text": f'Create realistic design brief for the {design_type} and {industry}.'})
    return res.content

design_type=input("Enter design type eg. logo,bilboard,packaging etc. ")
Industy=input("Enter Industry eg. Tech,Education,Food etc ")
print("***********************************************************")

# Example usage
current_datetime = get_current_datetime()

result=brief(design_type,Industy,current_datetime)
print(result)
