import gzip
import xml.etree.ElementTree as ET
import sys
import os
import json
from callback import get_papers, totalPapers

class Paper:
    def __init__(self):
        self.paper_id = None
        self.author = None
        self.doi = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None
        self.published_through = None
        self.citation_count = None
        self.file_source = None
        self.line_number = 0

DBLP_line_count_freq=-1

'''
@brief: used to parse through DBLP and MAG datasets. DBLP being in XML format and MAG being in txt but uses CSV

@author: Davis Spradling
'''

'''
used to parse through DBLP

@param: file_path - file path to access DBLP

@param: callback - methods you want to be executed everytime a paper is parsed

@param: count_to - paper number you want to quit performing callbacks on

@param: start_paper - paper to start performing callbacks on

since values are being parsed using xml it is suggested to make sure that you pass in 0 as the start_paper
'''
        
def parse_DBLP_file(callback,start_paper,count_to):
    current_paper = None
    paper_title_arr = []
    if(start_paper>=count_to):
        print("Error: Start paper is greater then or equal to end paper. Adjust so that start paper is less then the end paper.")
        sys.stdout.flush()

    with open('../data/dblp.xml', 'rt', encoding='utf-8') as gz_file:
        count_line = 0
        pap = []
        i = 0
        current_paper = None
        #help us keep track of if we are inside a paper currently
        inside_paper = False
        for current_line in gz_file:
            if i > count_to:
                return paper_title_arr
            
            #check for closing tag first for cases such as
            #</incollection><incollection mdate="2017-07-12" key="reference/cn/Prinz14" publtype="encyclopedia">
            if '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                inside_paper = False
                if current_paper is not None and current_paper.title is not None and current_paper.paper_id is not None:
                    #print("Paper is an Object")
                    #for i in range(len(pap)):
                    #   print(pap[i])
                    if(start_paper<=i):
                        for fnction in callback:
                            fnction(current_paper)
                        paper_title_arr.append(current_paper.title)

                    current_paper = None

                    i+=1

            #check for an opening tag to make a new Paper object
            if '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                if not inside_paper:
                    current_paper = Paper()
                    current_paper.file_source = "DBLP"
                    inside_paper = True

            if current_paper:
                if '<author>' in current_line:
                    current_paper.author = current_line.replace('<author>', '').replace('</author>', '').strip()
                elif '<year>' in current_line:
                    current_paper.year = current_line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in current_line:
                    current_paper.pages = current_line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<ee' in current_line:
                    doi_value = current_line.replace('<ee', '').replace('</ee>', '').strip()
                    doi_value = doi_value.replace('https://doi.org/', '')
                    current_paper.doi = doi_value
                elif '<title>' in current_line:
                    current_paper.title = current_line.replace('<title>', '').replace('</title>', '').strip()
                elif '<url>' in current_line:
                    current_paper.url = current_line.replace('<url>', '').replace('</url>', '').strip()
                elif 'key="' in current_line:
                    key_start = current_line.find('key="') + 5
                    #end is the parenthesis that close the key
                    key_end = current_line.find('"', key_start)
                    #if a valid key
                    if key_start != -1 and key_end != -1:
                        current_paper.paper_id = current_line[key_start:key_end]

                pap.append(current_line)
                count_line += 1

    return paper_title_arr








