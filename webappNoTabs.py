import datetime
import base64
import pdb
import xmlschema
import os
import scipy.io.wavfile as wavfile
import dash
import pandas as pd
import dash_table
import yaml
import io
import webbrowser
from flask import Flask
import flask
from textwrap import dedent
from zipfile import *
#----------------------------------------------------------------------------------------------------
import sys
sys.path.append("../ijal_interlinear")
from audioExtractor import *
from text import *
#----------------------------------------------------------------------------------------------------
UPLOAD_DIRECTORY = "./UPLOADS"
PROJECTS_DIRECTORY = "./PROJECTS"
#----------------------------------------------------------------------------------------------------
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, static_folder='PROJECTS')
app.config['suppress_callback_exceptions'] = True
app.title = "IJAL Text Upload"

app.scripts.config.serve_locally = True

#------------------------------------------------------------------------------------------------------------------------

@app.server.route('/PROJECTS/<path:urlpath>')
def serve_static_file(urlpath):
   print("--- serve_static_file")
   print("urlpath:  %s" % urlpath)
   fullPath = os.path.join("PROJECTS", urlpath)
   dirname = os.path.dirname(fullPath)
   filename = os.path.basename(fullPath)
   print("about to send %s, %s" % (dirname, filename))
   return flask.send_from_directory(dirname, filename)


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
def create_eafUploader():

    uploader = dcc.Upload(id='upload-eaf-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_setTitleTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   setTitleInput = dcc.Input(id="setTitleTextInput",
                         placeholder='enter convenient, concise text title here, no spaces please!',
                         value="",
                         style={'width': '512px', 'fontSize': 20})

   setTitleButton = html.Button(id='setTitleButton', type='submit', children='Submit')
