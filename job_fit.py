from extraction.resumee import Resumee
from extraction.jobs import Jobs

# job_info example:
# {"产品运营": {"学历要求": 0, "专业要求": "无要求", "最低工作年限": 2, "最高工作年限": 99, "年龄要求": 0}, ...}
# person_info_example:
# {"人物": "赖俊军", "年龄": 25, "工作年限": 2, "专业": "市场管理", "学历": "4", "任职意向": "市场销售相关工作岗位", "最高学历学校": "上海交通大学"}

def job_fit(job_info, person_info, topk=1):
    return [] # topk