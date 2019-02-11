# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import xmlschema
from xml.etree import ElementTree as etree

from textwrap import dedent
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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

   print("--- createTierMappingMenus: %s" % eafFilename)
   dropDownMenus = html.H5("failure in extracting tierIDs from %s" % eafFilename)

   if(os.path.exists(eafFilename)):
      tmpDoc = etree.parse(eafFilename)
      userProvidedTierNamesToAssignToStandardTiers = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
      print(userProvidedTierNamesToAssignToStandardTiers)

      tierChoices = userProvidedTierNamesToAssignToStandardTiers
      tierChoices = ["pending EAF file selection"]

      dropDownMenus = html.Table(id='tierMappingMenus', children=[
         html.Tr([html.Th("Standard interlinear tiers"), html.Th("User tier names (from EAF file)", style={'width': "60%"})]),
         html.Tr([html.Td("speech"), html.Td(createPulldownMenu("speech", tierChoices))]),
         html.Tr([html.Td("translation"), html.Td(createPulldownMenu("translation", tierChoices))]),
         html.Tr([html.Td("morpheme"), html.Td(createPulldownMenu("morpheme", tierChoices))]),
         html.Tr([html.Td("morphemeGloss"), html.Td(createPulldownMenu("morphemeGloss", tierChoices))]),
         html.Tr([html.Td("morphemePacking"), html.Td(createPulldownMenu("morphemePacking", ["tabs", "lines"]))])
         ], style={'margin': 100, 'margin-top': 20, 'width': 600}
         )

   return dropDownMenus

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

   dropDownMenus =  createTierMappingMenus("../inferno-threeLines/inferno-threeLines.eaf")
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

   setFileButton =  html.Button('Set File', id='setFileButton', style={"margin": "20px"})
   children = [
       html.H4("IJAL Upload", style={'text-align': 'center'}, id='pageTitleH4'),
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
    Output('tierGuideMenu-speech', 'options'),
    [Input('setFileButton', 'n_clicks')])
def populateTierGuidePulldowns(n_clicks):
    if n_clicks is None:
        s = "pending selection of EAF file"
        return [{'label': s, 'value': "pending"}]
    print("=== populateTierGuidePulldowns")
    return [{'label': "foobar", 'value': "foobar"}]

#------------------------------------------------------------------------------------------------------------------------

