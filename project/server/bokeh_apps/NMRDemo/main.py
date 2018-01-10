"""
################################
Literature NMR Data - Bokeh Demo
################################

This application is divorced from any database. Rather, it
simply loads a set of demo metadata files.

"""

# General imports
# import os
# import sys
# import collections
# import itertools
# import json
# Bokeh imports
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc

# isaDream imports.
from isadream.nmr_demo_sa import *

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

# Assign the columnDataSources.
# data = ColumnDataSource()
# metadata = ColumnDataSource()


def create_figure():
    """
    Create the bokeh plot.
    """
    # fig_source = ColumnDataSource()

    fig = figure(
        name='primary_figure',
        width=800,
        tools="pan,wheel_zoom,box_zoom,reset,tap",
    )

    fig.circle(
        x=data_frame[x_selector.value],
        y=data_frame[y_selector.value],
    )

    return fig


def update(attr, old, new):
    """
    Define the function to be run upon an update call.
    """
    layout.children[1] = create_figure()
    pass


def callback(event):
    """The callback event to be run upon the selection of a data point.
    """
    pass


# Controls and Selectors ------------------------------------------------------
x_selector = Select(title='X Axis', options=columns, value=columns[0])
x_selector.on_change('value', update)

y_selector = Select(title='Y-Axis', options=columns, value=columns[1])
y_selector.on_change('value', update)

controls = widgetbox([x_selector, y_selector])
layout = layout(
    children=[
        [controls],
        [create_figure()]
    ],
    sizing_mode='fixed'
)

curdoc().add_root(layout)
curdoc().title = "27 Al NMR Crossfilter"
