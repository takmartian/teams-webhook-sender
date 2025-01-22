import requests
import json


class TeamsWebhook():
    def __init__(self, webhook_url: str):
        """
        Initialize the TeamsWebhook object
        :param webhook_url: Webhook URL
        """
        self.webhook_url = webhook_url

    def send_teams_card(self, data: dict) -> dict:
        """
        Send Card Teams Channel
        :param data: Card data
        :return: Response
        """
        headers = {
            "Content-Type": "application/json"
        }

        title = data.get("title")
        description = data.get("description")
        table = data.get("table")
        at_list = data.get("at_list")
        buttons = data.get("buttons")

        # initialize the body of the message
        body = []

        # initialize the title of the message
        if not title:
            return {"code": 4001, "error": "title is required"}
        elif type(title) != str:
            return {"code": 4002, "error": "title must be a string"}
        else:
            title_code = {
                "type": "TextBlock",
                "size": "Large",
                "weight": "Bolder",
                "text": title,
                "style": "heading"
            }
            body.append(title_code)

        # initialize the description of the message
        if description and type(description) != str:
            return {"code": 4003, "error": "description must be a string"}
        elif description:
            description_code = {
                "type": "TextBlock",
                "text": description,
                "horizontalAlignment": "Left",
            }
            body.append(description_code)

        # initialize the table of the message
        if table:
            facts = []
            for key in table:
                fact = {
                        "title": str(key),
                        "value": str(table[key])
                    }
                facts.append(fact)
            fact_set = {
                "type": "FactSet",
                "facts": facts
            }
            body.append(fact_set)

        # initialize the @ list of the message
        mention_list = []
        if at_list:
            new_name_list = []
            for name in at_list:
                new_name = "<at>" + name + "</at>"
                new_name_list.append(new_name)
            name_list_str = ", ".join(new_name_list)

            # add the @ list to the message content
            at_code  = {
                "type": "TextBlock",
                "text": name_list_str,
                "horizontalAlignment": "Left",
                "spacing": "ExtraLarge"
            }
            body.append(at_code)

            # bind the username and ID of @ to the message
            for name in at_list:
                mention = {
                    "type": "mention",
                    "text": "<at>" + name + "</at>",
                    "mentioned": {
                        "id": at_list[name],
                        "name": name
                    }
                }
                mention_list.append(mention)

        # initialize the buttons of the message
        actions = []
        if buttons:
            for key in buttons:
                action_code = {
                    "type": "Action.OpenUrl",
                    "title": key,
                    "url": buttons[key],
                }
                actions.append(action_code)

        # initialize the message data
        data = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "body": body,
                        "msteams": {
                            "width": "Full",
                            "entities": mention_list
                        },
                        "actions": actions,
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                    }
                }
            ]
        }
        # send the message
        response = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))

        # return the response
        if response.status_code == 200:
            return {"code": 200, "message": "Message sent successfully"}
        else:
            return {"code": response.status_code, "error": response.text}


if __name__ == '__main__':
    webhook_url = "teams webhook url"
    teams_webhook = TeamsWebhook(webhook_url)
    data = {
        "title": "this is a title",
        "description": "this is a description",
        "table": {
            "title1": "value1",
            "title2": "value2",
        },
        "at_list": {
            "@name": "@id(email)"
        },
        "buttons": {
            "button text": "https://www.example.com"
        }
    }
    result = teams_webhook.send_teams_card(data)
    print(result)
