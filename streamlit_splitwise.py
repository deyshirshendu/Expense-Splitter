import streamlit as st
import pandas as pd
from itertools import combinations

def show_splitting(df, members):
    # Calculate and display settlements
    df_spend = df.groupby(by="Name")[['Amount']].sum().reset_index()
    splitting_mat = pd.DataFrame(0, index=members, columns=members)
    for name in df_spend['Name']:
        splitting_mat.loc[name] = df_spend.loc[df_spend['Name'] == name, 'Amount'].squeeze() / len(members)

    tran_mat = splitting_mat - splitting_mat.T

    comb = list(combinations(members, 2))
    st.subheader("Settlements:")
    for c in comb:
        x = tran_mat.loc[c[0], c[1]]
        if x > 0:
            st.write(f'{c[1]} will pay {c[0]}: {x}')
        elif x < 0:
            st.write(f'{c[0]} will pay {c[1]}: {-x}')



def splitwise_app():
    st.title('Expense Splitter')

    members = st.text_input("Enter the names among which the amount will be split (comma-separated):")
    members = [member.strip() for member in members.split(",")]

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Date", "Name", "Amount", "Reason"])

    st.subheader("Add Record")
    ncol = st.session_state.df.shape[1]  # col count
    rw = -1

    with st.form(key="add form", clear_on_submit= True):
        cols = st.columns(ncol)
        rwdta = []

        rwdta.append(cols[0].date_input(st.session_state.df.columns[0]))
        rwdta.append(cols[1].selectbox(st.session_state.df.columns[1], options = members))
        rwdta.append(cols[2].number_input(st.session_state.df.columns[2]))
        rwdta.append(cols[3].text_input(st.session_state.df.columns[3]))

        if st.form_submit_button("Add"):
            rw = st.session_state.df.shape[0] + 1
            st.session_state.df.loc[rw] = rwdta

    # Display the entered data
    st.dataframe(st.session_state.df)

    if st.button("Show Splitting"):
        show_splitting(df=st.session_state.df, members=members)

    

if __name__ == "__main__":
    splitwise_app()
