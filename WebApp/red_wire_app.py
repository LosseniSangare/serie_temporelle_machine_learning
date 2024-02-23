# red_wire_app v0.1
#   Draft & untested initial version


#################
# Import & Load #
#################

# Import Python librairies
import numpy as np
import pandas as pd

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dash import no_update
from dash_extensions.enrich import Output, DashProxy, Input, State, MultiplexerTransform
from dash.exceptions import PreventUpdate

from predict import load_model_and_predict
from connect import create_session, get_last_connection_date, register_new_connection
from visualize import make_figure_from_prediction

# Set application path and load data(sub)set
app_path = '/var/www/red-wire/'
file_path = 'data/REE_data.csv'
data_df = pd.read_csv(app_path+file_path, encoding = "ISO-8859-1")


#############################
# Declare dataset variables #
#############################

# Create lists that will be used to manage Dash inputs
# 1) List of model inputs
input_ids =     ['start', 'end']
# 2) List of model inputs translated in the language of the application interface
input_labels =  ["Début de période", "Fin de période"]
# 3) List of short descriptions of model inputs
input_notes =   ["choisissez la date de début", "choisissez la date de fin"]


# The code below manages the user interface using Dash tabs and callbacks

########################################
# Declare Dash variables and functions #
########################################

# Function to determine greeting text on user connection
def get_greeting_text(name):
    session = create_session(app_path)
    last_date = get_last_connection_date(session, name)
    register_new_connection(session, name)
    session.commit()

    if last_date is None:
        text1 = f"Bonjour {name}"
        text2 = "Bienvenue dans notre application !"
    else:
        formatted_date = last_date.strftime("%d/%m/%Y à %H:%M:%S")
        text1 = f"Bonjour {name}, vous êtes de retour !"
        text2 = [
                    "Nous sommes heureux de vous revoir.",
                    html.Br(),
                    f"Votre dernière connexion a eu lieu le {formatted_date}."
                ]
    return text1, text2

# Global parameters for Dash
app = DashProxy(
    __name__,
    prevent_initial_callbacks=True,
    transforms=[MultiplexerTransform()],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = 'Red Wire App.'

# Application name and logo displayed on top left of all tabs
logo_and_title = dbc.Row(
    [
        dbc.Col(
            html.Img(
                src=dash.get_asset_url("logo_utt_eut.png"),
                className="img-fluid",
            ),
            width=4,
        ),
        dbc.Col(
            [
                html.H1("Red Wire App.", style={"color": "orange"}),
                html.H4("Prévisions de consommation électrique en Espaggne", style={"color": "blue"}),
            ],
            width=8,
            className="text-center",
        ),
    ],
    # Use flexible display and make zero gap between columns
    className="d-flex g-0 align-items-center mb-4",
)

# Home button managed by HIDE_HOME_BUTTON
home_button = dbc.Row(
    [
        dbc.Col(dbc.Button("Revenir à l'accueil", className="btn-secondary", id="home-button"))
    ],
    className="mb-4"
)

# Buttons on first 4 tabs, allowing to get to the next tab up to the 5th and last tab
buttons = [
    # Button to get from Home tab to Connection tab
    dbc.Button("Commencer", id="start-button"),

    # Button to get from Connection tab to Welcome tab
    dbc.Button("Se connecter", id="connect-button"),

    # Button to get from Welcome tab to Parameters tab
    dbc.Button("Lancer l'application", id="launch-button"),

    # Button to get from Parameters tab to Result tab
    dbc.Button("Obtenir une prédiction", id="predict-button"),

    # Button to get back to Parameters tab from Result tab
    dbc.Button("Modifier les paramètres", id="param-button"),
]

# Input form for model parameters, other than those selecting an area and its default parameter values
input_form = []
for i in range(0, len(input_ids)):
    input_form.append(
        html.Div(
            [
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(input_labels[i]),
                        dbc.Input(id=input_ids[i], placeholder=input_notes[i], type="number"),
                        dbc.Alert("Veuillez entrer une valeur.", color="danger", fade=True, is_open=False, id="alert-"+str(i)),
                    ]
                )
            ],
            className="mb-2",
        )
    )

# Function to increment active_tab_number and get to the next tab
def get_next_tab(active_tab):
    # Extract the 5th character of active_tab_number, which is the current tab number
    active_tab_number = int(active_tab[4:])
    # Increment active_tab_number except when getting back from the 5th (Result) tab to the 4th (Parameters) tab
    if active_tab_number == 4:
        return f"tab-{3}"
    else:
        return f"tab-{active_tab_number + 1}"

# Dash parameters to control displaying tabs and home button
HIDE_TABS = True
HIDE_HOME_BUTTON = False

