from ai_models.__init__ import prepareDataset
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# output parser
output_parser = StrOutputParser()

# Datasets
TCC_Dataset = prepareDataset("ai_models/dataset/TCC_Dataset.csv")
CAIT_Dataset = prepareDataset("ai_models/dataset/CAIT_Dataset.csv")

class OpenSourceLLM:

    def __init__(self) -> None:
        self.taskClassificationPrompt = ChatPromptTemplate.from_messages(TCC_Dataset)
        self.generalAssistantPrompt = ChatPromptTemplate.from_messages(CAIT_Dataset)

    def chainInitializer(self, llm):
        self.taskClassificationChain = self.taskClassificationPrompt | llm | output_parser
        self.generalAssistantChain = self.generalAssistantPrompt | llm | output_parser
    
    # For classifying the user query into specific task category
    def classifyTaskCategory(self, user_input):
        response = self.taskClassificationChain.invoke({"text": user_input})
        return response

    # General & specialized task assistance
    def generalAssistant(self, user_input, chatHistory):
        # Extend the chat prompt with the previous chat history
        self.generalAssistantPrompt.extend(chatHistory)
        # Append the current query to the chat prompt
        self.generalAssistantPrompt.append(user_input)
        response = self.generalAssistantChain.invoke({"text": user_input})
        return response


# --------------------------------------------------------------------------------- #
#                 Very Light Weight Open-Source LLMs (Good for 4GB)                 #
# --------------------------------------------------------------------------------- #

# Gemma 2b from Google DeepMind
# ---> 2 billion parameter
class Gemma_2b:

    def __init__(self):
        self.llm = Ollama(model="gemma:2b")
        self.gemma_2b = OpenSourceLLM()
        self.gemma_2b.chainInitializer(self.llm)

    def classifyTaskCategory(self, user_input):
        return self.gemma_2b.classifyTaskCategory(user_input)

    def generalAssistant(self, user_input, chatHistory):
        return self.gemma_2b.generalAssistant(user_input, chatHistory)



# --------------------------------------------------------------------------------- #
#                   Light Weight Open-Source LLMs (Good for 8GB)                    #
# --------------------------------------------------------------------------------- #

# llama 8b from Meta (Best in class)
# ---> 8 billion parameter
class Llama_8b:

    def __init__(self):
        self.llm = Ollama(model="llama3:8b")
        self.llama_8b = OpenSourceLLM()
        self.llama_8b.chainInitializer(self.llm)

    def classifyTaskCategory(self, user_input):
        return self.llama_8b.classifyTaskCategory(user_input)

    def generalAssistant(self, user_input, chatHistory):
        return self.llama_8b.generalAssistant(user_input, chatHistory)
