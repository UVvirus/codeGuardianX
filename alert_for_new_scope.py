import requests
import os
import find_secrets_from_source_code as source_code_secrets
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import notification_sender

load_dotenv(find_dotenv())
db_url = os.getenv('DB_URL')

mongo_client = MongoClient(db_url)
dbname = mongo_client['bounty_targets']
collection_name = dbname['sensitive_information']


def mongo_db(timestamp: str):
    collection_name.insert_one({"timestamp":timestamp})


def check_for_new_commit(json_response):
    # latest commit url
    #print(json_response['message'])
    commit_url = json_response[0]["url"]
    print(commit_url)
    open_commit_url = requests.get(commit_url)
    result_of_commit_url = open_commit_url.json()
    latest_commit_timestamp = result_of_commit_url['commit']['author']['date']

    item_details = collection_name.find()
    for item in item_details:
        # This does not give a very readable output
        print("item:",item)
        timestamp_in_db=item['timestamp']

        if timestamp_in_db == latest_commit_timestamp:
            # print("success!!!")
            # notification_sender.webhook2("success")
            return 0
        else:
            mongo_db(latest_commit_timestamp)
            parsing_commits(json_response)


def commit_history():
    access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
    owner = "arkadiyt"
    repo = "bounty-targets-data"
    api = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(api, headers)
    json_response = response.json()
    # parsing_commits(json_response)
    # print(json_response)
    check_for_new_commit(json_response)


def parsing_commits(json_response):
    global list_of_urls
    filtered_urls = []
    try:

        # latest commit
        commit_url = json_response[0]["url"]

        commit_response = requests.get(commit_url)
        json_commit = commit_response.json()
        for i in range(len(json_commit["files"])):
            filename = json_commit["files"][i]["filename"]
            if filename == "data/domains.txt":
                patch = json_commit["files"][i]["patch"]
                list_of_urls = patch.split("\n")

        print(list_of_urls)

        for url in list_of_urls:
            if "+" in url:
                split_url = url.replace("+", "")
                # print(split_url)
                filtered_urls.append(split_url)

        source_code_secrets.getting_response(filtered_urls)

    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    commit_history()
