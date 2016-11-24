# python imports
import Tkinter as tk
from Tkinter import *
from lib.db_conn import MongoConn
from lib.tools import MultiListbox
import pdfkit

TITLE_FONT = ("Helvetica", 18, "bold")


class Application(tk.Tk):
    """
    Description: Main application class
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Sai Hospital")
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.attributes("-fullscreen", True)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MainPage, RegisterPage, LastPage, ListPage, ViewPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """
        Description: Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"


class StartPage(tk.Frame):
    """
    Description: Class holds starting page services
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')
        labelframe = LabelFrame(self, bd=0, padx=50, pady=20)
        labelframe.pack(fill=None, expand=False, pady=250)
        label = Label(labelframe, text="LOGIN", font=TITLE_FONT)
        label.grid(columnspan=2, padx=100, pady=30)
        l1 = Label(labelframe, text="User Name")
        l1.grid(row=1)
        self.e1 = Entry(labelframe, width=25)
        self.e1.grid(row=1, column=1)
        l2 = Label(labelframe, text="Password",  pady=30)
        l2.grid(row=2)
        self.e2 = Entry(labelframe, width=25)
        self.e2.grid(row=2, column=1)

        button1 = tk.Button(labelframe, text="login",  height=2, width = 15,  command=self.validate_user)
        button1.grid(columnspan=2, pady=15)

    def validate_user(self):
        """
        Description: Validate user credentials from database
        """
        user_name = self.e1.get()
        password = self.e2.get()
        conn = MongoConn(collection="User")
        record = conn.read_document({'username': user_name, "password": password})
        if record:
            self.controller.show_frame("MainPage")
        else:
            label = tk.Label(self, text="invalid username and password")
            label.pack()


class MainPage(tk.Frame):
    """
    Description: Class handle main page operation of application
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')
        frame = LabelFrame(self, bd=0, padx=80, pady=40, bg='antique white')
        frame.pack(pady=80)

        label = tk.Label(frame, text="Sai Hospital", font=("Helvetica", 50, "bold"), bg='antique white')
        label.grid(columnspan=1, pady=30)

        label = tk.Label(frame, text="Welcome", font=("Helvetica", 30, "bold"), bg='antique white')
        label.grid(columnspan=2, pady=30)

        button = tk.Button(frame, text="Register Patient", command=self.register, width=30, height=4)
        button.grid(columnspan=3, pady=50)

        button = tk.Button(frame, text="List of Patient", command=self.view_list, width=30, height=4)
        button.grid(columnspan=4, pady=50)

        button = tk.Button(frame, text="Patient Details", command=self.show, width=30, height=4)
        button.grid(columnspan=5, pady=50)

    def register(self):
        self.controller.show_frame("RegisterPage")

    def view_list(self):
        self.controller.show_frame("ListPage")

    def show(self):
        self.controller.show_frame("ViewPage")


