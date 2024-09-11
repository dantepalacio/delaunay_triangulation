import numpy as np
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt


def read_nodes(file_path, skip_first_line, use_indices_0_1):
    """Чтение координат точек из файла model.node"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if skip_first_line:
            lines = lines[1:]
        nodes = []
        for line in lines:
            parts = line.strip().split()
            if use_indices_0_1:
                x, y = float(parts[0]), float(parts[1])
            else:
                x, y = float(parts[1]), float(parts[2])
            nodes.append((x, y))
    print(nodes[0])
    return np.array(nodes)


def delauney_triangulation(nodes):
    """Генерация элементов с использованием триангуляции Делоне"""
    delaunay = Delaunay(nodes)
    return delaunay.simplices

def plot_triangles(nodes, elements, save_path=None):
    """Визуализация сгенерированных треугольников"""
    plt.figure(figsize=(10, 10))
    plt.triplot(nodes[:, 0], nodes[:, 1], elements, 'go-', lw=1.0)
    plt.plot(nodes[:, 0], nodes[:, 1], 'ro', markersize=2)
    plt.title("Триангуляция Делоне")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')  # Устанавливаем равные масштабы по осям
    if save_path:
        plt.savefig(save_path, format='png', dpi=300)  # Сохраняем график
    plt.show()


def save_triangulation(elements, output_file):
    """Сохранение триангуляции в файл"""
    with open(output_file, 'w') as file:
        for i, element in enumerate(elements):
            # file.write(f"{i}: {element[0]} {element[1]} {element[2]}\n")
            file.write(f"{element[0]} {element[1]} {element[2]}\n")


def save_voronoi_vertices(vor, output_file):
    with open(output_file, 'w') as f:
        for region in vor.regions:
            if not -1 in region and len(region) > 0:
                polygon = [vor.vertices[i] for i in region]
                for vertex in polygon:
                    f.write(f"{vertex[0]} {vertex[1]}\n")
                f.write("\n")


def get_thiessen_polygon(points, thiessen_output_file):
    vor = Voronoi(points)
    save_voronoi_vertices(vor, thiessen_output_file)
    return vor

def plot_thiessen(vor, points, save_path=None):
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)
    ax.plot(points[:, 0], points[:, 1], 'o', markersize=5, color='red')
    ax.set_aspect('equal')  # Устанавливаем равные масштабы по осям
    if save_path:
        plt.savefig(save_path, format='png', dpi=300)  # Сохраняем график
    plt.show()
