# Teams Webhook Sender
## Initial Teams Webhook
```python
import TeamsWebhook
```

## Create Teams Webhook

```python
webhook_url = "your teams webhook url"
teams_webhook = TeamsWebhook(webhook_url)
```

## Send Message

```python
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
```

## Error Code

| code | message                      |
|------|------------------------------|
| 200  | success                      |
| 4001 | title is required            |
| 4002 | title must be a string       |
| 4003 | description must be a string |
| ...  | ...                          |

