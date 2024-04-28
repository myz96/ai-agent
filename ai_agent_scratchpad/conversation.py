from termcolor import colored  

class Conversation:
    def __init__(self):
        self.conversation_history = []

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
        
    def add_function(self, function_name, content):
        message = {"role": "function", "name": function_name, "content": str(content)} 
        self.conversation_history.append(message)

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        for message in self.conversation_history:
            if message["role"] == "function":
                print(
                    colored(
                        f"{message['role']}: {message['name']}({message['content']})\n",
                        role_to_color[message["role"]],
                    )
                )
            else:
                print(
                    colored(
                        f"{message['role']}: {message['content']}\n",
                        role_to_color[message["role"]],
                    )
                )