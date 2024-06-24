from flask import Flask
from flask_socketio import SocketIO
from functools import cache
from ai_models.ChatGPT import ChatGPT_3_5
from ai_models.Gemini import Gemini_1_5_Pro, Gemini_1_Pro, Gemini_1_5_Flash
from prompts.prompt import givePrompt
from langchain.schema import HumanMessage, AIMessage

# import datetime
# from email_validator import validate_email
# from google_apps.gmail_bot import GoogleGmailManager
# from google_apps.calendar_bot import GoogleCalendarManager
# from google_apps.contact_bot import GoogleContactManager
# from google_apps.task_bot import GoogleTaskManager


# Initializing AI Models
chatgpt_3_5 = ChatGPT_3_5()
gemini_1_5_pro = Gemini_1_5_Pro()
gemini_1_pro = Gemini_1_Pro()
gemini_1_5_flash = Gemini_1_5_Flash()


# # Function to validate email address
# def validateEmail(emailId):
#     try:
#         validate_email(emailId)
#         return True
#     except:
#         return False


# # Function to send an email
# def sendInstantEmail(recipient_email, subject, body):
#     gmail = GoogleGmailManager()
#     return gmail.sendEmail(recipient_email, subject, body)


# # Function to create a draft email
# def createDraftEmail(subject, body, recipient_email=None):
#     gmail = GoogleGmailManager()
#     if recipient_email != None:
#         return gmail.createDraft(
#             body=body, recipient_email=recipient_email, subject=subject
#         )
#     else:
#         return gmail.createDraft(body=body, subject=subject)


# # Function to decode the email body and subject from the raw email text
# def decodeEmail(text):
#     lines = text.split("\n")
#     subject_index = next(
#         (i for i, line in enumerate(lines) if "Subject:" in line), None
#     )
#     body = "\n".join(lines[subject_index + 2 :]) if subject_index is not None else text
#     subject = next(
#         (line.replace("Subject: ", "") for line in lines if "Subject" in line), None
#     )
#     return body, subject


# # Function to get the ordinal suffix for a day number (e.g., 1st, 2nd, 3rd, 4th)
# def getOrdinalSuffix(
#     day,
# ):  # This function helps determine the ordinal suffix for a day number.
#     if 4 <= day % 100 <= 20:
#         suffix = "th"
#     else:
#         suffix = ("st", "nd", "rd")[day % 10 if day % 10 < 4 else 0]
#     return suffix


# # Function to format the date and time from a timestamp
# def formatDatetime(timestamp: str):
#     timestamp = timestamp[:16]
#     if "T" not in timestamp:
#         parsed_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d")
#         formatted_time = "whole day"

#     elif "T" in timestamp:
#         parsed_date = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
#         formatted_time = parsed_date.strftime(
#             "%I:%M %p"
#         )  # %I for 12-hour format, %p for AM/PM
#         timestamp = timestamp.split("T")[0]
#         parsed_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

#     try:
#         # Get the day, month name, and day name
#         day = parsed_date.day
#         day_with_suffix = f"{day}{getOrdinalSuffix(day)}"
#         month_name = parsed_date.strftime("%b")
#         day_name = parsed_date.strftime("%A")  # Full day name (Monday, Tuesday, etc.)

#         # Format the date with all desired components
#         formatted_date = (
#             f"{day_name}, {month_name} {day_with_suffix}, {parsed_date.year}"
#         )

#     except:
#         formatted_date, formatted_time = "...", "..."
#     return formatted_date, formatted_time


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
        # chatHistory.append(AIMessage(content=ai_response))
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


