import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Modules.Home.Home import Ui_MainWindow
from Api.MainAPI import API
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QVBoxLayout, QMainWindow
from datetime import datetime, timedelta

from temp import week_days


class HomeExt(QMainWindow, Ui_MainWindow,API):
    name="siu"
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connector() #Kết nối MongoDB

    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        self.connector()
        self.layoutPie = self.Piechart
        self.layoutColumns = self.Columnchart
        self.show_Pie_Chart(self.layoutPie)  # hiển thị biểu đồ tròn ở ô màu đỏ thứ hai
        self.show_Colunm_Chart(self.layoutColumns)

    def show_Pie_Chart(self, layout: QVBoxLayout):
        # Dùng "$unwind" tách các elements trg Username1 thành từng doc lẻ
        # Nhóm các doc chung Categories("_id":"$Username1.Categories")
        # Cộng tổng Amount cho từng Categories ("$sum": "$Username1.Amount")
        # Thay tên ng dùng vào Username1
        pipeline = [
            {"$unwind": "$Username1"},
            {"$group": {"_id": None, "total_expenses": {"$sum": "$Username1.Amount"}}}
        ]

        total_expenses = list(self.expenses_collection.aggregate(pipeline))[0]["total_expenses"]
        category_pipeline = [
            {"$unwind": "$Username1"},  # Tách dữ liệu trong Username1
            {"$group": {"_id": "$Username1.Categories", "total": {"$sum": "$Username1.Amount"}}} #"_id" là bắt buộc nên k thể thay = category
        ]
        temp = list(self.expenses_collection.aggregate(category_pipeline))
        total_expenses_by_category= {cate["_id"]:cate["total"] for cate in temp} #{"Foods":35000,"Drugs":50000}

        #Set label cho Piechart
        label = list(total_expenses_by_category.keys())
        #Set size cho các pie trong piechart
        value= list(total_expenses_by_category.values())
        size=[i/total_expenses for i in value]

        # Tạo Figure và Axes để vẽ biểu đồ tròn
        fig, ax = plt.subplots(figsize=(5, 4))
        # Màu sắc cho mỗi lát bánh (tham khảo Bootstrap 5 colors)
        colors = ["#14B8A6", "#F59E0B", "#6366F1", "#3B82F6", "#3B82F6"]
        ax.pie(size, labels=label, autopct='%1.1f%%', startangle=140)
        ax.axis("equal") #đảm bảo piechart là hình tròn not elip
        # Chuyển Figure thành widget Canvas
        canvas = FigureCanvas(fig)
        # Thêm Canvas vào layout đã truyền vào
        layout.addWidget(canvas)

    def show_Colunm_Chart(self, layout: QVBoxLayout):
        try:
            category_pipeline = [
                {"$unwind": "$Username1"},  # Tách dữ liệu trong Username1
                {"$group": {"_id": "$Username1.Date", "total_by_date": {"$sum": "$Username1.Amount"}}}
                # "_id" là bắt buộc nên k thể thay = category
            ]
            temp = list(self.expenses_collection.aggregate(category_pipeline))
            expenses_by_date= [{i["_id"]:i["total_by_date"]} for i in temp]

            #Xác định 7 ngày gần nhất
            today = datetime.today()
            last_7_days = [(today - timedelta(days=i)).strftime("%m/%d/%Y") for i in range(7)][::-1]

            week_days=[] #Đây là biến cột x
            for i in range(1, 8):
                day = today - timedelta(days=i)
                # print(str(day),type(day)) #trả về dạng date có d/m/y + time
                week_days.append(day.strftime("%A"))

            #chuẩn bị giá trị cho các label tứ
            expenses_last_7_days = []
            print("expenses_by_date:",expenses_by_date)
            for i in last_7_days:
                for c in expenses_by_date:
                    try:
                        if str(c[i]).isdigit():
                            expenses_last_7_days.append(c[i])
                        else:
                            c[i] = 0
                            expenses_last_7_days.append(c[i])
                    except KeyError:
                        pass

            # Vẽ Columnchart
            n_groups = len(last_7_days)  # = 7
            print("n_groups:", n_groups)
            index = np.arange(n_groups)  # [0,1,2,3,4,5,6]
            # # index=[1,2,3,4,5,6,7]
            print("index:", len(index))
            print("expenses_last_7_days:",len(expenses_last_7_days))
            print("last_7_days:",len(last_7_days))
            # bar_width = 0.5  # Độ rộng mỗi cột

            # 3) Tạo Figure, Axes
            plt.close('all')  # Đóng mọi figure cũ, tránh vẽ chồng
            fig, ax = plt.subplots(figsize=(6, 4))

            # 4) Vẽ cột Expense (x = index) và Income (x = index + bar_width)
            ax.bar(index, expenses_last_7_days, color='#1814F3', label='Expense')
            print("#*10")
            # 5) Cài đặt trục X
            if len(index) == len(week_days):
                ax.set_xticks(index/2)  # Đặt nhãn ngày ở giữa 2 cột
                ax.set_xticklabels(week_days, rotation=45)
            else:
                print("❌ Lỗi: Số lượng ticks và nhãn không khớp!")
            try:
                ax.set_ylim(0, max(tuple(expenses_last_7_days)) + 50)
                ax.set_ylabel('Amount')
                # ax.legend()
                canvas = FigureCanvas(fig)
                ax.set_xlabel('Day')
                ax.set_title('Expense by Date in Weekdays')
                ax.legend()

                # Chuyển Figure thành widget Canvas
                plt.tight_layout()
                canvas = FigureCanvas(fig)
                # Thêm Canvas vào layout đã truyền vào

                layout.addWidget(canvas)
            except:
                print("Loi")
        except:
            pass

