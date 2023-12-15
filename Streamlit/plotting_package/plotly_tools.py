import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

    def set_title(self, title):
        self.fig.update_layout({'title': title})

    def set_x_axis_title(self, axis_title):
        self.fig.update_layout(xaxis_title=axis_title)

    def set_y_axis_title(self, axis_title):
        self.fig.update_layout(yaxis_title=axis_title)

    def show_fig(self):
        self.fig.show()


class Timeline:
    def __init__(self, df):
        self.df = df
        self.fig = go.Figure()


if __name__ == "__main__":
    path = r"D:\\BAL Projects\\01_Misc\\MN_Colab\\Streamlit\\Misc\\timeline_2.csv"
    df = pd.read_csv(path)
    plot = PlotBuilder(df)
    plot.get_go_line(x="Vehicle", y="Date", group_by=["Dept", "Vehicle"])
    print("Done")