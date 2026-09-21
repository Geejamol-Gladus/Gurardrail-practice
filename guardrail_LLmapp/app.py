import os
from dotenv import load_dotenv

from langchain_community.llms import Ollama

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



