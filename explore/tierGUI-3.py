# -*- coding: utf-8 -*-

import pdb
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import xmlschema
from xml.etree import ElementTree as etree

from textwrap import dedent
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

buttonStyle = {'width': '140px',
               'height': '60px',
               'color': 'gray',
               'fontFamily': 'HelveticaNeue',
               'margin-right': 10,
               'lineHeight': '60px',
               'borderWidth': '1px',
               'borderStyle': 'solid',
               'borderRadius': '5px',
               'textAlign': 'center',
               'text-decoration': 'none',
               'display': 'inline-block'
               }
disabledButtonStyle = buttonStyle
disabledButtonStyle["disabled"] = True

#----------------------------------------------------------------------------------------------------
#  tmpDoc = etree.parse(filename)
#  tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
#  print(tierIDs)
def createPulldownMenu(menuName, tierChoices):

   options = []
   for item in tierChoices:
       newElement={"label": item, "value": item}
       options.append(newElement)

   idName = "tierGuideMenu-%s" % menuName
   menu = dcc.Dropdown(options=options, clearable=False, id=idName)
   return(menu)

#----------------------------------------------------------------------------------------------------
def createTierMappingMenus(eafFilename):

   print("--- createTierMappingMenus: %s [exists: %s]" % (eafFilename, os.path.exists(eafFilename)))
   dropDownMenus = html.H5("failure in extracting tierIDs from %s" % eafFilename)

   if(os.path.exists(eafFilename)):
      tmpDoc = etree.parse(eafFilename)
      userProvidedTierNamesToAssignToStandardTiers = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
      print(userProvidedTierNamesToAssignToStandardTiers)

      tierChoices = userProvidedTierNamesToAssignToStandardTiers
      #tierChoices = ["pending EAF file selection"]

      dropDownMenus = html.Table(id='tierMappingMenus', children=[
         html.Tr([html.Th("Standard interlinear tiers"), html.Th("User tier names (from EAF file)", style={'width': "60%"})]),
         html.Tr([html.Td("speech"), html.Td(createPulldownMenu("speech", tierChoices))]),
         html.Tr([html.Td("translation"), html.Td(createPulldownMenu("translation", tierChoices))]),
         html.Tr([html.Td("morpheme"), html.Td(createPulldownMenu("morpheme", tierChoices))]),
         html.Tr([html.Td("morphemeGloss"), html.Td(createPulldownMenu("morphemeGloss", tierChoices))]),
         html.Tr([html.Td("morphemePacking"), html.Td(createPulldownMenu("morphemePacking", ["tabs", "lines"]))])
         ], style={'margin': 100, 'margin-top': 10, 'margin-bottom': 0, 'width': 600}
         )

   saveTierMappingChoicesButton = html.Button('Save Choices', id='saveTierMappingSelectionsButton',
                                       style={"margin-left": 100, "margin-top": 10})

   tierMappingChoicesResultDisplay = html.Span(id="tierMappingChoicesResultDisplay", children="tmcrd")
   enclosingDiv = html.Div(children=[dropDownMenus, saveTierMappingChoicesButton, tierMappingChoicesResultDisplay])
   #return dropDownMenus
   return(enclosingDiv)

