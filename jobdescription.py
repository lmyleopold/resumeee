from docx import Document
import re
import json

def convert(word_file):
    # 打开 Word 文档
    job_data = []
    doc = Document(word_file)
    # 提取文本内容
    # text_content = []
    content = ''
    for paragraph in doc.paragraphs:
        content += paragraph.text + ('\n')
        # text_content.append(paragraph.text)

    title_pattern = r"(?<=\d、)([^\n]+)(?=\n岗位职责)"
    title_matches = re.findall(title_pattern, content, re.DOTALL)
    for i in range(len(title_matches)):
        job_info = {}

        # 设置岗位名称
        job_info['岗位名称'] = title_matches[i]

        print(i+1,"岗位名称：",title_matches[i])
        # job_description_pattern = r"(?<=岗位职责：\n)(?=任职要求：)"
        # job_description_matches = re.findall(job_description_pattern, content, re.DOTALL)
        # print(job_description_matches)

        if i + 1 < len(title_matches):
            start_index = content.index(title_matches[i]) + len(title_matches[i])
            end_index = content.index(title_matches[i + 1])
            job_information = content[start_index:end_index]
            # print("-----------------------------")
            # print("岗位信息：",job_information)
            # print("-----------------------------\n")
            job_description_pattern = r"(?<=\n岗位职责：\n).*(?=\n任职要求|\n职位要求)"
            job_description_match = re.findall(job_description_pattern, job_information, re.DOTALL)
            for jddescription in job_description_match:
                job_info['岗位职责'] = jddescription
                print("岗位职责：\n",jddescription)
                # print("----end-----")
            job_requirement_pattern = r"(?<=任职要求：\n|职位要求：\n|任职要求:\n|职位要求:\n).*(?=\d、)"
            job_requirement_match = re.findall(job_requirement_pattern, job_information, re.DOTALL)
            for jrdescription in job_requirement_match:
                # education_requirement_match = re.search(r".*(\b学历\b)*.", jrdescription)
                # if education_requirement_match:
                #     print("！！学历要求：",education_requirement_match.group())
                # experience_requirement_match = re.search(r"[^.!?]*学历[^.!?\n]")
                job_info['任职要求'] = jrdescription
                print("任职要求：\n",jrdescription)
                print("----end-----\n")


        else:
            start_index = content.index(title_matches[i]) + len(title_matches[i])
            job_information = content[start_index:]
            # print("-----------------------------")
            # print("岗位信息：",job_information)
            # print("-----------------------------\n")
            job_description_pattern = r"(?<=岗位职责：\n).*(?=任职要求：|职位要求：|任职要求:|职位要求:)"
            job_description_match = re.findall(job_description_pattern, job_information, re.DOTALL)
            for description in job_description_match:
                job_info['岗位职责'] = jddescription
                print("岗位职责：\n", description)
            job_requirement_pattern = r"(?<=任职要求：\n|职位要求：\n|任职要求:\n|职位要求:\n).*(?=\d、)"
            job_requirement_match = re.findall(job_requirement_pattern, job_information, re.DOTALL)
            for jrdescription in job_requirement_match:
                job_info['任职要求'] = jrdescription
                print("任职要求：\n", jrdescription)
                print("----end-----\n")
        job_data.append(job_info)

    json_data = json.dumps(job_data, ensure_ascii=False)

    # 将 JSON 字符串保存到文件
    with open('./data/job_data.json', 'w', encoding='utf-8') as file:
        file.write(json_data)

# Word 文件路径
word_file = "./data/岗位要求.docx"


# 调用函数进行转换
convert(word_file)

