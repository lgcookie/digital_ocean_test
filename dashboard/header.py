from dash import dcc, html
import dash_mantine_components as dmc
import dash_daq as daq
import dash
def make_header():
    return html.Div([
        # Store components
        dcc.Store(id="graph-layout", data=False),
        dcc.Store(id="graph-layout-blank", data=False),
        dcc.Store(id="optimisation-result", data=False),
        dcc.Store(id="data-theme", data="light"),
        dcc.Store(id="selected-colors", data=False),
        dcc.Location(id='url'),
        dcc.Store(id="inital-load", data=False),
        dcc.Store(id="dummy", data=False),
        html.Div(id="output-clientside"),

        # Mantine Header
        dmc.Header(
            height=70,
            fixed=True,
            className="header-container",
            children=[
                dmc.Container(
                    fluid=True,
                    children=[
                        dmc.Group(
                            position="apart",
                            align="center",
                            spacing="xl",
                            children=[
                                # Logo section
                                dmc.Group(
                                    children=[
                                        dmc.Anchor(
                                            href="/",
                                            children=[
                                                html.Img(
                                                    src="https://zenobe-cdn.theconstantmedia.com/wp-content/uploads/2022/05/Zenobe-Logo-2048x381.png",
                                                    id="logo-image",
                                                    style={
                                                        "height": "40px",
                                                        "width": "auto",
                                                        "marginTop": "15px"
                                                    },
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                
                                # Navigation and Theme Toggle Group
                                dmc.Group(
                                    position="right",
                                    align="center",
                                    children=[
                                        # Navigation Links
                                        dmc.Group(
                                            children=[
                                                dcc.Link(
                                                    page['name'],
                                                    href=page["relative_path"],
                                                    style={
                                                        "textDecoration": "none",
                                                        "marginRight": "20px",
                                                        "color": "var(--text-primary)",
                                                    }
                                                ) for page in dash.page_registry.values()
                                            ],
                                            spacing="lg",
                                        ),
                                        
                                        # Theme Toggle
                                        dmc.Group(
                                            children=[
                                                dmc.Text(
                                                    id="color-scheme",
                                                    size="sm",
                                                    className="theme-text"
                                                ),
                                                daq.BooleanSwitch(
                                                    id="color-switch",
                                                    on=False,
                                                    className="theme-switch"
                                                ),
                                            ],
                                            spacing="sm",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ])