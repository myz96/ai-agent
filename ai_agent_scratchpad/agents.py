import copy
from openai import OpenAI
import redis
from conversation import Conversation
from utils import chat_completion_request, execute_function_call, execute_function_call_static
from scratchpad import store_value_local, store_value_redis, insert_scratchpad_local, insert_scratchpad_redis, remove_tool

class BDRAgent:
    def __init__(self, tools, client=OpenAI()):
        SYSTEM_MESSAGE = """You're a world class BDR researcher who can do detailed research on any topic and produce facts-based results. \nYou work for Emily who is a account executive at EdApp. When responded to external messages reply as if you are Emily. \n\nPlease make sure you complete the objective following these rules:\n1/ For each research task, you should try to find any recent news about the prospect company, or recent posts.\n2/ When using google search, use quotation mark to wrap around the company name, e.g. \"Salesforce\", because some company name is generic, this help google return better results; \n3/ You should do enough research to gather as much information as possible about the objective. If there are URL's of relevant links & articles, you will scrape it to gather more information. After scraping & search, you should think \"are there any new things I should search & scrape based on the data I collected to increase the research quality?\" If the answer is yes: continue. But don't do this more than 3 times. Maximum iterations is 3.\n4/ You should not make things up. You should only write about facts & data that you have gathered.\n"""
        self.scratchpad = {}
        self.conversation = Conversation()
        self.tools = tools
        self.curr_tools = copy.deepcopy(tools)
        self.conversation.add_message("system", SYSTEM_MESSAGE)
        self.end_conversation = False
        self.client = client

    def respond_to_user_input(self, user_input):
        self.conversation.add_message("user", user_input)
        while not self.end_conversation:
            response = self._get_response()
            if response[0] == "function":
                self.conversation.add_function(response[1], response[2])
                self.scratchpad = store_value_local(self.scratchpad, response[1], response[2])
                self.curr_tools = remove_tool(response[1], self.curr_tools)
            else:
                self.conversation.add_message(response[0], response[1])
                self.end_conversation = True
                
    def _get_response(self):
        response = chat_completion_request(messages=self.conversation.conversation_history, tools=self.tools, client=self.client)
        message = response.choices[0].message
        if message.tool_calls:
            function = message.tool_calls[0].function
            print(f"Function generation requested, calling function {function.name}...")
            results = execute_function_call(message)
            return ("function", function.name, results)
        else:
            print(f"Function not required, responding to user")
            return ("assistant", message.content)

class LocalBDRAgent(BDRAgent):
    def __init__(self, tools, client=OpenAI(), scratchpad={}):
        super().__init__(tools, client)
        self.scratchpad = scratchpad
        
    def _get_response(self):
        response = chat_completion_request(messages=self.conversation.conversation_history, tools=self.tools, client=self.client)
        message = response.choices[0].message
        if message.tool_calls:
            # Insert scratchpad values into the function call
            function = insert_scratchpad_local(message, self.scratchpad, self.curr_tools, self.tools)
            print(f"Function generation requested, calling function {function.name}...")
            results = execute_function_call(message)
            # Store the results in the scratchpad and remove the tool from the schema
            self.scratchpad = store_value_local(self.scratchpad, function.name, results)
            self.curr_tools = remove_tool(function.name, self.curr_tools)
            return ("function", function.name, results)
        else:
            print(f"Function not required, responding to user")
            return ("assistant", message.content)
        
class RedisBDRAgent(BDRAgent):
    def __init__(self, tools, client=OpenAI(), scratchpad=redis.Redis(host='localhost', port=6379, decode_responses=True)):
        super().__init__(tools, client)
        self.scratchpad = scratchpad
        
    def _get_response(self):
        response = chat_completion_request(messages=self.conversation.conversation_history, tools=self.tools, client=self.client)
        message = response.choices[0].message
        if message.tool_calls:
            # Insert scratchpad values into the function call
            function = insert_scratchpad_redis(message, self.scratchpad, self.curr_tools, self.tools)
            print(f"Function generation requested, calling function {function.name}...")
            results = execute_function_call(message)
            # Store the results in the scratchpad and remove the tool from the schema
            self.scratchpad = store_value_redis(self.scratchpad, function.name, results)
            self.curr_tools = remove_tool(function.name, self.curr_tools)
            return ("function", function.name, results)
        else:
            print(f"Function not required, responding to user")
            return ("assistant", message.content)
        
class StaticBDRAgent(BDRAgent):
    def __init__(self, tools, client=OpenAI()):
        super().__init__(tools, client)
        
    def _get_response(self):
        response = chat_completion_request(messages=self.conversation.conversation_history, tools=self.tools, client=self.client)
        message = response.choices[0].message
        if message.tool_calls:
            function = message.tool_calls[0].function
            print(f"Function generation requested, calling function {function.name}...")
            results = execute_function_call_static(message)
            return ("function", function.name, results)
        else:
            print(f"Function not required, responding to user")
            return ("assistant", message.content)