# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
==== No Bugs in code, just some Random Unexpected FEATURES ====
┌─────────────────────────────────────────────────────────────┐
│┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐│
││Esc│!1 │@2 │#3 │$4 │%5 │^6 │&7 │*8 │(9 │)0 │_- │+= │|\ │`~ ││
│├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┤│
││ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{[ │}] │ BS  ││
│├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤│
││ Ctrl │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  ││
│├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┤│
││ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│Shift │Fn ││
│└─────┬──┴┬──┴──┬┴───┴───┴───┴───┴───┴──┬┴───┴┬──┴┬─────┴───┘│
│      │Fn │ Alt │         Space         │ Alt │Win│   HHKB   │
│      └───┴─────┴───────────────────────┴─────┴───┘          │
└─────────────────────────────────────────────────────────────┘

测试已经训练好的本地模型。

Author: pankeyu
Date: 2022/10/21
"""
import os
from typing import List

import torch
from transformers import AutoTokenizer

from model import convert_inputs, get_bool_ids_greater_than, get_span


def inference(
    model,
    tokenizer,
    device: str,
    contents: List[str], 
    prompts: List[str], 
    max_length=512, 
    prob_threshold=0.5
    ) -> List[str]:
    """
    输入 promot 和 content 列表，返回模型提取结果。    

    Args:
        contents (List[str]): 待提取文本列表, e.g. -> [
                                                    '《琅琊榜》是胡歌主演的一部电视剧。',
                                                    '《笑傲江湖》是一部金庸的著名小说。',
                                                    ...
                                                ]
        prompts (List[str]): prompt列表，用于告知模型提取内容, e.g. -> [
                                                                    '主语',
                                                                    '类型',
                                                                    ...
                                                                ]
        max_length (int): 句子最大长度，小于最大长度则padding，大于最大长度则截断。
        prob_threshold (float): sigmoid概率阈值，大于该阈值则二值化为True。

    Returns:
        List: 模型识别结果, e.g. -> [['琅琊榜'], ['电视剧']]
    """
    inputs = convert_inputs(tokenizer, prompts, contents, max_length=max_length)
    model_inputs = {
        'input_ids': inputs['input_ids'].to(device),
        'token_type_ids': inputs['token_type_ids'].to(device),
        'attention_mask': inputs['attention_mask'].to(device),
    }
    output_sp, output_ep = model(**model_inputs)
    output_sp, output_ep = output_sp.detach().cpu().tolist(), output_ep.detach().cpu().tolist()
    start_ids_list = get_bool_ids_greater_than(output_sp, prob_threshold)
    end_ids_list = get_bool_ids_greater_than(output_ep, prob_threshold)

    res = []                                                    # decode模型输出，将token id转换为span text
    offset_mapping = inputs['offset_mapping'].tolist()
    for start_ids, end_ids, prompt, content, offset_map in zip(start_ids_list, 
                                                            end_ids_list,
                                                            prompts,
                                                            contents,
                                                            offset_mapping):
        span_set = get_span(start_ids, end_ids)                 # e.g. {(5, 7), (9, 10)}
        current_span_list = []
        for span in span_set:
            if span[0] < len(prompt) + 2:                       # 若答案出现在promot区域，过滤
                continue
            span_text = ''                                      # 答案span
            input_content = prompt + content                    # 对齐token_ids
            for s in range(span[0], span[1] + 1):               # 将 offset map 里 token 对应的文本切回来
                span_text += input_content[offset_map[s][0]: offset_map[s][1]]
            current_span_list.append(span_text)
        res.append(current_span_list)
    return res


def event_extract_example(
    model,
    tokenizer,
    device: str,
    sentence: str, 
    schema: dict, 
    prob_threshold=0.6,
    max_seq_len=384,
    ) -> dict:
    """
    UIE事件抽取示例。

    Args:
        sentence (str): 待抽取句子, e.g. -> '5月17号晚上10点35分加班打车回家，36块五。'
        schema (dict): 事件定义字典, e.g. -> {
                                            '加班触发词': ['时间','地点'],
                                            '出行触发词': ['时间', '出发地', '目的地', '花费']
                                        }
        prob_threshold (float, optional): 置信度阈值（0~1），置信度越高则召回结果越少，越准确。
    
    Returns:
        dict -> {
                '触发词1': {},
                '触发词2': {
                    '事件属性1': [属性值1, 属性值2, ...],
                    '事件属性2': [属性值1, 属性值2, ...],
                    '事件属性3': [属性值1, 属性值2, ...],
                    ...
                }
            }
    """
    rsp = {}
    trigger_prompts = list(schema.keys())

    for trigger_prompt in trigger_prompts:
        rsp[trigger_prompt] = {}
        triggers = inference(
            model,
            tokenizer,
            device,
            [sentence], 
            [trigger_prompt], 
            max_length=128, 
            prob_threshold=prob_threshold)[0]
        
        for trigger in triggers:
            if trigger:
                arguments = schema.get(trigger_prompt)
                contents = [sentence] * len(arguments)
                prompts = [f"{trigger}的{a}" for a in arguments]
                res = inference(
                    model,
                    tokenizer,
                    device,
                    contents, 
                    prompts,
                    max_length=max_seq_len, 
                    prob_threshold=prob_threshold)
                for a, r in zip(arguments, res):
                    rsp[trigger_prompt][a] = r
    return rsp


def information_extract_example(
    model,
    tokenizer,
    device: str,
    sentence: str, 
    schema: dict, 
    prob_threshold=0.6, 
    max_seq_len=512
    ) -> dict:
    """
    UIE信息抽取示例。

    Args:
        sentence (str): 待抽取句子, e.g. -> '麻雀是几级保护动物？国家二级保护动物'
        schema (dict): 事件定义字典, e.g. -> {
                                            '主语': ['保护等级']
                                        }
        prob_threshold (float, optional): 置信度阈值（0~1），置信度越高则召回结果越少，越准确。
    
    Returns:
        dict -> {
                '麻雀': {
                        '保护等级': ['国家二级']
                    },
                ...
            }
    """
    rsp = {}
    subject_prompts = list(schema.keys())

    for subject_prompt in subject_prompts:
        subjects = inference(
            model,
            tokenizer,
            device,
            [sentence], 
            [subject_prompt], 
            max_length=512, 
            prob_threshold=prob_threshold)[0]
        
        for subject in subjects:
            if subject:
                rsp[subject] = {}
                predicates = schema.get(subject_prompt)
                contents = [sentence] * len(predicates)
                prompts = [f"{subject}的{p}" for p in predicates]
                res = inference(
                    model,
                    tokenizer,
                    device,
                    contents, 
                    prompts,
                    max_length=max_seq_len, 
                    prob_threshold=prob_threshold
                )
                for p, r in zip(predicates, res):
                    rsp[subject][p] = r
    return rsp
    

def ner_example(
    model,
    tokenizer,
    device: str,
    sentence: str, 
    schema: list, 
    prob_threshold=0.6
    ) -> dict:
    """
    UIE做NER任务示例。

    Args:
        sentence (str): 待抽取句子, e.g. -> '5月17号晚上10点35分加班打车回家，36块五。'
        schema (list): 待抽取的实体列表, e.g. -> ['出发地', '目的地', '时间']
        prob_threshold (float, optional): 置信度阈值（0~1），置信度越高则召回结果越少，越准确。
    
    Returns:
        dict -> {
                实体1: [实体值1, 实体值2, 实体值3...],
                实体2: [实体值1, 实体值2, 实体值3...],
                ...
            }
    """
    rsp = {}
    sentences = [sentence] * len(schema)    #  一个prompt需要对应一个句子，所以要复制n遍句子
    res = inference(
        model,
        tokenizer,
        device,
        sentences, 
        schema, 
        max_length=512, 
        prob_threshold=prob_threshold)
    for s, r in zip(schema, res):
        rsp[s] = r
    return rsp


if __name__ == "__main__":
    from rich import print

    device = 'cuda:0'                                       # 指定GPU设备
    saved_model_path = 'model/UIE_Resume/'     # 训练模型存放地址
    tokenizer = AutoTokenizer.from_pretrained(saved_model_path) 
    model = torch.load(os.path.join(saved_model_path, 'model.pt'))
    model.to(device).eval()

    sentences = [
        ' Photos  基本信息   姓    名：刘姿婷 出生年月：1988.05   民    族：汉   性    别：女  电    话：13800138000 政治面貌：中共党员  邮    箱：liuziting@qq.com  住    址：湖北省武汉市    教育背景   2010.07-2013.06                 武汉大学                市场营销（硕士） 主修课程：管理学、微观经济学、宏观经济学、管理信息系统、统计学、会计学、财务管理、市场营销、经济法、消费者行为学、国际市场营销。  2006.07-2010.06                 武汉大学                 市场营销（本科） 主修课程：管理学、微观经济学、宏观经济学、管理信息系统、统计学、会计学、财务管理、市场营销、经济法、消费者行为学、国际市场营销。 校园实践 2007.05-2008.06                 武汉大学辩论队（队长） 负责50余人团队的日常训练、选拔及团队建设； ⚫作为负责人对接多项商业校园行活动，如《奔跑吧兄弟》大学站录制、《时代周末》校园行。 ⚫ 2008.11-2010.06                 沟通与交流协会                 创始人/副会长 协助湖北省沟通协会创立武汉大学分部，从零开始组建初期团队； ⚫策划协会会员制，选拔、培训协会导师，推出一系列沟通课程。 ⚫工作经历 2018.08-至今                     皓铭控股集团                副总监 负责协助集团旗下事业部开展各项工作，制定品牌传播方案； ⚫结合集团与事业部发展，制定营销策略、广告策略、品牌策略和公关策略，组织推进执行； ⚫制定和执行媒体投放计划，跟踪和监督媒体投放效果，进行数据分析与撰写报告； ⚫研究行业发展动态，定期进行市场调查,为产品更新提供建议。 ⚫ 2015.08-2018.08                 诺晨有限公司                 市场及运营总监 根据公司发展情况进行战略调整，配合前端销售部门搭建销售渠道； ⚫研究行业发展动态，定期进行市场调查,为产品更新提供建议； ⚫负责公司部门制度规范，负责组织及监管市场部关于对外合作、推广策划以相关工作的落实。 ⚫ 2013.08-2015.08                 恒仟俱乐部                   市场副总监 负责事业部产 品对外推广和宣传，制定各种整合营销的活动； ⚫执行媒体投放计划，跟踪和监督媒体投放效果，进行数据分析撰写报告； ⚫向市场总监提供营销支 持，并协助相关的公关事宜。 ⚫ 项目经历   诺晨集团品牌升级发布会  集团全新品牌logo及VI上线，在多渠道进行了传播； ⚫ 企业VIP客户群体逾60人，结合了线上发布、线下体验； ⚫ 后续媒体报道持续升温，子品牌结合明星代言人制造话题营销，为期3周。  ⚫  恒仟商业模式发布会  整场活 动以会议+洽谈双重模式进行，首日以介绍恒仟内部平台资源优势，政府背景优势等为主，一对多推介会 ⚫进行推广普及； 现场签署地方合作意向书，如：新疆、江西、浙江等优秀企业商户； ⚫以中国的波尔多为宣传点，主推旗下新疆大型项目，制造营销、品牌热点。 ⚫ 皓铭投资控股集团6A自媒体生态圈建设 本项目重构了公司现有微信企业号的功能与架构； ⚫提高公众号的关注粉丝量的同时，对于有客户进行统一宣传，统一管理。 ⚫奖项荣誉 2013年  新长城武汉大学自强社“优秀社员” 2012年  三下乡”社会实践活动“优秀学生” 2011年  武汉大学学生田径运动会10人立定跳远团体赛第三名 2010年  学生军事技能训练“优秀学员” 2009年  武汉大学盼盼杯烘焙食品创意大赛优秀奖 2008年  西部高校大学生主题征文一等奖 2007年  武汉大学“点燃川大梦 畅享我青春”微博文征集大赛二等奖  技能证书 普通话一级甲等 通过全国计算机二级考试，熟练运用office相关软件。 熟练使用绘声绘 色软件，剪辑过各种类型的电影及班级视频。 大学英语四/六级（CET-4/6），良好听说读写能力，快速浏览英语专业书籍。 兴趣爱好 阅读 / 旅行 / 跑步 / 羽毛球 / 爬山 / 烹饪 自我评价 拥有多年的市场管理及品牌营销经验，卓越的规划、组织、策划、方案执行和团队领导能力，积累较强的人际关系处理能力和商务谈判技巧，善于沟通，具备良好的合作关系掌控能力与市场开拓能力；敏感的商业和市场意识，具备优秀的资源整合能力、业务推 进能力； 思维敏捷，有培训演讲能力，懂激励艺术，能带动团队的积极性；擅长协调平衡团队成员的竞争与合作的关系，善于通过培训提高团队综合能力和凝聚力。'
    ]
    
    # NER 示例
    for sentence in sentences:
        rsp = ner_example(
            model,
            tokenizer,
            device,
            sentence=sentence, 
            schema=['人物', '教育背景触发词', '工作经历触发词', '日期']
        )
        print('[+] NER Results: ', rsp)

    # SPO抽取示例
    for sentence in sentences:
        rsp = information_extract_example(
            model,
            tokenizer,
            device,
            sentence=sentence, 
            schema={
                    '人物': ['性别', '出生年月', '年龄', '就业意向','民族', ' 电话', '政治面貌', '邮箱', '住址'],
                }
        )
        print('[+] Information-Extraction Results: ', rsp)

    for sentence in sentences:
        rsp = event_extract_example(
            model,
            tokenizer,
            device,
            sentence=sentence, 
            schema={
                    '教育背景触发词': ['学校', '阶段', '专业', '主修课程', '时间'],
                    '工作经历触发词': ['公司', '职位', '工作内容', '时间']
                }
        )
        print('[+] Event-Extraction Results: ', rsp)