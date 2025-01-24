from xml.etree.ElementTree import parse
from svgpathtools import Path, parse_path
from math import ceil
import numpy as np
import turtle

# SVG File
svg_file = 'Mouthwashing Chibis_Anya.svg'  # Replace with your SVG file name

def extract_shapes_with_colors(svg_file):
    """Extract paths, polygons, and lines with colors from the SVG file."""
    try:
        tree = parse(svg_file)
        root = tree.getroot()
        namespace = {'svg': 'http://www.w3.org/2000/svg'}
        shapes_with_colors = []

        # Extract paths
        for path_elem in root.findall('.//svg:path', namespaces=namespace):
            d_attr = path_elem.attrib.get('d')
            fill_color = path_elem.attrib.get('fill', 'black')  # Default to black if no fill specified
            if d_attr:
                shapes_with_colors.append((parse_path(d_attr), fill_color, 'path'))

        # Extract polygons
        for poly_elem in root.findall('.//svg:polygon', namespaces=namespace):
            points_attr = poly_elem.attrib.get('points')
            fill_color = poly_elem.attrib.get('fill', 'black')  # Default to black if no fill specified
            if points_attr:
                points = [
                    tuple(map(float, point.split(',')))
                    for point in points_attr.strip().split(' ')
                    if ',' in point
                ]
                shapes_with_colors.append((points, fill_color, 'polygon'))

        # Extract lines
        for line_elem in root.findall('.//svg:line', namespaces=namespace):
            x1 = float(line_elem.attrib.get('x1', 0))
            y1 = float(line_elem.attrib.get('y1', 0))
            x2 = float(line_elem.attrib.get('x2', 0))
            y2 = float(line_elem.attrib.get('y2', 0))
            color = line_elem.attrib.get('stroke', 'black')  # Default to black if no stroke specified
            shapes_with_colors.append(((x1, y1, x2, y2), color, 'line'))

        return shapes_with_colors
    except Exception as e:
        print("Error parsing SVG:", e)
        return []

def draw_turtle_path(t, path, scale=1, offset_x=0, offset_y=0, color="black"):
    """Draw a single path using Turtle."""
    t.color(color)
    t.penup()
    for seg in path:
        interp_num = max(ceil(seg.length()), 30)  # Ensure enough interpolation
        points = [seg.point(t) for t in np.linspace(0, 1, interp_num)]
        for i, point in enumerate(points):
            x, y = point.real * scale + offset_x, -point.imag * scale + offset_y
            if i == 0:
                t.goto(x, y)
                t.pendown()
            else:
                t.goto(x, y)
    t.penup()

def draw_polygon(t, points, scale=1, offset_x=0, offset_y=0, color="black"):
    """Draw a polygon using Turtle."""
    t.color(color)
    t.penup()
    if points:
        # Move to the first point
        x, y = points[0]
        t.goto(x * scale + offset_x, -y * scale + offset_y)
        t.pendown()
        # Draw lines between each consecutive point
        for x, y in points[1:]:
            t.goto(x * scale + offset_x, -y * scale + offset_y)
        # Close the polygon by returning to the first point
        x, y = points[0]
        t.goto(x * scale + offset_x, -y * scale + offset_y)
    t.penup()

def draw_line(t, x1, y1, x2, y2, scale=1, offset_x=0, offset_y=0, color="black"):
    """Draw a single line using Turtle."""
    t.color(color)
    t.penup()
    t.goto(x1 * scale + offset_x, -y1 * scale + offset_y)  # Turtle's Y-axis is inverted
    t.pendown()
    t.goto(x2 * scale + offset_x, -y2 * scale + offset_y)
    t.penup()

# Extract shapes from the SVG
shapes_with_colors = extract_shapes_with_colors(svg_file)
if not shapes_with_colors:
    print("No shapes found in the SVG file.")
else:
    print(f"Found {len(shapes_with_colors)} shapes in the SVG.")

# Turtle Graphics Setup
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Adjust the screen size if necessary
screen = turtle.Screen()
screen.setup(width=800, height=800)

# Scale and offsets for positioning
scale = 1  # Adjust this if the SVG is too large/small
offset_x, offset_y = 0, 0  # Centering offsets if needed

# Draw each shape with its corresponding color and type
for shape_data in shapes_with_colors:
    if len(shape_data) != 3:
        print(f"Invalid shape data: {shape_data}")
        continue  # Skip malformed entries

    shape, color, shape_type = shape_data

    if shape_type == 'path':
        draw_turtle_path(t, shape, scale, offset_x, offset_y, color=color)
    elif shape_type == 'polygon':
        draw_polygon(t, shape, scale, offset_x, offset_y, color=color)
    elif shape_type == 'line':
        x1, y1, x2, y2 = shape
        draw_line(t, x1, y1, x2, y2, scale, offset_x, offset_y, color=color)
    else:
        print(f"Unknown shape type: {shape_type}")

# Finalize Turtle graphics
turtle.done()
