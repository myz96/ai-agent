import json

from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from functions import extract_profile_information, retrieve_relevant_value_prop, retrieve_email_thread_content, get_email_thread_id, compose_outreach_email
from functions_static import extract_profile_information_static, retrieve_relevant_value_prop_static, retrieve_email_thread_content_static, get_email_thread_id_static, compose_outreach_email_static

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, client=OpenAI(), model="gpt-3.5-turbo-0613"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=0,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def execute_function_call(message):
    function = message.tool_calls[0].function
    function_arguments = json.loads(function.arguments)
    if function.name == "extract_profile_information":
        return extract_profile_information(function_arguments["name"])
    elif function.name == "get_email_thread_id":
        profileinfojson = function_arguments["extract_profile_information"]
        return get_email_thread_id(json.loads(profileinfojson))
    elif function.name == "retrieve_relevant_value_prop":
        profileinfojson = function_arguments["extract_profile_information"]
        # We reparse the JSON to get the dictionary since the OpenAI API response returns the value as a string
        return retrieve_relevant_value_prop(json.loads(profileinfojson))
    elif function.name == "retrieve_email_thread_content":
        return retrieve_email_thread_content(function_arguments["get_email_thread_id"])
    elif function.name == "compose_outreach_email":
        profileinfojson = function_arguments["extract_profile_information"]
        relevant_value_prop = function_arguments["retrieve_relevant_value_prop"]
        email_thread_id = function_arguments["get_email_thread_id"]
        email_thread_content = function_arguments["retrieve_email_thread_content"]
        return compose_outreach_email(json.loads(profileinfojson), relevant_value_prop, email_thread_id, email_thread_content)
    else:
        raise Exception(f"Error: function {function.name} not found.")
    
def execute_function_call_static(message):
    function = message.tool_calls[0].function
    function_arguments = json.loads(function.arguments)
    prospect_identifier = function_arguments["name"]
    if function.name == "extract_profile_information":
        return extract_profile_information_static(prospect_identifier)
    elif function.name == "get_email_thread_id":
        return get_email_thread_id_static(prospect_identifier)
    elif function.name == "retrieve_relevant_value_prop":
        # We reparse the JSON to get the dictionary since the OpenAI API response returns the value as a string
        return retrieve_relevant_value_prop_static(prospect_identifier)
    elif function.name == "retrieve_email_thread_content":
        return retrieve_email_thread_content_static(prospect_identifier)
    elif function.name == "compose_outreach_email":
        return compose_outreach_email_static(prospect_identifier)
    else:
        raise Exception(f"Error: function {function.name} not found.")