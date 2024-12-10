import streamlit as st

@st.dialog("Confirmar sentença")
def choice(item):
    st.write(f"Essa ação será irreversível e afetará os itens no banco de dados, deseja prosseguir?")
    if st.button("Confirmar"):
        st.rerun()

if "choice" not in st.session_state:
    st.write("Você deseja executar essa ação?")
    if st.button("Sim"):
        choice("Sim")
    if st.button("Não"):
        st.write("Que pena!")
else:
    pass