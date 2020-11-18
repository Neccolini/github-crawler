from main import GetGitHubRepositories, DownloadGithubAll
import json
filename="repository.json"

"""
# jsonファイルに保存
py_dict=GetGitHubRepositories("javascript",max_num=1000)
with open(filename, "w") as f:
    json.dump(py_dict,f,indent=4)
"""

# ファイルから読み込み、保存
with open(filename,"r")as f:
    repos_dict=json.loads(f.read())
    print(len(repos_dict))


"""コメントアウトを外すと1000件ダウンロードします"""

# DownloadGithubAll(repos_dict,unzip=True) 

