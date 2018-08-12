import re

from errbot import BotPlugin, re_botcmd
from errbot import Message

# errbot doesn't let you pass in a pre-compiled regex AFAICT. So we do it twice,
# I guess
pattern = re.compile(
    r"""
w+h+a+t*[.!?\s]*$|
w+a+t+[.!?\s]*$|
wot[.!?\s]*$|
h+u+h+[.!?\s]*$|
w+h+a+t+\ n+o+w+[.!?\s]*$|
repeat+\ that+[.!?\s]*$|
come+\ again+[.!?\s]*$|
wha+t+\ do+\ (yo+u+|u+)\ mean+|
w+h+a+t+\ (.+)?did+\ (you+|u+)\ (just\ )?sa+y+|
i+\ ca+n'?t+\ h+e+a+r+(\ (you+|u+))?|
i'?m\ hard\ of\ hearing
""",
    re.VERBOSE | re.MULTILINE |re.IGNORECASE
)


class Yell(BotPlugin):
    """
    Plugin that yells at people when they can't hear. Built for the Slack
    integration.
    """

    @re_botcmd(
        pattern=r"""
            w+h+a+t*[.!?\s]*$|
            w+a+t+[.!?\s]*$|
            wot[.!?\s]*$|
            h+u+h+[.!?\s]*$|
            w+h+a+t+\ n+o+w+[.!?\s]*$|
            repeat+\ that+[.!?\s]*$|
            come+\ again+[.!?\s]*$|
            wha+t+\ do+\ (yo+u+|u+)\ mean+|
            w+h+a+t+\ (.+)?did+\ (you+|u+)\ (just\ )?sa+y+|
            i+\ ca+n'?t+\ h+e+a+r+(\ (you+|u+))?|
            i'?m\ hard\ of\ hearing
        """,
        prefixed=False,
        flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE
    )
    def yell(self, msg, args):
        """Everyone's a little bit hard of hearing sometimes."""
        if msg.frm.room.name in self.previous_message_dict:
            previous_message = self.previous_message_dict[msg.frm.room.name]
        else:
            return (
                "I KNOW YOU'RE HAVING TROUBLE BUT I JUST JOINED THIS ROOM! "
                "I DON'T KNOW WHAT'S GOING ON EITHER."
            )
        # noinspection PyUnresolvedReferences
        return "{}: {}".format(
            previous_message.frm.person,
            previous_message.body.upper()
        )


    def callback_message(self, message: Message):
        # back up the last message sent that doesn't match the patterns.
        # Keep a running dict based on the channel it came from.
        if not hasattr(self, 'previous_message_dict'):
            self.previous_message_dict = dict()

        if not re.match(pattern, message.body):
            self.previous_message_dict[message.frm.room.name] = message
