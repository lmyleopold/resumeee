import os
from typing import List
import torch
from transformers import AutoTokenizer

from doc_to_text import doc_to_text
from person_info import *
from person_extraction import *
from job_fit import job_fit


device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
saved_model_path = 'model/UIE_Resume'
tokenizer = AutoTokenizer.from_pretrained(saved_model_path)
if device == 'cuda:0':
    model = torch.load(os.path.join(saved_model_path, 'model.pt')).half()
else:
    model = torch.load(os.path.join(saved_model_path, 'model.pt'), map_location=torch.device('cpu'))
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
        self.person_info = get_person_info(self.ner, self.information)
    
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

    def fit(self, job_info, topk=1):
        return job_fit(job_info, self.person_info, topk)