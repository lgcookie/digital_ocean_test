
revenue_sources = ["dynamic_containment_low","dynamic_containment_high","dynamic_regulation_low","dynamic_regulation_high","dynamic_moderation_low","dynamic_moderation_high","wholesale_trading","balancing_mechanism","firm_frequency_response"]
colors = {
    'background': '#120d01',
    'text': '#2E2E2E',
    "header-text":"#ffffff",
    "graph_line_primary":'#ffffff',
    "graph_line_secondary":'#d40434',
    "graph_line_tertiary":'#9cd404',
    "graph_box":"2E2E2E",
    "black": "#282828",
    "plot-background":"rgba(0,0,0,0)",
    "PN":"#0F1EFF",
    "MELS":"#09BF0C",
    "MILS":"#0FC8FF",
    "QPN":"#D6E747",
    "MEL":"#09BF0C",
    "MIL":"#0FC8FF",
    "QPN":"#D6E747",
    "BOALF":"#F70000",
    "DCH":"#581845", #DARK RED,
    "DCL":"#F18888", #LIGHT RED,
    "DRH":"#3B00D9", #DARK BLUE
    "DRL":"#BEA6FF", #LIGHT BLUE,
    "DMH":"#008923", #DARK GREEN
    "DML":"#91EDA9", #LIGHT GREEN,
    "CM":"#d40434", # DARK GREY
    "dynamic containment high":"#581845", #DARK RED,
    "dynamic containment low":"#F18888", #LIGHT RED,
    "dynamic regulation high":"#3B00D9", #DARK BLUE
    "dynamic regulation low":"#BEA6FF", #LIGHT BLUE,
    "dynamic moderation high":"#008923", #DARK GREEN
    "dynamic moderation low":"#91EDA9", #LIGHT GREEN,
    "firm frequency response":"#d40434",
    "capacity market":"#d40434", # DARK GREY
    "balancing mechanism": "#DB6CFF",# LIGHT PURPLE
    "balancing mechanism import": "#DB6CFF",# LIGHT PURPLE
    "balancing mechanism export": "#DB6CFF",# LIGHT PURPLE
    "wholesale import":"#1B8D73",#TEAL
    "wholesale export":"#1B8D73",#TEAL,
    "wholesale trading":"#1B8D73",#TEAL
  "yellow":"#581845",
  "belectric_red":"rgba(241,136,136,1)",
  "belectric_grey":"rgba(212, 4, 52,1)",
  "mini-container":"#555555",
  "container":"#747474",
}
font = "BlinkMacSystemFont"
layout = dict(
    autosize=True,
    automargin=True,
    hovermode="closest",
    plot_bgcolor=colors["plot-background"],
    paper_bgcolor=colors["plot-background"],
    legend=dict(font=dict(size=14), orientation="h"),
    title="",
    font=dict(color=colors["header-text"],size=18),
    xaxis=dict(showline=False,linewidth=2,linecolor="white",showgrid=False),
    yaxis=dict(showline=False,linewidth=2,linecolor="white",showgrid=False),
    mapbox=dict(
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
    title_font_color=colors["header-text"],
    title_font=dict(
        title_font_color=colors["black"]
    )
)