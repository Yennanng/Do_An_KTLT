import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Modules.Home.Home import Ui_Home
from Api.Login_API import LoginAPI

class HomeExt(QMainWindow, Ui_Home,LoginAPI):

    def __init__(self,using_user=None):
        super().__init__()
        self.setupUi(self)
        self.connector() # Kết nối MongoDB
        self.using_user = using_user
        self.update_income_saving()
        self.update_total()
        self.update_balance()
        print("ở bên HomeEx, usingname đang có tên là:",self.using_user)


        # Kiểm tra và đảm bảo Piechart và Columnchart tồn tại
        try:
            self.layoutPie = self.Piechart
            self.layoutColumns = self.Columnchart
            self.show_Pie_Chart(self.layoutPie)  # Hiển thị biểu đồ tròn
            self.show_Colunm_Chart(self.layoutColumns)  # Hiển thị biểu đồ cột
        except Exception as e:
            print(e)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all)
        self.timer.start(5000)

        # Kết nối nút Reset
        if hasattr(self, "pushButton_Reset"):
            self.pushButton_Reset.clicked.connect(self.reset_charts)

    def update_all(self):
        """Gọi cả 3 hàm cập nhật cùng lúc"""
        self.update_income_saving()
        self.update_total()
        self.update_balance()

    def update_income_saving(self):
        """Lấy income và saving từ MongoDB và cập nhật lên giao diện."""
        user_data = self.users_collection.find_one({"username": self.using_user}, {"income": 1, "_id": 0})

        if user_data:
            income = user_data.get("income", 0)

            self.label_setincome.setText(f"{income}")
        else:
            self.label_setincome.setText("Income: N/A")

    def update_total(self):
        """Tính tổng Amount của người dùng và cập nhật vào label_setexpense"""
        pipeline = [
            {"$unwind": f"${self.using_user}"},
            {"$group": {"_id": None, "total_expenses": {"$sum": f"${self.using_user}.Amount"}}}
        ]

        total_expenses = list(self.expenses_collection.aggregate(pipeline))

        if total_expenses:  # Kiểm tra xem có dữ liệu không
            total_expenses_value = total_expenses[0]["total_expenses"]
            self.label_setexpense.setText(f"{total_expenses_value}")
        else:
            self.label_setexpense.setText("0")  # Nếu không có dữ liệu, hiển thị 0

    def update_balance(self):
        """Tính Balance = Income - Expense và cập nhật vào label_setmybalance"""

        # Lấy giá trị từ label_setincome và label_setexpense, nếu rỗng thì mặc định là 0
        income_text = self.label_setincome.text().strip()
        expense_text = self.label_setexpense.text().strip()

        # Chuyển đổi sang số (mặc định là 0 nếu không hợp lệ)
        income = float(income_text) if income_text.replace('.', '', 1).isdigit() else 0
        expense = float(expense_text) if expense_text.replace('.', '', 1).isdigit() else 0

        # Tính toán Balance
        balance = income - expense

        # Cập nhật vào label_setmybalance
        self.label_setmybalance.setText(f"{balance}")

    def reset_charts(self):
        """Xóa và vẽ lại biểu đồ"""
        self.clear_layout(self.layoutPie)
        self.clear_layout(self.layoutColumns)
        self.show_Pie_Chart(self.layoutPie)
        self.show_Colunm_Chart(self.layoutColumns)


    def clear_layout(self, layout):
        """Xóa tất cả widget trong layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_Pie_Chart(self, layout: QVBoxLayout):
        # Xóa biểu đồ cũ
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Pipeline truy vấn MongoDB
        print("Tên ng dùng đang dùng:",self.using_user)
        pipeline = [
            {"$unwind": f"${self.using_user}"},
            {"$group": {"_id": None, "total_expenses": {"$sum": f"${self.using_user}.Amount"}}}
        ]
        total_expenses = list(self.expenses_collection.aggregate(pipeline))
        print("Data để vẽ piechart",total_expenses)
        if not total_expenses:
            print(" Không có dữ liệu chi tiêu để vẽ biểu đồ tròn!")
            return

        total_expenses = total_expenses[0]["total_expenses"]

        category_pipeline = [
            {"$unwind": f"${self.using_user}"},
            {"$group": {"_id": f"${self.using_user}.Categories", "total": {"$sum": f"${self.using_user}.Amount"}}}
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
        """ Vẽ biểu đồ cột theo dữ liệu từ MongoDB với tính năng hover để hiển thị giá trị """
        try:
            # Xóa biểu đồ cũ
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            category_pipeline = [
                {"$unwind": f"${self.using_user}"},
                {"$group": {"_id": f"${self.using_user}.Date", "total_by_date": {"$sum": f"${self.using_user}.Amount"}}}
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
            bars = ax.bar(index, expenses_last_7_days, color='#1814F3', label='Expense')

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

            # Thêm annotation để hiển thị giá trị khi hover
            annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="w"),
                                arrowprops=dict(arrowstyle="->"))
            annot.set_visible(False)

            def update_annot(bar, event):
                """Cập nhật vị trí annotation khi hover"""
                x = bar.get_x() + bar.get_width() / 2
                y = bar.get_height()
                annot.xy = (x, y)
                annot.set_text(f"{y:,.0f} VND")  # Hiển thị số tiền với định dạng dễ đọc
                annot.set_visible(True)
                canvas.draw_idle()

            def on_hover(event):
                """Xử lý sự kiện hover chuột"""
                vis = annot.get_visible()
                for bar in bars:
                    if bar.contains(event)[0]:
                        update_annot(bar, event)
                        return
                if vis:
                    annot.set_visible(False)
                    canvas.draw_idle()

            canvas.mpl_connect("motion_notify_event", on_hover)

        except Exception as e:
            print("Lỗi khi vẽ biểu đồ cột:", e)