#----------------------------------------------------------------------------------------------------
def create_tierMapGui():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   helpText = dcc.Markdown(dedent('''There are four standard interlinear tiers.'''))

   helpTextDisplay = html.Div(children=helpText,
                        style={'margin': 100,
                               'margin-top': 10,
                               'margin-bottom': 10,
                               'border': '1px solid gray',
                               'border-radius': 5,
                               'padding': 20,
                               'width': "80%"})

   #dropDownMenus =  createTierMappingMenus("../inferno-threeLines/inferno-threeLines.eaf")
   dropDownMenus = html.Div(id="tierMappingMenus")

   submitInteractiveTierMapButton =  html.Button("Submit", style=buttonStyle, id="submitInteractiveTierMapButton")

   textArea = dcc.Textarea(id='writeTierGuideFileTextArea',
                           placeholder='tier guide write status goes here',
                           value="",
                           style={'width': 600, 'height': 50})

   div = html.Div(children=[helpTextDisplay,
                            dropDownMenus,
                            submitInteractiveTierMapButton,
                            html.Br(),
                            textArea],
                  id='tierMapGui-div', className="twelve columns") #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_allDivs():

   style = {'margin': 20,
            'border': '1px solid #aaa;',
            'border-radius': 4,
            'padding': '.5em .5em 0'}

   setFileButton =  html.Button('Set File', id='setFileButton', style={"margin": "5px"})
   children = [
       html.H4("IJAL Upload", style={'text-align': 'center'}, id='pageTitleH4'),
       html.P(id='eafFilename_hiddenStorage',       children="", style={'display': 'none'}),
       html.P(id='speechTier_hiddenStorage',        children="", style={'display': 'none'}),
       html.P(id='translationTier_hiddenStorage',   children="", style={'display': 'none'}),
       html.P(id='morphemeTier_hiddenStorage',      children="", style={'display': 'none'}),
       html.P(id='morphemeGlossTier_hiddenStorage', children="", style={'display': 'none'}),
       html.P(id='morphemePacking_hiddenStorage',   children="", style={'display': 'none'}),
       setFileButton,
       html.Details([html.Summary('Tier Guide, option 2: specify interactively'),
                     html.Div(create_tierMapGui())], style=style)
       ]

   div = html.Div(children=children, id='main-div', className="twelve columns") # , style=style)

   return div

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(children=[create_allDivs()])
#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('eafFilename_hiddenStorage', 'children'),
    [Input("setFileButton", 'n_clicks')])
def saveFilename(n_clicks):
    print("---- setFileButton clicked")
    if n_clicks is None:
        return("")
    print(n_clicks)
    print("setting eafFilename_hiddenStorage")
    return("../inferno-threeLines/inferno-threeLines.eaf")

@app.callback(
     Output('tierMapGui-div', 'children'),
     [Input("eafFilename_hiddenStorage", 'children')])
def populateTierGuidePulldowns(filename):
    print("=== populateTierGuidePulldowns: %s" % filename)
    if filename == '':
        return ''
    # pdb.set_trace()
    return createTierMappingMenus("../inferno-threeLines/inferno-threeLines.eaf")
    #return html.Div(html.H3("hobo")) #createTierMappingMenus("../inferno-threeLines/inferno-threeLines.eaf")


@app.callback(
    Output('speechTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-speech', 'value')])
def updateSpeechTier(value):
    print("speech tier user name: %s" % value)
    return value

@app.callback(
    Output('translationTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation', 'value')])
def updateTranslationTier(value):
    print("translation tier user name: %s" % value)
    return value

@app.callback(
    Output('morphemeTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morpheme', 'value')])
def updateMorphemeTier(value):
    print("morpheme tier user name: %s" % value)
    return value

@app.callback(
    Output('morphemeGlossTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morphemeGloss', 'value')])
def updateMorphemeGlossTier(value):
    print("morphemeGloss tier user name: %s" % value)
    return value

@app.callback(
    Output('morphemePacking_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morphemePacking', 'value')])
def updateMorphemePackingUserChoice(value):
    print("morphemePacking: %s" % value)
    return value

@app.callback(
    Output('tierMappingChoicesResultDisplay', 'children'),
    [Input('saveTierMappingSelectionsButton', 'n_clicks')],
    [State('speechTier_hiddenStorage',        'children'),
     State('translationTier_hiddenStorage',   'children'),
     State('morphemeTier_hiddenStorage',      'children'),
     State('morphemeGlossTier_hiddenStorage', 'children'),
     State('morphemePacking_hiddenStorage',   'children')])
def saveTierMappingSelection(n_clicks, speechTier, translationTier, morphemeTier, morphemeGlossTier, morphemePacking):
    if n_clicks is None:
        return("")
    print("saveTierMappingSelectionsButton: %d" % n_clicks)
    print("speechTier: %s" % speechTier)
    print("translationTier: %s" % translationTier)
    print("morphemeTier: %s" % morphemeTier)
    print("morphemeGlossTier: %s" % morphemeGlossTier)
    print("morphemePacking: %s" % morphemePacking)
    return("saved!")

#----------------------------------------------------------------------------------------------------
# @app.callback(
#      Output('tierMappingMenus', 'children'),
#      [Input('setFileButton', 'n_clicks')])
# def populateTierGuidePulldowns(n_clicks):
#      if n_clicks is None:
#          return ""
#      print("=== populateTierGuidePulldowns: %d" % n_clicks)
#      return createTierMappingMenus("../inferno-threeLines/inferno-threeLines.eaf")

#------------------------------------------------------------------------------------------------------------------------

