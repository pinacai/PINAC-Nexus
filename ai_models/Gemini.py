import os
from ai_models.__init__ import prepareDatasetWithoutSystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Loading Local API Keys
from dotenv import load_dotenv
load_dotenv(dotenv_path="configs/.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# output parser
output_parser = StrOutputParser()

# Datasets
TCC_Dataset = prepareDatasetWithoutSystemMessage("ai_models/dataset/TCC_Dataset.csv")
CAIT_Dataset = prepareDatasetWithoutSystemMessage("ai_models/dataset/CAIT_Dataset.csv")
TNR_Dataset = prepareDatasetWithoutSystemMessage("ai_models/dataset/TNR_Dataset.csv")


class Gemini:

    def __init__(self):
        self.taskClassificationPrompt = ChatPromptTemplate.from_messages(TCC_Dataset)
        self.generalAssistantPrompt = ChatPromptTemplate.from_messages(CAIT_Dataset)
        self.nameRecognitionPrompt = ChatPromptTemplate.from_messages(TNR_Dataset)

    def chainInitializer(self, llm):
        self.taskClassificationChain = self.taskClassificationPrompt | llm | output_parser
        self.generalAssistantChain = self.generalAssistantPrompt | llm | output_parser
        self.nameRecognitionChain = self.nameRecognitionPrompt | llm | output_parser

    # For classifying the user query into specific task category
    def classifyTaskCategory(self, user_input):
        try:
            aiResponse = self.taskClassificationChain.invoke({"text": user_input})
            response = {"error-occurred": False, "category": aiResponse, "error": None}
        except Exception as e:
            response = {"error-occurred": True, "category": None, "error": str(e)}
        return response

    # General & specialised task assistance
    def generalAssistant(self, user_input, chatHistory):
        try:
            # Extend the chat prompt with the previous chat history
            self.generalAssistantPrompt.extend(chatHistory)
            # Append the current query to the chat prompt
            self.generalAssistantPrompt.append(user_input)
            aiResponse = self.generalAssistantChain.invoke({"text": user_input})
            response = {"error-occurred": False, "response": aiResponse, "error": None}

        except Exception as e:
            response = {"error-occurred": True, "response": None, "error": str(e)}

        return response

    # For Google contact automation, we need to extract and return names from the query
    def findName(self, user_input):
        try:
            aiResponse = self.nameRecognitionChain.invoke({"text": user_input})
            response = {"error-occurred": False, "response": aiResponse, "error": None}
        except Exception as e:
            response = {"error-occurred": True, "response": None, "error": str(e)}
        return response


# Text, Img & Video Input
# >>>   Most Capable Gemini: Complex reasoning tasks such as code and text generation,
#       -------------------  text editing, problem solving, data extraction and generation
class Gemini_1_5_Pro:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", api_key=GOOGLE_API_KEY)
        self.Gemini = Gemini()
        self.Gemini.chainInitializer(self.llm)

    def classifyTaskCategory(self, user_input):
        return self.Gemini.classifyTaskCategory(user_input)

    def generalAssistant(self, user_input, chatHistory):
        return self.Gemini.generalAssistant(user_input, chatHistory)

    def findName(self, user_input):
        return self.Gemini.findName(user_input)


# Only text input
# >>>   Natural language tasks, multi-turn text and code chat, and code generation
class Gemini_1_Pro:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", api_key=GOOGLE_API_KEY)
        self.Gemini = Gemini()
        self.Gemini.chainInitializer(self.llm)

    def classifyTaskCategory(self, user_input):
        return self.Gemini.classifyTaskCategory(user_input)

    def generalAssistant(self, user_input, chatHistory):
        return self.Gemini.generalAssistant(user_input, chatHistory)

    def findName(self, user_input):
        return self.Gemini.findName(user_input)


# Text, Img & Video Input
# >>>   Fastest Gemini: Fast and versatile performance across a diverse variety of tasks
#       --------------
class Gemini_1_5_Flash:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=GOOGLE_API_KEY)
        self.Gemini = Gemini()
        self.Gemini.chainInitializer(self.llm)

    def classifyTaskCategory(self, user_input):
        return self.Gemini.classifyTaskCategory(user_input)

    def generalAssistant(self, user_input, chatHistory):
        return self.Gemini.generalAssistant(user_input, chatHistory)

    def findName(self, user_input):
        return self.Gemini.findName(user_input)
