from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSet,
    QChart,
    QChartView,
    QHorizontalStackedBarSeries,
    QValueAxis,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter


class BarChartBuilder:
    """
    A class to build and update bar charts.

    This class provides methods to create and update bar charts using the PySide6 QtCharts library.
    It allows for customization of the chart's title, axis labels, and data series.

    Attributes:
        series (QHorizontalStackedBarSeries): The data series for the chart.
        axisY (QBarCategoryAxis): The Y-axis for the chart.
        axisX (QValueAxis): The X-axis for the chart.
        chart (QChart): The chart object.

    Methods:
        __init__(): Initializes the chart builder with default settings.
        build(chart_data: dict): Builds the chart with the provided data.
        update(chart_data: dict): Updates the chart with new data.
    """

    def __init__(self):
        """
        Initializes the chart builder with default settings.

        Creates a new instance of the QHorizontalStackedBarSeries, QBarCategoryAxis, QValueAxis, and QChart classes.
        """
        self.series = QHorizontalStackedBarSeries()
        self.axisY = QBarCategoryAxis()
        self.axisX = QValueAxis()
        self.chart = QChart()

    def build(self, chart_data: dict):
        """
        Builds the chart with the provided data.

        Args:
            chart_data (dict): A dictionary containing the chart data.

        Returns:
            QChartView: The chart view object.
        """
        self.series.clear()
        self.axisY.clear()

        group_count = chart_data["group_count"]
        for param_value in range(group_count):
            param = chart_data["file_type"][param_value]
            value = chart_data["count"][param_value]
            bar_set = QBarSet(param)
            bar_set.append(value)
            self.series.append(bar_set)

        self.chart.addSeries(self.series)
        self.chart.setTitle("File types count")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["File type"]
        self.axisY.append(categories)
        self.axisX.setLabelFormat("%d")

        max_range = sum(chart_data["count"])
        self.axisX.setRange(0, max_range)

        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.series.attachAxis(self.axisY)
        self.series.attachAxis(self.axisX)

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view

    def update(self, chart_data: dict):
        """
        Updates the chart with new data.

        Args:
            chart_data (dict): A dictionary containing the new chart data.
        """
        self.series.clear()
        self.axisY.clear()

        group_count = chart_data["group_count"]
        for param_value in range(group_count):
            param = chart_data["file_type"][param_value]
            value = chart_data["count"][param_value]
            bar_set = QBarSet(param)
            bar_set.append(value)
            self.series.append(bar_set)

        self.chart.addSeries(self.series)
        self.chart.setTitle("File types count")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["File type"]
        self.axisY.append(categories)

        self.axisX.setLabelFormat("%d")
        max_range = sum(chart_data["count"])
        self.axisX.setRange(0, max_range)

        self.chart.update()
