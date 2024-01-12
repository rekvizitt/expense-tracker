import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtChart import QChartView, QChart, QPieSeries
from PyQt5.QtCore import Qt

class ExpenseManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Manager")
        self.resize(500, 600)
        self.setWindowIcon(QIcon("src/icon.ico"))

        self.create_menu()
        self.create_chart()

    def create_menu(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("View")
        add_menu = menubar.addMenu("Add")
        options_menu = menubar.addMenu("Options")

    def create_chart(self):
        data_file = "src/data.csv"

        if not os.path.isfile(data_file):
            # Создание пустого файла, если он не существует
            with open(data_file, "w") as file:
                create_data_file(data_file)

        # Загрузка данных из файла с помощью Pandas
        data = pd.read_csv(data_file)

        # Создание кругового графика с сегментами с помощью Matplotlib
        chart_data = data.groupby("scope").sum()
        chart_data = chart_data.reset_index()

        # Создание круговой диаграммы
        plt.figure(figsize=(6, 6))
        plt.pie(chart_data["expense"], labels=chart_data["scope"], autopct="%1.1f%%")

        # Создание графика QtChart
        chart = QChart()
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        # Создание серии для графика QtChart
        series = QPieSeries()
        for label, value in zip(chart_data["scope"], chart_data["expense"]):
            series.append(label, value)

        chart.addSeries(series)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

def create_data_file(file_path):
    # Создание файла с заданными колонками
    data = pd.DataFrame(columns=["title", "scope", "expense", "currency"])
    data.to_csv(file_path, index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseManagerWindow()
    window.show()
    sys.exit(app.exec_())