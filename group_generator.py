import os
import random
import urllib.request
import json


def send_message_to_slack(msg, attachments):
    """
    Send a message to Slack.

    Parameters:
    msg (str): The main message to be sent to the Slack channel.
    attachments (list): The list of attachments to be included in the message.

    Returns:
    None
    """
    send_data = {
        "channel": os.environ["SLACK_CHANNEL"],
        "attachments": attachments,
        "username": "eureco time bots",
        "text": msg,
    }
    payload = "payload=" + json.dumps(send_data)
    slack_request = urllib.request.Request(
        os.environ["SLACK_HOOK_URL"], data=payload.encode("utf-8"), method="POST"
    )
    with urllib.request.urlopen(slack_request) as slack_response:
        response_body = slack_response.read().decode("utf-8")


def divide_members(num_people, num_groups):
    """
    Divide the members into the specified number of groups.

    Parameters:
    num_people (int): The number of people to be divided into groups.
    num_groups (int): The number of groups to divide the people into.

    Returns:
    A list of the number of members in each group.
    """
    base_group_size = num_people // num_groups
    group_sizes = [base_group_size] * num_groups
    remainder = num_people % num_groups
    for i in range(remainder):
        group_sizes[i] += 1
    return group_sizes


def main():
    # Load environment variables
    members = eval(os.environ["MEMBERS"])
    slack_mentions = eval(os.environ["SLACK_MENTIONS"])
    num_groups = int(os.environ["NUM_DIVISIONS"])
    group_names = eval(os.environ["GROUP_NAMES"])

    # Divide members into groups
    group_sizes = divide_members(len(members), num_groups)
    groups = []
    for group_size in group_sizes:
        group = random.sample(members, k=group_size)
        groups.append(group)
        members = [member for member in members if member not in group]

    # Prepare message attachments for Slack
    attachments = []
    for i, group in enumerate(groups):
        attachments.append({
            "color": "#06a790",
            "fields": [{"title": group_names[i], "value": ",\n".join(group)}],
        })

    # Prepare message body for Slack
    with open('topics.txt') as f:
        all_topics = f.read().split("\n")
    topics = random.sample(all_topics, k=5)
    topics_message = "*\n".join(topics)

    message = f"<{'> <'.join(slack_mentions)}> \n本日は、Coffee Chatの日です。\nグループは、以下の通りです。"
    # Append topic message to attachments
    attachments.append({
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"本日のトークテーマです！（ご参考までに）\n```{topics_message}```"
                }
            }
        ]
    })

    # Send message to Slack
    send_message_to_slack(message, attachments)

if __name__ == "__main__":
    main()