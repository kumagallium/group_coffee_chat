import random
import urllib.request
import json
import os


def send_message_to_slack(msg, attachments):
    # make slack message body
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

def main():
    members = eval(os.environ["MEMBERS"])
    group1_mc = members[0]
    group2_mc = members[1]
    members = members[2:]

    members_num = len(members)
    group1_num = int((members_num - (members_num % 2)) / 2)
    group2_num = members_num - group1_num
    all_idxs = list(range(len(members)))
    group1 = random.sample(set(all_idxs), k=group1_num)
    remain_idxs = set(all_idxs) ^ set(group1)
    group2 = random.sample(remain_idxs, k=group2_num)

    group1_name = [group1_mc]
    for g in group1:
        group1_name.append(members[g])

    group2_name = [group2_mc]
    for g in group2:
        group2_name.append(members[g])

    group1_m = ",\n".join(group1_name)

    group2_m = ",\n".join(group2_name)

    attachments = [
        {
            # "fallback":"fallback",
            # "pretext":"",
            "color": "#06a790",
            "fields": [{"title": "Group1", "value": group1_m}],
        },
        {
            # "fallback":"fallback",
            # "pretext":"",
            "color": "#fdea8f",
            "fields": [{"title": "Group2", "value": group2_m}],
        },
    ]
    message = "本日のグループは、以下の通りです。"
    send_message_to_slack(message, attachments)


if __name__ == "__main__":
    main()
