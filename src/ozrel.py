from fbchat import Client
from fbchat.models import *
import re

turn_on_off = re.compile('^!turn (on|off)')
hi = re.compile('^!hi')


class OzrelBot(Client):
    def __init__(self, configs, email, password):
        super().__init__(email, password)
        self.configs = configs

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        try:
            #
            if hi.match(message_object.text):
                self.send(Message(text='Hey you!'), thread_id=author_id, thread_type=ThreadType.USER)
            #
            turn_on_off_command = turn_on_off.match(message_object.text)
            if turn_on_off_command:
                mode = turn_on_off_command.group(1)
                config = self.configs.get(thread_id)
                if config is not None:
                    if author_id in config['admins']:
                        if mode == 'on':
                            config['quiet'] = 'False'
                        if mode == 'off':
                            config['quiet'] = 'True'
                        self.send(Message(text='{0} # quiet = {1}'.format(thread_id, config['quiet'])),
                                  thread_id=author_id,
                                  thread_type=ThreadType.USER)
        except Exception as e:
            print(e)

    def broadcast(self, message, thread_id):
        self.send(message, thread_id=thread_id, thread_type=ThreadType.GROUP)
