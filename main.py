import streamlit as st
from streamlit_sortables import sort_items

st.title("Ваш помічник у виборі університету")
universities = []
st.markdown("Введіть назви університетів, які ви розглядаєте для вступу")
if "universities" not in st.session_state:
    st.session_state.universities = []

# session_state - хранит данные вовремя session
new_uni = st.text_input("Назва університету")
if st.button("Додати університет"):
    if new_uni is not None and new_uni not in st.session_state.universities:
        st.session_state.unoversities.append(new_uni)
        st.sucess(f"Додано {new_uni}")
    elif new_uni in st.session_state.universities:
        st.warning("Такий університет вже додано")

if st.session_state.universities is not None:
    st.write("Ви додали")
    for u in st.session_state.universities:
        st.markdown(f"* {u}")

#=====================================================================

st.markdown("Наші запропоновані критерії")
if "criterias" not in st.session_state:
    st.session_state.criterias = {} 
# criterias[crit] = {subcr1, ...}
new_crit = st.text_input("Новий критерій")
if st.button("Додати критерій"):
    if new_crit is not None and new_crit not in st.session_state.criterias:
        st.session_state.criterias.append(new_crit)
        new_subcr = st.text_input("Підкритерій")
        if st.button(f"Додати підкритерій критерію {new_crit}"):
            if new_subcr is not None and new_subcr not in st.session_state.criterias[new_crit]:
                st.session_state.criterias[new_crit].append(new_subcr)
                st.sucess(f"До {new_crit} додано {new_subcr}")
            elif new_subcr in st.session_state.criterias[new_crit]:
                st.warning("Ви вже це додали")
    elif new_crit in st.session_state.criterias:
        st.warning("Такий критерій вже додано")

#=====================================================================

st.markdown("Оцініть кожен університет за певним критерієм")
st.markdown("Використайте таку шкалу оцінюваня: відмінний, вище середнього, нижче середнього, поганий")
scale = {
    'відмінний' : 5,
    'вище середнього' : 4,
    'середній' : 3,
    'нижче середнього' : 2,
    'поганий' : 1
}
if "scores" not in st.session_state:
    st.session_state.scores = {}

# трёхмерный массив scores[university][criteria][subcriteria]
for u in st.session_state.universities:
    st.subheader(u)
    st.session_state.scores[u] = {}
    for c, subcrs in st.session_state.criterias.items():
        st.markdown(c)
        st.session_state.scores[u][c] = {}
        for subcr in subcrs:
            score = st.selectbox(
                f"Оцініть за підкритерієм {subcr}", list(scale.keys()), key=f"{u}-{c}-{subcr}"
            )
            st.session_state.scores[u][c][subcr] = scale[score]

#=====================================================================         
st.markdown("Розташуйте критерії за порядком важливості для вас")
if st.session_state.criterias:
    st.markdown(f"Розташуйте за порядком важливості підкритерії критерію {c}")
    st.markdown("(зверху - найважливіший)")
    sorting = sort_items(list(st.session_state.criterias.keys(), direction="vertical"))
    st.session_state.crit_sorted = sorting
    for c in sorting:
      subcrs = st.session_state.criterias[c]
      if subcrs is not None:
          st.write(f"Відсортуйте підкритерії критерію {c}")
          sorting2 = sort_items(subcrs, direction="vertical")
          st.session_state.criterias[c] = sorting2



st.button("Обрати найкращий університет")
st.markdown("Зачекайте")

# бек ========================================
# строит табличку сравнения уников по критерию
def build_table_comp_criteria():


# табличка с нормированным собственным вектором
def build_norm_vec():


# табличка с попарным сравнением подкритериев
def build_table_com_subcriteria():



