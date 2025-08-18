from openai import OpenAI
from pypdf import PdfReader
from docx import Document
import os
import gradio as gr
from dotenv import load_dotenv
import re

class Me:
    def __init__(self):
        load_dotenv(override=True)
        self.openAI = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv("OPENROUTER_API_KEY"))
        self.LinkedinProfile = ""
        reader = PdfReader("./me/Profile.pdf")
        for page in reader.pages:
            self.LinkedinProfile += page.extract_text()
        self.summary = ""
        doc = Document("./me/Summary.docx")
        for para in doc.paragraphs:
            self.summary += para.text

    def set(self):
        self.name = "Srinivasan Amaranathan"

        self.SystemPrompt = f"You are acting as {self.name}.What ever Question raised relared to professional life you should be able to answer\
                as {self.name} . i am sharing you both resume and Linked profile.\
                Resume is {self.summary} and \
                Linked profile is {self.LinkedinProfile}.\
                Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
                If you don't know the answer, say so."
        
    def evaluation(self,Question,response,history):
        self.esystemprompt = f"your an evaluator. you are going to evalute the questions \
                    and the response related professional life of {self.name}.\
                    {self.name} resume is {self.summary} and his \
                    Linked profile is {self.LinkedinProfile}.Just reply me either correct or wrong"
        
        self.euserprompt = f"History of coveration is {history}\
                    Latest Question Asked is {Question}\
                        response is {response}."
        
        client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv("OPENROUTER_API_KEY"))
        Messages = [{"role":"system","content": self.esystemprompt}]+history+[{"role":"user","content":self.euserprompt}]
        response = client.chat.completions.create(
            model="tngtech/deepseek-r1t2-chimera:free",
            messages=Messages)
        return response.choices[0].message.content
        
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.SystemPrompt}] + history + [{"role": "user", "content": message}]
        response = self.openAI.chat.completions.create(model="tngtech/deepseek-r1t2-chimera:free", messages=messages)
        reply = response.choices[0].message.content
        response = self.evaluation(message,reply,history)
        if re.search("correct", response, re.IGNORECASE) :
            return reply
        else:
            return f"issue in AI response. Evaluator reply is {response}. error is {reply}."
        
if __name__ == "__main__":
    print("hi")
    me = Me()
    me.set()
    gr.ChatInterface(me.chat, type="messages").launch()
    #result = me.chat("hi",[])
    #print(result)

    
        

