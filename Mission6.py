import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class ScatterPlotApp:
    def __init__(self, root, df):
        self.root = root
        self.root.title("산점도 분석기 - 최종 수정판")
        self.df = df

        # 숫자 데이터만 필터링 (X, Y축용)
        self.numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        self.all_cols = df.columns.tolist()

        self.setup_ui()

    def setup_ui(self):
        control_frame = ttk.Frame(self.root, padding="15")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # X축
        ttk.Label(control_frame, text="X축:").grid(row=0, column=0, padx=5)
        self.x_var = tk.StringVar()
        self.x_combo = ttk.Combobox(control_frame, textvariable=self.x_var, values=self.numeric_cols, state="readonly")
        self.x_combo.grid(row=0, column=1, padx=5)
        if self.numeric_cols: self.x_combo.current(0)

        # Y축
        ttk.Label(control_frame, text="Y축:").grid(row=0, column=2, padx=5)
        self.y_var = tk.StringVar()
        self.y_combo = ttk.Combobox(control_frame, textvariable=self.y_var, values=self.numeric_cols, state="readonly")
        self.y_combo.grid(row=0, column=3, padx=5)
        if len(self.numeric_cols) > 1: self.y_combo.current(1)

        # 색상 구분
        ttk.Label(control_frame, text="색상 구분:").grid(row=1, column=0, padx=5, pady=10)
        self.hue_var = tk.StringVar(value="전공")
        self.hue_combo = ttk.Combobox(control_frame, textvariable=self.hue_var, values=["없음"] + self.all_cols,
                                      state="readonly")
        self.hue_combo.grid(row=1, column=1, padx=5)

        # 추세선 체크박스
        self.reg_var = tk.BooleanVar(value=False)
        self.reg_check = ttk.Checkbutton(control_frame, text="추세선 표시", variable=self.reg_var)
        self.reg_check.grid(row=1, column=2, padx=5)

        # 버튼
        self.btn_draw = ttk.Button(control_frame, text="그래프 업데이트", command=self.update_plot)
        self.btn_draw.grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

        # 그래프 영역
        self.plot_frame = ttk.Frame(self.root, padding="10")
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_plot(self):
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        hue_col = self.hue_var.get()
        show_reg = self.reg_var.get()

        self.ax.clear()
        current_hue = None if hue_col == "없음" else hue_col

        try:
            # 1. 추세선을 먼저 그립니다 (색상 구분 없이 전체 데이터 기준)
            if show_reg:
                sns.regplot(data=self.df, x=x_col, y=y_col, ax=self.ax,
                            scatter=False, color='red', line_kws={'label': '전체 추세선'})

            # 2. 산점도를 그 위에 그립니다 (색상 구분 적용)
            sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=current_hue, ax=self.ax)

            # 범례 표시
            if current_hue or show_reg:
                self.ax.legend()

            self.ax.set_title(f"[{x_col}] 과 [{y_col}]의 상관관계 분석")
            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("오류 발생", f"그래프를 그리는 중 문제가 발생했습니다.\n{e}")


if __name__ == "__main__":
    try:
        df = pd.read_csv('6주차_실습4.csv')
        root = tk.Tk()
        app = ScatterPlotApp(root, df)
        root.mainloop()
    except Exception as e:
        print(f"오류: {e}")