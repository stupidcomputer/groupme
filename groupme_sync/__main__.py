from sys import argv
import json

from .groupme import GroupMe
from .emailwrap import send_email

def main() -> None:
    filename = argv[1]
    with open(filename, "r") as file:
        data = json.loads(file.read())
    
    chats = GroupMe(data["token"])
    for message in chats:
        title = "[GroupMe] {} sent a message in {}".format(message["name"], message["group_name"])
        body = """
        Greetings,

        {} sent a message in group {} -- it reads as follows:

        {}

        Much regards,
        the internal beepboop.systems mail system
        """.format(
            message["name"],
            message["group_name"],
            message["text"]
        )

        send_email(
            title=title,
            body=body,
            smtp_server=data["smtp_server"],
            smtp_username=data["smtp_username"],
            smtp_password=data["smtp_password"],
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
        )
        print(message)

main()