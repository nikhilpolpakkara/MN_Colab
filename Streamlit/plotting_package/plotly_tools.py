import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as colors


class PlotBuilder:
    def __init__(self, df):
        self.df = df
        self.fig = go.Figure()

    def get_express_line(self, x, y):
        fig = px.line(self.df, x=x, y=y)
        return fig

    def get_go_line(self, x, y, group_by=None):
        if group_by is None:
            x = self.df[x]
            for variable in y:
                self.fig.add_trace(go.Scatter(x=x, y=self.df[variable], name=variable))
        else:
            grouped_df = self.df.groupby(group_by)
            for group_name, group_data in grouped_df:
                if len(group_by) == 1:
                    self.fig.add_trace(go.Scatter(x=group_data[x], y=group_data[y], name=group_name))
                else:
                    self.fig.add_trace(go.Scatter(x=group_data[x], y=group_data[y], name=str(group_name)))

    def get_scatter_timeline(self, x, y, hovertext=None, group_by=None):
        dept_color_code = {
           "durability": '#e41a1c',
           "cal":  '#377eb8',
           "nvh": '#4daf4a',
           "ctl": '#ff7f00',
           "drivability": '#f781bf',
           "performance": '#a65628',
        }
        # annotations = [dict(
        #     x=date,
        #     y=value,
        #     xref='x',
        #     yref='y',
        #     text=event,
        #     # showarrow=True,
        #
        # ) for date, value, event in zip(self.df['date'], self.df['vehicle'], self.df['test_activity'])]

        group_added = []
        grouped_df = self.df.groupby(group_by)
        for group_name, group_data in grouped_df:
            trace = go.Scatter(x=group_data[x], y=group_data[y],
                   name=str(group_name[0]),
                   legendgroup=group_name[0],
                   # line=dict(color=dept_color_code[group_name[0]]),
                   hovertext=group_data[hovertext]
                   )

            if group_name[0] in group_added:
                trace["showlegend"] = False

            else:
                trace["showlegend"] = True
                group_added.append(group_name[0])

            self.fig.add_trace(trace)

    def get_px_timeline(self):
        self.fig = px.line(df, x='Date', y='Vehicle',
                           color='Dept',
                           title='Line Chart with Sorted Dates Within Each Group')

    def generate_color_palette(self, num_colors):
        # Choose a base color scale
        base_color_scale = colors.qualitative.Plotly

        # Adjust the length of the base color scale to match the desired number of colors
        color_scale_length = len(base_color_scale)
        repeat_factor = max(1, num_colors // color_scale_length)
        adjusted_color_scale = base_color_scale * repeat_factor

        # Take the first 'num_colors' colors from the adjusted color scale
        color_palette = adjusted_color_scale[:num_colors]

        return color_palette

    def set_title(self, title):
        self.fig.update_layout({'title': title})

    def set_x_axis_title(self, axis_title):
        self.fig.update_layout(xaxis_title=axis_title)

    def set_y_axis_title(self, axis_title):
        self.fig.update_layout(yaxis_title=axis_title)

    def set_theme(self, theme):
        self.fig.update_layout(template=theme, title='Line Chart with Dark Theme')

    def show_fig(self):
        self.fig.show()

    def set_column_to_datetime(self, column_name):
        print(self.df)
        self.df[column_name] = pd.to_datetime(self.df[column_name], format='%d-%m-%Y %H:%M:%S')
        self.df = self.df.sort_values(column_name)


class Timeline:
    def __init__(self, df):
        self.df = df
        self.fig = go.Figure()


if __name__ == "__main__":
    path = r"D:\\BAL Projects\\01_Misc\\MN_Colab\\Streamlit\\Misc\\timeline_2.csv"
    df = pd.read_csv(path)
    # df = df[df["Dept"] == "Ctl"]
    df = df[df["Model"] == "M1"]
    plot = PlotBuilder(df)
    plot.set_column_to_datetime("Date")
    # plot.get_px_timeline()
    # plot.get_scatter_timeline(y="Vehicle", x="Date", group_by=["Dept", "Vehicle"], hovertext="Name")
    plot.get_scatter_timeline(y="dept", x="date", group_by=["dept"], hovertext="test_activity")
    plot.set_theme(theme='plotly_white')
    plot.fig.write_html("timeline.html")
    plot.fig.show()
    print("Done")