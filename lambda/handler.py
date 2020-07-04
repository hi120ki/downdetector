import os
import requests
import json
import dns.resolver
from slack import WebClient
from slack.errors import SlackApiError


with open("secret") as f:
    token = f.read()

client = WebClient(token=token)

def report(audit, name, item, info):
    text = (
        audit
        + " Error @ "
        + name
        + "\n> Target: "
        + item
        + "\n> Info: "
        + info
        + "\n\n"
    )
    return text


def domain(domain, ip):
    check = 0

    for _ in range(3):
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ["8.8.8.8"]
            answers = dns.resolver.query(domain, "A")
            for rdata in answers:
                if str(rdata) != ip:
                    check += 1
        except:
            check += 1

    if check != 0:
        log = report("DNS", domain, ip, "resolve error")
        return log
    else:
        return ""


def http(domain, url):
    check = 0
    status_code_log = []

    for _ in range(3):
        try:
            res = requests.get(
                url, headers={"User-Agent": "Wani Down Detector"}, timeout=2.0
            )
            status_code_log.append(res.status_code)
            if res.status_code != 200:
                check += 1
        except:
            status_code_log.append(504)
            check += 1

    if check != 0:
        log = report("HTTP", domain, url, "status_code " + str(status_code_log))
        return log
    else:
        return ""


def slack(log):
    try:
        response = client.chat_postMessage(channel="#downdetector", text=log)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


def main(event, context):
    log = ""
    with open("target.json") as f:
        data = json.load(f)

    for target in data["target"]:
        log += domain(target["domain"], target["ip"])
        for url in target["url"]:
            log += http(target["domain"], url)

    if log != "":
        slack(log)

    return 0
