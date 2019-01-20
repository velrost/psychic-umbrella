from spyre import  server
import pandas as pd
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np

class DataGen(server.App):
    title = "DATA GEN"
    inputs = [{"type": 'dropdown',
               "label": 'Area',
               "options": [{"label": "Vinnitsya", "value": "1"},
                           {"label": "Volyn", "value": "2"},
                           {"label": "Dnipropetrovsk", "value": "3"},
                           {"label": "Donetsk", "value": "4"},
                           {"label": "Zhytomyr", "value": "5"},
                           {"label": "Zacarpathia", "value": "6"},
                           {"label": "Zaporizhzhya", "value": "7"},
                           {"label": "Ivano-Frankivsk", "value": "8"},
                           {"label": "Kiev", "value": "9"},
                           {"label": "Kirovohrad", "value": "10"},
                           {"label": "Luhansk", "value": "11"},
                           {"label": "Lviv", "value": "12"},
                           {"label": "Mykolayiv", "value": "13"},
                           {"label": "Odessa", "value": "14"},
                           {"label": "Poltava", "value": "15"},
                           {"label": "Rivne", "value": "16"},
                           {"label": "Sumy", "value": "17"},
                           {"label": "Ternopil", "value": "18"},
                           {"label": "Kharkiv", "value": "19"},
                           {"label": "Kherson", "value": "20"},
                           {"label": "Khmelnytskyy", "value": "21"},
                           {"label": "Cherkasy", "value": "22"},
                           {"label": "Chernivtsi", "value": "23"},
                           {"label": "Chernihiv", "value": "24"},
                           {"label": "Crimea", "value": "25"}],
               "key": 'area',
               "action_id": "update_data"},

               {"input_type": "slider",
               "variable_name": "year",
               "label": "Year",
               "min": 1981, "max": 2018, "value": 1981,
               "key": 'year',
               "action_id": "update_data"},

               {"type": 'dropdown',
                "label": 'Index  ',
                "options": [{"label": "VCI", "value": "VCI"},
                            {"label": "TCI", "value": "TCI"},
                            {"label": "VHI", "value": "VHI"},
                            {"label": "TCI", "value": "TCI"},
                            {"label": "SMT", "value": "SMT"},
                            {"label": "SMN", "value": "SMN"},],
                "key": 'index',
                "action_id": "update_data"},

               {"type": 'slider',
                "label": 'First week',
                "min": 1, "max": 52, "value": 1,
                "key": 'first_w',
                "action_id": 'update_data'},

               {"type": 'slider',
                "label": 'Last week',
                "min": 1, "max": 52, "value": 1,
                "key": 'last_w',
                "action_id": 'update_data'}
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [{"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table"},

               {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}
               ]

    def getData(self, params):
        year = params['year']
        index = params['index']
        first_w = params['first_w']
        last_w = params['last_w']
        area = params['area']
        url = ("downloads/{}.csv").format(area)
        print(url)
        df = pd.read_csv(url,index_col=False)
        df_new = df[(df['Year'] == int(year)) & (df['Week'] >= int(first_w)) & (df['Week'] <= int(last_w))]
        df_new = df_new[['Week', index]]
        return df_new

    def getPlot(self, params):
        year = params['year']
        index = params['index']
        first_w = params['first_w']
        last_w = params['last_w']
        area = params['area']
        df = self.getData(params).set_index('Week')
        plt_obj = df.plot()
        plt_obj.set_ylabel(index)
        fig = plt_obj.get_figure()
        return fig


app = DataGen()
app.launch()