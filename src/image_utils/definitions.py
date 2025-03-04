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
IMAGE_MAX_HEIGHT = 150
image_style = {
    "maxHeight": f"{IMAGE_MAX_HEIGHT}px",
    "maxWidth": "100%",
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
