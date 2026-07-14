import random

import streamlit as st

st.set_page_config(page_title="영단어 게임", page_icon="📚", layout="centered")

WORDS = [
    {"word": "friend", "meaning": "친구"},
    {"word": "beautiful", "meaning": "아름다운"},
    {"word": "exercise", "meaning": "운동"},
    {"word": "travel", "meaning": "여행"},
    {"word": "library", "meaning": "도서관"},
    {"word": "important", "meaning": "중요한"},
    {"word": "weather", "meaning": "날씨"},
    {"word": "vacation", "meaning": "방학"},
    {"word": "science", "meaning": "과학"},
    {"word": "delicious", "meaning": "맛있는"},
]


def reset_game():
    st.session_state.questions = random.sample(range(len(WORDS)), len(WORDS))
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.feedback = ""
    st.session_state.game_over = False


if "questions" not in st.session_state:
    reset_game()

st.title("📚 중학생 영단어 게임")
st.write("한글 뜻을 보고 올바른 영어 단어를 고르면 됩니다!")

with st.sidebar:
    st.header("게임 설정")
    st.write(f"현재 문제 수: {len(WORDS)}개")
    if st.button("새 게임 시작", use_container_width=True):
        reset_game()

if st.session_state.game_over:
    st.success("게임이 끝났습니다!")
    st.metric("맞힌 개수", f"{st.session_state.score}/{len(WORDS)}")
    st.write("다시 도전하고 싶으면 새 게임을 시작하세요.")
    if st.button("다시 시작", use_container_width=True):
        reset_game()
else:
    current_question = WORDS[st.session_state.questions[st.session_state.current_index]]
    options = [current_question["word"]]
    other_words = [word["word"] for word in WORDS if word["word"] != current_question["word"]]
    options.extend(random.sample(other_words, 3))
    random.shuffle(options)

    st.progress((st.session_state.current_index + 1) / len(WORDS))
    st.subheader(f"문제 {st.session_state.current_index + 1}/{len(WORDS)}")
    st.write(f"뜻: {current_question['meaning']}")

    for option in options:
        if st.button(option, key=f"option_{st.session_state.current_index}_{option}"):
            if option == current_question["word"]:
                st.session_state.score += 1
                st.session_state.feedback = f"정답입니다! {current_question['word']}는(은) {current_question['meaning']}입니다."
            else:
                st.session_state.feedback = (
                    f"아쉽네요. 정답은 {current_question['word']}입니다."
                )
            st.session_state.submitted = True
            st.rerun()

    if st.session_state.submitted:
        st.info(st.session_state.feedback)
        if st.button("다음 문제", use_container_width=True):
            st.session_state.current_index += 1
            st.session_state.submitted = False
            st.session_state.feedback = ""
            if st.session_state.current_index >= len(WORDS):
                st.session_state.game_over = True
            st.rerun()
