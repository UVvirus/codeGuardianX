import os
import tldextract
import requests
import re
from bs4 import BeautifulSoup
import json
import find_secrets_from_source_code

API_KEY = os.environ.get("API_KEY")


def _cli(hostname: str, filename: str):
    try:
        os.mkdir(filename)
        os.chdir(filename)
        run_cmd = os.environ.get("RUN_CMD")
        print(run_cmd)
        os.system(run_cmd)
        parse_cmd = os.environ.get("PARSE_CMD")
        os.system(parse_cmd)
        getting_response(filename)

    except Exception as e:
        # print(e)
        init_cmd(hostname, filename)

#START
def init_cmd(hostname: str, filename: str):
    _init_cmd = os.environ.get("INIT_CMD")
    os.system(_init_cmd)
    _cli(hostname, filename)


def getting_response(filename: str):
    list_of_domains = parsing_list_of_domain_names(filename)

    for domain in list_of_domains:
        if "http://" or "https://" not in domain:
            # domain = "https://stg.rds.9c9media.ca"  # + domain
            filename = domain.replace('.', '_').replace("/", "_")
            domain = "https://" + domain

            try:
                response = requests.get(url=domain, timeout=5)
                if response.status_code == 200:
                    print("working:", domain)
                    page_source = response.text
                    save_scraped_results_in_a_file(filename, page_source)
                    find_secrets_from_source_code.regex_method(filename)
            except Exception as error:
                print(error)
                pass

def parsing_list_of_domain_names(filename: str):
    with open(f"{filename}.json", 'r') as file:
        # with open("test.json", 'r') as file:
        readed_file = file.read()
        replacing_semicolon = readed_file.replace(";", "\n")
        list_of_domain_names = replacing_semicolon.split("\n")
        print(list_of_domain_names)
    file.close()
    return list_of_domain_names

def save_scraped_results_in_a_file(hostname: str, page_source):
    with open(hostname, "w") as file:
        file.writelines(page_source)
    file.close()



if __name__ == "__main__":
     # name_of_the_file=extract_domainName("xittel.net")
     # _cli("xittel.net", name_of_the_file)
     _cli("xittel.net", "xittel.net")
    # parsing_logic("test")
    # extract_domainName("epic.ca")
    # getting_response("epic.ca")
    # ripgrep()
    # domain_and_suffix("epic.ca")
    # ripgrep("xittel")
    #other_regex("epic")
