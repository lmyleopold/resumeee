import os
from typing import List
import torch
from transformers import AutoTokenizer

from text_extraction.doc_to_text import doc_to_text
from inference import inference, event_extract_example, information_extract_example, ner_example


device = 'cuda:0'
saved_model_path = 'model/UIE_Resume'
tokenizer = AutoTokenizer.from_pretrained(saved_model_path) 
model = torch.load(os.path.join(saved_model_path, 'model.pt'))
model.to(device).eval()


class Resumee(object):
    # example token: {'ner': ['token'], 'information': {'token': ['information']}, 'event': {'token': ['event']}}
    def __init__(self, path, token={'ner': [], 'information': {}, 'event': {}}): 
        self.path = path
        self.name = os.path.basename(self.path)
        _, self.ext = os.path.splitext(self.name)
        self.text = doc_to_text(self.path, self.ext)
        self.token = token
        self.ner, self.information, self.event = self.extraction(token)
    
    def extraction(self, token, save=False):
        try:
            schema = token['ner']
            try:
                ner = ner_example(model, tokenizer, device, sentence=self.text, schema=schema)
            except IndexError:
                ner = {}
        except KeyError:
            ner = {}
        
        try:
            schema = token['information']
            information = information_extract_example(model, tokenizer, device, sentence=self.text, schema=schema)
        except KeyError:
            information = {}
        
        try:
            schema = token['event']
            event = event_extract_example(model, tokenizer, device, sentence=self.text, schema=schema)
        except KeyError:
            event = {}
        
        if save:
            self.ner = ner
            self.information = information
            self.event = event
        
        return ner, information, event
            
        
        
