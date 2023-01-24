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

    group1_tmp = random.sample(set(members), k=group1_num)
    remains = set(members) ^ set(group1_tmp)
    group2_tmp = random.sample(set(remains), k=group2_num)

    group1 = [group1_mc] + group1_tmp
    group2 = [group2_mc] + group2_tmp

    group1_m = ",\n".join(group1)
    group2_m = ",\n".join(group2)

    with open('topics.txt') as f:
        topics_tmp = f.read()
    all_topics = topics_tmp.split("\n")
    topics = random.sample(set(all_topics), k=5)
    topics_m =  "\n*".join(topics)
    topics_m =  "*" + topics_m


    print(group1_m)
    print(group2_m)
    print(topics_m)

    attachments = [
        {
            # "fallback":"fallback",
            # "pretext":"",
            "color": "#06a790",
            "fields": [{"title": "グループ1", "value": group1_m}],
        },
        {
            # "fallback":"fallback",
            # "pretext":"",
            "color": "#fdea8f",
            "fields": [{"title": "グループ2", "value": group2_m}],
        },{
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "本日のトークテーマです！参考にしてください。\n```"+topics_m+"```"
                    }
                }
            ]
        }
    ]
    message = "本日のグループは、以下の通りです。"
    send_message_to_slack(message, attachments)




if __name__ == "__main__":
    main()
