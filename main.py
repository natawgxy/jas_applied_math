import streamlit as st
from universities_data import uni_options
from universities_data import cr_subcr_options

st.title("Ваш помічник у виборі університету")
st.markdown("Введіть назви університетів, які ви розглядаєте для вступу")
if "universities" not in st.session_state:
    st.session_state.universities = []

# session_state - хранит данные вовремя session
# идея: сделать список университетов для выбора с фильтрацией: Украина, Европа, Америка, Азия. чел может начать вводить название и ему выдаёт возможные варики

def apply_filters(filters, uni_options):
    final_list = []
    for country, unis in uni_options.items():
        if country in filters:
            final_list.extend(unis)
    return final_list

filters = st.multiselect(
    "Оберіть бажане розташування",
    options=list(uni_options.keys()),
)
filtered_list = apply_filters(filters, uni_options)
selected_unis = st.multiselect(
    "Оберіть університет(и). Іноземні університети пишіть англійською мовою",
    options=filtered_list,
    default=[]
)
new_uni = st.text_input("Введіть університет, якщо не знайшли у списку")
if st.button("Додати свій"):
    selected_unis.append(new_uni)

st.session_state.universities = selected_unis

if selected_unis is not None:
    st.write("Ви додали")
    for u in selected_unis:
        st.markdown(f"* {u}")

#=====================================================================
st.markdown("Оберіть запропоновані критерії")
if "criterias" not in st.session_state:
    st.session_state.criterias = {}

selected_criterias = st.multiselect(
    options=list(cr_subcr_options.keys())
)

selected_subcriterias = []
for cr in selected_criterias:
    subcrs = st.multiselect(
        f"Підкритерії для {cr}:",
        options=cr_subcr_options[cr]
    )
    selected_subcriterias.extend((cr, subcr) for subcr in subcrs)


st.markdown("Зробіть свої критерії")
# criterias[crit] = {subcr1, ...}
new_crit = st.text_input("Новий критерій")
if st.button("Додати критерій"):
    if new_crit is not None and new_crit not in st.session_state.criterias:
        st.session_state.criterias[new_crit] = []
        st.success(f"Додано критерій {new_crit}")
    elif new_crit in st.session_state.criterias:
        st.warning("Такий критерій вже додано")

if st.session_state.criterias:
    crit_for_subcr = st.selectbox("Оберіть критерій до якого хочете додати підкритерій", list(st.session_state.criterias.keys()))
    new_subcr = st.text_input(" ")
    if st.button(f"Додати підкритерій до {crit_for_subcr}"):
        if new_subcr is not None and new_subcr not in st.session_state.criterias[crit_for_subcr]:
            st.session_state.criterias[crit_for_subcr].append(new_subcr)
            st.success(f"До {crit_for_subcr} додано {new_subcr}")
        elif new_subcr in st.session_state.criterias[crit_for_subcr]:
            st.warning("Ви вже це додали")
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
if st.session_state.criterias:
    variants = list(st.session_state.criterias.keys())
    sorting = st.multiselect(
        label="Оберіть порядок критеріїв (перший - найважливіший)",
        options=variants, default=variants, key="s1")
    st.session_state.crit_sorted = sorting

    tmp_sorted_subcrs = {}
    for c in sorting:
      subcrs = st.session_state.criterias[c]
      if subcrs is not None:
          st.write(f"Відсортуйте підкритерії критерію {c}")
          sorting2 = st.multiselect(
              label="(перший - найважливіший)",
              options=subcrs, default=subcrs, key=f"s2-{c}")
          tmp_sorted_subcrs[c] = sorting2
    
    for c, sorted_subcrs in tmp_sorted_subcrs.items():
        st.session_state.criterias[c] = sorted_subcrs

