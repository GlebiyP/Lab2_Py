import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def min_area_rectangle(points):
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]

    min_area = np.inf
    min_rectangle = None

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
                                min_rectangle = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

    return min_rectangle

# Генерація випадкових точок
num_points = 100

np.random.seed(0)
points = np.random.rand(num_points, 2)

# Знаходження мінімального прямокутника
rectangle = min_area_rectangle(points)

# Вивід результату на графіку
plt.plot(points[:,0], points[:,1], 'o', label='Точки')
for simplex in ConvexHull(points).simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

rectangle.append(rectangle[0])  # З'єднання останньої точки з першою для закриття фігури
rectangle = np.array(rectangle)
plt.plot(rectangle[:, 0], rectangle[:, 1], 'r--', label='Мінімальний прямокутник')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Мінімальний прямокутник Петуніна')
plt.legend()
plt.axis('equal')
plt.show()