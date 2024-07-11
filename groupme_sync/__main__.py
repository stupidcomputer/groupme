from sys import argv

from .groupme import GroupMe

def main() -> None:
    filename = argv[1]
    with open(filename, "r") as file:
        token = file.readlines()[0].rstrip()
    
    chats = GroupMe(token)
    for message in chats:
        print(message)

main()