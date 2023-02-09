import os

chat_language = os.getenv("INIT_LANGUAGE", default = "en")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default = 20))
LANGUAGE_TABLE = {
  "en": "Hi!"
}

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.msg_list.append(f"AI:{LANGUAGE_TABLE[chat_language]}")
    
    def add_msg(self, new_msg):
        self.msg_list.append(new_msg)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
