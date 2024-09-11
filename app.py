import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QCheckBox, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from utils import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Триангуляция Делоне и полигоны Тиссена")
        self.setGeometry(50, 50, 400, 300)  
        self.layout = QVBoxLayout()

        # Верхний горизонтальный layout для версии
        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        # Метка для отображения версии
        self.version_label = QLabel("version 0.2")
        self.version_label.setAlignment(Qt.AlignRight)
        self.version_label.setStyleSheet("font-size: 8pt;")  # Устанавливаем маленький шрифт
        self.top_layout.addWidget(self.version_label)

        # Метка для отображения выбранного файла
        self.label = QLabel("Выберите файл с точками")
        self.layout.addWidget(self.label)

        # Кнопка для выбора файла
        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.file_button)

        # Галочка для триангуляции Делоне
        self.delaunay_checkbox = QCheckBox("Триангуляция Делоне")
        self.delaunay_checkbox.stateChanged.connect(self.update_calculate_button_state)
        self.delaunay_checkbox.stateChanged.connect(self.update_save_plot_checkboxes_visibility)
        self.layout.addWidget(self.delaunay_checkbox)

        # Галочка для полигонов Тиссена
        self.thiessen_checkbox = QCheckBox("Полигоны Тиссена")
        self.thiessen_checkbox.stateChanged.connect(self.update_calculate_button_state)
        self.thiessen_checkbox.stateChanged.connect(self.update_save_plot_checkboxes_visibility)
        self.layout.addWidget(self.thiessen_checkbox)

        # Галочка для сохранения графика Триангуляции
        self.save_delaunay_plot_checkbox = QCheckBox("Сохранить график Триангуляции")
        self.save_delaunay_plot_checkbox.setVisible(False)  # Изначально скрыта
        self.layout.addWidget(self.save_delaunay_plot_checkbox)

        # Галочка для сохранения графика полигонов Тиссена
        self.save_thiessen_plot_checkbox = QCheckBox("Сохранить график полигонов Тиссена")
        self.save_thiessen_plot_checkbox.setVisible(False)  # Изначально скрыта
        self.layout.addWidget(self.save_thiessen_plot_checkbox)

        # Галочка для пропуска первой строки
        self.skip_first_line_checkbox = QCheckBox("Пропускать первую строку")
        self.layout.addWidget(self.skip_first_line_checkbox)

        # Галочка для использования индексов 0 и 1
        self.use_indices_0_1_checkbox = QCheckBox("Использовать индексы 0 и 1 для координат")
        self.layout.addWidget(self.use_indices_0_1_checkbox)

        # Кнопка для расчета
        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)
        self.calculate_button.setEnabled(False)  # Изначально кнопка неактивна
        self.layout.addWidget(self.calculate_button)

        self.setLayout(self.layout)

    def open_file_dialog(self):
        global nodes_file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл с точками", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            nodes_file = file_name
            self.label.setText(f"Файл выбран: {file_name}")

    def update_calculate_button_state(self):
        self.calculate_button.setEnabled(self.delaunay_checkbox.isChecked() or self.thiessen_checkbox.isChecked())

    def update_save_plot_checkboxes_visibility(self):
        # скрытие галочек графиков
        self.save_delaunay_plot_checkbox.setVisible(self.delaunay_checkbox.isChecked())
        self.save_thiessen_plot_checkbox.setVisible(self.thiessen_checkbox.isChecked())

    def calculate(self):
        if nodes_file is None:
            self.label.setText("Пожалуйста, выберите файл.")
            return

        skip_first_line = self.skip_first_line_checkbox.isChecked()
        use_indices_0_1 = self.use_indices_0_1_checkbox.isChecked()
        nodes = read_nodes(nodes_file, skip_first_line, use_indices_0_1)

        if self.delaunay_checkbox.isChecked():
            elements = delauney_triangulation(nodes)
            save_triangulation(elements, 'triangulation_output.txt')
            print(f"Триангуляция Делоне сохранена в triangulation_output.txt")
            if self.save_delaunay_plot_checkbox.isChecked():
                plot_triangles(nodes, elements, save_path='triangulation_plot.png')

        if self.thiessen_checkbox.isChecked():
            vor = get_thiessen_polygon(nodes, 'thiessen_output.txt')
            print(f"Полигоны Тиссена сохранены в thiessen_output.txt")
            if self.save_thiessen_plot_checkbox.isChecked():
                plot_thiessen(vor, nodes, save_path='thiessen_plot.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())