import os
import json
import requests
import sys
import re
import time
import datetime
from github import GITHUB_ACCESS_TOKEN
import zipfile
if GITHUB_ACCESS_TOKEN is None:
    headers=False
else:
    headers = {'Authorization': GITHUB_ACCESS_TOKEN}

"""
language:指定する言語
max_num:取ってくるレポジトリーの数(<=1000)
sort:ソートの基準 (githubのapiを参照)
download:zipファイルをダウンロードするかどうか
dir:ダウンロードするローカルディレクトリ
"""
def GetGitHubRepositories(language,max_num=100,sort="stars",download=False,dir=None):
    if headers!=False:
        print("Authorized account!")
    repos_dict={}
    page_iterator=1
    while 1:
        url="https://api.github.com/search/repositories?q=language:"+language+"&sort="+sort+"&page="+str(page_iterator)

        info=requests.get(url,headers=headers).content
        info_dict=json.loads(info)
        if "items" not in info_dict:
            if "message" in info_dict:
                print(info_dict["message"])
                if info_dict["message"]=="Validation Failed":
                    print("url is wrong.")
                    break
                if info_dict["message"]=="Only the first 1000 search results are available":
                    break
                reset_time=GetResetTimeForGithub()
                waitUntilReset(reset_time)

            else :
                print("An error occured.")
                return repos_dict
            continue
        repos=info_dict["items"]
        for r in repos:
            if len(repos_dict)>=max_num:
                break
            repos_dict[len(repos_dict)]={"name":r["name"],"url":r["html_url"],"default_branch":r["default_branch"]}
        page_iterator+=1
        if len(repos_dict)>=max_num:
            break

    if download==True:
        percentage=DownloadGithubAll(repos_dict,dir)
        print("{}% repositories were Downloaded.".format(percentage))

    return repos_dict


"""
repos_dict: 要素が[repository_name, url, default_branch]からなるリスト
dir: ダウンロードするディレクトリ,Noneならカレントディレクトリに
"""
def DownloadGithubAll(repos_dict:dict,unzip=False,dir=None):
    if len(repos_dict)==0:
        return 0
    download_count=0
    for index in repos_dict:
        if DownloadGithub(github_url=repos_dict[index]["url"], default_branch=repos_dict[index]["default_branch"], unzip=unzip, dir=dir):
            download_count+=1
            print("{} was downloaded successfully.".format(repos_dict[index]["name"]))
            continue
        print("Download failed: {}".format(repos_dict[index]["name"]))
    return download_count / len(repos_dict) * 100 #ダウンロードできた割合を返す



def DownloadGithub(github_url:str, default_branch="master",unzip=False,dir=None,filename=None)->bool:
    if github_url[-1]=='/':
        github_url=github_url[:-1]
    url=github_url+"/archive/"+default_branch+".zip"
    if filename is None:
        filename=github_url.split("/")[-1]+"-"+default_branch+".zip"
    if dir is None:
        dir="./"
    if dir[-1]!='/':
        dir+='/'
    return DownloadFile(url,dir,filename,unzip)

def DownloadFile(url,dir,filename,unzip:bool)->bool:
    r=requests.get(url,stream=True)
    with open(dir+filename, "wb") as w:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                w.write(chunk)
                w.flush()
    if unzip==True:
        with zipfile.ZipFile(dir+filename) as existing_zip:
            existing_zip.extractall(dir)
        os.remove(dir+filename)
    return True


def GetResetTimeForGithub(api_object="search"):
    url="https://api.github.com/rate_limit"
    info=requests.get(url,headers=headers).text
    info_dict=json.loads(info)
    #print(info_dict)
    return int(info_dict["resources"][api_object]["reset"])

def waitUntilReset(reset):
    '''
    reset 時刻まで sleep
    '''
    seconds = reset - time.mktime(datetime.datetime.now().timetuple())
    seconds = max(seconds, 0)
    print ('\n     =====================')
    print ('     == waiting %d sec ==' % seconds)
    print ('     =====================')
    sys.stdout.flush()
    time.sleep(seconds + 3)  # 念のため + 3 秒

