import base64
import io
import tempfile
import zipfile

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from PIL import Image

from image_utils.definitions import (
    IMAGE_MAX_HEIGHT,
    accent_color,
    button_style,
    centered_text_style,
    content_style,
    font_family,
    image_style,
    link_style,
    primary_color,
    secondary_color,
    sidebar_style,
    summary_info_style,
    text_color,
)
from image_utils.pages.image_compressor_layout import image_compressor_layout
from image_utils.pages.image_to_pdf_layout import combine_image_to_pdf

app = dash.Dash(__name__, suppress_callback_exceptions=True)


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
                        dcc.Link("Image to PDF", href="/tool2", style=link_style),
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


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/tool2":
        return combine_image_to_pdf
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


def create_image_div(compressed_image, download_filename, original_size, compressed_size):
    return html.Div(
        [
            html.Div(html.Img(src=compressed_image, style=image_style), style={"height": f"{IMAGE_MAX_HEIGHT}px"}),
            html.Div(
                html.A(
                    "Download",
                    id="download-link",
                    download=download_filename,
                    href=compressed_image,
                    target="_blank",
                    style={
                        "display": "block",
                        "textAlign": "center",
                        "marginTop": "10px",
                        "color": "#fff",
                        "textDecoration": "none",
                        "fontFamily": font_family,
                        "fontWeight": "bold",
                        "padding": "10px 20px",
                        "backgroundColor": primary_color,
                        "borderRadius": "5px",
                    },
                ),
                style={"textAlign": "center"},
            ),
            html.Div(
                download_filename,
                title=download_filename,  # Add title attribute to show full filename on hover
                style={
                    "textAlign": "center",
                    "marginTop": "10px",
                    "fontFamily": font_family,
                    "color": text_color,
                    "fontSize": "12px",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "whiteSpace": "nowrap",
                    "width": "100%",
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


def convert_images_to_pdf(contents_list, filenames):
    images = []
    for contents, filename in zip(contents_list, filenames):
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        image = Image.open(io.BytesIO(decoded))

        # Convert image to RGB if it has an alpha channel
        if image.mode == "RGBA":
            image = image.convert("RGB")

        images.append(image)

    pdf_buffer = io.BytesIO()
    images[0].save(pdf_buffer, format="PDF", resolution=100.0, save_all=True, append_images=images[1:])
    pdf_buffer.seek(0)
    return pdf_buffer


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


@app.callback(
    Output("upload-info-pdf", "children"),
    Input("upload-image-pdf", "contents"),
    State("upload-image-pdf", "filename"),
)
def update_upload_info_pdf(contents, filenames):
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
    Output("download-pdf-link", "children"),
    Input("convert-button", "n_clicks"),
    State("upload-image-pdf", "contents"),
    State("upload-image-pdf", "filename"),
)
def convert_to_pdf(n_clicks, contents, filenames):
    if contents is not None:
        pdf_buffer = convert_images_to_pdf(contents, filenames)
        pdf_base64 = base64.b64encode(pdf_buffer.read()).decode("utf-8")
        pdf_href = f"data:application/pdf;base64,{pdf_base64}"

        return html.Div(
            html.A(
                "Download PDF",
                id="download-pdf",
                download="converted_images.pdf",
                href=pdf_href,
                target="_blank",
                style=button_style,
            ),
            style={"textAlign": "center"},
        )
    return None


if __name__ == "__main__":
    app.run_server(debug=True)
