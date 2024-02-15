
import os
import openai
import logging
from key import key
class Qtype:
    def __init__(self, type="True/False Questions", number=5):
        self.type = type
        self.number = number
    def set(self, type, number):
        self.type = type
        self.number = number
        return 0
    def get(self):
        return f"{self.number} {self.type}"
class questioner:
    def __init__(mod, model="gpt-3.5-turbo"):
        mod.model = model
        openai.api_key = key
    def typer(mod, types):
        response = ""
        for type in types:
            logging.error(types)
            logging.error(type)
            temp = type.get()
            if temp[0] == "1":
                temp = temp.replace("*", "")
            else:
                temp = temp.replace("*", "s")
            response += temp + ", "
        return response[:-2:]
    def writeText(mod, text, types):
        chat_completion = openai.ChatCompletion.create(
            model=mod.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a test creator, I will give you texts, and you will create tests based in information in them.
            I want you to create a few questions from each category provide answers for them in the end based on the TEXT: {" ".join([tp.get() for tp in types])}
            You should NOT say anything apart from questions and answers. Text begins after TEXT:
            You should numerate your questions. Do not write questions before you analyzed the whole text. Remember NOT to double questions and NOT to write different questions using  one  sentence. DO NOT write text again. Answers can't all be the same. For True/False questions there should be almost equal amount of questions with answer True and False. ALWAYS write answers for created questions in the end of the response, but DO NOT write them after each question. DO NOT write more or less questions than specified.""",
                },
                {"role": "user", "content": text},
            ],
        )
        return chat_completion["choices"][0]["message"]["content"]
