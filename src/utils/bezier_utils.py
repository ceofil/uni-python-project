from src.shapes.line import Line


def interpolate(x1, y1, x2, y2, current_step, total_steps):
    dx1, dy1 = (x2 - x1) / total_steps, (y2 - y1) / total_steps
    mx1, my1 = x1 + dx1 * current_step, y1 + dy1 * current_step
    return mx1, my1


def three_points_bezier(x1, y1, x2, y2, x3, y3, canvas, color, stroke_width):
    steps = 1000

    points = []
    for idx in range(steps + 1):
        mx1, my1 = interpolate(x1, y1, x2, y2, idx, steps)
        mx2, my2 = interpolate(x2, y2, x3, y3, idx, steps)

        px, py = interpolate(mx1, my1, mx2, my2, idx, steps)
        points.append((px, py))

    for a, b in zip(points[:-1], points[1:]):
        lx1, ly1 = a
        lx2, ly2 = b
        Line(lx1, ly1, lx2, ly2, color, stroke_width).draw(canvas)


def four_points_bezier(x1, y1, x2, y2, x3, y3, x4, y4, canvas, color, stroke_width):
    steps = 90
    points = []
    for idx in range(steps + 1):
        mx1, my1 = interpolate(x1, y1, x2, y2, idx, steps)
        mx2, my2 = interpolate(x2, y2, x3, y3, idx, steps)
        mx3, my3 = interpolate(x3, y3, x4, y4, idx, steps)

        px1, py1 = interpolate(mx1, my1, mx2, my2, idx, steps)
        px2, py2 = interpolate(mx2, my2, mx3, my3, idx, steps)

        qx, qy = interpolate(px1, py1, px2, py2, idx, steps)
        points.append((qx, qy))

    for a, b in zip(points[:-1], points[1:]):
        lx1, ly1 = a
        lx2, ly2 = b
        Line(lx1, ly1, lx2, ly2, color, stroke_width).draw(canvas)
