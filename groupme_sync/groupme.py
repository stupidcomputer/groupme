from dataclasses import dataclass
from typing import ClassVar, Any
from urllib.parse import urlencode
from time import sleep

from requests import get

@dataclass
class GroupMe:
    """
    The class implementing a GroupMe api client.

    A very thin wrapper at best
    """

    http_api_url: ClassVar[str] = "https://api.groupme.com/v3"
    api_token: str
    latest_message_ids = {}
    iteration_to_return = []

    def _get(self, url: str, params: dict[str, str] = {}):
        token_qs = {"token": self.api_token}
        params = {**token_qs, **params} # combine the dicts

        url = "{}{}?{}".format(self.http_api_url, url, urlencode(params))

        print(url)

        return get(url)

    def _update_latest(self, group_id: str, request: list) -> None:
        """
        Update the latest messages dictionary with a list of JSON-encoded
        message objects. It's the stuff you get from the /groups/{}/messages
        endpoint.
        """

        try:
            messages = request["messages"]
        except KeyError:
            return

        latest_message = 0
        latest_message_id = None
        for message in messages:
            created_at = int(message["created_at"])

            if created_at > latest_message:
                latest_message = created_at
                latest_message_id = message["id"]

        if latest_message_id:
            self.latest_message_ids[group_id] = latest_message_id

    @property
    def groups(self):
        r = self._get("/groups")
        return r.json()["response"]

    @property
    def chats(self):
        r = self._get("/chats")
        return r.json()["response"]

    @property
    def grouplikes(self):
        return self.groups + self.chats

    def get_messages_from_group(self, group_id: str):
        r = self._get("/groups/{}/messages".format(group_id))
        r = r.json()["response"]

        self._update_latest(group_id, r)
        return r

    def get_messages_from_group_after_message_id(self, group_id: str, message_id: str):
        if not message_id:
            return self.get_messages_from_group(group_id)

        r = self._get("/groups/{}/messages".format(group_id), {"since_id": message_id})
        if r.status_code == 304: # none updated yet
            return {
                "messages": []
            }
        r = r.json()["response"]

        self._update_latest(group_id, r)
        return r

    def get_new_messages_from_group(self, group_id: str):
        return self.get_messages_from_group_after_message_id(
            group_id,
            self.latest_message_ids[group_id]
        )
    
    def get_all_new_messages(self):
        messages = []
        for i in self.groups:
            try:
                last_message_id = self.latest_message_ids[i["id"]]
            except KeyError:
                last_message_id = None

            messages_to_append = self.get_messages_from_group_after_message_id(i["id"], last_message_id)["messages"]
            for index, message in enumerate(messages_to_append):
                messages_to_append[index]["group_name"] = i["name"]

            messages += messages_to_append

        return messages

    def __iter__(self): # iterate to get new messages
        for group in self.groups:
            # we don't want to return past messages
            self.get_messages_from_group(group["id"])

        return self

    def __next__(self):
        # check if there's any messages on the stack
        if self.iteration_to_return:
            return self.iteration_to_return.pop()

        # else scan for new messages
        new = []
        while not new:
            sleep(10)
            new = self.get_all_new_messages()

        self.iteration_to_return = new
        return self.iteration_to_return.pop()