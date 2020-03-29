import pandas as pd
import random

class autofill:
    def __init__(self,file_location):
        self.df = self.read_csv(file_location)

    def read_csv(self,location):
        try:
            file_reader = pd.read_csv(str(location))
            return file_reader
        except:
            return 'autofill[read_csv]: no file was found!'

    def catch(self,quest_no):
        quest_comb = self.df.loc[self.df['quest_no'] == '{}'.format(quest_no)]['quest_type','quest_condition ','quest_force_ans'].to_list()
        # quest_comb = self.df.loc[self.df['quest_no'] == '{}'.format(quest_no)].to_dict()
        if len(quest_comb):
            return self.fill(quest_comb)
        else:
            return "autofill[catch]: quest_no wasn't in the list!"

    def fill(self,quest_comb):
        quest_type,quest_condition,quest_force_ans = quest_comb[0],quest_comb[1],quest_comb[2]

