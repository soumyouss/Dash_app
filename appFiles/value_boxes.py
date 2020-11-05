import dash_html_components as html
import dash_admin_components as dac
import pandas as pd

df = pd.read_csv("data/coronavirus1.csv")
nb_pays = len(df["countryCode"].unique())
cas_confirmes = df["confirmed"].sum()
cas_gueris = df["recovered"].sum()
deces = df["death"].sum()
cas_actifs = cas_confirmes - cas_gueris - deces


value_boxes_row = html.Div([
  html.H4('Value Boxes'),
        html.Div([
            dac.ValueBox(
                value=cas_confirmes,
                subtitle="Cas confirmes",
                color = "primary",
                icon = "shopping-cart",
                href = "#"
            ),
            dac.ValueBox(
              elevation = 4,
              value = cas_actifs,
              subtitle = "Cas actifs",
              color = "warning",
              icon = "cogs"
            ),
            dac.ValueBox(
              value = cas_gueris,
              subtitle = "Guéris",
              color = "success",
              icon = "suitcase"
            ),
            dac.ValueBox(
              value = deces,
              subtitle = "Décès",
              color = "danger",
              icon = "database"
            )
        ], className='row'),
        html.H4('Info Boxes'),
        html.Div([
            dac.InfoBox(
              title = "Messages",
              value = 1410,
              icon = "envelope"
            ),
            dac.InfoBox(
              title = "Bookmarks",
              color = "info",
              value = 240,
              icon = "bookmark"
            ),
            dac.InfoBox(
              title = "Comments",
              gradient_color = "danger",
              value = 41410,
              icon = "comments"
            )
        ], className='row'),
  ])