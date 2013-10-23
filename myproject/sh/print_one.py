#!/usr/bin/env python
#coding: utf-8
from myproject.dataframe import DataFrame
import sys
d = DataFrame()
item = d.QueryByUrl(sys.argv[1]) 
if item:
    for key, value in item.items():
        print key
        print value
        print '-'*10
 
