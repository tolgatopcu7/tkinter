import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from evds import evdsAPI
from datetime import datetime

APP_COLOR = '#383061'
APP_ALT_COLOR = '#BB8FCE'
LABEL_FONT = ('Courier', 10)
BUTTON_FONT = ('Courier', 10)
evds = evdsAPI('ZGhjBH73U6')

class MainApplication(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("TolgaTopcu")
        self.iconphoto(False, tk.PhotoImage(file="lock.png"))
        self.title_font = tkfont.Font(family='Verdana', size=20,
                                      weight="bold", slant="italic")
        self.default_font = tkfont.Font(family='Verdana', size=5)
        self.center_window(300, 300)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts

        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg= APP_COLOR)
        self.controller = controller
        # self.controller.iconphoto(False, tk.PhotoImage(file="lock.png"))
        # label of frame Layout 2

        year_label = tk.Label(self, fg="white", bg=APP_COLOR, text="Yılı seçiniz:")
        year_label.pack()
        self.year_combobox = ttk.Combobox(self, values=[str(i) for i in range(2019, 2024)])
        self.year_combobox.set(datetime.today().strftime('20%y'))
        self.year_combobox.pack()

        month_label = tk.Label(self,fg="white", bg=APP_COLOR, text="Ayı seçiniz:" )
        month_label.pack()
        self.month_combobox = ttk.Combobox(self, values=[str(i) for i in range(1, 13)])
        self.month_combobox.set(datetime.today().strftime('%m'))
        self.month_combobox.pack()

        calculate_button = tk.Button(self, text="Hesapla", command=self.calculate_average_dollar)
        # calculate_button = tk.Button(self, text="Hesapla")
        calculate_button.pack(pady=10)

        self.result_label = tk.Label(self, text="",bg=APP_COLOR)
        self.result_label.pack()

        button1 = tk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_frame(Page1),
                            font=BUTTON_FONT)
        button2 = tk.Button(self, text="Go to Page 2",
                            command=lambda: controller.show_frame(Page2),
                            font=BUTTON_FONT)

        button2.pack(side=tk.BOTTOM, pady=5)
        button1.pack(side=tk.BOTTOM, pady=0)

    def get_monthly_average_dollar(self, year, month):
        series_code = "TP.DK.USD.S.EF.YTL"
        start_date = f"01-{month}-{year}"
        end_date = f"31-{month}-{year}"

        dollar_data = evds.get_data(['TP.DK.USD.S.EF.YTL'], startdate=start_date, enddate=end_date)
        monthly_average_dollar = dollar_data['TP_DK_USD_S_EF_YTL'].mean()
        return monthly_average_dollar

    # Kullanıcıdan ay ve yıl seçimini alacak olan işlev
    def calculate_average_dollar(self):
        selected_month = int(self.month_combobox.get())
        selected_year = int(self.year_combobox.get())
        result = self.get_monthly_average_dollar(selected_year, selected_month)
        # Sonucu ekranda gösterme
        self.result_label.config(bg="white", text=f"Aylık Ortalama Dolar Kuru: {result:.4f}")


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_COLOR)
        self.controller = controller
        # label of frame Layout 2
        label = tk.Label(self, text=f"Hello,"
                                    f"\n This is Page 1 ",
                         font=controller.title_font, bg=APP_COLOR, fg='white')
        label.pack(side="top", fill="x", pady=20, padx=15)

        button1 = tk.Button(self, text="Go to Page 2",
                            command=lambda: controller.show_frame(Page2),
                            font=BUTTON_FONT)
        button2 = tk.Button(self, text="Go to StartPage",
                            command=lambda: controller.show_frame(StartPage),
                            font=BUTTON_FONT)

        button1.pack(pady=5)
        button2.pack(pady=5)


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=APP_COLOR)
        self.controller = controller
        # label of frame Layout 2
        label = tk.Label(self, text=f"Hello,"
                                    f"\n This is Page 2 ",
                         font=controller.title_font, bg=APP_COLOR, fg='white')
        label.pack(side="top", fill="x", pady=20, padx=15)

        button1 = tk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_frame(Page1),
                            font=BUTTON_FONT)
        button2 = tk.Button(self, text="Go to StartPage",
                            command=lambda: controller.show_frame(StartPage),
                            font=BUTTON_FONT)

        button1.pack(pady=5)
        button2.pack(pady=5)
        a = 5

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
