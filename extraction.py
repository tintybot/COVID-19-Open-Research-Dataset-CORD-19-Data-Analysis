import os
import json
import pandas as pd
from tqdm import tqdm
import numpy as np
from nltk.corpus import wordnet
import re
import matplotlib.pyplot as plt

#lets say we are searching for 'incubation'
synonyms=list()
for syn in wordnet.synsets("incubation"):
    for name in syn.lemma_names():
        if name not in synonyms:
        	synonyms.append(name)

#load a file
dirs_=["biorxiv_medrxiv\\biorxiv_medrxiv",
"comm_use_subset\\comm_use_subset",
"noncomm_use_subset\\noncomm_use_subset",
"pmc_custom_license\\pmc_custom_license"]
data_=list()
for dir_ in dirs_:
	for filename in tqdm(os.listdir(dir_)):

		#reading the file
		with open(os.path.join(dir_,filename)) as file:
			data=json.loads(file.read())
		
		#take out the data from the json format
		paper_id=data['paper_id']
		meta_data=data['metadata']
		abstract=data['abstract']
		abstract_text=""
		for text in abstract:
			abstract_text+=text['text']+" "
		body_text=data['body_text']
		full_text=""
		for text in body_text:
			full_text+=text['text']+" "
		back_matter=data['back_matter']
		#store everything to a dataframe
		data_.append([paper_id,abstract_text,full_text])

df=pd.DataFrame(data_,columns=['paper_id','abstract','full_text'])
#save as a csv
#df.to_csv('biorxiv_medrxiv.csv', index = True)


#############################################################################################
#for incubation period
#incubation=df[df['full_text'].str.contains('incubation')]

incubation_synonym=df[df['full_text'].str.contains('|'.join(synonyms))]

#incubation.to_csv('biorxiv_medrxiv_incubation.csv', index = True)
#incubation_synonym.to_csv('biorxiv_medrxiv_incubation_synonyms.csv', index = True)

all_details=list()
texts=incubation_synonym['full_text']
for tex in texts:
	#print(tex)
	for t in tex.split(". "):
		if 'incubation' in t:
			regex=re.findall("\d{1,2} days| \d{1,2}-\d{1,2} days| \d{1,2} to \d{1,2} days| \d+\.\d+ days|\d+\.\d+-\d+\.\d+ days|\d+\.\d+ to \d+\.\d+ days",t)
			if len(regex)!=0:
				#print(t)
				#print(regex)
				#print('\n')
				all_details.append(regex)

#extracting incubation periods from data
incubation_period=list()
for samples in all_details:
	for sam in samples:
		for data in sam.split(" "):
			try:
				incubation_period.append(float(data))
			except:
				#ingore the days n all
				pass
#incubation_period=np.array(incubation_period)
#print(incubation_period)
dataf=pd.DataFrame(incubation_period)
print(dataf.describe())

#datadescription and plots
hist=dataf.hist(bins=50)
plt.ylabel('Frequency as per research paper')
plt.xlabel('No of days')
plt.title('COVID 19 incubation period')
plt.show()



