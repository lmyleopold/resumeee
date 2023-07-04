from resumee import Resumee
from tqdm import tqdm

for i in tqdm(range(1,101)):
    try:
        test = Resumee("data/dataset_CV/CV/{0}.docx".format(i))
        with open("data/text/{0}.txt".format(i), "w", encoding="utf-8") as f:
            f.write(test.text)
    except:
        continue