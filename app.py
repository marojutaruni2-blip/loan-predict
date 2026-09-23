import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ================= PAGE CONFIGURATION =================

st.set_page_config(
    page_title="Loan Analysis Dashboard",
    page_icon="💰",
    layout="wide"
)


# ================= LOAD DATASET =================

@st.cache_data
def load_data():
    data = pd.read_excel("loan_data.xlsx")
    return data


loan = load_data()


# ================= TITLE =================

st.title("💰 Loan Analysis Dashboard")
st.write(
    "This dashboard analyzes loan application data and displays "
    "important patterns, statistics, visualizations, and applicant details."
)

st.divider()


# ================= DASHBOARD OVERVIEW =================

st.header("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        loan.shape[0]
    )

with col2:
    st.metric(
        "Total Attributes",
        loan.shape[1]
    )

with col3:
    st.metric(
        "Approved Loans",
        (loan["Loan_Status"] == "Y").sum()
    )

with col4:
    st.metric(
        "Rejected Loans",
        (loan["Loan_Status"] == "N").sum()
    )


st.divider()


# ================= KEY INSIGHTS =================

st.header("🔍 Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("**Average Applicant Income**")
    st.write(f"{loan['ApplicantIncome'].mean():.2f}")

with col2:
    st.write("**Average Loan Amount**")
    st.write(f"{loan['LoanAmount'].mean():.2f}")

with col3:
    st.write("**Most Common Education**")
    st.write(loan["Education"].mode()[0])

with col4:
    st.write("**Most Common Property Area**")
    st.write(loan["Property_Area"].mode()[0])


st.divider()


# ================= GRAPHS =================

st.header("📈 Data Visualizations")


# Create two columns
col1, col2 = st.columns(2)


# -------- Graph 1 --------

with col1:

    st.subheader("Loan Approval vs Rejection")

    status_count = loan["Loan_Status"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))

    status_count.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Number of Applications")
    ax.set_title("Loan Approval vs Rejection")

    st.pyplot(fig)


# -------- Graph 2 --------

with col2:

    st.subheader("Credit History vs Loan Status")

    credit = pd.crosstab(
        loan["Credit_History"],
        loan["Loan_Status"]
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    credit.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Credit History")
    ax.set_ylabel("Number of Applications")
    ax.set_title("Credit History vs Loan Status")

    st.pyplot(fig)


# -------- Graph 3 --------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Applicant Income Distribution")

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.hist(
        loan["ApplicantIncome"],
        bins=10
    )

    ax.set_xlabel("Applicant Income")
    ax.set_ylabel("Number of Applicants")
    ax.set_title("Applicant Income Distribution")

    st.pyplot(fig)


# -------- Graph 4 --------

with col2:

    st.subheader("Loan Amount Distribution")

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.hist(
        loan["LoanAmount"],
        bins=20
    )

    ax.set_xlabel("Loan Amount")
    ax.set_ylabel("Number of Applications")
    ax.set_title("Loan Amount Distribution")

    st.pyplot(fig)


st.divider()


# ================= APPLICATION SEARCH =================

st.header("🔎 Application Search")

st.write(
    "Enter an Application ID to view the applicant's details "
    "and existing loan status."
)

application_id = st.text_input(
    "Enter Application ID"
)


if application_id:

    result = loan[
        loan["Loan_ID"].astype(str).str.strip()
        == application_id.strip()
    ]

    if result.empty:

        st.error("Application ID not found.")

    else:

        applicant = result.iloc[0]

        st.subheader("👤 Applicant Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write("**Application ID:**", applicant["Loan_ID"])

            st.write("**Gender:**", applicant["Gender"])

            st.write("**Married:**", applicant["Married"])

            st.write("**Dependents:**", applicant["Dependents"])

            st.write("**Education:**", applicant["Education"])

        with col2:

            st.write(
                "**Self Employed:**",
                applicant["Self_Employed"]
            )

            st.write(
                "**Applicant Income:**",
                applicant["ApplicantIncome"]
            )

            st.write(
                "**Co-applicant Income:**",
                applicant["CoapplicantIncome"]
            )

            st.write(
                "**Loan Amount:**",
                applicant["LoanAmount"]
            )

        with col3:

            st.write(
                "**Loan Amount Term:**",
                applicant["Loan_Amount_Term"]
            )

            st.write(
                "**Credit History:**",
                applicant["Credit_History"]
            )

            st.write(
                "**Property Area:**",
                applicant["Property_Area"]
            )


        # ================= LOAN STATUS =================

        st.subheader("🏦 Loan Status")

        if str(applicant["Loan_Status"]).strip().upper() == "Y":

            st.success("✅ LOAN APPROVED")

        else:

            st.error("❌ LOAN NOT APPROVED")


st.divider()


# ================= FOOTER =================

st.caption(
    "Loan Analysis Dashboard | Data Analysis Essentials | "
    "Academic Year 2026–2027"
)