class RegisterPage(tk.Frame):
    """
    Description: Class handle main page operation of application
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')

        frame = LabelFrame(self, bd=0, padx=80, pady=40)
        frame.pack(pady=50)
        label = tk.Label(frame, text="Patient Details", font=TITLE_FONT)
        label.grid(columnspan=2, pady=50)

        l_name = Label(frame, text="Patient Name")
        l_name.grid(row=1, pady=15)
        self.e_name = Entry(frame, width=60)
        self.e_name.grid(row=1, column=1)

        l_age = Label(frame, text="Patient Age")
        l_age.grid(row=2, pady=15)
        self.e_age = Entry(frame, width=60)
        self.e_age.grid(row=2, column=1)

        l_sons = Label(frame, text="""Number of living sons with age of
        each living son""")
        l_sons.grid(row=3, pady=15)
        self.e_sons = Entry(frame, width=60)
        self.e_sons.grid(row=3, column=1)

        l_daughter = Label(frame, text="""Number of living Daughters with age of
        each living Daughter""")
        l_daughter.grid(row=4, pady=15)
        self.e_daughter = Entry(frame, width=60)
        self.e_daughter.grid(row=4, column=1)

        l_family = Label(frame, text="Husband's/Wife's/Father's/Mother's Name")
        l_family.grid(row=5, pady=15)
        self.e_family = Entry(frame, width=60)
        self.e_family.grid(row=5, column=1)

        l_mobile = Label(frame, text="Contact number")
        l_mobile.grid(row=6, pady=15)
        self.e_mobile = Entry(frame, width=60)
        self.e_mobile.grid(row=6, column=1)

        l_address = Label(frame, text="Full postal address of patient")
        l_address.grid(row=7, pady=15)
        self.e_address = Entry(frame, width=60)
        self.e_address.grid(row=7, column=1)

        l_week = Label(frame, text="Last menstrual period or weeks of pregnancy")
        l_week.grid(row=8, pady=15)
        self.e_week = Entry(frame, width=60)
        self.e_week.grid(row=8, column=1)

        l_referal = Label(frame, text="Referred by")
        l_referal.grid(row=9, pady=15)
        self.e_referal = Entry(frame, width=60)
        self.e_referal.grid(row=9, column=1)

        l_diagnostic_procedure = Label(frame, text="""Self-Referral by Gynaecologist/Radiologist/
        Registered Medical Practitioner conducting
        the diagnostic procedures""")
        l_diagnostic_procedure.grid(row=10, pady=15)
        self.e_diagnostic_procedure = Entry(frame, width=60)
        self.e_diagnostic_procedure.grid(row=10, column=1)

        button = tk.Button(frame, text="Back", command=self.back_main, width=20, height=2)
        button.grid(row=11, pady=50)

        button = tk.Button(frame, text="Save", command=self.save_data, width=20, height=2)
        button.grid(row=11,column=1)

    def back_main(self):
        self.controller.show_frame("MainPage")

    def save_data(self):
        """
        Description: Save patient information in database
        """
        data = {
            "PatientName": self.e_name.get(),
            "PatientAge": self.e_age.get(),
            "NumberOfLivingSons": self.e_sons.get(),
            "NumberOfLivingDaughters": self.e_daughter.get(),
            "FamilyName": self.e_family.get(),
            "Address": self.e_address.get(),
            "ContactNumber": self.e_mobile.get(),
            "WeeksOfPregnancy": self.e_week.get(),
            "DiagnosticProcedure": self.e_diagnostic_procedure.get(),
            "SelfReferral": self.e_referal.get()
        }
        conn = MongoConn(collection="PatientDetails")
        conn.insert_with_unique_id(doc=data)
        self.controller.show_frame("LastPage")
        # self.generate_pdf()

    def list_view(self):
        """

        """
        self.controller.show_frame("LastPage")


    def generate_pdf(self):
        """
        Description: Generate pdf from html file
        """
        fp = open("files/pdf.html", "r")
        data = fp.read()
        data = data.replace("{name}", self.e_name.get())
        data = data.replace("{age}", self.e_age.get())
        data = data.replace("{sons}", self.e_sons.get())
        data = data.replace("{daughter}", self.e_daughter.get())
        data = data.replace("{family}", self.e_family.get())
        data = data.replace("{address}", self.e_address.get())
        data = data.replace("{mobile}", self.e_mobile.get())
        data = data.replace("{referal}", self.e_referal.get())
        data = data.replace("{diagnostic}", self.e_diagnostic_procedure.get())
        data = data.replace("{week}", self.e_week.get())
        data = unicode(data, 'utf-8')
        pdfkit.from_string("test", "out.pdf")


class ListPage(tk.Frame):
    """
    Description: Class handle main page operation of application
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')
        Label(self, text='Patient List', font=TITLE_FONT, bg='antique white').pack(pady=50)
        mlb = MultiListbox(self, (('PatientName', 30), ('FamilyName', 30), ('ContactNumber', 20), ('Address', 50),
                                  ('DiagnosticProcedure', 20),('NumberOfLivingSons', 20),('NumberOfLivingDaughters', 20),
                                  ('WeeksOfPregnancy', 20), ("Options", 20)))

        conn = MongoConn(collection="PatientDetails")
        data = conn.get_all_document()
        print data
        for row in data:
            mlb.insert(END,
                       (row['PatientName'], row['FamilyName'], row['ContactNumber'], row['Address'], row['PatientAge'],
                        row['DiagnosticProcedure'], row['NumberOfLivingSons'], row['NumberOfLivingDaughters'],
                        row['WeeksOfPregnancy']))
        mlb.pack()
        button = tk.Button(self, text="Back", command=self.back_main, width=20, height=2)
        button.pack(pady=30)

    def back_main(self):
        self.controller.show_frame("MainPage")


