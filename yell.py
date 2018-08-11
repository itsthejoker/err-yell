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
w+h+a+t+ n+o+w+[.!?\s]*$|
repeat+ that+[.!?\s]*$|
come+ again+[.!?\s]*$|
wha+t+ do+ (yo+u+|u+) mean+|
w+h+a+t+ (.+)?did+ (you+|u+) (just )?sa+y+|
i+ ca+n'?t+ h+e+a+r+( (you+|u+))?|
i'?m hard of hearing
""",
    re.VERBOSE | re.MULTILINE |re.IGNORECASE
)


class Yell(BotPlugin):
    """Plugin that yells at people when they can't hear."""

    @re_botcmd(
        pattern=r"""
            w+h+a+t*[.!?\s]*$|
            w+a+t+[.!?\s]*$|
            wot[.!?\s]*$|
            h+u+h+[.!?\s]*$|
            w+h+a+t+ n+o+w+[.!?\s]*$|
            repeat+ that+[.!?\s]*$|
            come+ again+[.!?\s]*$|
            wha+t+ do+ (yo+u+|u+) mean+|
            w+h+a+t+ (.+)?did+ (you+|u+) (just )?sa+y+|
            i+ ca+n'?t+ h+e+a+r+( (you+|u+))?|
            i'?m hard of hearing
        """,
        prefixed=False,
        flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE
    )
    def yell(self, msg, args):
        """Everyone's a little bit hard of hearing sometimes."""
        return "{}: {}".format(self.prev_message.frm, self.prev_message.body.upper())


    def callback_message(self, message: Message):
        # back up the last message sent that doesn't match the patterns.
        if not re.match(pattern, message.body):
            self.prev_message = message
