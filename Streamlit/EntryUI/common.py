import plotly.express as px

def generate_color_palette(variables):
    # Create a color palette based on the provided variables
    color_scale = px.colors.qualitative.Set1  # You can choose a different color scale
    palette = [color_scale[i % len(color_scale)] for i in range(len(variables))]

    return palette