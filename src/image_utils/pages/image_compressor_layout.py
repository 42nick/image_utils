import base64
import io
import zipfile

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image

from image_utils.definitions import (
    IMAGE_MAX_HEIGHT,
    accent_color,
    background_color,
    button_style,
    centered_text_style,
    content_style,
    font_family,
    image_style,
    link_style,
    primary_color,
    secondary_color,
    text_color,
    upload_style,
)

image_compressor_layout = html.Div(
    [
        html.H1(
            "Image Compressor",
            style={**centered_text_style, "color": text_color, "marginBottom": "20px"},
        ),
        dcc.Upload(
            id="upload-image",
            children=html.Div(["Drag and Drop or ", html.A("Select Images")]),
            style=upload_style,
            multiple=True,
        ),
        html.Div(id="upload-info", style={"textAlign": "center", "margin": "10px"}),
        html.Div(
            dcc.Slider(
                id="compression-slider",
                min=1,
                max=100,
                step=1,
                value=85,
                marks={
                    i: {"label": str(i), "style": {"color": text_color, "fontFamily": font_family}}
                    for i in range(0, 101, 10)
                },
                tooltip={"placement": "bottom", "always_visible": True},
            ),
            className="slider-container",
            style={"textAlign": "center"},
        ),
        html.Div(
            html.Button(
                "Compress Images",
                id="compress-button",
                n_clicks=0,
                style=button_style,
            ),
            style={"textAlign": "center"},
        ),
        html.Div(id="download-links", style={"textAlign": "center"}),
        html.Div(id="output-image-upload", style={"textAlign": "center"}),
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
