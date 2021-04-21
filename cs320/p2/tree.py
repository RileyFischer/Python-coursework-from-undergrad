#!/usr/bin/env python
# coding: utf-8

# In[3]:


# project: p2
#submitter: rjfischer
#partner: none


# In[35]:


import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
from zipfile import ZipFile
import os 
import csv


def get_bank_names(reader):
    names = []
    for row in reader.csv_iter():
        t = row['agency_abbr']
        if t in names:
            continue
        else:
            names.append(t)
            
    return names

class ZippedCSVReader:
    def __init__(self, zip):
        self.zip = zip
        self.set_paths(self.zip)


    def set_paths(self, zip):
        temp = []
        abs_paths = []
        with ZipFile(zip) as z:
            temp = z.namelist()
        self.paths = sorted(temp)
        return self.paths
    
    def lines(self, name):
        with ZipFile(self.zip) as zf:
            with zf.open(name) as f:
                for line in TextIOWrapper(f):
                    yield line
                    
        
                    
    def csv_iter(self, name = None):
        if name:
            with ZipFile(self.zip) as zf:
                with zf.open(name) as f:
                    tio = TextIOWrapper(f)
                    reader = csv.DictReader(tio)
                    for line in reader:
                        yield line 
        else:
            with ZipFile(self.zip) as zf:
                for path in self.paths:
                    if path == None:
                        print("null path")
                    with zf.open(path) as f:
                        tio = TextIOWrapper(f)
                        reader = csv.DictReader(tio)
                        for line in reader:
                            yield line

class Loan:
    def __init__(self, amount, purpose, race, income, decision):
        self.amount = amount
        self.purpose = purpose
        self.race = race
        self.income = income
        self.decision = decision
        self.dict = {
            'amount' : self.amount,
            'purpose' : self.purpose,
            'race' : self.race,
            'income' : self.income,
            'decision' : self.decision
        }
        

    def __repr__(self):
        return f"Loan({self.amount}, '{self.purpose}', '{self.race}', {self.income}, '{self.decision}')"

    def __getitem__(self, lookup):
        # TODO: deal with ints
        for key, val in self.dict.items():
            if lookup == key:
                return self.dict[lookup]
            elif str(val) == lookup:
                return 1
        return 0
    def set_race(self,new_race):
        self.race=new_race


class Bank:
    
    def __init__(self, name, reader):
        self.name = name
        self.reader = reader
        self.set_loans(reader, name)
        
    def set_loans(self, reader, name):
        self.loans = []
        for row in self.reader.csv_iter():
            a= row['loan_amount_000s']
            if a == '':
                a = 0
            p =  row['loan_purpose_name']
            if p == '':
                p = 0
            r = row['applicant_race_name_1']
            if r == '':
                r = 0
            i = row['applicant_income_000s']
            if i == '':
                i = 0
            ac = row['action_taken_name']
            if ac == '':
                ac = 0
                
            loan = Loan(int(a), p, r, int(i), ac)
            if name == None:
                self.loans.append(loan)
            elif row['agency_abbr'] == name:
                self.loans.append(loan)
            else:
                continue
        return self.loans
        
        
    def loan_iter(self):
        return iter(self.loans)
    
    def loan_filter(self, loan_min, loan_max, loan_purpose):
        
        filtered = [loan for loan in self.loans 
                        if loan_min <= loan.amount <= loan_max 
                        and loan.purpose == loan_purpose]
    
        return filtered


class SimplePredictor():
    def __init__(self):
        self.count = 0
        
    def predict(self, loan):
        if loan.purpose == "Home improvement":
            self.count += 1
            return True
        else:
            return False

    def getApproved(self):
        return self.count

class Node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None
    
    def set_val(self,val):
        self.val=val

class DTree(SimplePredictor):
    def __init__(self):
        SimplePredictor.__init__(self)
        self.root=None
        self.node_depths={}
        self.num_disaproved=0
        self.num_approved = 0
    def readTree(self,reader, path):
        self.root= Node()
        self.node_depths[0]=[self.root]
        
        for line in reader.lines(path):
            line=(line.split("---"))
            depth=(len(line[0].split("   ")))
            line_attributes=line[1].split(" ")
            #reads in lines
            
            parent_name=line[1].split("<=")
            if len(parent_name) == 1:
                parent_name=line[1].split(">")
            parent_n=""
            for i in parent_name:
                parent_n+=i
            #This is the value of the nodes:example is (income 98.50).The values have 2 spaces inbetween variable name and number value
            
            parent=self.node_depths[depth-1][0]
            #This is the path of the nodes:example is root.right.left.left
            
            if parent_n.strip()=="class: 0":
            #if line_attributes[1]+line_attributes[-2].strip()=="class:0":
                parent.set_val("class 0")
            elif parent_n.strip()=="class: 1":
            #elif line_attributes[1]+line_attributes[-2].strip()=="class:1":
                parent.set_val("class 1")   
            #if and elif for cases where node value is "class: 0" or "class: 1"
                
            elif line_attributes[-2]=="<=":
                self.node_depths[depth-1]=[parent, parent.set_val(parent_n.strip())]
                #self.node_depths[depth-1]=[parent, parent.set_val(line_attributes[1]+line_attributes[-2].strip())]
                parent.left=Node()
                self.node_depths[depth]=[parent.left]
            elif line_attributes[-3]==">":
                self.node_depths[depth-1]=[parent, parent.set_val(parent_n.strip())]
                #self.node_depths[depth-1]=[parent, parent.set_val(line_attributes[1]+line_attributes[-2].strip())]
                parent.right=Node()
                self.node_depths[depth]=[parent.right]
            #above 2 elif for creating nodes    
            
        return(self.root)  
        
    def predict(self,data,current_node=None):
        if current_node==None:
            current_node=self.root
        loan_attribute=current_node.val.split("  ")[0]
        loan_att_amount=current_node.val.split("  ")[-1]
        #print(loan_attribute)
        #print(data[loan_attribute])
        #print(type(data[loan_attribute]))
        if loan_attribute=="class 0":
            self.num_disaproved +=1
            return(False)
        elif loan_attribute=="class 1":
            self.num_approved += 1
            return(True)
        elif float(loan_att_amount)>=data[loan_attribute]:
            return(self.predict(data,current_node.left))
        elif float(loan_att_amount)<data[loan_attribute]:
            return(self.predict(data,current_node.right))


    def getDisapproved(self):
        return self.num_disaproved
    
    def getApproved(self):
        return self.num_approved

class RandomForest(SimplePredictor):
    def __init__(self, trees):
        self.trees=trees
    def predict(self, loan):
        total_approved=0
        total_denied=0
        for tree in self.trees:
            if tree.predict(loan)==True:
                total_approved+=1
            else:
                total_denied+=1
        if total_approved>total_denied:
            return True
        else:
            return False 

def bias_test(bank, predictor, race_override):
    total_changed=0
    total=0
    for loan in bank.loan_iter():
        before= predictor.predict(loan)
        new_loan=Loan(loan.amount, loan.purpose, race_override, loan.income, loan.decision)
        after=predictor.predict(new_loan)
        if before==after:
            pass
        else:
            total_changed+=1
        total+=1
    return (total_changed/total)   