# бек ========================================
# строит табличку сравнения уников по подкритерию
def comp_uni_subcr(scores, cr, subcr):
    unis = st.session_state.universities
    n = len(unis)
    table = [[0 for _ in range(n)] for _ in range(n)]
    
    # табличка формата
    #     ХПИ    КНУ  ЛНУ
    #ХПИ   1     1/3    5
    #КНУ   3     1     1/7
    #ЛНУ   1/5   7      1
    # то, что в столбике справа более/менее приоритетнее того, что в верхней строке
    
    for i in range(n):
        table[i][i] = 1 

    for i in range(n):
        for j in range(i+1, n):
            if table[i][j] != 0:
                continue

            if scores[unis[i]][cr][subcr] == scores[unis[j]][cr][subcr]:
                table[i][j] = 1
                table[j][i] = 1
            elif abs(scores[unis[i]][cr][subcr] - scores[unis[j]][cr][subcr]) == 1:
                if scores[unis[i]][cr][subcr] > scores[unis[j]][cr][subcr]:
                    table[i][j] = 3 
                    table[j][i] = 1/3
                else:
                    table[i][j] = 1/3
                    table[j][i] = 3
            elif abs(scores[unis[i]][cr][subcr] - scores[unis[j]][cr][subcr]) == 2:
                if scores[unis[i]][cr][subcr] > scores[unis[j]][cr][subcr]:
                    table[i][j] = 5 
                    table[j][i] = 1/5
                else:
                    table[i][j] = 1/5 
                    table[j][i] = 5
            elif abs(scores[unis[i]][cr][subcr] - scores[unis[j]][cr][subcr]) == 3:
                if scores[unis[i]][cr][subcr] > scores[unis[j]][cr][subcr]:
                    table[i][j] = 7 
                    table[j][i] = 1/7
                else:
                    table[i][j] = 1/7
                    table[j][i] = 7
            elif abs(scores[unis[i]][cr][subcr] - scores[unis[j]][cr][subcr]) == 4:
                if scores[unis[i]][cr][subcr] > scores[unis[j]][cr][subcr]:
                    table[i][j] = 9
                    table[j][i] = 1/9
                else:
                    table[i][j] = 1/9
                    table[j][i] = 9

    score_subcr = {} # словарь: уник, взвешенная оценка по подкритерию
    # власний вектор 
    vl_vecs = []   
    for i in range(n):
        vl_vec = 1
        for j in range(n):
            vl_vec = vl_vec * table[i][j] 
        vl_vec = vl_vec ** (1/n)
        vl_vecs.append(vl_vec)

    # сразу нормируем
    all_sum = sum(vl_vecs)
    for x in vl_vecs:
        x /= all_sum

    for i, u in enumerate(unis):
        score_subcr[u] = vl_vecs[i]

    result = [subcr, score_subcr]
    return result

# табличка с попарным сравнением критериев/подкритериев
def com_cr_or_subcr(sorted_list):
    # у меня логика такая: находим позицию каждого критерия/подкритерия в отсорт. массиве и сравниваем попарно позиции, если разница == 1, то ..
    n = len(sorted_list)
    table = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        table[i][i] = 1
    
    for i in range(n):
        for j in range(i+1, n):
            diff = abs(j-i)
            if diff == 1:
                table[i][j] = 3
                table[j][i] = 1/3
            if diff == 2:
                table[i][j] = 5
                table[j][i] = 1/5
            if diff == 3:
                table[i][j] = 7
                table[j][i] = 1/7
            if diff == 4:
                table[i][j] = 9
                table[j][i] = 1/9
    vl_vecs = []   
    for i in range(n):
        vl_vec = 1
        for j in range(n):
            vl_vec = vl_vec * table[i][j] 
        vl_vec = vl_vec ** (1/n)
        vl_vecs.append(vl_vec)

    # сразу нормируем
    all_sum = sum(vl_vecs)
    for x in vl_vecs:
        x /= all_sum

    result = [[sorted_list[i], round(vl_vecs[i], 3)] for i in range(n)]
    return result

    
def integral_score(uni, crs_w, subcrs_w, score_w):
    sum1 = 0
    for [cr_name, cr_w] in crs_w:
        sum2 = 0
        for [subcr_name, subcr_w] in subcrs_w[cr_name]:
            sum2 += (subcr_w * score_w[1][uni])
        sum2 = sum2 * cr_w
        sum1 += sum2
    return sum1
    

#================
if st.button("Обрати найкращий університет"):
    if "crit_sorted" not in st.session_state or not st.session_state.crit_sorted:
        st.error("Спочатку відсортуйте критерії за важливістю")
    else:
        int_scores = {} # uni, iintegral score
        crs = st.session_state.crit_sorted
        crs_w = com_cr_or_subcr(crs)
        for c in st.session_state.criterias:
            subcrs = st.session_state.criterias[c]
            subcrs_w = com_cr_or_subcr(subcrs)
            for subcr in subcrs:
                w_scores = comp_uni_subcr(st.session_state.scores, c, subcr)
                for uni in st.session_state.universities:
                    sc = integral_score(uni, crs_w, subcrs_w, w_scores)
                    int_scores[uni] = sc

        max_sc = 0
        ans_name = ""
        for [uni_name, iscore] in int_scores:
            if iscore > max_sc:
                max_sc = iscore
                ans_name = uni_name

    st.markdown(f"Найкращий університет для вас: {ans_name}")
    if st.button("Подивитися деталі аналізу"):
        st.write("Інтегральна оцінка кожного університета")
        st.table(int_scores, border=True)


