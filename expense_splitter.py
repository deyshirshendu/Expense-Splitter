import streamlit as st
import pandas as pd
from itertools import combinations


def display_data(df, lst):
    # Check if the lengths match
    if len(df) != len(lst):
        st.error("Lengths of DataFrame and list do not match.")
        return

    # Combine DataFrame and list into a single DataFrame
    combined_df = pd.concat([df, pd.DataFrame({'Split Among': lst})], axis=1)

    # Display the combined DataFrame in a table
    st.write("Combined Data:")
    st.table(combined_df)


def show_splitting(df, among, members):
    splitting_mat = pd.DataFrame(0, index = members, columns=members)
    for i in range(len(df)):
        name = df.loc[i, "Name"]
        if name not in splitting_mat.index:
            splitting_mat.loc[name, among[i]] = df.loc[i, "Amount"] / len(among[i])
        else:
            splitting_mat.loc[name, among[i]] += df.loc[i, "Amount"] / len(among[i])
        splitting_mat.fillna(0)

    tran_mat = splitting_mat - splitting_mat.T

    comb = list(combinations(members, 2))
    st.subheader("Settlements:")
    for c in comb:
        x = tran_mat.loc[c[0], c[1]]
        if x > 0:
            st.write(f'{c[1]} will pay {c[0]}: {x:.2f}')
        elif x < 0:
            st.write(f'{c[0]} will pay {c[1]}: {-x:.2f}')


def splitwise_app():
    st.title('Expense Splitter')

    #members = add_members()
    members = st.text_input("Enter the names among which the amount will be split (comma-separated):")
    members = [member.strip() for member in members.split(",")]
    #st.success(f"Members: {members}")

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Date", "Name", "Amount", "Reason"])
        st.session_state.split_among = list()

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
        #rwdta.append(cols[4].multiselect(st.session_state.df.columns[4], options=members, default=members))
        s_a = st.multiselect("Split Among:", options=members, default=members)
        
        if st.form_submit_button("Add"):
            rw = st.session_state.df.shape[0]
            st.session_state.df.loc[rw] = rwdta
            st.session_state.split_among.append(s_a)
            st.success("Added Successfully")

    if st.button("View All Expenses:"):
        #st.write(st.session_state.df, st.session_state.split_among)
        display_data(df = st.session_state.df, lst = st.session_state.split_among)

    if st.button("Show Splitting"):
        show_splitting(df=st.session_state.df, among = st.session_state.split_among, members=members)

    

if __name__ == "__main__":
    splitwise_app()
