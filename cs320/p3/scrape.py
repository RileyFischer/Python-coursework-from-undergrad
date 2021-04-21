#!/usr/bin/env python
# coding: utf-8

# In[1]:


# project: p3
#submitter: rjfischer
#partner: none


# In[2]:


import time
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    # required
    def	__init__(self, driver, home_url):
        self.driver = driver
        self.home_url =	home_url
        self.dfs=[]
        self.bfs=[]
        self.children=[]
        self.todo_BFS = []
        self.added = set()
        self.added_DFS=[]
         
    def visit_page(self,url,Search_type=""):   
        self.driver.get(url)
        if Search_type=="dfs":
            dfs_btn=self.driver.find_element_by_id("DFS")
            dfs_btn.click()
            self.dfs.append(dfs_btn.text)
        elif Search_type=="bfs":
            bfs_btn=self.driver.find_element_by_id("BFS")
            bfs_btn.click()
            self.bfs.append(bfs_btn.text)
        links = self.driver.find_elements_by_tag_name("a")
        return [link.get_attribute("href") for link in links]

    def easter_egg(self):
        self.driver.get(self.home_url)
        Parts=(self.driver.find_elements_by_tag_name("span"))
        egg=""
        for Part in Parts:
            egg+=(Part.text)
        return(egg)

    def dfs_visit(self):
        for child in self.children:
            if child not in self.added_DFS:
                self.added_DFS.append(child)
                self.children=(self.visit_page(child))
                self.visit_page(child,'dfs')
                self.dfs_visit() 
        return(self.dfs)
                
    def dfs_pass(self):
        self.driver.get(self.home_url)
        home_link=self.driver.find_elements_by_tag_name("a")[0].get_attribute("href")
        self.children.append(home_link)
        password=self.dfs_visit()
        password=""
        for i in self.dfs:
            password+=i
        return(password)

    def bfs_pass(self):  
        self.driver.get(self.home_url)
        home_link=self.driver.find_elements_by_tag_name("a")[0].get_attribute("href")
        self.todo_BFS.append(home_link)
        self.added.add(home_link)
            
        while len(self.todo_BFS)>0:
            url = self.todo_BFS.pop(0)
            children_urls = self.visit_page(url,"bfs")
            for child_url in children_urls:
                if not child_url in self.added:
                    self.todo_BFS.append(child_url)
                    self.added.add(child_url)
        password=""
        for i in self.bfs:
            password+=i
        return(password)

    # write the code for this one individually
    def protected_df(self, password):
        self.driver.get(self.home_url)
        box=self.driver.find_element_by_id("password-input")
        box.clear()
        box.send_keys(password)
        btn=self.driver.find_element_by_id("attempt-button")
        btn.click()
        num_rows_b=-1
        num_rows_a=0
        while num_rows_b!=num_rows_a:
            try:
                btn=self.driver.find_element_by_id("more-locations-button")
                btn.click()
            except:
                pass
            page=BeautifulSoup(self.driver.page_source,features="html.parser")
            tables=page.find_all("tr")
            num_rows_b=len(tables)
            time.sleep(1)
            page=BeautifulSoup(self.driver.page_source,features="html.parser")
            tables=page.find_all("tr")
            num_rows_a=len(tables)
        
        table=page.find_all("table")[0]
        rows=[]
        th_tags=[]
        for tr in table.find_all("tr"):
            if tr==table.find_all("tr")[0]:
                for col in tr.find_all("th"):
                    th_tags.append(col.get_text())
            else:
                rows.append([td.get_text() for td in tr.find_all("td")])
        
        return(pd.DataFrame(rows,columns=th_tags))


