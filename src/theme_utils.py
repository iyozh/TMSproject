def switch_color(theme):
    if not theme:
        theme["background_color"] = "white"
        theme["text_color"] = "black"

    return theme