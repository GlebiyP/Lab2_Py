import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

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

def draw_rectangle(points, line, parallel_lines, perpendicular_lines):
    plt.scatter(points[:,0], points[:,1], color='blue')
    plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color='red')
    
    for parallel_line in parallel_lines:
        for i in range(len(parallel_line)-1):
            plt.plot([parallel_line[i][0], parallel_line[i+1][0]], [parallel_line[i][1], parallel_line[i+1][1]], color='green')
    
    for perpendicular_line in perpendicular_lines:
        for i in range(len(perpendicular_line)-1):
            plt.plot([perpendicular_line[i][0], perpendicular_line[i+1][0]], [perpendicular_line[i][1], perpendicular_line[i+1][1]], color='green')

    # Побудова опуклої оболонки
    hull = ConvexHull(points)
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    plt.axis('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Petunin Rectangle')
    plt.grid(True)
    plt.show()

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

def main():
    # Задаємо кількість точок
    num_points = 100
    
    # Генеруємо випадкові точки
    points = np.random.rand(num_points, 2) * 10  # Генеруємо в діапазоні [0, 10)
    
    # Знаходимо дві найвіддаленіші точки
    furthest_points = find_furthest_points(points)
    
    # Знаходимо пряму між найвіддаленішими точками
    line = furthest_points
    
    # Знаходимо по одній найвіддаленішій точці від прямої з кожної сторони
    left_point, right_point = find_points_furthest_from_line(line, points)
    
    # Знаходимо паралельні прямі, що проходять через ці точки
    parallel_lines = find_parallel_lines(line, [left_point, right_point])
    
    # Знаходимо перпендикулярні прямі, що проходять через найвіддаленіші точки
    perpendicular_lines = find_perpendicular_lines(line, furthest_points)
    
    # Малюємо прямокутник Петуніна
    draw_rectangle(points, line, parallel_lines, perpendicular_lines)

if __name__ == "__main__":
    main()