#tierIDsBlankDiv = html.Div(children=[html.H4("blank")], id="tierIDsBlankDiv")

   children = [html.Br(),
               setTitleInput,
               html.Br(),
               html.Br(),
               setTitleButton
               #tierIDsBlankDiv
               ]

   div = html.Div(children=children, id='setTitleDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_eafUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="eafUploadTextArea",
                           placeholder='xml validation results go here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_eafUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='eafUploaderDiv') #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_soundFileUploader():

    uploader = dcc.Upload(id='upload-sound-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_soundFileUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="soundFileUploadTextArea",
                           placeholder='sound file validation results go here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_soundFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='soundFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapFileUploader():

    uploader = dcc.Upload(id='upload-tierMap-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_tierMapUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="tierMapUploadTextArea",
                           placeholder='tierGuide.yaml will be displayed here',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(),
               html.Div([create_tierMapFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='tierGuideFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsUploaderTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   textArea = dcc.Textarea(id="grammaticalTermsUploadTextArea",
                           placeholder='grammatical terms will be displayed here',
                           value="",
                           style={'width': 600, 'height': 300})

   button =  html.Button('No Grammatical Terms', id='noGrammaticalTermsButton', style={"margin": "20px"})

   children = [html.Br(),
               button,
               html.Div([create_grammaticalTermsFileUploader()],
                        style={'display': 'inline-block'}),
               html.Br(),
               html.Br(),
               textArea
               ]

   div = html.Div(children=children, id='grammaticalTermsFileUploaderDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsFileUploader():

    uploader = dcc.Upload(id='upload-grammaticalTerms-file',
                          children=html.Div([html.A('Select File', style=buttonStyle)]),
                          multiple=False,
                          style={'display': 'inline-block'})

    return uploader

#----------------------------------------------------------------------------------------------------
def create_associateEAFandSoundTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   button =  html.Button('Extract Sounds By Phrase', id='extractSoundsByPhraseButton', style={"margin": "20px"})

   textArea = dcc.Textarea(id="associateEAFAndSoundInfoTextArea",
                           placeholder='eaf + soundFile',
                           value="",
                           style={'width': 600, 'height': 300})

   children = [html.Br(), button, html.Br(), textArea]

   div = html.Div(children=children, id='associateEAFandSoundDiv', style={'display': 'block'})

   return div

#----------------------------------------------------------------------------------------------------
def create_webPageCreationTab():

   style = {'border': '5px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   createButton =  html.Button('Create Web Page', id='createWebPageButton', style={"margin": "20px"})
   displayButton =  html.Button('Display Web Page', id='displayIJALTextButton', style={"margin": "20px"})
   downloadWebpageButton =  html.Button('Download Page', id='downloadWebpageButton', style={"margin": "20px"})

   textArea = dcc.Textarea(id="createWebPageInfoTextArea",
                           placeholder='progress info will appear here',
                           value="",
                           style={'width': 600, 'height': 30})

   webPageIframe = html.Iframe(id="storyIFrame", src="<h3>the story goes here</h3>", width=1200, height=800)

   saveWebpageProgressTextArea = dcc.Textarea(id="saveWebpageProgressTextArea",
                                              placeholder='progress info will appear here',
                                              value="",
                                              style={'width': 600, 'height': 30})

   children = [html.Br(), createButton, displayButton, downloadWebpageButton, html.Br(), textArea,
               html.Br(), webPageIframe, saveWebpageProgressTextArea]

   div = html.Div(children=children, id='createWebPageDiv', style={'display': 'block'})

   return div

#----------------------------------------------------------------------------------------------------
def create_masterDiv():

   style = {'border': '1px solid green',
            'border-radius': '5px',
            'padding': '10px'}

   title = html.H4("Status")
   eafStatus = html.Label("EAF: ", id="eafStatusLabel", style={"font-size": 14})
   soundStatus = html.Label("Sound: ")
   tierMapStatus = html.Label("Tier map: ")
   grammaticalTermsStatus = html.Label("Grammatical terms: ")
   run_button = html.Button("Run", style=buttonStyle)

   children = [title, eafStatus, soundStatus, tierMapStatus, grammaticalTermsStatus,
               html.Br(), run_button]

   div = html.Div(children=children, id='master-div', className="four columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_uploadsDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '1px'}

   tabsStyle = {'width': '100%',
                'fontFamily': 'Sans-Serif',
                'font-size': 12,
                'margin-left': 'auto',
                'margin-right': 'auto'
                }

   tabs = dcc.Tabs(id="tabs-example", value='tab-1-example',
                   children=[dcc.Tab(label='Set Title', children=create_setTitleTab()),
                             dcc.Tab(label='EAF', children=create_eafUploaderTab()),
                             dcc.Tab(label='Sound', children=create_soundFileUploaderTab()),
                             dcc.Tab(label='Tier Map', children=create_tierMapUploaderTab()),
                             dcc.Tab(label='Tier GUI', children=create_tierGuiTab()),
                             dcc.Tab(label='GrammaticalTerms', children=create_grammaticalTermsUploaderTab()),
                             dcc.Tab(label='EAF+Sound', children=create_associateEAFandSoundTab()),
                             dcc.Tab(label='Create Web Page', children=create_webPageCreationTab()),


                   ], style=tabsStyle)

   children = tabs;
   div = html.Div(children=children, id='uploads-div', className="twelve columns") # , style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_allDivs():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '1px'}


   style = {'margin': 20,
            'border': '1px solid #aaa;',
            'border-radius': 4,
            'padding': '.5em .5em 0'}

   children = [
       html.H4("IJAL Upload", style={'text-align': 'center'}, id='pageTitleH4'),
       html.Details([html.Summary('Set Title'), html.Div(create_setTitleTab())], style=style),
       html.Details([html.Summary('EAF'), html.Div(create_eafUploaderTab())], style=style),
       html.Details([html.Summary('Sound'), html.Div(create_soundFileUploaderTab())], style=style),
       html.Details([html.Summary('Tier Guide, option 1: upload from file'), html.Div(create_tierMapUploaderTab())], style=style),
       html.Details([html.Summary('Tier Guide, option 2: specify interactively'), html.Div(create_tierMapGui())], style=style),
       html.Details([html.Summary('GrammaticalTerms'), html.Div(create_grammaticalTermsUploaderTab())], style=style),
       html.Details([html.Summary('EAF+Sound'), html.Div(create_associateEAFandSoundTab())], style=style),
       html.Details([html.Summary('Create Web Page'), html.Div(create_webPageCreationTab())], style=style)]

   div = html.Div(children=children, id='main-div', className="twelve columns") # , style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('tierMapDiv'),
               html.Label('tierMap upload'),
               html.Label('tierMap display')]

   div = html.Div(children=children, id='tierMap-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapGui():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   helpText = dcc.Markdown(dedent('''
There are four standard interlinear tiers.  We ask that you associate your tier names with them, using the
dropdown menus below.

* speech
* translation (into the linguist's language)
* morpheme
* morphemeGloss

In addition, we ask you to specify whether morpheme's and their glosses are packed
into a single eaf XML line (separated by tabs) or spread out over multiple xml elements.
'''))


   helpTextDisplay = html.Div(children=helpText,
                        style={'margin': 100,
                               'margin-top': 10,
                               'margin-bottom': 10,
                               'border': '1px solid gray',
                               'border-radius': 5,
                               'padding': 20,
                               'width': "80%"})

   #button = html.Button("Extract tier Ids", id="extractTierIDsButton", style={"width": 180})

   tierIDsBlankDiv = html.Div(children=[html.H4("blank")], id="tierIDsBlankDiv")

   dropDownMenus = html.Table(id='tierMappingMenus')
   submitInteractiveTierMapButton =  html.Button("Submit", style=buttonStyle, id="submitInteractiveTierMapButton")


      # just to keep dash happy.  i hope this is replaced by dynamically created pulldown menus
   #menuPlaceHolderElement =  html.P(id='tierGuideMenu', children="", style={'display': 'none'}),


   #      html.Tr([html.Th("Standard interlinear tiers"), html.Th("User tiers (from EAF file)", style={'width': "60%"})]),
   #      html.Tr([html.Td("speech"), html.Td(createPulldownMenu(userTiers))]),
   #      html.Tr([html.Td("translation"), html.Td(createPulldownMenu(userTiers))]),
   #      html.Tr([html.Td("morpheme"), html.Td(createPulldownMenu(userTiers))]),
   #      html.Tr([html.Td("morphemeGloss"), html.Td(createPulldownMenu(userTiers))]),
   #      html.Tr([html.Td("morphemePacking"), html.Td(createPulldownMenu(["tabs", "lines"]))])
   #      ], style={'margin': 100, 'margin-top': 20, 'width': 600}
   #      )

   textArea = dcc.Textarea(id='writeTierGuideFileTextArea',
                           placeholder='tier guide write status goes here',
                           value="",
                           style={'width': 600, 'height': 50})

   div = html.Div(children=[helpTextDisplay,
                            dropDownMenus,
                            tierIDsBlankDiv,
                            submitInteractiveTierMapButton,
                            #menuPlaceHolderElement,
                            html.Br(),
                            textArea],
                  id='tierMapGui-div', className="twelve columns") #, style=style)

   return div

#----------------------------------------------------------------------------------------------------
def createTierMappingMenus(eafFilename):

   dropDownMenus = html.H5("failure in extracting tierIDs from %s" % eafFilename)

   if(os.path.exists(eafFilename)):
      tmpDoc = etree.parse(eafFilename)
      userTiers = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
      print(userTiers)

      dropDownMenus = html.Table(id='tierMappingMenus', children=[
         html.Tr([html.Th("Standard interlinear tiers"), html.Th("User tier names (from EAF file)", style={'width': "60%"})]),
         html.Tr([html.Td("speech"), html.Td(createPulldownMenu(userTiers))]),
         html.Tr([html.Td("translation"), html.Td(createPulldownMenu(userTiers))]),
         html.Tr([html.Td("morpheme"), html.Td(createPulldownMenu(userTiers))]),
         html.Tr([html.Td("morphemeGloss"), html.Td(createPulldownMenu(userTiers))]),
         html.Tr([html.Td("morphemePacking"), html.Td(createPulldownMenu(["tabs", "lines"]))])
         ], style={'margin': 100, 'margin-top': 20, 'width': 600}
         )

   return dropDownMenus

#----------------------------------------------------------------------------------------------------
#  tmpDoc = etree.parse(filename)
#  tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
#  print(tierIDs)
def createPulldownMenu(items):
   options = []
   for item in items:
       newElement={"label": item, "value": item}
       options.append(newElement)

   menu = dcc.Dropdown(options=options, clearable=False, id="tierGuideMenu")
   return(menu)

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsDiv():

   style = {'border': '1px solid purple',
            'border-radius': '5px',
            'padding': '10px'}

   children = [html.Label('grammaticalTermsDiv'),
               html.Label('grammaticalTerms upload'),
               html.Label('grammaticalTerms display')]

   div = html.Div(children=children, id='grammaticalTerms-div', className="three columns", style=style)

   return div

#----------------------------------------------------------------------------------------------------
def parse_eaf_upload(contents, filename, date):

   print("filename selected: %s" % filename)
   #pdb.set_trace()
   content_type, content_string = contents.split(',')
   nchar = len(content_string)
   print("%s (%s): %d characters" % (filename, content_type, nchar))
   return(nchar)

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        #create_masterDiv(),
        #create_uploadsDiv(),
        create_allDivs(),
        html.P(id='projectTitle_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='projectDirectory_hiddenStorage',          children="", style={'display': 'none'}),
        html.P(id='eaf_filename_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='sound_filename_hiddenStorage',            children="", style={'display': 'none'}),
        html.P(id='audioPhraseDirectory_hiddenStorage',      children="", style={'display': 'none'}),
        html.P(id='grammaticalTerms_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='tierGuide_filename_hiddenStorage',        children="", style={'display': 'none'}),
        ],
    className="row",
    id='outerDiv',
    style={'margin':  '10px',
           'padding': '20px',
           #'border': '1px blue solid',
           'border-radius': "5px",
           'height':  '300px',
        })

#----------------------------------------------------------------------------------------------------
# @app.callback(Output('eafStatusLabel', 'children'),
#              [Input('upload-eaf-file', 'contents')],
#              [State('upload-eaf-file', 'filename'),
#               State('upload-eaf-file', 'last_modified')])
#def updateEafLabel(contents, name, date):
#   if name is None:
#       return "EAF: "
#   if name is not None:
#       print("on_eafUpload, name: %s" % name)
#       return "EAF: %s" % name
#
#----------------------------------------------------------------------------------------------------
@app.callback(Output('eafUploadTextArea', 'value'),
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('upload-eaf-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_eafUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("on_eafUpload, name: %s" % name)
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    with open(filename, "wb") as fp:
         fp.write(base64.decodebytes(data))
         fileSize = os.path.getsize(filename)
         print("eaf file size: %d" % fileSize)
         schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
         validXML = schema.is_valid(filename)
         eaf_validationMessage = "%s: (%d bytes), valid XML: %s" % (filename, fileSize, validXML)
         if(not validXML):
            try:
               schema.validate(filename)
            except xmlschema.XMLSchemaValidationError as e:
               failureReason = e.reason
               eaf_validationMessage = "%s failure.  error: %s" % (filename, failureReason)
         return eaf_validationMessage

#----------------------------------------------------------------------------------------------------
@app.callback(Output('soundFileUploadTextArea', 'value'),
              [Input('upload-sound-file', 'contents')],
              [State('upload-sound-file', 'filename'),
               State('upload-sound-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_soundUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_soundUpload")
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    with open(filename, "wb") as fp:
       fp.write(base64.decodebytes(data))
       fileSize = os.path.getsize(filename)
       errorMessage = ""
       validSound = True
       try:
          rate, mtx = wavfile.read(filename)
       except ValueError as e:
          print("exeption in wavfile: %s" % e)
          rate = -1
          validSound = False
          errorMessage = str(e)
       print("sound file size: %d, rate: %d" % (fileSize, rate))
       sound_validationMessage = "%s:  (%d bytes), valid sound: %s %s" % (filename, fileSize,
                                                                          validSound, errorMessage)
       return sound_validationMessage

#----------------------------------------------------------------------------------------------------
@app.callback(Output('tierMapUploadTextArea', 'value'),
              [Input('upload-tierMap-file', 'contents')],
              [State('upload-tierMap-file', 'filename'),
               State('upload-tierMap-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_tierMapUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_tierMapUpload")
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    s = decodedString.decode('utf-8')
    yaml_list = yaml.load(s)
    filename = os.path.join(projectDirectory, name)
    with open(filename, "w") as fp:
       fp.write(s)
       fp.close()

    return("%s:\n %s" % (filename, s))

#----------------------------------------------------------------------------------------------------
@app.callback(Output('grammaticalTermsUploadTextArea', 'value'),
              [Input('upload-grammaticalTerms-file', 'contents')],
              [State('upload-grammaticalTerms-file', 'filename'),
               State('upload-grammaticalTerms-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_grammaticalTermsUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_grammaticalTermsUpload")
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    s = decodedString.decode('utf-8')
    yaml_list = yaml.load(s)
    filename = os.path.join(projectDirectory, name)
    with open(filename, "w") as fp:
       fp.write(s)
       fp.close()

    return("%s: %s" % (filename, s))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('associateEAFAndSoundInfoTextArea', 'value'),
    [Input('extractSoundsByPhraseButton', 'n_clicks')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage',   'children'),
     State('projectTitle_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage',   'children'),
    ])
def on_extractSoundPhrases(n_clicks, soundFileName, eafFileName, projectTitle, projectDirectory):
    if n_clicks is None:
        return("")
    print("=== on_extractSoundPhrases")
    print("n_clicks: %d" % n_clicks)
    if soundFileName is None:
        return("")
    if eafFileName is None:
        return("")
    soundFileName = soundFileName
    eafFileName = eafFileName
    eafFileFullPath = eafFileName # os.path.join(UPLOAD_DIRECTORY, eafFileName)
    soundFileFullPath = soundFileName # os.path.join(UPLOAD_DIRECTORY, soundFileName)
    print("soundFileName: %s" % soundFileName)
    print("eafFileName: %s" % eafFileName)
    phraseFileCount = extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory)
    print("after extractPhrases")
    return("%s: %d phrases" % (projectDirectory, phraseFileCount))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('sound_filename_hiddenStorage', 'children'),
    [Input("soundFileUploadTextArea", 'value')])
def update_output(value):
    print("=== update_output")
    print("sound_filename_hiddenStorage assignment, callback triggered by soundFileUploadTextArea change: %s" % value)
    soundFileName = value.split(":")[0]
    return(soundFileName)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('eaf_filename_hiddenStorage', 'children'),
    [Input("eafUploadTextArea", 'value')])
def update_output(value):
    print("=== eaf_filename_hiddenStorage assignment, callback triggered by eafUploadTextArea change: %s" % value)
    eafFileName = value.split(":")[0]
    return(eafFileName)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierIDsBlankDiv', 'children'),
    [Input("eaf_filename_hiddenStorage", 'children')])
def createTierMappingMenusCallback(eafFilename):
    if(eafFilename == ""):
       return("")
    print("=== extract tier ids from %s" % (eafFilename))
    #return(html.H4("infinite loop?"))
    return(createTierMappingMenus(eafFilename))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('audioPhraseDirectory_hiddenStorage', 'children'),
    [Input('associateEAFAndSoundInfoTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by assocateEAFAndSoundTextArea change: %s" % value)
    phraseDirectory = value.split(":")[0]
    return(phraseDirectory)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('grammaticalTerms_filename_hiddenStorage', 'children'),
    [Input('grammaticalTermsUploadTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by grammaticalTermsUploadTextArea change: %s" % value)
    grammaticalTermsFile  = value.split(":")[0]
    return(grammaticalTermsFile)

#----------------------------------------------------------------------------------------------------
# @app.callback(
#     Output('tierIDsBlankDiv', 'children'),
#     [Input('extractTierIDsButton', 'n_clicks')],
#     [State('eaf_filename_hiddenStorage', 'children')])
# def createTierMappingMenusCallback(n_clicks, eafFilename):
#     if n_clicks is None:
#         return("")
#     print("=== extract tier ids from %s: %d" % (eafFilename, n_clicks))
#     #return(html.H4("infinite loop?"))
#     return(createTierMappingMenus(eafFilename))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierGuide_filename_hiddenStorage', 'children'),
    [Input('tierMapUploadTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by grammaticalTermsUploadTextArea change: %s" % value)
    tierGuideFile  = value.split(":")[0]
    return(tierGuideFile)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('createWebPageInfoTextArea', 'value'),
    [Input('createWebPageButton', 'n_clicks')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage', 'children'),
     State('grammaticalTerms_filename_hiddenStorage', 'children'),
     State('tierGuide_filename_hiddenStorage', 'children')])
def createWebPageCallback(n_clicks, soundFileName, eafFileName, projectDirectory,
                          grammaticalTermsFile, tierGuideFile):
    if n_clicks is None:
        return("")
    print("=== create web page callback")
    print("        eaf: %s", eafFileName)
    print(" phrases in: %s", projectDirectory)
    if(grammaticalTermsFile == ""):
        grammaticalTermsFile = None
    html = createWebPage(eafFileName, projectDirectory, grammaticalTermsFile, tierGuideFile)
    absolutePath = os.path.abspath(os.path.join(projectDirectory, "text.html"))
    file = open(absolutePath, "w")
    file.write(html)
    file.close()
    #url = 'file:///%s' % absolutePath

    #url = 'http://0.0.0.0:8050/%s/text.html' % projectDirectory
    #webbrowser.open(url, new=2)
    return("wrote file")


#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('projectTitle_hiddenStorage', 'children'),
    [Input('setTitleButton', 'n_clicks'),
     Input('setTitleTextInput', 'value')]
    )
def setTitle(n_clicks, newTitle):
    print("=== title callback")
    if n_clicks is None:
        print("n_clicks is None")
        return("")
    print("nClicks: %d, currentTitle: %s" % (n_clicks, newTitle))
    print("--- set project title")
    #projectDirectory = os.path.join(PROJECTS_DIRECTORY, newTitle)
    #print("   creating projectDirectory if needed: %s" % projectDirectory)
    #if(not os.path.exists(projectDirectory)):
    #   os.mkdir(projectDirectory)
    return(newTitle)

@app.callback(
    Output('projectDirectory_hiddenStorage', 'children'),
    [Input('projectTitle_hiddenStorage', 'children')]
    )
def update_output(projectTitle):
    if(len(projectTitle) == 0):
        return('')
    print("=== project title has been set, now create project directory: '%s'" % projectTitle)
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectTitle)
    print("   creating projectDirectory if needed: %s" % projectDirectory)
    if(not os.path.exists(projectDirectory)):
        os.mkdir(projectDirectory)
    return(projectDirectory)

@app.callback(
    Output('pageTitleH4', 'children'),
    [Input('projectDirectory_hiddenStorage', 'children')]
    )
def update_pageTitle(projectDirectory):
    if(len(projectDirectory) == 0):
        return('IJAL Upload')
    print("=== projectDirectory_hiddenStorage has been set, now change project pageTitle: '%s'" % projectDirectory)
    #pdb.set_trace()
    newProjectTitle = projectDirectory.replace(PROJECTS_DIRECTORY, "")
    newProjectTitle = newProjectTitle.replace("/", "")
    return("IJAL Upload: %s" % newProjectTitle)

# @app.callback(
# Output('writeTierGuideFileTextArea', 'value'),
#    [Input('submitInteractiveTierMapButton', 'n_clicks'),
#     Input('tierGuideMenu', 'children')])
# def saveTierGuideToFile(n_clicks, menuValue):
#    if n_clicks is None:
#       return("")
#    print("need to saveTierGuidToFile");
#    return("pretese: saved choices")

@app.callback(
    Output('storyIFrame', 'src'),
    [Input('displayIJALTextButton', 'n_clicks'),
     Input('projectDirectory_hiddenStorage', 'children')])
def displayText(n_clicks, projectDirectory):
   if n_clicks is None:
      return("")
   print("=== displayText")
   pathToHTML = os.path.join(projectDirectory, "text.html")
   return(pathToHTML)

@app.callback(
    Output('saveWebpageProgressTextArea', 'value'),
    [Input('downloadWebpageButton', 'n_clicks'),
     Input('projectTitle_hiddenStorage', 'children')])
def saveWebpage(n_clicks, projectTitle):
   if n_clicks is None:
      return("")
   createZipFile(projectTitle)
   return("wrote web page as zip file")


#----------------------------------------------------------------------------------------------------
def extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory):

    print("------- entering extractPhrases")
    print("soundFileFullPath: %s" % soundFileFullPath)
    print("projectDirectory: %s" % projectDirectory)
    audioDirectory = os.path.join(projectDirectory, "audio")

    if not os.path.exists(audioDirectory):
        os.makedirs(audioDirectory)

    ea = AudioExtractor(soundFileFullPath, eafFileFullPath, audioDirectory)
    assert(ea.validInputs)
    ea.extract(quiet=True)
    phraseFileCount = len(os.listdir(audioDirectory))
    return(phraseFileCount)

#----------------------------------------------------------------------------------------------------
def createWebPage(eafFileName, projectDirectory, grammaticalTermsFileName, tierGuideFileName):

    print("-------- entering createWebPage")
    # pdb.set_trace()
    #audioDirectory = os.path.join(projectDirectory, "audio")
    audioDirectoryRelativePath = "audio"
    print("eafFileName: %s" % eafFileName)
    print("projectDirectory: %s" % projectDirectory)
    print("audioDirectoryRelativePath: %s" % audioDirectoryRelativePath)
    print("grammaticalTermsFile: %s" % grammaticalTermsFileName)
    print("tierGuideFile: %s" % tierGuideFileName)

    text = Text(eafFileName,
                audioDirectoryRelativePath,
                grammaticalTermsFileName,
                tierGuideFileName)

    return(text.toHTML())

#----------------------------------------------------------------------------------------------------
def createZipFile(projectName):

   currentDirectoryOnEntry = os.getcwd()
   projectDir = os.path.join(PROJECTS_DIRECTORY, projectName)
   os.chdir(projectDir)

   audioDir = "audio"
   filesToSave = [os.path.join("audio", f) for f in os.listdir(audioDir) if f.endswith('.wav')]
   filesToSave.insert(0, "text.html")

   zipFilename = "webpage.zip"
   zipHandle = ZipFile(zipFilename, 'w')

   for file in filesToSave:
      zipHandle.write(file)

   zipHandle.close()

   os.chdir(currentDirectoryOnEntry)

#----------------------------------------------------------------------------------------------------
server = app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=60041)
