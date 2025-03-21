import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Modules.Home.Home import Ui_Home
from Api.MainAPI import API


class HomeExt(QMainWindow, Ui_Home, API):
    name = "siu"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connector()  # Kết nối MongoDB

        # Kiểm tra và đảm bảo Piechart và Columnchart tồn tại
        try:
            self.layoutPie = self.Piechart
            self.layoutColumns = self.Columnchart
            self.show_Pie_Chart(self.layoutPie)  # Hiển thị biểu đồ tròn
            self.show_Colunm_Chart(self.layoutColumns)  # Hiển thị biểu đồ cột
        except AttributeError:
            print("Lỗi: Không tìm thấy Piechart hoặc Columnchart trong UI!")

    def show_Pie_Chart(self, layout: QVBoxLayout):
        # Pipeline truy vấn MongoDB
        pipeline = [
            {"$unwind": "$Username1"},
            {"$group": {"_id": None, "total_expenses": {"$sum": "$Username1.Amount"}}}
        ]
        total_expenses = list(self.expenses_collection.aggregate(pipeline))
        if not total_expenses:
            print(" Không có dữ liệu chi tiêu để vẽ biểu đồ tròn!")
            return

        total_expenses = total_expenses[0]["total_expenses"]

        category_pipeline = [
            {"$unwind": "$Username1"},
            {"$group": {"_id": "$Username1.Categories", "total": {"$sum": "$Username1.Amount"}}}
        ]
        temp = list(self.expenses_collection.aggregate(category_pipeline))
        if not temp:
            print("Không có dữ liệu danh mục chi tiêu!")
            return

        total_expenses_by_category = {cate["_id"]: cate["total"] for cate in temp}

        labels = list(total_expenses_by_category.keys())
        values = list(total_expenses_by_category.values())
        sizes = [i / total_expenses for i in values]

        # Vẽ biểu đồ tròn
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis("equal")

        # Hiển thị trên UI
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def show_Colunm_Chart(self, layout: QVBoxLayout):
        """ Vẽ biểu đồ cột theo dữ liệu từ MongoDB """
        try:
            category_pipeline = [
                {"$unwind": "$Username1"},
                {"$group": {"_id": "$Username1.Date", "total_by_date": {"$sum": "$Username1.Amount"}}}
            ]
            temp = list(self.expenses_collection.aggregate(category_pipeline))

            if not temp:
                print("Không có dữ liệu để vẽ biểu đồ cột!")
                return

            expenses_by_date = {i["_id"]: i["total_by_date"] for i in temp}

            today = datetime.today()
            last_7_days = [(today - timedelta(days=i)).strftime("%m-%d-%Y") for i in range(7)][::-1]
            week_days = [(today - timedelta(days=i)).strftime("%A") for i in range(7)][::-1]

            expenses_last_7_days = [expenses_by_date.get(day, 0) for day in last_7_days]

            n_groups = len(last_7_days)
            index = np.arange(n_groups)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(index, expenses_last_7_days, color='#1814F3', label='Expense')

            ax.set_xticks(index)
            ax.set_xticklabels(week_days, rotation=45)
            ax.set_ylim(0, max(expenses_last_7_days) + 50)
            ax.set_ylabel('Amount')
            ax.set_xlabel('Date')
            ax.set_title('Expense by Date in Weekdays')
            ax.legend()

            plt.tight_layout()
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)

        except Exception as e:
            print("Lỗi khi vẽ biểu đồ cột:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    home_window = HomeExt()
    home_window.show()
    sys.exit(app.exec())
