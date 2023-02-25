import re
import tldextract
import requests
import os
import json
import subprocess
from subprocess import Popen, PIPE
import notification_sender



def getting_response(list_of_domains: list):
    # list_of_domains = ["epic.ca"]

    for domain in list_of_domains:
        if "http://" or "https://" not in domain:
            # domain = "https://stg.rds.9c9media.ca"  # + domain
            filename =domain.replace('.','_').replace("/","_")
            print("filename:",filename)
            domain = "https://" + domain

            different_file = domain_and_suffix(domain)
            try:
                response = requests.get(url=domain, timeout=5)
                if response.status_code == 200:
                    print("working:", domain)
                    page_source = response.text
                    save_scraped_results_in_a_file(filename, page_source)
                    # ripgrepp(different_file)
                    final_output=regex_method(filename)
                    notification_sender.webhook2(final_output)
            except Exception as error:
                print(error)
                pass


def save_scraped_results_in_a_file(hostname: str, page_source):
    with open(hostname, "w") as file:
        file.writelines(page_source)
    file.close()


def domain_and_suffix(hostname: str):
    tld = tldextract.extract(hostname)
    dom_and_suffix = '_'.join(tld[0:3])
    return dom_and_suffix


def regex_method(file_name: str):
    output_dict={}

    with open("regex_keys.json", "r") as json_file:
        json_data = json.loads(json_file.read())

        for key, value in json_data.items():
            # print(key,value["regex"])
            regex=value['regex']
            grep_cmd = f"rg -H -n -w  -- \"{regex}\"  {file_name}"
            # os.system(grep_cmd)
            try:
                print(key)
                #os.system(grep_cmd)
                output, error = subprocess.Popen(grep_cmd,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 shell=True
                                                 ).communicate()

                output = output.decode("utf-8").rstrip("\r\n")
                error = error.decode("utf-8")
                print("o:",output)
                #print("e:",error)
                if output=='':
                    pass
                else:
                    output_dict[key]=output
                #output_list.append(output)


            except (OSError, FileNotFoundError, subprocess.SubprocessError, subprocess.CalledProcessError) as e:
                print(e)
                pass

    #print(output_dict)
    return output_dict




if __name__ == "__main__":
    #regex_method("xittel")
     #getting_response(["bardown.com"])
    # getting_response(["stg.rds.9c9media.ca"])
    getting_response(["epic.ca/contact-us/"])
