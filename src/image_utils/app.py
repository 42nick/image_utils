import base64
import io
import zipfile

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define reusable style variables
font_family = "Arial, sans-serif"
primary_color = "#4CAF50"  # Green
secondary_color = "#f9f9f9"  # Light grey
accent_color = "#FF5722"  # Orange
text_color = "#333"  # Dark grey
background_color = "#fff"  # White

centered_text_style = {"textAlign": "center", "fontFamily": font_family, "color": text_color}
button_style = {
    "padding": "10px 20px",
    "fontSize": "16px",
    "color": "#fff",
    "backgroundColor": primary_color,
    "border": "none",
    "borderRadius": "5px",
    "textDecoration": "none",
    "fontFamily": font_family,
    "margin": "20px 0",  # Added margin for top and bottom
}
upload_style = {
    "width": "100%",
    "height": "100px",
    "lineHeight": "60px",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "5px",
    "textAlign": "center",
    "margin": "10px",
    "backgroundColor": secondary_color,
    "fontFamily": font_family,
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
}
image_style = {
    "height": "150px",
    "width": "auto",
    "display": "block",
    "margin": "auto",
    "borderRadius": "5px",
    "boxShadow": "0 0 5px rgba(0,0,0,0.1)",
}
summary_info_style = {
    "backgroundColor": secondary_color,
    "padding": "20px",
    "borderRadius": "10px",
    "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
    "margin": "20px 0",
}
sidebar_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "220px",
    "padding": "20px",
    "backgroundColor": primary_color,
    "color": "#fff",
    "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
}

content_style = {
    "marginLeft": "240px",
    "padding": "20px",
    "backgroundColor": background_color,
    "fontFamily": font_family,
}

link_style = {
    "display": "block",
    "padding": "10px 0",
    "color": "#fff",
    "textDecoration": "none",
}

link_hover_style = {
    "color": accent_color,
}

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                html.H2("Tools", style={"fontFamily": font_family, "color": "#fff"}),
                html.Hr(style={"borderColor": "#fff"}),
                html.Div(
                    [
                        dcc.Link("Image Compressor", href="/", style=link_style),
                        dcc.Link("Tool 2", href="/tool2", style=link_style),
                        dcc.Link("Tool 3", href="/tool3", style=link_style),
                        dcc.Link("Tool 4", href="/tool4", style=link_style),
                    ],
                    style={"fontFamily": font_family},
                ),
            ],
            style=sidebar_style,
        ),
        html.Div(id="page-content", style=content_style),
    ]
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


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/tool2":
        return html.Div([html.H1("Tool 2", style=centered_text_style)])
    elif pathname == "/tool3":
        return html.Div([html.H1("Tool 3", style=centered_text_style)])
    elif pathname == "/tool4":
        return html.Div([html.H1("Tool 4", style=centered_text_style)])
    else:
        return image_compressor_layout


def parse_contents(contents, compression_ratio):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    original_size = len(decoded)
    image = Image.open(io.BytesIO(decoded))

    # Convert image to RGB if it has an alpha channel
    if image.mode == "RGBA":
        image = image.convert("RGB")

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=compression_ratio, optimize=True)
    buffer.seek(0)
    compressed_size = buffer.getbuffer().nbytes

    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_image}", original_size, compressed_size


@app.callback(
    Output("upload-info", "children"),
    Input("upload-image", "contents"),
    State("upload-image", "filename"),
)
def update_upload_info(contents, filenames):
    if contents is not None:
        num_files = len(contents)
        return html.Div(
            [
                html.Span(f"{num_files} image(s) uploaded.", style={"fontSize": "20px", "fontWeight": "bold"}),
            ],
            style={"color": "green", "textAlign": "center", "marginTop": "10px"},
        )
    return html.Div(
        [
            html.Span("0 images uploaded.", style={"fontSize": "20px", "fontWeight": "bold"}),
        ],
        style={"textAlign": "center", "marginTop": "10px"},
    )


