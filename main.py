import time

import numpy as np
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d

import matplotlib.pyplot as plt

start_time = time.time()

def read_nodes(file_path):
    """Чтение координат точек из файла model.node

        - file_path : str
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # пропуск первой строкм с заголовком
        # lines = file.readlines()
        nodes = []
        for line in lines:
            parts = line.strip().split()
            x, y = float(parts[1]), float(parts[2]) # менять индексы в соответствии с входными данными
            nodes.append((x, y))
    return np.array(nodes)

def generate_elements(nodes):
    """Генерация элементов (треугольников) с использованием триангуляции Делоне"""
    delaunay = Delaunay(nodes)
    return delaunay.simplices

def plot_triangles(nodes, elements):
    """Визуализация сгенерированных треугольников"""
    plt.figure(figsize=(10, 10))
    plt.triplot(nodes[:, 0], nodes[:, 1], elements, 'go-', lw=1.0)
    plt.plot(nodes[:, 0], nodes[:, 1], 'ro',markersize=2)
    plt.title("триангуляция Делоне")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

def save_elements(elements, output_file):
    """Сохранение элементов в файл"""
    with open(output_file, 'w') as file:
        for i, element in enumerate(elements):
            file.write(f"{i}: {element[0]} {element[1]} {element[2]}\n")

def get_thiessen_polygon(points):
    vor = Voronoi(points)
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)

    ax.plot(points[:, 0], points[:, 1], 'o', markersize=5, color='red')

    # ax.set_xlim(0, 1)
    # ax.set_ylim(0, 1)
    plt.show()

nodes_file = 'ASMO/model.node' # укажите ваш путь к Входным данным здесь
output_file = 'ASMO/big_model_elements_result.txt' # Путь для сохранения выходного файла


nodes = read_nodes(nodes_file)
print(len(nodes))

elements = generate_elements(nodes)

get_thiessen_polygon(nodes)

save_elements(elements, output_file)


# plot_triangles(nodes, elements)

end_time = time.time()
execution_time = end_time - start_time
print(f'Обработка заняла: {execution_time}')