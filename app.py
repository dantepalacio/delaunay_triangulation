import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QCheckBox, QLabel
from PyQt5.QtCore import Qt
from utils import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Триангуляция Делоне и полигоны Тиссена")
        self.setGeometry(50, 50, 500, 300)  
        self.layout = QVBoxLayout()

        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        self.version_label = QLabel("version 0.3")
        self.version_label.setAlignment(Qt.AlignRight)
        self.version_label.setStyleSheet("font-size: 8pt;")  
        self.top_layout.addWidget(self.version_label)

        self.label = QLabel("Выберите файл с точками")
        self.layout.addWidget(self.label)

        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.file_button)

        # Layout for Delaunay
        self.delaunay_layout = QVBoxLayout()
        self.delaunay_checkbox_layout = QHBoxLayout()
        self.delaunay_checkbox = QCheckBox("Триангуляция Делоне")
        self.delaunay_checkbox.stateChanged.connect(self.update_save_path_button_visibility)
        self.delaunay_checkbox.stateChanged.connect(self.update_calculate_button_state)
        self.delaunay_checkbox_layout.addWidget(self.delaunay_checkbox)

        self.triangulation_output_path_button = QPushButton("Указать путь для файла .tri")
        self.triangulation_output_path_button.clicked.connect(self.set_triangulation_output_path)
        self.triangulation_output_path_button.setVisible(False)  # Скрыта изначально
        self.delaunay_checkbox_layout.addWidget(self.triangulation_output_path_button)

        self.triangulation_output_path_label = QLabel("")
        self.triangulation_output_path_label.setAlignment(Qt.AlignRight)
        self.triangulation_output_path_label.setVisible(False)  # Скрыта изначально
        self.delaunay_layout.addLayout(self.delaunay_checkbox_layout)
        self.delaunay_layout.addWidget(self.triangulation_output_path_label)

        self.triangulation_output_path = None
        self.layout.addLayout(self.delaunay_layout)

        # Layout for Thiessen
        self.thiessen_layout = QVBoxLayout()
        self.thiessen_checkbox_layout = QHBoxLayout()
        self.thiessen_checkbox = QCheckBox("Полигоны Тиссена")
        self.thiessen_checkbox.stateChanged.connect(self.update_save_path_button_visibility)
        self.thiessen_checkbox.stateChanged.connect(self.update_calculate_button_state)
        self.thiessen_checkbox_layout.addWidget(self.thiessen_checkbox)

        self.thiessen_output_path_button = QPushButton("Указать путь для файла .poly")
        self.thiessen_output_path_button.clicked.connect(self.set_thiessen_output_path)
        self.thiessen_output_path_button.setVisible(False)  # Скрыта изначально
        self.thiessen_checkbox_layout.addWidget(self.thiessen_output_path_button)

        self.thiessen_output_path_label = QLabel("")
        self.thiessen_output_path_label.setAlignment(Qt.AlignRight)
        self.thiessen_output_path_label.setVisible(False)  # Скрыта изначально
        self.thiessen_layout.addLayout(self.thiessen_checkbox_layout)
        self.thiessen_layout.addWidget(self.thiessen_output_path_label)

        self.thiessen_output_path = None
        self.layout.addLayout(self.thiessen_layout)

        self.save_delaunay_plot_checkbox = QCheckBox("Сохранить график Триангуляции")
        self.save_delaunay_plot_checkbox.setVisible(False)  
        self.layout.addWidget(self.save_delaunay_plot_checkbox)

        self.save_thiessen_plot_checkbox = QCheckBox("Сохранить график полигонов Тиссена")
        self.save_thiessen_plot_checkbox.setVisible(False)  
        self.layout.addWidget(self.save_thiessen_plot_checkbox)

        self.skip_first_line_checkbox = QCheckBox("Пропускать первую строку")
        self.layout.addWidget(self.skip_first_line_checkbox)

        self.use_indices_0_1_checkbox = QCheckBox("Использовать индексы 0 и 1 для координат")
        self.layout.addWidget(self.use_indices_0_1_checkbox)

        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)
        self.calculate_button.setEnabled(False) 
        self.layout.addWidget(self.calculate_button)

        self.setLayout(self.layout)
        
        # Изначально нет выбранного файла
        self.nodes_file = None

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл с точками", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.nodes_file = file_name
            self.label.setText(f"Файл выбран: {file_name}")
            self.update_calculate_button_state()  # Проверяем, можно ли включить кнопку "Рассчитать"

    def set_triangulation_output_path(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Укажите путь для .tri файла", "", "Tri Files (*.tri)", options=options)
        if file_name:
            self.triangulation_output_path = file_name
            self.triangulation_output_path_label.setText(f"Путь: {file_name}")
            self.triangulation_output_path_label.setVisible(True)
            self.update_calculate_button_state()  # Проверяем, можно ли включить кнопку "Рассчитать"

    def set_thiessen_output_path(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Укажите путь для .poly файла", "", "Poly Files (*.poly)", options=options)
        if file_name:
            self.thiessen_output_path = file_name
            self.thiessen_output_path_label.setText(f"Путь: {file_name}")
            self.thiessen_output_path_label.setVisible(True)
            self.update_calculate_button_state()  # Проверяем, можно ли включить кнопку "Рассчитать"

    def update_save_path_button_visibility(self):
        # Обновление видимости кнопки для указания пути триангуляции
        if self.delaunay_checkbox.isChecked():
            self.triangulation_output_path_button.setVisible(True)
            self.triangulation_output_path_label.setVisible(True if self.triangulation_output_path else False)
            self.save_delaunay_plot_checkbox.setVisible(True)
        else:
            self.triangulation_output_path_button.setVisible(False)
            self.triangulation_output_path_label.setVisible(False)
            self.save_delaunay_plot_checkbox.setVisible(False)
            self.triangulation_output_path = None

        # Обновление видимости кнопки для указания пути полигонов Тиссена
        if self.thiessen_checkbox.isChecked():
            self.thiessen_output_path_button.setVisible(True)
            self.thiessen_output_path_label.setVisible(True if self.thiessen_output_path else False)
            self.save_thiessen_plot_checkbox.setVisible(True)
        else:
            self.thiessen_output_path_button.setVisible(False)
            self.thiessen_output_path_label.setVisible(False)
            self.save_thiessen_plot_checkbox.setVisible(False)
            self.thiessen_output_path = None
        
        self.update_calculate_button_state()  # Проверяем, можно ли включить кнопку "Рассчитать"

    def update_calculate_button_state(self):
        # Кнопка "Рассчитать" активна только если выбран входной файл и указан хотя бы один метод с путём к файлу
        if self.nodes_file and (
            (self.delaunay_checkbox.isChecked() and self.triangulation_output_path) or
            (self.thiessen_checkbox.isChecked() and self.thiessen_output_path)
        ):
            self.calculate_button.setEnabled(True)
        else:
            self.calculate_button.setEnabled(False)

    def calculate(self):
        if not self.nodes_file:
            self.label.setText("Пожалуйста, выберите файл.")
            return

        skip_first_line = self.skip_first_line_checkbox.isChecked()
        use_indices_0_1 = self.use_indices_0_1_checkbox.isChecked()
        nodes = read_nodes(self.nodes_file, skip_first_line, use_indices_0_1)

        if self.delaunay_checkbox.isChecked():
            elements = delauney_triangulation(nodes)
            if self.triangulation_output_path:
                save_triangulation(elements, self.triangulation_output_path)
                print(f"Триангуляция Делоне сохранена в {self.triangulation_output_path}")
            if self.save_delaunay_plot_checkbox.isChecked():
                plot_triangles(nodes, elements, save_path='triangulation_plot.png')

        if self.thiessen_checkbox.isChecked():
            if self.thiessen_output_path:
                vor = get_thiessen_polygon(nodes, self.thiessen_output_path)
                print(f"Полигоны Тиссена сохранены в {self.thiessen_output_path}")
            if self.save_thiessen_plot_checkbox.isChecked():
                plot_thiessen(vor, nodes, save_path='thiessen_plot.png')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())