# Debug flag to control console output
PRINT_to_LOG = False


#####################
# Declare Dash tabs #
#####################

tabs = dbc.Tabs([
    # 1st (Home) tab linked to button_to_next_tab callback
    dbc.Tab(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H5("Consultez des données obervées ou obtenez des prédictions de la consommation\
                                électrique en Espagne en sélectionnant une période passée ou future."),
                        style={'text-align': 'justify'}
                    )
                ],
                className="mt-4 mb-5",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.H5(f"Grâce à cette application vous pourrez..."),
                                style={"color": "blue"},
                                className="text-left pt-3"),
                        dbc.CardBody([
                            dcc.Markdown('''
                                + Consulter des données sur la consommation électrique en Espagne jusqu'à J-1
                                + Obtenir des prédictions de consommation électrique totale.
                            '''),
                        ],
                        style={'fontSize': '1.2em', 'font-weight': '500', 'margin-left': '-0.6em', 'padding-top': '1.2em'},
                        className="text-left",
                        ),
                    ])),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    # Bouton 'Commencer'
                    dbc.Col(buttons[0]),
                ],
                className="mb-4",
            ),
        ],
        label="Accueil"
    ),

    # 2nd (Connection) tab linked to button_to_next_tab and enter_id callbacks
    dbc.Tab(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.H5("Connectez vous pour commencer l'expérience",
                                    style={"color": "blue"},
                                    className="text-left pt-1")
                            ),
                            dbc.CardBody([
                                html.P(
                                    [
                                        dbc.Input(id="name-box", placeholder="Entrez votre nom"),
                                    ],
                                    className="mt-2 mb-2"
                                ),
                            ])
                        ])
                    )
                ],
            className="mb-4",
            ),
            dbc.Row(
                [
                    # Bouton 'Se connecter'
                    dbc.Col(buttons[1]),
                ],
                className="mb-4",
            )
        ],
        label="Connexion"
    ),

    # 3rd (Welcome) tab linked to button_to_next_tab and enter_id callbacks
    dbc.Tab(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card([
                        dbc.CardHeader(
                            html.H5(id="welcome-box1"),
                            style={"color": "blue"},
                            className="card-title text-left pt-3",
                        ),
                        dbc.CardBody(
                            html.P(id="welcome-box2"),
                            style={'fontSize': '1.1em', 'font-weight': '400'},
                            className="card-text text-left pt-4",
                        ),
                    ])),
                ],
                className="mb-4",
            ),
            dbc.Row([
                # Bouton 'Lancer l'application'
                dbc.Col(
                    buttons[2],
                    className="text-left mb-2",
                )
            ])
        ],
        label="Bienvenue"
    ),

    # 4th (Parameters) tab linked to several callbacks
    # Select an area and display/modify default parameter values
    dbc.Tab(
        [
            dbc.Form(
                [
                    html.H5(
                        "Sélectionnez une date de début et de fin de période.",
                        style={"color": "blue"},
                        className="mb-4"),
                ]
                # Input form displaying model parameters and their default values for the selected area
                + input_form
                # Button to get model prediction
                + [buttons[3]],
                className="mb-2",
            )
        ],
        label="Paramètres"
    ),

    # 5th (Result) tab
    # Display model prediction for the selected area based on selected parameter values
    dbc.Tab(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.H5(f"Valeurs courantes et prédictions"),
                                style={"color": "blue"},
                                className="text-center pt-3"),
                            dbc.CardBody(id="prediction-card")
                        ]),
                        className="mb-2",
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.H5(f"Comparaison graphique"),
                                style={"color": "blue"},
                                className="text-center pt-3"),
                            dbc.CardBody(dcc.Graph(id="prediction-graph")),
                        ]),
                        className="mb-2"
                    ),
                ],
            ),
            dbc.Row(
                [
                    # Button to modify model parameters
                    dbc.Col(
                        buttons[4],
                        className="mb-2",
                    ),
                ]
            ),
        ],
        label="Résultat"
    ),
], id="tabs", className="mb-4")


######################
# Application layout #
######################

if HIDE_TABS:
    tabs.className += " d-none"

if HIDE_HOME_BUTTON:
    home_button.className += " d-none"

