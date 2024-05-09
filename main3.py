import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

num_points = 200

def find_furthest_points(points):
    max_dist = 0
    furthest_points = None, None
    
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = np.linalg.norm(points[i] - points[j])
            if dist > max_dist:
                max_dist = dist
                furthest_points = points[i], points[j]
    
    return furthest_points

def find_points_furthest_from_line(line, points):
    max_dist_left = 0
    max_dist_right = 0
    furthest_point_left = None
    furthest_point_right = None
    
    for point in points:
        dist = np.abs(np.cross(line[1]-line[0], point-line[0])) / np.linalg.norm(line[1]-line[0])
        
        # Перевіряємо, з якої сторони від прямої знаходиться точка
        side = np.sign(np.cross(line[1]-line[0], point-line[0]))
        
        if dist > max_dist_left and side > 0:
            max_dist_left = dist
            furthest_point_left = point
            
        if dist > max_dist_right and side < 0:
            max_dist_right = dist
            furthest_point_right = point
    
    return furthest_point_left, furthest_point_right

def find_parallel_lines(line, points):
    parallel_lines = []

    for point in points:
        displacement = point - line[0]
        new_point = line[1] + displacement
        parallel_lines.append([point, new_point])

    return parallel_lines

def find_perpendicular_lines(line, furthest_points):
    perpendicular_lines = []

    # Знаходимо напрямок прямої
    direction = line[1] - line[0]
    slope = direction[1] / direction[0]
    
    # Знаходимо точки, через які треба провести перпендикуляри
    point1, point2 = furthest_points
    
    # Знаходимо крайні точки перпендикулярних прямих
    perpendicular_line1_point1 = point1
    perpendicular_line1_point2 = point1 + np.array([-direction[1], direction[0]])
    perpendicular_line2_point1 = point2
    perpendicular_line2_point2 = point2 + np.array([-direction[1], direction[0]])
    
    perpendicular_lines.append([perpendicular_line1_point1, perpendicular_line1_point2])
    perpendicular_lines.append([perpendicular_line2_point1, perpendicular_line2_point2])
    
    return perpendicular_lines

def calculate_min_rectangle_area(points):
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]

    min_area = np.inf

    for i in range(len(hull_points)):
        for j in range(i + 1, len(hull_points)):
            p1 = hull_points[i]
            p2 = hull_points[j]

            # Вектор, що сполучає дві точки
            v = p2 - p1

            # Нормалізований вектор перпендикулярний вектору v
            normal = np.array([-v[1], v[0]])

            # Знаходимо точки, що лежать на протилежних сторонах від прямої, що проходить через p1 та p2
            side1 = [p for p in hull_points if np.dot(normal, p - p1) > 0]
            side2 = [p for p in hull_points if np.dot(normal, p - p1) < 0]

            # Знаходимо мінімальний прямокутник для поточної пари точок
            for s1 in [side1, side2]:
                for s2 in [side1, side2]:
                    if len(s1) >= 2 and len(s2) >= 2:
                        min_x = min(p[0] for p in s1)
                        max_x = max(p[0] for p in s1)
                        min_y = min(p[1] for p in s2)
                        max_y = max(p[1] for p in s2)
                        area = (max_x - min_x) * (max_y - min_y)

                        if area < min_area:
                            # Перевіряємо, чи всі точки множини лежать всередині поточного прямокутника
                            if all(min_x <= p[0] <= max_x and min_y <= p[1] <= max_y for p in hull_points):
                                min_area = area

    return min_area

def petunin_rectangle_area(parallel_lines, perpendicular_lines):
    # Знаходимо довжини сторін прямокутника Петуніна
    length1 = np.linalg.norm(parallel_lines[0][0] - parallel_lines[0][1])
    length2 = np.linalg.norm(perpendicular_lines[0][0] - perpendicular_lines[0][1])
    return length1 * length2

def main():
    num_samples = 100
    total_petunin_area = 0
    total_min_rectangle_area = 0

    for _ in range(num_samples):
        # Генеруємо випадкові точки
        points = np.random.rand(num_points, 2)

        # Знаходимо дві найвіддаленіші точки
        furthest_points = find_furthest_points(points)
        
        # Знаходимо пряму між найвіддаленішими точками
        line = furthest_points
        
        # Знаходимо по одній найвіддаленішій точці від прямої з кожної сторони
        left_point, right_point = find_points_furthest_from_line(line, points)
        
        # Знаходимо паралельні прямі, що проходять через ці точки
        parallel_lines = find_parallel_lines(line, [left_point, right_point])
        
        # Знаходимо перпендикулярні прямі, що проходять через точки з пункту 1
        perpendicular_lines = find_perpendicular_lines(line, furthest_points)

        # Знаходимо площу прямокутника Петуніна
        petunin_area = petunin_rectangle_area(parallel_lines, perpendicular_lines)
        
        # Знаходимо площу мінімального прямокутника
        min_rectangle_area = calculate_min_rectangle_area(points)

        # Додаємо площу поточних прямокутників до загальної суми
        total_petunin_area += petunin_area
        total_min_rectangle_area += min_rectangle_area

    # Знаходимо середнє значення площі прямокутників
    avg_petunin_area = total_petunin_area / num_samples
    avg_min_rectangle_area = total_min_rectangle_area / num_samples

    print("Середня площа прямокутника Петуніна:", avg_petunin_area)
    print("Середня площа мінімального прямокутника:", avg_min_rectangle_area)

if __name__ == "__main__":
    main()