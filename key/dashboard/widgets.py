# AUTOGENERATED! DO NOT EDIT! File to edit: ../02b_widgets.ipynb.

# %% auto 0
__all__ = ['DATA_DIR', 'DATA_FILE', 'original_df', 'year_range', 'selected_df', 'selected_data_grid', 'window_size', 'poly_order',
           'plot_view', 'on_range_change', 'update_selected_datagrid', 'on_poly_order_change', 'on_window_size_change',
           'output_plot']

# %% ../02b_widgets.ipynb 8

import pandas as pd
import os
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
import ipywidgets as widgets # add import statement for Jupyter widgets

 # %% ../02b_widgets.ipynb 12
# Load data into memory from file
DATA_DIR = 'data'
DATA_FILE = 'land-ocean-temp-index.csv'

original_df = pd.read_csv(os.path.join(DATA_DIR, DATA_FILE), escapechar='#')

# %% ../02b_widgets.ipynb 15
year_range = widgets.IntRangeSlider(description = 'Range of Years')

# %% ../02b_widgets.ipynb 21

year_range.max =  max(original_df['Year']) # set the 'max' attribute of the slider to the minimum year of the our data
year_range.min = min(original_df['Year'])  # and let's do the same for 'min'

# %% ../02b_widgets.ipynb 27

selected_df = original_df[(original_df['Year'] >= year_range.value[0]) & (original_df['Year'] <= year_range.value[1])] # selected_df = original_df[(original_df['Year'] >= from_year) & (original_df['Year'] <= to_year)]

# %% ../02b_widgets.ipynb 37
# Create a function that will change the selected_df based on the range of
# years selected by the user using the year_range widget
def on_range_change(change):
    global selected_df
    selected_df = original_df[(original_df['Year'] >= change['new'][0])
                              & (original_df['Year'] <= change['new'][1])]
    # NOTE: You could also use:
    #  selected_df = original_df[(original_df['Year'] >= year_range.value[0])
    #                             & (original_df['Year'] <= year_range.value[1])]
    # but it is better to use the 'change' object passed to the function because it is
    # not dependent on the name of the widget.

# %% ../02b_widgets.ipynb 46

year_range.observe(on_range_change, 'value') # year_range.observe()

# %% ../02b_widgets.ipynb 62
from ipydatagrid import DataGrid

# Define a DatGrid widget containing our Pandas dataframe setting column and row sizes
selected_data_grid = DataGrid(selected_df, header_visibility="column", auto_fit_columns=True)

# %% ../02b_widgets.ipynb 65
# Create a handler function that will display the selected dataframe
def update_selected_datagrid(change):
    selected_data_grid.data = selected_df

# Attach the handler function to the year_range widget
year_range.observe(update_selected_datagrid, 'value')

# %% ../02b_widgets.ipynb 71
window_size = widgets.IntSlider(description = 'Window Size', value=20, min=1, max=100)

# %% ../02b_widgets.ipynb 74
poly_order = widgets.BoundedIntText(description = 'Poly Order', min=0, value=3, max=10)

# %% ../02b_widgets.ipynb 83

def on_poly_order_change(change):
    global original_df, selected_df
    # catch the change in the poly_order widget value and update the original_df
    original_df['Smoothed Data'] = savgol_filter(original_df['Temperature'], window_size.value, change['new']).round(decimals=3) # original_df['Smoothed Data'] = savgol_filter(original_df['Temperature'], window_size, poly_order).round(decimal=3)
    selected_df = original_df[(original_df['Year'] >= year_range.value[0]) & (original_df['Year'] <= year_range.value[1])]

# %% ../02b_widgets.ipynb 84
poly_order.observe(on_poly_order_change, 'value')
window_size.observe(update_selected_datagrid, 'value')

# %% ../02b_widgets.ipynb 89

def on_window_size_change(change):
    global original_data, selected, poly_order
    poly_order.max = min(10, change['new'] - 1) # change the maximum of the poly_order widget
    # catch the change in the window_size widget value and update the original_df
    original_df['Smoothed Data'] = savgol_filter(original_df['Temperature'],
                                                 change['new'],
                                                 poly_order.value).round(decimals=3)
    selected_df = original_df[(original_df['Year'] >= year_range.value[0])
                              & (original_df['Year'] <= year_range.value[1])]


# %% ../02b_widgets.ipynb 91
window_size.observe(on_window_size_change, 'value')
window_size.observe(update_selected_datagrid, 'value')

# %% ../02b_widgets.ipynb 95
window_size.value = 10
poly_order.value = 1

# %% ../02b_widgets.ipynb 99

plot_view = widgets.Output() # create an output widget called plot_output

# %% ../02b_widgets.ipynb 103

def output_plot(change):
    plot_view.clear_output(wait=True)
    with plot_view:
        plt.xlabel('Year')
        plt.ylabel('Temperature')
        plt.title('Global Temperature versus Time')
        plt.plot(selected_df['Year'], selected_df['Temperature'], label='Raw Data')
        plt.plot(selected_df['Year'], selected_df['Smoothed Data'], label='Smoothed Data')
        plt.show()

# %% ../02b_widgets.ipynb 107
year_range.observe(output_plot, 'value')
window_size.observe(output_plot, 'value')
poly_order.observe(output_plot, 'value')

# %% ../02b_widgets.ipynb 109
year_range.value = (1900, 2000)
