# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

userTiers = ["lushootseedSpeech",
             "phonemicLushootseed",
             "phonemicTranslation",
             "englishGloss"]

standardTiers=["speech", "translation", "morpheme", "morphemeGloss", "morphemePacking"]


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


app.layout = html.Div(children=[
    html.H4("Assign your tiers to the standard slexil tiers",
            style={'margin-left': 100}),

    html.Div(children=helpText,
        style={'margin': 100,
               'margin-top': 10,
               'margin-bottom': 10,
               'border': '1px solid gray',
               'border-radius': 5,
               'padding': 20,
               'width': "40%"}),

    html.Table([
        html.Tr([html.Th("Standard interlinear tiers"), html.Th("User tiers (from EAF file)", style={'width': "60%"})]),
        html.Tr([html.Td("speech"), html.Td(createPulldownMenu(userTiers))]),
        html.Tr([html.Td("translation"), html.Td(createPulldownMenu(userTiers))]),
        html.Tr([html.Td("morpheme"), html.Td(createPulldownMenu(userTiers))]),
        html.Tr([html.Td("morphemeGloss"), html.Td(createPulldownMenu(userTiers))]),
        html.Tr([html.Td("morphemePacking"), html.Td(createPulldownMenu(["tabs", "lines"]))])
        ], style={'margin': 100, 'margin-top': 20, 'width': 600}
    )
])

def createPulldownMenu(choicesFoo):
   options = []
   for item in choicesFoo:
       newElement={"label": item, "value": item}
       options.append(newElement)

   menu = dcc.Dropdown(options=options, clearable=False)
   return(menu)

#if __name__ == '__main__':
# app.run_server(debug=True)
