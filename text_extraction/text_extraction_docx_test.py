import re
import xml.dom.minidom as xdom

# 构建一个正则，去除<>标签
pattern_del_tag = re.compile(r'<[^>]+>',re.S)

# 加载文档
xp = xdom.parse('./text_extraction/test/test_resumee.xml')
root=xp.documentElement

# 获取body节点
bodys = root.getElementsByTagName("w:body")
body = bodys[0]

# 循环遍历body下的节点
for i, ele in enumerate(body.childNodes):
    # e_name = ele.nodeName
    # print(i,"->",e_name,"is",ele)

    # 找到包含w:t的标签,可能是多个
    wts = ele.getElementsByTagName("w:t")
    ele_text = ""
    for wt in wts:
        t_text =  pattern_del_tag.sub('', wt.toxml())
        ele_text = ele_text + t_text
    print(ele_text)