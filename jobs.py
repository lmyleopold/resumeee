import json

class Jobs(object):
    # example token: {'ner': ['token'], 'information': {'token': ['information']}, 'event': {'token': ['event']}}
    def __init__(self, path): # 初始化
        # 读取人岗描述文件
        self.path = path
        self.job_info = {# 类似的格式
            {
                "产品运营": {
                    "岗位职责": "1.负责产品上线前后的线上、线下的运营方案和推广工作，协助项目负责人对接市场、产品开发等，完成个项目目标；\n2.负责产品运营中与线下的各种合作，配合完成商务推广，实施项目评估和监控，提升用户活跃度和忠诚度；\n3.负责研究行业竞争动态，定期拜访客户，维护重要客户关系发现客户的需求，引导客户的业务需求，根据自身产品制定产品营销策略，达成既定目标；\n4.负责分析和挖掘产品运营数据、用户行为数据等重要价值信息\n5.负责跟进和整理产品用户反馈，协同产品经理提出产品迭代方案。",
                    "任职要求": "1.2年及以上产品运营经验；\n2.主动性强，逻辑清晰，沟通能力强，能独立负责和落地运营项目能调动资源为运营目标服务；\n3.有较强数据分析能力、数据敏感性强。"
                }
            }
        }

    def add_job(self, name, description): # 导入单个岗位说明
        self.job_info[name] = description

    def export(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.job_info, f, ensure_ascii=False, indent=4)