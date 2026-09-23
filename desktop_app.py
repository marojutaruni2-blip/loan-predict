import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ================= LOAD DATASET =================

DATA_FILE = "loan data set.xlsx"

try:
    loan = pd.read_excel(DATA_FILE)
except FileNotFoundError:
    loan = None


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("Loan Analysis System")
root.geometry("1200x750")
root.configure(bg="#f4f6f8")


# ================= TITLE =================

title = tk.Label(
    root,
    text="LOAN ANALYSIS SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white",
    pady=15
)

title.pack(fill="x")


# ================= CHECK DATASET =================

if loan is None:

    messagebox.showerror(
        "Dataset Error",
        "loan data set.xlsx was not found.\n\n"
        "Keep the Excel file in the same folder as desktop_app.py."
    )

    root.destroy()

else:

    # ================= DASHBOARD FRAME =================

    dashboard_frame = tk.Frame(
        root,
        bg="#f4f6f8",
        padx=20,
        pady=20
    )

    dashboard_frame.pack(fill="x")


    # ================= DASHBOARD VALUES =================

    total_records = loan.shape[0]
    total_attributes = loan.shape[1]

    approved = (
        loan["Loan_Status"]
        .astype(str)
        .str.upper()
        .eq("Y")
        .sum()
    )

    rejected = (
        loan["Loan_Status"]
        .astype(str)
        .str.upper()
        .eq("N")
        .sum()
    )


    # ================= CARDS =================

    def create_card(parent, title_text, value, column):

        frame = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            width=250,
            height=100
        )

        frame.grid(
            row=0,
            column=column,
            padx=10,
            sticky="nsew"
        )

        frame.grid_propagate(False)

        tk.Label(
            frame,
            text=title_text,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#555555"
        ).pack(pady=(15, 5))

        tk.Label(
            frame,
            text=str(value),
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#1f4e78"
        ).pack()


    create_card(
        dashboard_frame,
        "Total Records",
        total_records,
        0
    )

    create_card(
        dashboard_frame,
        "Total Attributes",
        total_attributes,
        1
    )

    create_card(
        dashboard_frame,
        "Approved Loans",
        approved,
        2
    )

    create_card(
        dashboard_frame,
        "Rejected Loans",
        rejected,
        3
    )


    # ================= INSIGHTS =================

    insight_frame = tk.Frame(
        root,
        bg="#f4f6f8",
        padx=30,
        pady=10
    )

    insight_frame.pack(fill="x")

    tk.Label(
        insight_frame,
        text="KEY INSIGHTS",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8",
        fg="#1f4e78"
    ).pack(anchor="w")


    avg_income = loan["ApplicantIncome"].mean()
    avg_loan = loan["LoanAmount"].mean()
    common_education = loan["Education"].mode()[0]
    common_property = loan["Property_Area"].mode()[0]


    insights_text = (
        f"Average Applicant Income : {avg_income:.2f}     |     "
        f"Average Loan Amount : {avg_loan:.2f}     |     "
        f"Most Common Education : {common_education}     |     "
        f"Most Common Property Area : {common_property}"
    )


    tk.Label(
        insight_frame,
        text=insights_text,
        font=("Arial", 11),
        bg="#f4f6f8",
        fg="#333333",
        wraplength=1100,
        justify="left"
    ).pack(anchor="w", pady=8)


    # ================= SEARCH FRAME =================

    search_frame = tk.Frame(
        root,
        bg="white",
        bd=1,
        relief="solid",
        padx=20,
        pady=15
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=10
    )


    tk.Label(
        search_frame,
        text="Application Search",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#1f4e78"
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="w",
        pady=(0, 10)
    )


    tk.Label(
        search_frame,
        text="Application ID:",
        font=("Arial", 11, "bold"),
        bg="white"
    ).grid(
        row=1,
        column=0,
        padx=5
    )


    application_entry = tk.Entry(
        search_frame,
        font=("Arial", 11),
        width=25
    )

    application_entry.grid(
        row=1,
        column=1,
        padx=10
    )


    # ================= DETAILS AREA =================

    details_frame = tk.Frame(
        root,
        bg="white",
        bd=1,
        relief="solid",
        padx=20,
        pady=15
    )

    details_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )


    details_text = tk.Text(
        details_frame,
        font=("Arial", 11),
        bg="white",
        fg="#333333",
        height=12,
        width=100
    )

    details_text.pack(
        fill="both",
        expand=True
    )


    # ================= SEARCH FUNCTION =================

    def search_application():

        application_id = application_entry.get().strip()

        if application_id == "":
            messagebox.showwarning(
                "Input Required",
                "Please enter an Application ID."
            )
            return


        result = loan[
            loan["Loan_ID"].astype(str).str.strip()
            == application_id
        ]


        details_text.delete(
            "1.0",
            tk.END
        )


        if result.empty:

            messagebox.showerror(
                "Not Found",
                "Application ID not found."
            )

            return


        applicant = result.iloc[0]


        details_text.insert(
            tk.END,
            "APPLICANT DETAILS\n"
        )

        details_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        details_text.insert(
            tk.END,
            f"Application ID      : {applicant['Loan_ID']}\n"
        )

        details_text.insert(
            tk.END,
            f"Gender              : {applicant['Gender']}\n"
        )

        details_text.insert(
            tk.END,
            f"Married             : {applicant['Married']}\n"
        )

        details_text.insert(
            tk.END,
            f"Dependents          : {applicant['Dependents']}\n"
        )

        details_text.insert(
            tk.END,
            f"Education           : {applicant['Education']}\n"
        )

        details_text.insert(
            tk.END,
            f"Self Employed       : {applicant['Self_Employed']}\n"
        )

        details_text.insert(
            tk.END,
            f"Applicant Income    : {applicant['ApplicantIncome']}\n"
        )

        details_text.insert(
            tk.END,
            f"Co-applicant Income : {applicant['CoapplicantIncome']}\n"
        )

        details_text.insert(
            tk.END,
            f"Loan Amount         : {applicant['LoanAmount']}\n"
        )

        details_text.insert(
            tk.END,
            f"Loan Amount Term    : {applicant['Loan_Amount_Term']}\n"
        )

        details_text.insert(
            tk.END,
            f"Credit History      : {applicant['Credit_History']}\n"
        )

        details_text.insert(
            tk.END,
            f"Property Area       : {applicant['Property_Area']}\n"
        )

        details_text.insert(
            tk.END,
            "\n----------------------------------------\n"
        )

        details_text.insert(
            tk.END,
            "LOAN STATUS\n"
        )


        status = str(
            applicant["Loan_Status"]
        ).strip().upper()


        if status == "Y":

            details_text.insert(
                tk.END,
                "✅ LOAN APPROVED"
            )

        elif status == "N":

            details_text.insert(
                tk.END,
                "❌ LOAN NOT APPROVED"
            )

        else:

            details_text.insert(
                tk.END,
                "Loan status not available."
            )


    # ================= SEARCH BUTTON =================

    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        command=search_application,
        font=("Arial", 10, "bold"),
        bg="#1f4e78",
        fg="white",
        padx=20,
        pady=5,
        cursor="hand2"
    )

    search_button.grid(
        row=1,
        column=2,
        padx=10
    )


    # ================= GRAPH WINDOW =================

    def show_graphs():

        graph_window = tk.Toplevel(root)

        graph_window.title(
            "Loan Analysis Graphs"
        )

        graph_window.geometry(
            "1200x750"
        )


        fig, axes = plt.subplots(
            2,
            2,
            figsize=(12, 8)
        )


        # Graph 1

        loan["Loan_Status"].value_counts().plot(
            kind="bar",
            ax=axes[0, 0]
        )

        axes[0, 0].set_title(
            "Loan Approval vs Rejection"
        )

        axes[0, 0].set_xlabel(
            "Loan Status"
        )

        axes[0, 0].set_ylabel(
            "Number of Applications"
        )


        # Graph 2

        credit = pd.crosstab(
            loan["Credit_History"],
            loan["Loan_Status"]
        )

        credit.plot(
            kind="bar",
            ax=axes[0, 1]
        )

        axes[0, 1].set_title(
            "Credit History vs Loan Status"
        )

        axes[0, 1].set_xlabel(
            "Credit History"
        )

        axes[0, 1].set_ylabel(
            "Number of Applications"
        )


        # Graph 3

        axes[1, 0].hist(
            loan["ApplicantIncome"].dropna(),
            bins=10
        )

        axes[1, 0].set_title(
            "Applicant Income Distribution"
        )

        axes[1, 0].set_xlabel(
            "Applicant Income"
        )

        axes[1, 0].set_ylabel(
            "Number of Applicants"
        )


        # Graph 4

        axes[1, 1].hist(
            loan["LoanAmount"].dropna(),
            bins=20
        )

        axes[1, 1].set_title(
            "Loan Amount Distribution"
        )

        axes[1, 1].set_xlabel(
            "Loan Amount"
        )

        axes[1, 1].set_ylabel(
            "Number of Applications"
        )


        plt.tight_layout()


        canvas = FigureCanvasTkAgg(
            fig,
            master=graph_window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # ================= GRAPH BUTTON =================

    graph_button = tk.Button(
        root,
        text="📊 VIEW GRAPHS",
        command=show_graphs,
        font=("Arial", 11, "bold"),
        bg="#1f4e78",
        fg="white",
        padx=25,
        pady=8,
        cursor="hand2"
    )

    graph_button.pack(
        pady=10
    )


# ================= RUN APPLICATION =================

root.mainloop()
