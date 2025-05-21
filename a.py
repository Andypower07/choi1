import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("고등학교 학기별 평균 등급 계산기")
if 'semesters' not in st.session_state:
    st.session_state.semesters = {}

st.sidebar.header("학기 추가")
semester_name = st.sidebar.text_input("학기 이름 (예: 1학년 1학기)", "")
num_subjects = st.sidebar.number_input("과목 수", min_value=1, max_value=10, value=1, step=1)

if semester_name:
    st.sidebar.subheader(f"{semester_name} 과목 입력")
    subjects = []
    with st.sidebar.form(key=f"form_{semester_name}"):
        for i in range(int(num_subjects)):
            st.write(f"과목 {i+1}")
            subject = st.text_input(f"과목 이름 {i+1}", key=f"subject_{semester_name}_{i}")
            grade = st.selectbox(f"등급 {i+1}", options=[1, 2, 3, 4, 5, 6, 7, 8, 9], key=f"grade_{semester_name}_{i}")
            credits = st.number_input(f"주당 수업 횟수(학점) {i+1}", min_value=1.0, max_value=10.0, step=1.0, key=f"credits_{semester_name}_{i}")
            subjects.append({"subject": subject, "grade": grade, "credits": credits})
        submit_button = st.form_submit_button("저장")
        if submit_button and all(s["subject"] for s in subjects):
            st.session_state.semesters[semester_name] = subjects
            st.sidebar.success(f"{semester_name} 저장 완료!")
        elif submit_button:
            st.sidebar.error("모든 과목 이름을 입력해주세요.")

avg_grade_data = {}
for semester, subjects in st.session_state.semesters.items():
    total_grade_points = sum(sub["grade"] * sub["credits"] for sub in subjects)
    total_credits = sum(sub["credits"] for sub in subjects)
    avg_grade = total_grade_points / total_credits if total_credits > 0 else 0.0
    avg_grade_data[semester] = round(avg_grade, 2)

if avg_grade_data:
    st.header("학기별 평균 등급")
    avg_grade_df = pd.DataFrame(list(avg_grade_data.items()), columns=["학기", "평균 등급"])
    st.table(avg_grade_df)
    st.header("학기별 평균 등급 그래프")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avg_grade_df["학기"], avg_grade_df["평균 등급"], marker='o', linestyle='-', color='b')
    ax.set_xlabel("학기")
    ax.set_ylabel("평균 등급 (1~9등급)")
    ax.set_title("학기별 평균 등급 추이")
    ax.grid(True)
    ax.invert_yaxis()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

if st.session_state.semesters:
    st.header("과목별 상세 정보")
    for semester, subjects in st.session_state.semesters.items():
        st.subheader(semester)
        df = pd.DataFrame(subjects)
        st.table(df)