app.layout = dbc.Container([
    # Full screen = 1 row
    dbc.Row(
        [
            # Left half of screen = 1st Col showing app header and tabs
            dbc.Col(
                [
                    logo_and_title,
                    home_button,
                    dbc.Row(
                        [
                            dbc.Col(tabs)
                        ]
                    ),
                ],
                # 12/12 = full screen on small and medium displays
                sm=12,
                # 6/12 = half of screen on large and extra-large displays
                lg=6,
            ),

            # Right half of the screen = 2nd Col showing image
            dbc.Col(
                html.Img(
                    src=dash.get_asset_url("solar_panels_on_ground.webp"),
                    style={'width': '80%'},
                    # Picture shown on large and extra-large displays only
                    className="d-sm-none d-lg-block mt-4 mb-4",
                ),
                # 0/12 = column not shown on small and medium displays
                sm=0,
                # 6/12 = half of screen on large and extra-large displays
                lg=6,
                style={'background-image': 'url(/assets/rectangle_blue_bubbles.webp)'},
                className="d-flex align-items-center",
            ),
        ],
        className="mt-4"
    ),
])


##########################
# Declare Dash CallBacks #
##########################

# Manage Home button
@app.callback(
    Output(component_id="tabs", component_property="active_tab"),

    Input(component_id="home-button", component_property="n_clicks"),
)
def home_button(n_clicks):
    return "tab-0"


# Manage Start and (application) Launch buttons on Home and Welcome tabs
@app.callback(
    Output(component_id="tabs", component_property="active_tab"),

    State(component_id="tabs", component_property="active_tab"),

    Input(component_id="start-button", component_property="n_clicks"),
    Input(component_id="launch-button", component_property="n_clicks"),
    Input(component_id="param-button", component_property="n_clicks"),
)
def button_to_next_tab(active_tab, *args):
    return get_next_tab(active_tab)


# Manage input for user identification
@app.callback(
    Output(component_id="welcome-box1", component_property="children"),
    Output(component_id="welcome-box2", component_property="children"),
    Output(component_id="tabs", component_property="active_tab"),
    Output(component_id="name-box", component_property="invalid"),

    State(component_id="name-box", component_property="value"),
    State(component_id="tabs", component_property="active_tab"),

    Input(component_id="connect-button", component_property="n_clicks"),
)
def enter_id_callback(name, active_tab, n_clicks):
    if name is None:
        return no_update, no_update, True

    text1, text2 = get_greeting_text(name)

    return text1, text2, get_next_tab(active_tab), False

# Gather all parameters, launch model prediction and trigger Result tab
@app.callback(
    Output(component_id="prediction-card", component_property="children"),
    Output(component_id="prediction-graph", component_property="figure"),
    Output(component_id="tabs", component_property="active_tab"),
    Output(component_id="alert-0", component_property="is_open"),
    Output(component_id="alert-1", component_property="is_open"),

    # Start and end dates
    inputs=[State(component_id=input_ids[0], component_property="value"),
    State(component_id=input_ids[1], component_property="value"),

    State(component_id="tabs", component_property="active_tab"),

    Input(component_id="predict-button", component_property="n_clicks")],
)
def get_result_callback(start_date, end_date, input_values, active_tab, n_clicks):
    if PRINT_to_LOG:
        print("******************************")
        print("Date de début :", start_date)
        print("Date de fin :", end_date)

    # Trigger a warning for blank state, county or FIPS
    invalid_start = (start_date == None)
    invalid_end = (end_date == None)
    if invalid_start or invalid_end:
        return no_update, no_update, invalid_start, invalid_end

    if PRINT_to_LOG:
        print("Valeurs retenues :", input_values)
    current_val = data_df[data_df["datetime"]==start_date]["demand"].values[0]
    prediction = load_model_and_predict(app_path+'data/Deep_Solar_model', input_values, input_ids)

    if PRINT_to_LOG:
        print("******************************")
        print("Inputs du CallBack :", dash.callback_context.states)
        print("******************************")
        print("Consommation observée en MW :", current_val)
        print("Consommation prédite en MW :", prediction)

    prediction_element = [
            dbc.Row(
                [
                    html.P(f"Surface totale actuelle (base installée) : {current_val} m²"),
                    html.P(f"Surface totale modélisée (prédiction) : {prediction} m²")
                ],
            className="text-center",
            )
    ]

    # Build conclusion depending on predicted value < or > installed base
    if prediction-current_val >0:
        conclusion_element = [
            dbc.Row(
                html.H4(f"La prédiction dépasse la valeur observée de {prediction-current_val} MW."),
                style={"color": "darkorange"},
                className="text-center",
            )
        ]
    else:
        conclusion_element = [
            dbc.Row(
                html.H4(f"La prédiction est inférieure de {current_val-prediction} MW par rapport à la valeur observée."),
                style={"color": "darkorange"},
                className="text-center",
            )
        ]

    prediction_text = prediction_element + conclusion_element
    prediction_figure = make_figure_from_prediction(current_val, prediction)

    return prediction_text, prediction_figure, get_next_tab(active_tab), False, False, False

server = app.server
if __name__ == '__main__':
    app.run_server(debug=False)