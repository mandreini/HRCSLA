# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 15:34:25 2015

@author: Matt
"""

from sql import render, tables, db

class Home:
    def GET(self):
        return render.home()
    
class Index_all:
    def GET(self):
        reports = db.select(tables[0])
        return render.index(reports)
        
class Index_month:
    def GET(self):
        reports = db.select(tables[1])
        return render.index(reports)
    
class Index_week:
    def GET(self):
        reports = db.select(tables[2])
        return render.index(reports)
        
class Index_day:
    def GET(self):
        reports = db.select(tables[3])
        return render.index(reports)

class Contact:
    def GET(self):
        return render.contact()
        
class Donate:
    def GET(self):
        return render.donate()
        
class Signin:
    def GET(self):
        return render.signin()
        
urls = (
    '/',        'Home',
    '/all',     'Index_all', 
    '/month',   'Index_month',
    '/week',    'Index_week',
    '/day',     'Index_day',
    '/contact', 'Contact',
    '/donate',  'Donate',
    '/signin',  'Signin')
