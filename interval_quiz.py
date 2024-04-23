import streamlit as st
from generation import *
from element import user_quality, user_interval, fun_emoji_list
from streamlit_extras.let_it_rain import rain

def main():
    st.set_page_config(page_title="Music Note App")
    if 'new_quest' not in st.session_state:
        st.session_state['new_quest'] = True
    if 'pic' not in st.session_state:
        st.session_state['pic'] = False
    
    def new_question():
        difficulty = st.session_state.get('difficulty', 0)
        ans, clef, clef2, fix_octave1, fix_octave2, note, note2 = score_generation(level=difficulty)
        lilypond_generation(clef, clef2, fix_octave1, fix_octave2, note, note2)
        st.session_state['current_answer'] = ans
        st.session_state['feedback'] = ""
        st.session_state['pic'] = True

    def check_answer():
        user_ans = f"{st.session_state['user_quality']} {st.session_state['user_interval']}"
        current_answer = st.session_state.get('current_answer')

        if current_answer is None:
            feedback = 'Error: No current answer available. Please try a new question.'
        elif user_ans.lower() == current_answer.lower():
            feedback = 'Correct!'
            fun_emoji = random.choice(fun_emoji_list)
            rain(emoji = fun_emoji,animation_length="5")
            st.session_state['new_quest'] = True
        else:
            feedback = f'Incorrect. The answer should be {current_answer}'

        st.session_state['feedback'] = feedback
    
    st.title("Music Note App")

    difficulty = st.selectbox("Choose difficulty:", [
        "Beginner", "Intermediate", "Advanced", "C clef Fanfare", "Expert", "Accidental Madness"
    ], index=st.session_state.get('difficulty', 0))
    st.session_state['difficulty'] = ["Beginner", "Intermediate", "Advanced", "C clef Fanfare", "Expert", "Accidental Madness"].index(difficulty)

    col1, col2 = st.columns(2)
    if st.session_state['pic']==True:
        image_path = "static/images/cropped_score_ans.png"
        st.image(image_path, use_column_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        Qualityans=st.selectbox("Quality", user_quality, key='user_quality')

    with col2:
        Intervalans=st.selectbox("Interval", user_interval, key='user_interval')

    with col3:
        if st.button("Check Answer") and Qualityans != "--"and Intervalans!= "--":
            check_answer()
            if st.session_state.get('feedback'):
                st.write(st.session_state['feedback'])

    if st.button("New Question"):
        st.session_state['pic']=False
        new_question()
        st.rerun()

if __name__ == '__main__':
    main()
