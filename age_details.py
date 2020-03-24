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
#for age groups
#incubation=df[df['full_text'].str.contains('incubation')]
wards=["years","infected","age","heath"]
body_=df[df['full_text'].str.contains('|'.join(wards))]

all_details=list()
for bod in body_['full_text']:
	for b in bod.split(". "):
		if 'age' in b or 'infected' in b or 'health' in b or 'years' in b:
			regex=re.findall(" \d{1,2} years| \d{1,2}-\d{1,2} years| \d{1,2} to \d{1,2} years| \d+\.\d+ years| \d+\.\d+-\d+\.\d+ years| \d+\.\d+ to \d+\.\d+ years",b)
			if len(regex)!=0:
				#print(b)
				#print(regex)
				#print("\n")
				all_details.append(regex)

#extracting age groups from data
age_group=list()
for samples in all_details:
	for sam in samples:
		for data in sam.split(" "):
			try:
				age_group.append(float(data))
			except:
				#ingore the days n all
				pass

#print(age_group)
#age_=np.array(age_group)

#dataf=pd.DataFrame(age_group)
#print(dataf.describe())
#datadescription and plots
for x in age_group:
	if x>=0 and x<=100:
		pass
	else:
		age_group.remove(x)
plt.hist(age_group,bins=50)
plt.ylabel('Frequency as per research paper')
plt.xlabel('Age of Human in years')
plt.title('COVID 19 infected age groups')
plt.show()



