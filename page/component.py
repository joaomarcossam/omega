from style import Style

class Component:
    def __init__(self, tag: str, style: Style = None, content: list | str = None, **kwargs):
        self.tag = tag
        self.style = style
        self.content = content

class Body(Component):
    def __init__(self, style: Style, content: str, **kwargs):
        super().__init__("body", style, content)

class Div(Component):
    def __init__(self, style: Style, content: str, **kwargs):
        super().__init__("div", style, content)

class Span(Component):
    def __init__(self, style: Style, content: str, **kwargs):
        super().__init__("span", style, content)

class Button(Component):
    def __init__(self, style: Style, content: str, **kwargs):
        super().__init__("button", style, content)

