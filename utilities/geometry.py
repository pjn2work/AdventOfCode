import math

PointType = tuple[int, int]
PolygonType = list[PointType]


def intersect(A: PointType, B: PointType, C: PointType, D: PointType) -> bool:
    """
    Check if line segments AB and CD intersect.
    Returns:
      True if they intersect properly (crossing each other)
      False otherwise.
    """
    def ccw(a: PointType, b: PointType, c: PointType) -> int:
        # Cross product to determine orientation
        val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
        if abs(val) < 1e-9: return 0  # Colinear
        return 1 if val > 0 else -1  # Clockwise or Counter-clockwise

    o1 = ccw(A, B, C)
    o2 = ccw(A, B, D)
    o3 = ccw(C, D, A)
    o4 = ccw(C, D, B)

    # Cross product: the points of one segment must be on opposite sides of the other
    if (o1 * o2 < 0) and (o3 * o4 < 0):
        return True
    return False


def is_point_on_edge(p: PointType, p1: PointType, p2: PointType) -> bool:
    """Check if point p is on the edge between p1 and p2 (segment p1-p2)"""
    x, y = p
    x1, y1 = p1
    x2, y2 = p2

    # Check if point is colinear to the edge
    cross_product = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
    if abs(cross_product) > 1e-9: return False
    
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)


def is_point_in_path(p: PointType, poly: PolygonType) -> bool:
    n = len(poly)
    # 1. Check if the point is exactly on any of the edges
    for i in range(n):
        if is_point_on_edge(p, poly[i], poly[(i + 1) % n]):
            return True # Está na borda -> considerar dentro
            
    # 2. Ray Casting
    inside = False
    x, y = p
    
    # 2.1 Start with the last point to close the loop
    p1x, p1y = poly[-1]
    
    for p2x, p2y in poly:
        # 2.2 Check if the point's Y is between the edge's Y-range
        # This condition also naturally ignores horizontal lines
        if (p1y > y) != (p2y > y):
            
            # 2.3 Calculate the X-intersection of the edge with the ray at height Y
            # This formula is derived from the linear equation of the edge
            intersect_x = (p2x - p1x) * (y - p1y) / (p2y - p1y) + p1x
            
            # 2.4 If the point's X is to the left of the intersection, flip the 'inside' state
            if x < intersect_x:
                inside = not inside
        
        # 2.5 Move to the next edge
        p1x, p1y = p2x, p2y
        
    return inside