class LastPage(tk.Frame):
    """
    Description: Last page which display message
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')
        frame = LabelFrame(self, bd=0, padx=80, pady=60)
        frame.pack(pady=200)
        label = tk.Label(frame, text=" Patient details save successfully..!!", font=TITLE_FONT)
        label.grid(row=0, column=1, pady=50)
        button = tk.Button(frame, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"), width=20, height=2)
        button.grid(row=1, column=1)
    """
    Description: Class handle main page operation of application
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')
        frame = LabelFrame(self, bd=0, padx=80, pady=60)
        frame.pack(pady=200)
        label = tk.Label(frame, text=" Patient details save successfully..!!", font=TITLE_FONT)
        label.grid(row=0, column=1, pady=50)
        button = tk.Button(frame, text="Home",
                           command=lambda: controller.show_frame("MainPage"), width=20, height=2)
        button.grid(row=1, column=1)

        button = tk.Button(frame, text="Back",
                           command=lambda: controller.show_frame("RegisterPage"), width=20, height=2)
        button.grid(row=1, column=2)


class ViewPage(tk.Frame):
    """
    Description: Class handle main page operation of application
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='antique white')
        frame = LabelFrame(self, bd=0, padx=150)
        frame.pack(pady=20)
        label = tk.Label(frame, text=" Find Patient details...", font=TITLE_FONT)
        label.grid(row=0, column=1, pady=20)

        id = Label(frame, text="Patient ID")
        id.grid(row=1, pady=10)

        self.e_name = Entry(frame, width=60)
        self.e_name.grid(row=1, column=1)

        button = tk.Button(frame, text="Back",
                           command=lambda: controller.show_frame("MainPage"), width=20, height=2)
        button.grid(row=2, column=1, pady=20)
        button = tk.Button(frame, text="Search",
                           command=self.search_patient, width=20, height=2)
        button.grid(row=2, column=2)

    def search_patient(self):

        frame = LabelFrame(self, bd=0, padx=80, pady=10)
        frame.place(relx=0.5, rely=0.6, anchor=CENTER)

        label = tk.Label(frame, text="Patient Details", font=TITLE_FONT)
        label.grid(columnspan=2, pady=20)
        conn = MongoConn(collection="PatientDetails")
        record = conn.read_document({"PatientName":"pratik"})
        print record

        l_name = Label(frame, text="Patient Name")
        l_name.grid(row=1, pady=10)
        e_name = Label(frame, text=record['PatientName'])
        e_name.grid(row=1, column=1)

        l_age = Label(frame, text="Patient Age")
        l_age.grid(row=2, pady=10)
        e_age = Label(frame, text=record['PatientAge'])
        e_age.grid(row=2, column=1)

        l_sons = Label(frame, text="""Number of living sons with age of
                each living son""")
        l_sons.grid(row=3, pady=10)
        e_sons = Label(frame, text=record['NumberOfLivingSons'])
        e_sons.grid(row=3, column=1)

        l_daughter = Label(frame, text="""Number of living Daughters with age of
                each living Daughter""")
        l_daughter.grid(row=4, pady=10)
        e_daughter = Label(frame, text=record['NumberOfLivingDaughters'])
        e_daughter.grid(row=4, column=1)

        l_family = Label(frame, text="Husband's/Wife's/Father's/Mother's Name")
        l_family.grid(row=5, pady=10)
        e_family = Label(frame, text=record['FamilyName'])
        e_family.grid(row=5, column=1)

        l_mobile = Label(frame, text="Contact number")
        l_mobile.grid(row=6, pady=10)
        e_mobile = Label(frame, text=record['ContactNumber'])
        e_mobile.grid(row=6, column=1)

        l_address = Label(frame, text="Full postal address of patient")
        l_address.grid(row=7, pady=10)
        e_address = Label(frame, text=record['Address'])
        e_address.grid(row=7, column=1)

        l_week = Label(frame, text="Last menstrual period or weeks of pregnancy")
        l_week.grid(row=8, pady=10)
        self.e_week = Label(frame, text=record['WeeksOfPregnancy'])
        self.e_week.grid(row=8, column=1)

        l_referal = Label(frame, text="Referred by")
        l_referal.grid(row=9, pady=10)
        e_referal = Label(frame, text=record['PatientName'])
        e_referal.grid(row=9, column=1)

        l_diagnostic_procedure = Label(frame, text="""Self-Referral by Gynaecologist/Radiologist/
                Registered Medical Practitioner conducting
                the diagnostic procedures""")
        l_diagnostic_procedure.grid(row=10, pady=10)
        e_diagnostic_procedure = Label(frame, text=record['DiagnosticProcedure'])
        e_diagnostic_procedure.grid(row=10, column=1)

        button = tk.Button(frame, text="Delete", command="", width=20, height=2)
        button.grid(row=11, pady=50)

        button = tk.Button(frame, text="Edit", command="", width=20, height=2)
        button.grid(row=11, column=1)

if __name__ == "__main__":
    app = Application()
    app.mainloop()