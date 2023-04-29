import os
import tldextract
from urllib.request import urlretrieve
import find_secrets_from_source_code
from urllib.parse import urlparse

#START
def scrap_javascript_from_webpage(url: str):
    filename = url.replace(".","_").replace("/","_")
    print("Saving into a file...")
    run_docker = os.environ.get("RUN_DOCKER")
    os.system(run_docker)
    print("Saved")
    extract_js_files(filename+".txt",filename)
    #ripgrepp("js_files")
    find_secrets_from_source_code.regex_method("js_files")


def extract_js_files(url_filelist,filename):
    try:
        path=f"js_files/{filename}/"
        isExist = os.path.exists(path)
        if isExist:
            pass
        else:
            os.makedirs(f"js_files/{filename}/")

        dirname=f"js_files/{filename}/"
        print("dirName:",dirname)
        with open(url_filelist, 'r') as file:
            list_of_urls = file.readlines()
            # print(read_file)

            for url in list_of_urls:
                #url="https://www.cinepop.ca/js/index.js"
                #default_filename = url.split("/")[-1]
                a= urlparse(url)
                default_filename=os.path.basename(a.path)
                if ".js" in default_filename:
                    print("js url:", url)
                    dst = f"{dirname}"+default_filename
                    print("dst:",dst)
                    urlretrieve(url, dst)
    except Exception as e:
        print(e)
        pass






if __name__ == "__main__":
    #scrap_javascript_from_webpage("epic.ca")
    extract_js_files("www_cinepop_ca.txt","www_cinepop_ca")
     #ripgrepp("js_files")
