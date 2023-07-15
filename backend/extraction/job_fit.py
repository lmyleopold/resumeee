import pandas as pd
from difflib import SequenceMatcher
import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine

# 加载预训练的中文BERT模型和tokenizer
model_name = 'bert-base-chinese'
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

def bert_similarity(word1, word2, model, tokenizer):
    # 对词语进行编码和分词
    input_ids = tokenizer.encode(word1, word2, add_special_tokens=True)
    input_ids = torch.tensor(input_ids).unsqueeze(0)  # 添加batch维度

    # 使用BERT模型计算词语的表示向量
    with torch.no_grad():
        outputs = model(input_ids)
        embeddings = outputs[0][0]  # 取出第一个词语的表示向量

    # 计算余弦相似度
    similarity = 1 - cosine(embeddings[0], embeddings[1])

    return similarity


def edit_distance_similarity(string1, string2):
    similarity = SequenceMatcher(None, string1, string2).ratio()
    # similarity = (similarity - 0) / (1 - 0) * (1 - 0.5) + 0.5
    return similarity

# job_info example:
# {"产品运营": {"学历要求": 0, "专业要求": "无要求", "最低工作年限": 2, "最高工作年限": 99, "年龄要求": 0}, ...}
# person_info_example:
# {"人物": "赖俊军", "年龄": 25, "工作年限": 2, "专业": "市场管理", "学历": "4", "任职意向": "市场销售相关工作岗位", "最高学历学校": "上海交通大学"}
def job_fit(job_info, person_info, topk=1):
    matchlist = []
    matchscorelist = []
    person_name = person_info['人物']
    person_qualification = int(person_info['学历'])
    person_work_year = int(person_info['工作年限'])
    person_major = person_info['专业']
    person_age = int(person_info['年龄'])
    person_target_job = person_info['任职意向']
    for job in job_info:
        job_name = job
        required_qualification = int(job_info[job]['学历要求'])
        lowest_work_year = int(job_info[job]['最低工作年限'])
        highest_work_year = int(job_info[job]['最高工作年限'])
        required_age = int(job_info[job]['年龄要求'])
        required_major = job_info[job]['专业要求']

        '''计算相似度（专业和专业要求、岗位名称和任职意向）'''

        if person_target_job is None or pd.isna(person_target_job): # 假如任职意向无内容
            job_similarity = 0.4
        else:
            # print(job_name, person_target_job)
            job_similarity_score1 = bert_similarity(job_name, person_target_job, model, tokenizer)
            job_similarity_score2 = edit_distance_similarity(job_name,person_target_job)
            job_similarity = job_similarity_score1*0.4 + job_similarity_score2*0.6
        # print('job:',person_target_job,job_name,job_similarity)
            # if job_similarity_score:
            #     job_similarity = 1

        if person_major is None or pd.isna(person_major) or required_major == '无要求': # 假如任职意向无内容
            major_similarity = 0.25
            major_similarity_score1 = 1
            major_similarity_score2 = 1
        else:
            major_similarity_score1 = bert_similarity(required_major, person_major, model, tokenizer)
            major_similarity_score2 = edit_distance_similarity(required_major, person_major)
            major_similarity = major_similarity_score1 * 0.4 + major_similarity_score2 * 0.6


        if required_qualification <= person_qualification \
            and lowest_work_year <= person_work_year <= highest_work_year \
            and required_age <= person_age \
            and job_similarity >= 0.4 \
            and major_similarity >= 0.25 :
            score = job_similarity + major_similarity
            # and major_similarity >= 0.867: # 学历、工作年限、年龄、专业
            # print(row2['编号'],row2['人物'],'match',row1['岗位名称'],score)
            matchlist.append(job)
            matchscorelist.append(score)
    combined  = list(zip(matchlist,matchscorelist))
    # 按分数进行降序排序
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)

    # 提取分数最高的两项的名称
    top_names = [item[0] for item in sorted_combined[:topk]]

    return top_names
