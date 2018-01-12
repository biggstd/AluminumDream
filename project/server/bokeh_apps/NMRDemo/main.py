"""
################################
Literature NMR Data - Bokeh Demo
################################

This application is divorced from any database. Rather, it
simply loads a set of demo metadata files.

"""

# General Imports
import pandas as pd

# Bokeh imports
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Select, HoverTool, TapTool
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Div
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap

# isaDream imports.
from isadream.nmr_demo_sa import *

COLORS = Spectral5

# Simulate the return from a database query.
# Build the investigation object.
invest = build_nmr_output()

# Run the search simulation.
matching_studies = get_studies_by_design_descriptor(invest, al_27_nmr)

# Convert the returned list of studies to pandas dataframes and python
# dictionaries for use in Bokeh's columnDataSource.
data_frame, metadata_dict = build_data_md_pair(matching_studies)

# Get the column names for use in the selectors.
columns = sorted(data_frame.columns)
discrete = [x for x in columns if data_frame[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(data_frame[x].unique()) > 20]

# Assign the columnDataSources.
source = ColumnDataSource()


def update_data():
    """Upodates the Bokeh ColumnDataSource with subsets of data
    collected from a search result."""

    # Set the X and Y values to those selected by the user.
    source.data = dict(
        x=data_frame[x_selector.value],
        y=data_frame[y_selector.value],
    )

    # Iterate over the entire dataframe generated by the 'search'
    # function, and add all of these generated columns to the
    # Bokeh ColumnDataSource.
    for col in list(data_frame):
        source.add(data=data_frame[col], name=col)


def tap_select_callback(attr, old, new):
    """The callback function for when a user uses the TapTool to
    select a single data point.
    """
    new_index = new['1d']['indices'][0]
    study_key = source.data['study_ID'][new_index]
    layout.children[1].children[2] = build_metadata_paragraph(study_key)


def build_hover_tool():
    """Constructs a Bokeh HoverTool instance based on current selections.
    """
    hover = HoverTool(
        tooltips=[
            ('X, Y', '($x, $y)'),
            ('ppm Al', '@{ppm aluminum}')
        ]
    )
    return hover


def create_figure():
    """
    Create the bokeh plot.
    """
    update_data()

    fig = figure(
        name='primary_figure',
        width=800,
    )

    if color.value != 'None':
        colors = factor_cmap(
            field_name=color.value,
            palette=Spectral5,
            factors=sorted(source.data[color.value].unique())
        )
    else:
        colors = "#31AADE"

    print(colors)
    print(type(colors))

    fig.circle(
        source=source,
        x='x',
        y='y',
        color=colors
    )

    x_title = x_selector.value
    y_title = y_selector.value

    fig.xaxis.axis_label = x_title
    fig.yaxis.axis_label = y_title

    fig.add_tools(build_hover_tool())
    fig.add_tools(TapTool())

    return fig


def update_plot(attr, old, new):
    """
    Define the function to be run upon an update call.
    """
    layout.children[1].children[1] = create_figure()
    pass


def format_assay_text(isa_assay_obj):
    """Prepares the ISA assay object for easy reading in an HTML
    format."""
    out_str = (
        '<strong>Publication Title</strong>: {}\n'
        'Publication DOI: {}\n'
        .format(
            isa_assay_obj.publications[0].title,
            isa_assay_obj.publications[0].doi
        )
    )
    return out_str


def build_metadata_paragraph(key=None):
    """Constructs an HTML paragraph based on a given key."""
    if key is None:
        return Div(
            text="No data point selected.",
            width=300,
            height=200,
        )
    else:
        active_dict_entry = metadata_dict[key]
        new_paragarph = Div(
            text=format_assay_text(active_dict_entry),
            width=300,
            height=200,
        )
        return new_paragarph


def callback(event):
    """The callback event to be run upon the selection of a data point.
    """
    pass


# HTML Elements ---------------------------------------------------------------
title_div = Div(text="<h1>Aluminate CrossFilter</h1>")

# Controls and Selectors ------------------------------------------------------
source.on_change('selected', tap_select_callback)

x_selector = Select(title='X Axis', options=continuous, value=continuous[0])
x_selector.on_change('value', update_plot)

y_selector = Select(title='Y-Axis', options=continuous, value=continuous[1])
y_selector.on_change('value', update_plot)

color = Select(title='Color', value='None', options=['None'] + discrete)
color.on_change('value', update_plot)

controls = widgetbox([x_selector, y_selector, color])

layout = layout(
    children=[
        title_div,
        [controls, create_figure(), build_metadata_paragraph()],
    ],
    sizing_mode='fixed'
)

curdoc().add_root(layout)
curdoc().title = "27 Al NMR Crossfilter"
