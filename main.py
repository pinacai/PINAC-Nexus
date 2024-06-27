import inquirer
from ai_models.ChatGPT import ChatGPT_3_5
from ai_models.Gemini import Gemini_1_5_Pro, Gemini_1_Pro, Gemini_1_5_Flash
from prompts.prompt import givePrompt
from langchain.schema import HumanMessage, AIMessage


# Initializing AI Models
chatgpt_3_5 = ChatGPT_3_5()
gemini_1_5_pro = Gemini_1_5_Pro()
gemini_1_pro = Gemini_1_Pro()
gemini_1_5_flash = Gemini_1_5_Flash()


# Initialize the chat history
chatHistory = []


# Clearing chat history
def clearHistory():
    chatHistory.clear()


def createResponse(AiModel, query, prompt_name, response_type):
    # gets the required prompt
    prompt = givePrompt(prompt_name, query)
    ai_response = AiModel.generalAssistant(prompt, chatHistory)
    if not ai_response["error_occurred"]:
        chatHistory.append(AIMessage(content=ai_response["response"]))
        return {
            "error_occurred": False,
            "response": {
                "type": response_type,
                "content": ai_response["response"],
            },
            "error": None,
        }
    else:
        return ai_response


def giveAiResponseArray(AiModel, query):
    chatHistory.append(HumanMessage(content=query))
    ai_response = AiModel.classifyTaskCategory(query)

    if not ai_response["error_occurred"]:
        #
        #
        if ai_response["category"] == "compose complaint email":
            response = createResponse(AiModel, query, "complaint email", "email")
        #
        else:
            response = createResponse(AiModel, query, "others", "others")

    else:
        response = ai_response

    return response


def processClientRequest(request: dict):
    if request["request_type"] == "user-input":
        if request["preferred_model"] == "ChatGPT-3.5 turbo":
            response = giveAiResponseArray(chatgpt_3_5, request["user_query"])
        elif request["preferred_model"] == "Gemini 1.5 Pro":
            response = giveAiResponseArray(gemini_1_5_pro, request["user_query"])
        elif request["preferred_model"] == "Gemini 1.0 Pro":
            response = giveAiResponseArray(gemini_1_pro, request["user_query"])
        elif request["preferred_model"] == "Gemini Flash 1.5":
            response = giveAiResponseArray(gemini_1_5_flash, request["user_query"])

    else:
        response = {
            "error_occurred": True,
            "response": None,
            "error": "Got unknown 'request-type'",
        }

    return response


if __name__ == "__main__":
    print()
    print()
    print(
        "  0101010101  01  0101      01  0101010101  0101010101       0101      01  01010101  01      01  01       01  0101010101  "
    )
    print(
        "  01      01  01  01 01     01  01      01  01               01 01     01  01         01    01   01       01  01          "
    )
    print(
        "  01      01  01  01  01    01  01      01  01               01  01    01  01          01  01    01       01  01          "
    )
    print(
        "  0101010101  01  01   01   01  0101010101  01        010101 01   01   01  01010101     0101     01       01  0101010101  "
    )
    print(
        "  01          01  01    01  01  01      01  01               01    01  01  01          01  01    01       01          01  "
    )
    print(
        "  01          01  01     01 01  01      01  01               01     01 01  01         01    01   01       01          01  "
    )
    print(
        "  01          01  01      0101  01      01  0101010101       01      0101  01010101  01      01  01010101001  0101010101  "
    )
    print()
    print()

    questions = [
        inquirer.List(
            "model",
            message="What AI Model You Want to Use?",
            choices=[
                "ChatGPT-3.5 turbo",
                # "Gemini 1.0 Pro",
                # "Gemini 1.5 Pro",
                "Gemini Flash 1.5",
            ],
        ),
    ]
    answer = inquirer.prompt(questions)
    print(answer["model"])
    print("type '/bye' to exit")
    print()
    while True:
        query = input(">>> ")
        if query == "/bye":
            break
        else:
            response = processClientRequest(
                {
                    "request_type": "user-input",
                    "preferred_model": answer["model"],
                    "user_query": query,
                }
            )
            print(response["response"]["content"])
