#!/usr/bin/env python
#coding: utf-8
from myproject.dataframe import DataFrame
import sys
d = DataFrame()
item = d.QueryByUrl(sys.argv[1]) 
if item:
    print item
 
