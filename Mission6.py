import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox

# 1. 한글 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class ScatterPlotApp:
    def __init__(self, root, df):
        self.root = root
        self.root.title("산점도 분석기 - 숫자 데이터 전용")
        self.df = df

        # [해결책] 데이터 중 '숫자'로 된 컬럼만 골라내서 리스트 만들기
        self.numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        # 색상 구분용은 모든 컬럼 사용
        self.all_cols = df.columns.tolist()

        self.setup_ui()

    def setup_ui(self):
        # 상단 설정 바
        control_frame = ttk.Frame(self.root, padding="15")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # X축: 숫자 데이터만 표시되도록 설정
        ttk.Label(control_frame, text="X축 (숫자):").grid(row=0, column=0, padx=5)
        self.x_var = tk.StringVar()
        self.x_combo = ttk.Combobox(control_frame, textvariable=self.x_var, values=self.numeric_cols, state="readonly")
        self.x_combo.grid(row=0, column=1, padx=5)
        if self.numeric_cols: self.x_combo.current(0)

        # Y축: 숫자 데이터만 표시되도록 설정
        ttk.Label(control_frame, text="Y축 (숫자):").grid(row=0, column=2, padx=5)
        self.y_var = tk.StringVar()
        self.y_combo = ttk.Combobox(control_frame, textvariable=self.y_var, values=self.numeric_cols, state="readonly")
        self.y_combo.grid(row=0, column=3, padx=5)
        if len(self.numeric_cols) > 1: self.y_combo.current(1)

        # 색상 구분 (범주형 가능)
        ttk.Label(control_frame, text="색상 구분:").grid(row=1, column=0, padx=5, pady=10)
        self.hue_var = tk.StringVar(value="전공")
        self.hue_combo = ttk.Combobox(control_frame, textvariable=self.hue_var, values=["없음"] + self.all_cols,
                                      state="readonly")
        self.hue_combo.grid(row=1, column=1, padx=5)

        # 추세선 체크박스
        self.reg_var = tk.BooleanVar(value=False)
        self.reg_check = ttk.Checkbutton(control_frame, text="추세선 표시", variable=self.reg_var)
        self.reg_check.grid(row=1, column=2, padx=5)

        # 업데이트 버튼
        self.btn_draw = ttk.Button(control_frame, text="그래프 그리기", command=self.update_plot)
        self.btn_draw.grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

        # 그래프 출력 프레임
        self.plot_frame = ttk.Frame(self.root, padding="10")
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Matplotlib Figure 생성 (별도 창 안 뜨게 방지)
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_plot(self):
        # 현재 선택된 값 가져오기
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        hue_col = self.hue_var.get()
        show_reg = self.reg_var.get()

        self.ax.clear()
        current_hue = None if hue_col == "없음" else hue_col

        try:
            # 그래프 그리기
            if show_reg:
                # 회귀선(추세선) 표시
                sns.regplot(data=self.df, x=x_col, y=y_col, ax=self.ax, scatter_kws={'alpha': 0.3})
                if current_hue:
                    sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=current_hue, ax=self.ax)
            else:
                # 일반 산점도
                sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=current_hue, ax=self.ax)

            self.ax.set_title(f"{x_col}와 {y_col}의 상관관계")
            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("오류", f"그래프를 생성할 수 없습니다.\n{e}")


# 실행부
if __name__ == "__main__":
    try:
        # 파일 이름이 정확한지 확인하세요!
        df = pd.read_csv('6주차_실습4.csv')
        root = tk.Tk()
        app = ScatterPlotApp(root, df)
        root.mainloop()
    except FileNotFoundError:
        print("CSV 파일을 찾을 수 없습니다. 파일명을 확인해 주세요.")