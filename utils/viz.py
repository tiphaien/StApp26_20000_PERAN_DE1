# chart functions to enforce consistent style

"""Fonctions graphiques : même style pour toute l'app."""
import plotly.express as px

BLEU, ORANGE = "#2a78d6", "#eb6834"
MOIS_COURTS = ["janv", "févr", "mars", "avr", "mai", "juin",
               "juil", "août", "sept", "oct", "nov", "déc"]


def courbe_mois(graph):
    fig = px.line(graph, x="mois", y="taux", color="Type de contrôle", markers=True,
                  labels={"mois": "Mois de l'année 2024", "taux": "Prélèvements non conformes (%)"},
                  color_discrete_sequence=[BLEU, ORANGE])
    fig.update_traces(hovertemplate="%{y:.2f} %")
    fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=MOIS_COURTS)
    fig.update_yaxes(rangemode="tozero", ticksuffix=" %")
    fig.add_vrect(x0=9.6, x1=10.4, fillcolor=ORANGE, opacity=0.12, line_width=0,
                  annotation_text="Cévennes floods (mid-October)",
                  annotation_position="top left")
    return fig


def carte(par_dept, geojson, col_eval):
    fig = px.choropleth(par_dept, geojson=geojson, locations="dept", featureidkey="properties.code",
                        color="taux", color_continuous_scale="Blues", hover_name="dept",
                        hover_data={"dept": False, "taux": ":.1f", col_eval: True},
                        labels={"taux": "Non conformes (%)", col_eval: "Prélèvements évalués"})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def classement(top, taux_national, col_nc, col_eval):
    fig = px.bar(top, x="taux", y="dept", orientation="h",
                 labels={"taux": "Prélèvements non conformes (%)", "dept": "Département"},
                 hover_data={col_eval: True, col_nc: True, "taux": ":.1f"},
                 color_discrete_sequence=[BLEU])
    fig.update_yaxes(categoryorder="total ascending", type="category")
    fig.add_vline(x=taux_national, line_dash="dash", line_color=ORANGE,
                  annotation_text=f"Moyenne : {taux_national:.1f} %", annotation_position="top")
    fig.update_xaxes(ticksuffix=" %")
    fig.update_layout(height=150 + 25 * len(top))
    return fig