@cache
def giveAiResponseArray(AiModel, query):
    chatHistory.append(HumanMessage(content=query))
    ai_response = AiModel.classifyTaskCategory(query)

    if not ai_response["error_occurred"]:
        #
        #
        if ai_response["category"] == "compose complaint email":
            response = createResponse(AiModel, query, "complaint email", "email")

        elif ai_response["category"] == "compose formal request email":
            response = createResponse(AiModel, query, "formal request email", "email")

        elif ai_response["category"] == "compose inquiry email":
            response = createResponse(AiModel, query, "inquiry email", "email")

        elif ai_response["category"] == "compose formal proposal or suggestion email":
            response = createResponse(
                AiModel, query, "formal proposal or suggestion email", "email"
            )

        elif ai_response["category"] == "compose acknowledgment email":
            response = createResponse(AiModel, query, "acknowledgment email", "email")

        elif ai_response["category"] == "compose informal email":
            response = createResponse(AiModel, query, "informal email", "email")

        # elif "show calendar" in ai_response:
        # calendar = GoogleCalendarManager()
        # amount = 10
        # if "amount: " in ai_response:
        #     amount = int(ai_response.split("amount: ", 1)[1].split(")", 1)[0])
        # event_list = calendar.upcomingEvent(amount)
        # if event_list:
        #     events = []
        #     for item in event_list:
        #         events.append({"title": item[2],
        #                      "start": item[1],
        #                      "end": item[1],
        #                      "type": "event"})
        #     response = ["schedule", events]
        # else:
        #     events = "Unfortunately, the event you are searching for does not appear to be exist"
        #     response = ["no schedule", events]
        # chatHistory.append(AIMessage(content=str(events)))

        # elif "today's events" in ai_response:
        # calendar = GoogleCalendarManager()
        # event_list = calendar.todaysEvent()
        # if event_list:
        #     events = []
        #     for item in event_list:
        #         events.append({"title": item[2],
        #                      "start": item[1],
        #                      "end": item[1],
        #                      "type": "event"})
        #     response = ["schedule", events]
        # else:
        #     events = "Unfortunately, the event you are searching for does not appear to be exist"
        #     response = ["no schedule", events]
        # chatHistory.append(AIMessage(content=str(events)))

        # elif "contact" in ai_response:
        # name = ai_model.findName(query)
        # contact = GoogleContactManager()
        # contact_info = contact.phoneNumber(name)
        # if contact_info:
        #     text = "Sure, here is your contact: \n\n" + "\n".join(
        #         f"{item[0]} : {item[1]}" for item in contact_info
        #     )
        # else:
        #     text = "I am unable to locate any contact number you are searching for in Google Contact"
        # response = ["contact", text]
        # chatHistory.append(AIMessage(content="I have shown contact on screen"))

        # elif "task todo" in ai_response:
        # task = GoogleTaskManager()
        # task_list = task.dueTask()
        # if task_list:
        #     tasks = []
        #     for item in task_list:
        #         tasks.append({"title": item[0],
        #                      "start": item[1],
        #                      "end": item[1],
        #                      "type": "task"})
        #     response = ["schedule", tasks]
        # else:
        #     tasks = "Unfortunately, the event you are searching for does not appear to be exist"
        #     response = ["no schedule", tasks]
        # chatHistory.append(AIMessage(content=str(tasks)))

        # elif "complete schedule" in ai_response:
        #     text = "Sorry, this feature is still not available, waiting for the next update"
        #     response = ["calendar all", text]
        #     chatHistory.append(AIMessage(content=text))

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

    # elif request["request_type"] == "send-email":
    #     if validateEmail(request["recipient_email"]):
    #         response = sendInstantEmail(
    #             recipient_email=request["recipient_email"],
    #             subject=request["email_subject"],
    #             body=request["email_body"],
    #         )
    #     else:
    #         response = {
    #             "error_occurred": True,
    #             "response": False,
    #             "error": "Invalid email id",
    #         }

    # elif request["request_type"] == "create-draft" and request["have_recipient_email"]:
    #     if validateEmail(request["recipient_email"]):
    #         response = createDraftEmail(
    #             recipient_email=request["recipient_email"],
    #             subject=["email_subject"],
    #             body=request["email_body"],
    #         )

    #     else:
    #         response = {
    #             "error_occurred": True,
    #             "response": False,
    #             "error": "Invalid email id",
    #         }

    # elif (
    #     request["request_type"] == "create-draft"
    #     and request["have_recipient_email"] == "no"
    # ):
    #     response = createDraftEmail(
    #         subject=request["email_subject"], body=request["email_body"]
    #     )

    else:
        response = {
            "error_occurred": True,
            "response": None,
            "error": "Got unknown 'request-type'",
        }

    return response


app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on("message")
def handle_message(requestData):
    serverResponse = processClientRequest(dict(requestData))
    socketio.emit("message-reply", serverResponse)


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True, debug=False)
