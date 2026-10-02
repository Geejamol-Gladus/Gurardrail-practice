import os
from dotenv import load_dotenv

from langchain_community.llms import Ollama
from typing import Any, Dict
from guardrails.errors import ValidationError

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from guardrails import Guard,OnFailAction
# adding my own custom validator 

from guardrails.validator_base import(

    FailResult,
    PassResult,
    Validator,
    ValidationResult,
    register_validator,
)
@register_validator(name ="topic_validator",data_type="string")
class Restuarant_topic_validator(Validator):
    def validate(
            self,
            value:Any,
            metadata:Dict
    )-> ValidationResult:
        allowed_words={

             "restaurant",
            "food",
            "menu",
            "meal",
            "dish",
            "pizza",
            "service",
            "staff",
            "delivery",
            "review",
            "rating",
            "price",
            "taste",
            "customer",
            "experience"
        }


        question =str(value).lower()
        if not any (word in question for word in allowed_words):
            return FailResult(
                error_message=("the question is unrealted to teh restaurant ")
            )
        return PassResult()
##_______________________________________
#create your own guard 
##---------------------------------------

topic_guard =Guard().use(Restuarant_topic_validator(on_fail="exception"))

    

load_dotenv()
# Check whether the LangSmith API key was loaded
if not os.getenv("LANGSMITH_API_KEY"):
    st.error("LANGSMITH_API_KEY was not found in the .env file.")
    st.stop()

#os.environ["LANGSMITH_API_KEY"] =os.getenv("LANGSMITH_API_KEY")
#os.environ["LANGSMITH_PROJECT"]=os.getenv("LANGSMITH_PROJECT")

# Prompt Template

prompt =ChatPromptTemplate.from_messages([

    (# what the ssytem has to do 
        "system","you are a helpful asssitant ,respond to the question asked "),
    (# user 
        "user","question:{question}" )

])
##2. design streamlit frame work

st.title("LangChain Demo with Gemma ")

input_text=st.text_input("What question do you have in mind?")


###call the ollama model

llm =Ollama(model="gemma:2b")

output_parser =StrOutputParser()

##chain

chain=prompt|llm|output_parser

# the guardrail are implemented here
if input_text:
    try:
        topic_guard.validate(input_text)

    except ValidationError:
        st.warning("Please tyep arestaurant related question ")


    else:
        with st.spinner("generating an answer"):
            st.write(chain.invoke({"question":input_text}))

