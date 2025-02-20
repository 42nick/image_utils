import base64
import io
import zipfile

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "Image Compressor",
            style={
                "textAlign": "center",
                "color": "#333",
                "marginBottom": "20px",
                "fontFamily": "Arial, sans-serif",
            },
        ),
        dcc.Upload(
            id="upload-image",
            children=html.Div(["Drag and Drop or ", html.A("Select Images")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                "backgroundColor": "#f9f9f9",
                "fontFamily": "Arial, sans-serif",
            },
            multiple=True,
        ),
        html.Div(id="upload-info", style={"textAlign": "center", "margin": "10px"}),
        dcc.Slider(
            id="compression-slider",
            min=1,
            max=100,
            step=1,
            value=85,
            marks={i: str(i) for i in range(0, 101, 10)},
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Div(
            html.Button(
                "Compress Images",
                id="compress-button",
                n_clicks=0,
                style={
                    "padding": "10px 20px",
                    "fontSize": "16px",
                    "color": "#fff",
                    "backgroundColor": "#007bff",
                    "border": "none",
                    "borderRadius": "5px",
                    "textDecoration": "none",
                    "fontFamily": "Arial, sans-serif",
                },
            ),
            style={"textAlign": "center"},
        ),
        html.Div(id="download-links"),
        html.Div(id="output-image-upload"),
    ],
    style={
        "maxWidth": "1000px",
        "margin": "auto",
        "padding": "20px",
        "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
        "borderRadius": "10px",
        "backgroundColor": "#fff",
        "fontFamily": "Arial, sans-serif",
    },
)


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
                if filename:
                    name, ext = filename.rsplit(".", 1)
                    download_filename = f"{name}_compressed.jpg"
                else:
                    download_filename = "compressed_image.jpg"
                images_and_links.append(
                    html.Div(
                        [
                            html.Img(
                                src=compressed_image,
                                style={
                                    "height": "150px",
                                    "width": "auto",
                                    "display": "block",
                                    "margin": "auto",
                                    "borderRadius": "5px",
                                    "boxShadow": "0 0 5px rgba(0,0,0,0.1)",
                                },
                            ),
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
                                    "color": "#007bff",
                                    "textDecoration": "none",
                                    "fontFamily": "Arial, sans-serif",
                                },
                            ),
                            html.Div(
                                f"Before: {original_size / 1024:.2f} KB",
                                style={
                                    "textAlign": "center",
                                    "marginTop": "10px",
                                    "fontFamily": "Arial, sans-serif",
                                },
                            ),
                            html.Div(
                                f"After: {compressed_size / 1024:.2f} KB",
                                style={
                                    "textAlign": "center",
                                    "marginTop": "10px",
                                    "fontFamily": "Arial, sans-serif",
                                },
                            ),
                        ],
                        style={
                            "display": "inline-block",
                            "width": "200px",
                            "margin": "10px",
                            "verticalAlign": "top",
                        },
                    )
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
                style={
                    "display": "inline-block",
                    "padding": "10px 20px",
                    "fontSize": "16px",
                    "color": "#fff",
                    "backgroundColor": "#007bff",
                    "border": "none",
                    "borderRadius": "5px",
                    "textDecoration": "none",
                    "textAlign": "center",
                    "margin": "10px",
                    "fontFamily": "Arial, sans-serif",
                },
            ),
            style={"textAlign": "center"},
        )
        return html.Div(
            images_and_links,
            style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center"},
        ), zip_link
    return None, None


if __name__ == "__main__":
    app.run_server(debug=True)