class Polygon:
    def __init__(self, points: PolygonType) -> None:
        if len(points) < 3:
            raise ValueError("Polygon must have at least 3 points")
        if not all(len(point) == 2 for point in points):
            raise ValueError("All points must have 2 coordinates")
        
        self.points: PolygonType = points
    
    def get_grid_area(self) -> int:
        """
        Returns the area of the polygon considering integer points (pixels).
        For the rectangle [(9,5), (9,3), (2,3), (2,5)], it will return 24.
        """
        # 1. Calculate the area of the polygon using the Shoelace formula
        geom_area = self.get_area()
        
        # 2. Count the number of integer points on the edges (Grid perimeter)
        boundary_points = 0
        n = len(self.points)
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            
            # The number of integer points on a segment from (x1,y1) to (x2,y2)
            # is the Greatest Common Divisor of the difference of the coordinates.
            dx = abs(p2[0] - p1[0])
            dy = abs(p2[1] - p1[1])
            boundary_points += math.gcd(dx, dy)
            
        # 3. Apply Pick's theorem variation to obtain the internal + boundary points
        # Internal points (I) = Area - (B/2) + 1
        # What you want is: I + B (Internal + Boundary)
        grid_area = int(geom_area + (boundary_points / 2) + 1)
        return grid_area

    def get_area(self) -> float:
        """Returns the area inside the polygon."""
        n = len(self.points)
        area = 0.0
        for i in range(n):
            # j is the next point (using module circle back and connect the last point to the first point)
            j = (i + 1) % n
        
            x_i, y_i = self.points[i][0], self.points[i][1]
            x_j, y_j = self.points[j][0], self.points[j][1]

            area += x_i * y_j
            area -= x_j * y_i
        
        return abs(area) / 2.0

    def get_perimeter(self) -> float:
        """Returns the perimeter of the polygon."""
        n = len(self.points)
        perimeter = 0.0
        for i in range(n):
            # j is the next point (using module circle back and connect the last point to the first point)
            j = (i + 1) % n
            
            x_i, y_i = self.points[i][0], self.points[i][1]
            x_j, y_j = self.points[j][0], self.points[j][1]
            
            perimeter += math.sqrt((x_j - x_i) ** 2 + (y_j - y_i) ** 2)
        
        return perimeter

    def get_polygon_relationship(self, other_poly) -> int:
        """
        Returns the relationship between two polygons.

        Returns:
           -1: self and other_poly do not intersect (both outside each other)
            0: self and other_poly intersect (partially inside each other)
            1: self is fully inside other_poly
            2: other_poly is fully inside self
            3: self and other_poly are the same polygon
        """
        poly_a = self.points
        if not isinstance(other_poly, Polygon):
            other_poly = Polygon(other_poly)
        poly_b = other_poly.points

        # 1. Check if any edges intersect
        for i in range(len(poly_a)):
            edge_a1, edge_a2 = poly_a[i], poly_a[(i + 1) % len(poly_a)]
            for j in range(len(poly_b)):
                edge_b1, edge_b2 = poly_b[j], poly_b[(j + 1) % len(poly_b)]
                if intersect(edge_a1, edge_a2, edge_b1, edge_b2):
                    return 0 

        # 2. Check if all points (vertices + midpoints) of P_SUB are in P_PARENT
        def is_fully_contained(p_sub, p_parent):
            for i in range(len(p_sub)):
                p1 = p_sub[i]
                p2 = p_sub[(i + 1) % len(p_sub)]
                midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                
                # Checa o vértice e o ponto médio da aresta que sai dele
                if not is_point_in_path(p1, p_parent) or not is_point_in_path(midpoint, p_parent):
                    return False
            return True

        a_in_b = is_fully_contained(poly_a, poly_b)
        b_in_a = is_fully_contained(poly_b, poly_a)

        if a_in_b and not b_in_a:
            return 1
        if b_in_a and not a_in_b:
            return 2
        if a_in_b and b_in_a:
            return 3

        # 3. If not fully contained, but some point touches or is inside
        # Check only vertices for performance here
        if any(is_point_in_path(pt, poly_b) for pt in poly_a) or \
           any(is_point_in_path(pt, poly_a) for pt in poly_b):
            return 0

        return -1


def test_polygon_relationship():
    p = Polygon([(5, 5), (15, 5), (15, 15), (5, 15)])
    p0 = Polygon([(1, 1), (9, 1), (9, 9), (1, 9)])
    p1 = Polygon([(5, 0), (10, 5), (5, 10), (0, 5)])
    p2 = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    p3 = Polygon([(20, 20), (30, 20), (30, 30), (20, 30)])  

    print("\n> -1 Outside----------------")
    print(p2.get_polygon_relationship(p3))
    print(p3.get_polygon_relationship(p2))
    
    print("\n> 0 Intersect----------------")
    print(p2.get_polygon_relationship(p))
    print(p.get_polygon_relationship(p2))
    print(p0.get_polygon_relationship(p1))
    print(p1.get_polygon_relationship(p0))
    
    print("\n> 1 Self A fully inside Other B----------------")
    print(p0.get_polygon_relationship(p2))
    print(p1.get_polygon_relationship(p2))
    
    print("\n> 2 Other B fully inside Self A----------------")
    print(p2.get_polygon_relationship(p0))
    print(p2.get_polygon_relationship(p1))

    print("\n> 3 Self A and Other B are the same polygon----------------")
    print(p2.get_polygon_relationship(p2))
    print(p1.get_polygon_relationship(p1.points))


if __name__ == "__main__":
    test_polygon_relationship()
