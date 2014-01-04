#! /usr/bin/python
#! -*- coding: utf-8 -*-
from scrapy.item import Item, Field

class MongodbItemCategory(Item):

    #Data to collect for categories
    #The following data should be collected and stored for each category page (where ever possible):
    sourceid = Field()          #string 
                                #identifier identifying the product (If no ID can be retrieved from the page, serves as unique key for the category)
    source = Field()            #string 
                                #the spider name
    urls = Field()              #list of string 
                                #where this category was seen
    createddatetime = Field()   #datetime 
                                #When the (mongodb) document wascreated
    name = Field()              #string 
                                #The category name
    description = Field()       #string 
                                #Any text on the page describing the category
    productlinks = Field()      #list of string Products being linked to from the category page
    imagelinks = Field()        #list of string 
                                #Category images

class MongodbItem(Item):

    #Data to collect for products
    #The following data should be collected for each product page (where ever possible)
    sourceid = Field()          #string 
                                #identifier identifying the product (If no ID can be retrieved from the page, serves as unique key for the category)
    source = Field()            #string 
                                #the spider name
    raw_document = Field()      #string 
                                #the html source code of the page.
    urls = Field()              #list of string 
                                #where this category was seen
    createddatetime = Field()   #datetime 
                                #When the (mongodb) document wascreated
    name = Field()              #string 
    onstock = Field()           #boolean
    mainimage = Field()         #string 
    otherimages = Field()       #list of string
    shortdescription = Field()  #string 
    description = Field()       #string 
    details = Field()           #string 
    relatedlinks = Field()      #list of string
    upselllinks = Field()       #list of string
    price = Field()             #double
    specialprice = Field()      #double (optional)
    currency = Field()          #currency code (string?)
    
    
   


