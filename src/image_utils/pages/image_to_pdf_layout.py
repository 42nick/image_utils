from dash import dcc, html

from image_utils.definitions import (
    background_color,
    button_style,
    centered_text_style,
    font_family,
    text_color,
    upload_style,
)

combine_image_to_pdf = html.Div(
    [
        html.H1(
            "Image to PDF Converter",
            style={**centered_text_style, "color": text_color, "marginBottom": "20px"},
        ),
        dcc.Upload(
            id="upload-image-pdf",
            children=html.Div(["Drag and Drop or ", html.A("Select Images")]),
            style=upload_style,
            multiple=True,
        ),
        html.Div(id="upload-info-pdf", style={"textAlign": "center", "margin": "10px"}),
        html.Div(
            html.Button(
                "Convert to PDF",
                id="convert-button",
                n_clicks=0,
                style=button_style,
            ),
            style={"textAlign": "center"},
        ),
        html.Div(id="download-pdf-link", style={"textAlign": "center"}),
    ],
    style={
        "maxWidth": "1000px",
        "margin": "auto",
        "padding": "20px",
        "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
        "borderRadius": "10px",
        "backgroundColor": background_color,
        "fontFamily": font_family,
        "textAlign": "center",
    },
)