def create_image_div(compressed_image, download_filename, original_size, compressed_size):
    return html.Div(
        [
            html.Img(src=compressed_image, style=image_style),
            html.A(
                "Download " + download_filename,
                id="download-link",
                download=download_filename,
                href=compressed_image,
                target="_blank",
                style={
                    "display": "block",
                    "textAlign": "center",
                    "marginTop": "10px",
                    "color": primary_color,
                    "textDecoration": "none",
                    "fontFamily": font_family,
                    "fontWeight": "bold",
                },
            ),
            html.Div(
                f"Before: {original_size / 1024:.2f} KB",
                style={
                    "textAlign": "center",
                    "marginTop": "10px",
                    "fontFamily": font_family,
                    "color": text_color,
                },
            ),
            html.Div(
                f"After: {compressed_size / 1024:.2f} KB",
                style={
                    "textAlign": "center",
                    "marginTop": "10px",
                    "fontFamily": font_family,
                    "color": text_color,
                },
            ),
        ],
        style={
            "display": "inline-block",
            "width": "220px",
            "margin": "10px",
            "padding": "10px",
            "borderRadius": "10px",
            "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
            "backgroundColor": secondary_color,
            "verticalAlign": "top",
        },
    )


@app.callback(
    Output("output-image-upload", "children"),
    Output("download-links", "children"),
    Input("compress-button", "n_clicks"),
    State("upload-image", "contents"),
    State("upload-image", "filename"),
    State("compression-slider", "value"),
)
def update_output(compress_clicks, contents, filenames, compression_ratio):
    if contents is not None:
        images_and_links = []
        zip_buffer = io.BytesIO()
        total_original_size = 0
        total_compressed_size = 0

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for content, filename in zip(contents, filenames):
                if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    return html.Div(
                        [
                            html.Span(
                                "Unsupported file format for ",
                                style={"fontSize": "20px", "fontWeight": "bold"},
                            ),
                            html.Span(
                                filename,
                                style={"fontSize": "24px", "fontWeight": "bold"},
                            ),
                            html.Span(
                                " Please upload only PNG, JPG, or JPEG images.",
                                style={"fontSize": "20px"},
                            ),
                        ],
                        style={
                            "color": "red",
                            "textAlign": "center",
                            "marginTop": "10px",
                        },
                    ), None

                compressed_image, original_size, compressed_size = parse_contents(content, compression_ratio)
                total_original_size += original_size
                total_compressed_size += compressed_size

                if filename:
                    name, ext = filename.rsplit(".", 1)
                    download_filename = f"{name}_compressed.jpg"
                else:
                    download_filename = "compressed_image.jpg"
                images_and_links.append(
                    create_image_div(compressed_image, download_filename, original_size, compressed_size)
                )
                image_data = base64.b64decode(compressed_image.split(",")[1])
                zip_file.writestr(download_filename, image_data)

        zip_buffer.seek(0)
        zip_base64 = base64.b64encode(zip_buffer.read()).decode("utf-8")
        zip_href = f"data:application/zip;base64,{zip_base64}"

        zip_link = html.Div(
            html.A(
                "Download All Images as Zip",
                id="download-zip-link",
                download="compressed_images.zip",
                href=zip_href,
                target="_blank",
                style=button_style,
            ),
            style={"textAlign": "center"},
        )

        size_reduction = 100 * (total_original_size - total_compressed_size) / total_original_size

        summary_info = html.Div(
            [
                html.Div(
                    f"Total Original Size: {total_original_size / 1024:.2f} KB",
                    style={
                        "textAlign": "center",
                        "marginTop": "10px",
                        "fontFamily": font_family,
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "color": text_color,
                    },
                ),
                html.Div(
                    f"Total Compressed Size: {total_compressed_size / 1024:.2f} KB",
                    style={
                        "textAlign": "center",
                        "marginTop": "10px",
                        "fontFamily": font_family,
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "color": text_color,
                    },
                ),
                html.Div(
                    f"Size Reduction: {size_reduction:.2f}%",
                    style={
                        "textAlign": "center",
                        "marginTop": "10px",
                        "fontFamily": font_family,
                        "fontSize": "20px",
                        "fontWeight": "bold",
                        "color": accent_color,
                    },
                ),
            ],
            style=summary_info_style,
        )

        return html.Div(
            [html.Div(summary_info), html.Div(images_and_links)],
            style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center"},
        ), zip_link
    return None, None


if __name__ == "__main__":
    app.run_server(debug=True)
