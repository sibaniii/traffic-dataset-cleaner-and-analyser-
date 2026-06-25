# ============================================================
# SMART TRAFFIC ANALYSIS DASHBOARD
# FINAL STABLE + IMPROVED VISUAL VERSION
# ============================================================

# INSTALL REQUIRED LIBRARIES:
#
# pip install pandas matplotlib seaborn openpyxl
# pip install customtkinter tkinterdnd2
#
# ============================================================

import customtkinter as ctk

# FIX PYTHON 3.12 CUSTOMTKINTER ISSUE
ctk.deactivate_automatic_dpi_awareness()

from tkinter import (
    messagebox,
    filedialog
)

from tkinterdnd2 import (
    TkinterDnD,
    DND_FILES
)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# SETTINGS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# BETTER GRAPH STYLE
plt.style.use("seaborn-v0_8")


# ============================================================
# MAIN APP
# ============================================================

class TrafficDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart Traffic Analysis Dashboard"
        )

        self.root.geometry("1450x850")

        self.df = None

        # ====================================================
        # SIDEBAR
        # ====================================================

        self.sidebar = ctk.CTkFrame(
            root,
            width=250,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="TRAFFIC\nDASHBOARD",
            font=("Arial", 28, "bold")
        ).pack(pady=30)

        # ====================================================
        # BUTTONS
        # ====================================================

        buttons = [
            ("Browse Dataset", self.browse_file),
            ("Auto Clean Data", self.clean_data),
            ("Show Dataset Info", self.show_info),
            ("Generate Visualization", self.visualize_window),
            ("Traffic Insights", self.generate_insights)
        ]

        for text, cmd in buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd
            )

            btn.pack(
                pady=10,
                padx=20,
                fill="x"
            )

        # ====================================================
        # MAIN AREA
        # ====================================================

        self.main = ctk.CTkFrame(root)

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            self.main,
            text="Smart Traffic Analysis Dashboard",
            font=("Arial", 30, "bold")
        ).pack(pady=20)

        # ====================================================
        # KPI CARDS
        # ====================================================

        self.cards_frame = ctk.CTkFrame(self.main)

        self.cards_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.rows_card = self.create_card(
            "Total Records",
            "0"
        )

        self.cols_card = self.create_card(
            "Columns",
            "0"
        )

        self.null_card = self.create_card(
            "Missing Values",
            "0"
        )

        self.traffic_card = self.create_card(
            "Avg Traffic",
            "0"
        )

        # ====================================================
        # DRAG & DROP AREA
        # ====================================================

        self.drop_frame = ctk.CTkFrame(
            self.main,
            height=150
        )

        self.drop_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="⬇ DRAG & DROP TRAFFIC DATASET HERE ⬇",
            font=("Arial", 22, "bold")
        )

        self.drop_label.pack(expand=True)

        self.drop_label.drop_target_register(
            DND_FILES
        )

        self.drop_label.dnd_bind(
            "<<Drop>>",
            self.load_file_dragdrop
        )

        # ====================================================
        # OUTPUT BOX
        # ====================================================

        self.output = ctk.CTkTextbox(
            self.main,
            width=1100,
            height=400
        )

        self.output.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

    # ========================================================
    # KPI CARD
    # ========================================================

    def create_card(self, title, value):

        card = ctk.CTkFrame(
            self.cards_frame,
            width=220,
            height=120
        )

        card.pack(
            side="left",
            padx=15,
            pady=10,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 30)
        )

        value_label.pack(pady=10)

        card.value_label = value_label

        return card

    # ========================================================
    # BROWSE FILE
    # ========================================================

    def browse_file(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv"),
                ("Excel Files", "*.xlsx")
            ]
        )

        if not file_path:
            return

        self.process_file(file_path)

    # ========================================================
    # DRAG & DROP LOAD
    # ========================================================

    def load_file_dragdrop(self, event):

        file_path = event.data.strip("{}")

        self.process_file(file_path)

    # ========================================================
    # PROCESS FILE
    # ========================================================

    def process_file(self, file_path):

        try:

            if file_path.endswith(".csv"):

                self.df = pd.read_csv(file_path)

            elif file_path.endswith(".xlsx"):

                self.df = pd.read_excel(file_path)

            else:

                messagebox.showerror(
                    "Error",
                    "Only CSV and Excel supported"
                )

                return

            self.basic_clean()

            self.auto_detect_datetime()

            self.update_cards()

            self.output.delete("1.0", "end")

            self.output.insert(
                "end",
                "DATASET LOADED SUCCESSFULLY\n\n"
            )

            self.output.insert(
                "end",
                str(self.df.head())
            )

            messagebox.showinfo(
                "Success",
                "Dataset Loaded Successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # BASIC CLEAN
    # ========================================================

    def basic_clean(self):

        self.df = self.df.dropna(
            axis=1,
            how="all"
        )

        self.df = self.df.loc[
            :,
            ~self.df.columns.astype(str).str.contains(
                "Unnamed"
            )
        ]

        self.df.columns = (
            self.df.columns
            .astype(str)
            .str.strip()
        )

    # ========================================================
    # DATETIME DETECTION
    # ========================================================

    def auto_detect_datetime(self):

        for col in self.df.columns:

            if (
                "date" in col.lower()
                or
                "time" in col.lower()
            ):

                try:

                    self.df[col] = pd.to_datetime(
                        self.df[col]
                    )

                    self.df["hour"] = (
                        self.df[col].dt.hour
                    )

                    self.df["day"] = (
                        self.df[col].dt.day_name()
                    )

                except:
                    pass

    # ========================================================
    # UPDATE KPI CARDS
    # ========================================================

    def update_cards(self):

        rows, cols = self.df.shape

        missing = (
            self.df.isnull()
            .sum()
            .sum()
        )

        avg_traffic = "N/A"

        for col in self.df.columns:

            if (
                "traffic" in col.lower()
                or
                "volume" in col.lower()
            ):

                try:

                    avg_traffic = round(
                        pd.to_numeric(
                            self.df[col],
                            errors="coerce"
                        ).mean(),
                        2
                    )

                    break

                except:
                    pass

        self.rows_card.value_label.configure(
            text=str(rows)
        )

        self.cols_card.value_label.configure(
            text=str(cols)
        )

        self.null_card.value_label.configure(
            text=str(missing)
        )

        self.traffic_card.value_label.configure(
            text=str(avg_traffic)
        )

    # ========================================================
    # SHOW INFO
    # ========================================================

    def show_info(self):

        if self.df is None:

            messagebox.showwarning(
                "Warning",
                "Upload dataset first"
            )

            return

        self.output.delete("1.0", "end")

        self.output.insert(
            "end",
            "========== DATASET PREVIEW ==========\n\n"
        )

        self.output.insert(
            "end",
            str(self.df.head())
        )

        self.output.insert(
            "end",
            "\n\n========== DATA SUMMARY ==========\n\n"
        )

        self.output.insert(
            "end",
            str(
                self.df.describe(
                    include="all"
                )
            )
        )

    # ========================================================
    # AUTO CLEAN DATA
    # ========================================================

    def clean_data(self):

        if self.df is None:

            messagebox.showwarning(
                "Warning",
                "Upload dataset first"
            )

            return

        try:

            # REMOVE DUPLICATES
            self.df.drop_duplicates(inplace=True)

            # CLEAN COLUMNS
            for col in self.df.columns:

                # NUMERIC COLUMN
                if pd.api.types.is_numeric_dtype(
                    self.df[col]
                ):

                    self.df[col] = self.df[col].fillna(
                        self.df[col].mean()
                    )

                # DATETIME COLUMN
                elif pd.api.types.is_datetime64_any_dtype(
                    self.df[col]
                ):

                    self.df[col] = self.df[col].ffill()

                # TEXT COLUMN
                else:

                    self.df[col] = self.df[col].fillna(
                        self.df[col].mode()[0]
                    )

            self.update_cards()

            messagebox.showinfo(
                "Success",
                "Data Cleaned Successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Cleaning Error",
                str(e)
            )

    # ========================================================
    # VISUALIZATION WINDOW
    # ========================================================

    def visualize_window(self):

        if self.df is None:

            messagebox.showwarning(
                "Warning",
                "Upload dataset first"
            )

            return

        win = ctk.CTkToplevel(self.root)

        win.title("Traffic Visualization")

        win.geometry("500x600")

        columns = list(self.df.columns)

        numeric_cols = self.df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        text_cols = self.df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        if not text_cols:
            text_cols = columns

        if not numeric_cols:
            numeric_cols = columns

        # ====================================================
        # X AXIS
        # ====================================================

        ctk.CTkLabel(
            win,
            text="Select X Axis"
        ).pack(pady=10)

        x_var = ctk.StringVar(
            value=text_cols[0]
        )

        ctk.CTkOptionMenu(
            win,
            variable=x_var,
            values=columns
        ).pack(pady=5)

        # ====================================================
        # Y AXIS
        # ====================================================

        ctk.CTkLabel(
            win,
            text="Select Y Axis"
        ).pack(pady=10)

        y_var = ctk.StringVar(
            value=numeric_cols[0]
        )

        ctk.CTkOptionMenu(
            win,
            variable=y_var,
            values=numeric_cols
        ).pack(pady=5)

        # ====================================================
        # GRAPH TYPE
        # ====================================================

        ctk.CTkLabel(
            win,
            text="Select Graph Type"
        ).pack(pady=10)

        chart_var = ctk.StringVar(
            value="Bar"
        )

        ctk.CTkOptionMenu(
            win,
            variable=chart_var,
            values=[
                "Bar",
                "Line",
                "Scatter",
                "Histogram",
                "Pie",
                "Boxplot",
                "Area",
                "Heatmap"
            ]
        ).pack(pady=5)

        # ====================================================
        # GRAPH HELP
        # ====================================================

        help_text = """
BEST GRAPH COMBINATIONS:

Bar:
X = hour/day/weather
Y = traffic_volume

Line:
X = hour
Y = traffic_volume

Scatter:
X = temp
Y = traffic_volume

Histogram:
Y = traffic_volume

Pie:
X = weather_main

Heatmap:
No X/Y needed
"""

        ctk.CTkTextbox(
            win,
            width=350,
            height=180
        ).insert(
            "0.0",
            help_text
        )

        # ====================================================
        # BUTTON
        # ====================================================

        ctk.CTkButton(
            win,
            text="Generate Graph",
            command=lambda: self.plot_graph(
                x_var.get(),
                y_var.get(),
                chart_var.get()
            )
        ).pack(pady=20)

    # ========================================================
    # PLOT GRAPH
    # ========================================================

    def plot_graph(self, x, y, chart):

        try:

            df = self.df.copy()

            # PERFORMANCE FIX
            df = df.head(500)

            # SAFE NUMERIC
            if y in df.columns:

                df[y] = pd.to_numeric(
                    df[y],
                    errors="coerce"
                )

                df = df.dropna(subset=[y])

            plt.figure(figsize=(12, 6))

            # =================================================
            # BAR GRAPH
            # =================================================

            if chart == "Bar":

                grouped = df.groupby(x)[y].mean()

                grouped.plot(kind="bar")

            # =================================================
            # LINE GRAPH
            # =================================================

            elif chart == "Line":

                grouped = df.groupby(x)[y].mean()

                grouped.plot(kind="line")

            # =================================================
            # SCATTER
            # =================================================

            elif chart == "Scatter":

                plt.scatter(
                    df[x],
                    df[y]
                )

            # =================================================
            # HISTOGRAM
            # =================================================

            elif chart == "Histogram":

                plt.hist(
                    df[y],
                    bins=20
                )

            # =================================================
            # PIE CHART
            # =================================================

            elif chart == "Pie":

                counts = (
                    df[x]
                    .value_counts()
                    .head(10)
                )

                plt.pie(
                    counts,
                    labels=counts.index,
                    autopct="%1.1f%%"
                )

            # =================================================
            # BOXPLOT
            # =================================================

            elif chart == "Boxplot":

                sns.boxplot(
                    x=df[x],
                    y=df[y]
                )

            # =================================================
            # AREA CHART
            # =================================================

            elif chart == "Area":

                grouped = df.groupby(x)[y].mean()

                grouped.plot(kind="area")

            # =================================================
            # HEATMAP
            # =================================================

            elif chart == "Heatmap":

                corr = (
                    df.select_dtypes(
                        include=["number"]
                    ).corr()
                )

                sns.heatmap(
                    corr,
                    annot=False
                )

            plt.title(
                f"{chart} Visualization"
            )

            plt.xticks(rotation=45)

            plt.grid(True)

            plt.tight_layout()

            plt.show()

        except Exception as e:

            messagebox.showerror(
                "Visualization Error",
                str(e)
            )

    # ========================================================
    # TRAFFIC INSIGHTS
    # ========================================================

    def generate_insights(self):

        if self.df is None:

            messagebox.showwarning(
                "Warning",
                "Upload dataset first"
            )

            return

        self.output.delete("1.0", "end")

        self.output.insert(
            "end",
            "========== TRAFFIC INSIGHTS ==========\n\n"
        )

        traffic_col = None

        for col in self.df.columns:

            if (
                "traffic" in col.lower()
                or
                "volume" in col.lower()
            ):

                traffic_col = col
                break

        # PEAK HOUR
        if (
            traffic_col
            and
            "hour" in self.df.columns
        ):

            peak_hour = (
                self.df.groupby("hour")[
                    traffic_col
                ]
                .mean()
                .idxmax()
            )

            self.output.insert(
                "end",
                f"🚦 Peak Traffic Hour: {peak_hour}:00\n\n"
            )

        # AVG TRAFFIC
        if traffic_col:

            avg_traffic = round(
                pd.to_numeric(
                    self.df[traffic_col],
                    errors="coerce"
                ).mean(),
                2
            )

            self.output.insert(
                "end",
                f"🚗 Average Traffic Volume: {avg_traffic}\n\n"
            )

        # MISSING VALUES
        missing = (
            self.df.isnull()
            .sum()
            .sum()
        )

        self.output.insert(
            "end",
            f"⚠ Missing Values: {missing}\n\n"
        )

        # DUPLICATES
        duplicates = (
            self.df.duplicated()
            .sum()
        )

        self.output.insert(
            "end",
            f"📄 Duplicate Rows: {duplicates}\n\n"
        )

        # TOTAL RECORDS
        self.output.insert(
            "end",
            f"📊 Total Records: {len(self.df)}\n\n"
        )


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    root = TkinterDnD.Tk()

    app = TrafficDashboard(root)

    root.mainloop()
