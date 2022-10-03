import math
import pandas as pd
import streamlit as st

st.title("キーカードドロー確率計算ツール")
st.caption("Shadowverseで任意のターンにキーカードをドローする確率が何パーセントか計算することができます。")

st.sidebar.title("条件を入力してください")
st.sidebar.markdown("---")
op1 = st.sidebar.slider("■ デッキ枚数", min_value=30, max_value=40, step=1, value=30)
col = st.sidebar.columns([8, 1, 1])
col[0].write("■ キーカード採用枚数")
increase_button1 = col[1].button('+')
decrease_button2 = col[2].button('-')

if increase_button1:
    if st.session_state.count != 5:
        st.session_state.count += 1
elif decrease_button2:
    if st.session_state.count != 0:
        st.session_state.count -= 1

op2 = []
op2.append(st.sidebar.selectbox("Card1", list(range(1, op1 + 1))))
if 'count' not in st.session_state:
    st.session_state.count = 0
elif st.session_state.count != 0:
    for x in range(st.session_state.count):
        a = st.sidebar.selectbox("Card" + str(x + 2), list(range(1, op1 + 1)))
        op2.append(a)

op3 = st.sidebar.radio(label="■ 先攻 or 後攻", options=("先攻", "後攻"), index=0, horizontal=True)
if op3 == "先攻":
    op3 = 0
else:
    op3 = 1

check = 0
for y in range(len(op2)):
    check = check + op2[y]

if check > op1:
    st.error('キーカードの総枚数がデッキ枚数を超えているため計算できません')
else:
    lt = []
    l0 = []
    l1 = []
    l2 = []
    l3 = []
    l0x = []
    l1x = []
    l2x = []
    l3x = []


    def pro(option1, option2, option3, mulligan, turn):
        p1 = math.perm(option1 - option2, 3)
        p2 = math.perm(option1, 3)
        px = p1 / p2
        if option1 - option2 - 3 < 0:
            py = 1
            pz = 1
        else:
            p3 = math.perm(option1 - option2 - 3, mulligan)
            p4 = math.perm(option1 - 3, mulligan)
            py = p3 / p4
            p5 = math.perm(option1 - 3 - option2, turn + option3)
            p6 = math.perm(option1 - 3, turn + option3)
            pz = p5 / p6
        return 1 - px * py * pz


    for t in range(21):
        for m in range(4):
            per = 0
            per1 = 0
            per2 = 0
            per3 = 0
            per4 = 0
            per5 = 0
            op2_sum = 0
            for n in range(len(op2)):
                per1 = per1 + pro(op1, op2[n], op3, m, t)
                op2_sum = op2_sum + op2[n]
            if len(op2) > 2:  # A&B&C
                for a in range(len(op2)):
                    for b in range(len(op2)):
                        if b > a:
                            per2 = per2 + pro(op1, op2[a] + op2[b], op3, m, t)
            if len(op2) > 3:  # A&B&C&D
                for a in range(len(op2)):
                    for b in range(len(op2)):
                        for c in range(len(op2)):
                            if c > b > a:
                                per3 = per3 + pro(op1, op2[a] + op2[b] + op2[c], op3, m, t)
            if len(op2) > 4:  # A&B&C&D&E
                for a in range(len(op2)):
                    for b in range(len(op2)):
                        for c in range(len(op2)):
                            for d in range(len(op2)):
                                if d > c > b > a:
                                    per4 = per4 + pro(op1, op2[a] + op2[b] + op2[c] + op2[d], op3, m, t)
            if len(op2) > 1:
                per5 = pro(op1, op2_sum, op3, m, t)
            if len(op2) % 2 == 0:
                per5 = -per5
            if 3 + op3 + t > len(op2) - 1:  # キーカード種類数>初手枚数なら0%
                per = abs(per1 - per2 + per3 - per4 + per5) * 100
            if m == 0:
                l0.append(per)
            elif m == 1:
                l1.append(per)
            elif m == 2:
                l2.append(per)
            elif m == 3:
                l3.append(per)
        lt.append(t)

    df = pd.DataFrame({
        "0": pd.Series(l0, index=lt),
        "1": pd.Series(l1, index=lt),
        "2": pd.Series(l2, index=lt),
        "3": pd.Series(l3, index=lt)
    })

    l0x = ['{:.2f}'.format(i) + "%" for i in l0]
    l1x = ['{:.2f}'.format(i) + "%" for i in l1]
    l2x = ['{:.2f}'.format(i) + "%" for i in l2]
    l3x = ['{:.2f}'.format(i) + "%" for i in l3]

    lt = [str(i) + " t" for i in lt]

    dfx = pd.DataFrame({
        "0": pd.Series(l0x, index=lt),
        "1": pd.Series(l1x, index=lt),
        "2": pd.Series(l2x, index=lt),
        "3": pd.Series(l3x, index=lt)
    })

    st.sidebar.markdown("---")
    stocks = st.sidebar.multiselect(label="■マリガン枚数",
                                    options=df.columns,
                                    default=["0", "1", "2", "3"]
                                    )
    st.markdown("---")
    if st.checkbox("Show table"):
        st.dataframe(dfx[stocks])
    st.markdown("---")
    if st.checkbox("Show graphic"):
        st.line_chart(df[stocks])
    st.markdown("---")
