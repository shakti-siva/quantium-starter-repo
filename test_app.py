from app import app
from dash import html, dcc

def find_components(layout, component_type):
    """Recursively collect components of a given type."""
    found = []
    if isinstance(layout, component_type):
        found.append(layout)
    if hasattr(layout, "children"):
        children = layout.children
        if not isinstance(children, (list, tuple)):
            children = [children]
        for child in children:
            found.extend(find_components(child, component_type))
    return found

def test_header_present():
    headers = find_components(app.layout, html.H1)
    assert any("Pink Morsel Sales Visualiser" in h.children for h in headers)

def test_graph_present():
    graphs = find_components(app.layout, dcc.Graph)
    assert any(g.id == "sales-graph" for g in graphs)

def test_region_picker_present():
    dropdowns = find_components(app.layout, dcc.Dropdown)
    assert any(d.id == "region-picker" for d in dropdowns)
