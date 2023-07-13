# resumeee

## 下载模型文件

模型文件保存在`model`文件夹下，可以在[huggingface](https://huggingface.co/Fsadness/UIE_Resume)仓库内下载，默认文件位置为`model\UIE_Resume`，在`resumee.py`文件内更改
huggingface仓库已上传最新训练好的模型

##必做功能
### 岗位要求提取

使用正则表达式提取岗位要求，仅支持docx

运行jobdescription.py，可以在data中生成job_data.json，其中包含岗位名称，岗位职责和任职要求

### 岗位要求分析

使用正则表达式提取岗位要求细节，输入时job_data.json

运行jobdetail.py，可以在data中生成job_detail.csv，其中包含岗位名称，专业要求，最低工作年限要求，最高工作年限要求，学历要求以及年龄要求


##选做功能
### 人才画像

运行portrait.py，可以在data中生成labels.csv，label是通过简单判定给应聘者贴的标签。

