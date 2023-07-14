from union import *
from inference import inference, event_extract_example, information_extract_example, ner_example


# 每隔256字符做截断，上下设置64字符上下文            
def ner_extraction(model, tokenizer, device, sentence, schema):
    context = 64
    split_num = 256
    length = len(sentence)

    ner = {}
    i = context
    while True:
        try:
            start_id = i - context
            end_id = i + split_num + context
            tmp = ner_example(model, tokenizer, device, 
                        sentence=sentence[start_id: end_id if end_id > length else -1],
                        schema=schema)
            union_dict(ner, tmp)
        except IndexError:
            tmp = {}
            break
        if end_id > length:
            break
        else:
            i = i + split_num
    return ner

def information_extraction(model, tokenizer, device, sentence, schema):
    context = 64
    split_num = 256
    length = len(sentence)

    information = {}
    i = context
    while True:
        start_id = i - context
        end_id = i + split_num + context
        tmp = information_extract_example(model, tokenizer, device, 
                        sentence=sentence[start_id: end_id if end_id > length else -1],
                        schema=schema)
        union_double_dict(information, tmp)
        if end_id > length:
            break
        else:
            i = i + split_num
    return information