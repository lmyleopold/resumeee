import json

from job_extract import *

class Jobs(object):
    # example token: {'ner': ['token'], 'information': {'token': ['information']}, 'event': {'token': ['event']}}
    def __init__(self, path): # 初始化
        # 读取人岗描述文件
        self.path = path
        self.description = read_description(path)
        self.job_info = extract_job_info(self.description)

    # def add_job(self, name, description): # 导入单个岗位说明
    #     self.job_info[name] = description

    def export(self, path, action="job_info"): # else "description"
        with open(path, 'w', encoding='utf-8') as f:
            if action == "job_info":
                json.dump(self.job_info, f, ensure_ascii=False, indent=4)
            elif action == "description":
                json.dump(self.description, f, ensure_ascii=False, indent=4)
            else:
                return
