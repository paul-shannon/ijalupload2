# text.py: a class to represent a complete IJAL interlinear text, and to transform its
# represention in ELAN xml (eaf) format, accompanied by audio, into html
#----------------------------------------------------------------------------------------------------
import re
import sys
import os
import yaml
import unittest
from ijalLine import *
import importlib
pd.set_option('display.width', 1000)
import pdb
#----------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class Text:

   xmlFilename = ''
   audioPath = ''
   grammaticalTermsFile = None
   grammaticalTerms = []
   xmlDoc = None
   htmlDoc = None
   lineCount = 0
   quiet = True

   def __init__(self, xmlFilename, audioPath, grammaticalTermsFile, tierGuideFile, quiet=True):
     self.xmlFilename = xmlFilename
     self.audioPath = audioPath
     self.grammaticalTermsFile = grammaticalTermsFile
     self.tierGuideFile = tierGuideFile
     self.validInputs()
     self.quiet = quiet
     self.xmlDoc = etree.parse(self.xmlFilename)
     self.lineCount = len(self.xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
     with open(tierGuideFile, 'r') as f:
        self.tierGuide = yaml.load(f)
     self

   #def discoverTiers(self):
   #  tmpDoc = etree.parse(self.xmlFilename)
   #  tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
   #  return(tierIDs)

   def getTierSummary(self):
     tmpDoc = etree.parse(self.xmlFilename)
     tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
     tiers = tmpDoc.findall("TIER")
     #print(self.tierGuide)
     tbl = pd.DataFrame(list(self.tierGuide.items()), columns=['key', 'value']).ix[0:3]
     tbl['count'] = [0, 0, 0, 0]
     tierValues = tbl["value"].tolist()
     for i in range(4):
        tier = tiers[i]
        tierValue = tierValues[i]
        tierID = tier.attrib["TIER_ID"]
        count = len(tier.findall("ANNOTATION"))
        rowNumber = tbl[tbl['value']==tierValue].index.item()
        tbl.ix[rowNumber, 'count'] = count
        #print(" %30s: %4d" % (tierID, count))
     self.tierTable = tbl
     return(tbl)


     return(tierIDs)

   def validInputs(self):
     assert(os.path.isfile(self.xmlFilename))
     assert(os.path.isfile(self.tierGuideFile))
     #assert(self.audioPath == None or os.path.isdir(self.audioPath))
     if(not self.grammaticalTermsFile == None):
        assert(os.path.isfile(self.grammaticalTermsFile))
        self.grammaticalTerms = open(self.grammaticalTermsFile).read().split("\n")
        assert(len(self.grammaticalTerms) > 0)
     return(True)

   def getLineAsTable(self, lineNumber):
     x = IjalLine(self.xmlDoc, lineNumber, self.tierGuide)
     x.parse()
     return(x.getTable())

   def traverseStructure(self):
      lineNumbers = range(self.lineCount)
      for i in lineNumbers:
         x = IjalLine(self.xmlDoc, i, self.tierGuide)
         x.parse()
         tbl = x.getTable()
         print("%d: %d tiers" % (i, tbl.shape[0]))

   def toHTML(self, lineNumber=None):

     htmlDoc = Doc()

     if(lineNumber == None):
        lineNumbers = range(self.lineCount)
     else:
        lineNumbers = [lineNumber]

     htmlDoc.asis('<!DOCTYPE html>')
     with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="http://pshannon.net/ijal/ijal.css">')
            htmlDoc.asis('<script src="http://pshannon.net/ijal/ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for i in lineNumbers:
                    if(not self.quiet):
                       print("line %d/%d" % (i, self.lineCount))
                    line = IjalLine(self.xmlDoc, i, self.tierGuide, self.grammaticalTerms)
                    line.parse()
                    with htmlDoc.tag("div",  klass="line-wrapper"):
                        tbl = line.getTable()
                        lineID = tbl.ix[0]['ANNOTATION_ID']
                        with htmlDoc.tag("div", klass="line-sidebar"):
                            line.htmlLeadIn(htmlDoc, self.audioPath, )
                        line.toHTML(htmlDoc)

     self.htmlDoc = htmlDoc
     self.htmlText = htmlDoc.getvalue()
     return(self.htmlText)

