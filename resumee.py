import os
from typing import List
import torch
from transformers import AutoTokenizer

from union import *
from text_extraction.doc_to_text import doc_to_text
from inference import inference, event_extract_example, information_extract_example, ner_example


device = 'cuda:0'
saved_model_path = 'model/UIE_Resume'
tokenizer = AutoTokenizer.from_pretrained(saved_model_path) 
model = torch.load(os.path.join(saved_model_path, 'model.pt')).half()
model.to(device).eval()


class Resumee(object):
    # example token: {'ner': ['token'], 'information': {'token': ['information']}, 'event': {'token': ['event']}}
    def __init__(self, path, token={'ner': [], 'information': {}, 'event': {}}): 
        self.path = path
        self.name = os.path.basename(self.path)
        _, self.ext = os.path.splitext(self.name)
        self.text = doc_to_text(self.path, self.ext)
        self.token = token
        self.ner, self.information = self.extraction(token)
    
    def extraction(self, token, save=False):
        try:
            schema = token['ner']
            try:
                ner = ner_extraction(model, tokenizer, device, sentence=self.text, schema=schema)
            except IndexError:
                ner = {}
        except KeyError:
            ner = {}
        
        try:
            schema = token['information']
            information = information_extraction(model, tokenizer, device, sentence=self.text, schema=schema)
        except KeyError:
            information = {}
        
        # try:
        #     schema = token['event']
        #     event = event_extract_example(model, tokenizer, device, sentence=self.text, schema=schema)
        # except KeyError:
        #     event = {}
        
        if save:
            self.ner = ner
            self.information = information
            # self.event = event
        
        # return ner, information, event
        return ner, information


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