import os

from doc_to_text import *

class Resumee(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)
        _, self.ext = os.path.splitext(self.name)
        self.text = doc_to_text(self.path, self.ext)
