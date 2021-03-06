#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: arindam
"""


import pandas as pd
import numpy as np
import spacy
import re

trainingdata=[]
def findindex(file,word,substance):
    for m in re.finditer(word, file):
         trainingdata.append((file,dict(entities=[tuple(( m.start(), m.end(),substance))])))

DIR='D:\\DownloadFiles_\\'

data=pd.read_excel(r'D:\FilesData.xlsx')

data.columns


substance=list(data['Substance'])
filelist=list(data['File'])


for x,y in zip(filelist[0:7000],substance[0:7000]):
    try:
        file=open(DIR+x+'.txt',encoding='utf-8')
        file=file.read().lower()
        y=str(y)
        y=y.lower()
        findindex(file,y,'Substance')
    except Exception as e:
        print(e)
        pass
    

nlpsubstance = spacy.blank('en')

import random
ner = nlpsubstance.create_pipe('ner')
nlpsubstance.add_pipe(ner)
ner.add_label('Substance')


nlpsubstance.begin_training()
for i in range(10):
    random.shuffle(trainingdata)
    for batch in spacy.util.minibatch(trainingdata):
        texts = [text for text, annotation in batch]
        annotations = [annotation for text, annotation in batch]
        nlpsubstance.update(texts, annotations)    
    
    
    
for x in filelist[7001:8000]:
        try:
            file=open(DIR+x+'.txt',encoding='utf-8')
            file=file.read()
            doc=nlpsubstance(file)
            for ent in doc.ents:
                print(ent.text, ent.label_)
        except Exception as e:
            print(e)
            pass
                
            

nlpsubstance.to_disk(r'D:\substancener')
