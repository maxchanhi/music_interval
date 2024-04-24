import streamlit as st
from generation import *
from element import user_quality, user_interval, fun_emoji_list
from element import basic_accidentals, advance_accidentals, difficulty_list
from streamlit_extras.let_it_rain import rain
st.set_page_config(page_title="Music Note App")
if 'new_quest' not in st.session_state:
    st.session_state['new_quest'] = True
if 'pic' not in st.session_state:
    st.session_state['pic'] = False
if 'selected_clef' not in st.session_state:
    st.session_state['selected_clef'] = ["treble"]
if 'selected_acci' not in st.session_state:
    st.session_state['selected_clef'] = ["Natural (♮)"]
if 'difficulty' not in st.session_state:
    st.session_state['difficulty'] = "Beginner"

def new_question(selected_clef,selected_acci,compound_o):
    difficulty = st.session_state.get('difficulty', 0)
    
    ans, clef, clef2, fix_octave1, fix_octave2, note, note2 = score_generation(selected_clef,selected_acci,compound_o,level=difficulty)
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
        rain(emoji = fun_emoji,animation_length="1")
        st.session_state['new_quest'] = True
    else:
        feedback = f'Incorrect. The answer should be {current_answer}'

    st.session_state['feedback'] = feedback
def main():
    st.title("Music Note App")
    col1, col2 = st.columns(2)
    compound = st.session_state.get('compound_octave', False)
    auto_level = st.session_state.get('auto_mode', True)
    if auto_level:
        show_selectbox = True
        st.session_state['difficulty'] = st.select_slider("Pick you poison💀:",options=difficulty_list)
        st.session_state['selected_clef'] = level_difficulty(st.session_state['difficulty'])['clef']
        st.session_state['selected_acci'] = level_difficulty(st.session_state['difficulty'])['accidentals']
    else:
        show_selectbox = False
    with col1:
        st.checkbox("Auto mode", key='auto_mode',value=True)
        st.session_state['selected_clef']=st.multiselect("Select clef:", ["treble", "bass", "alto", "tenor"],
                                                         default=st.session_state['selected_clef'],disabled=show_selectbox)
    with col2:
        st.checkbox("Compound Interval", key='compound_octave')
        st.session_state['selected_acci']=st.multiselect("Select accidental:", advance_accidentals,
                                                         default=st.session_state['selected_acci'],disabled=show_selectbox)
    if not st.session_state['selected_clef'] or not st.session_state['selected_acci']:
        st.warning("Please select a clef and a accidental.")
    
    if st.button("New Question") and st.session_state['selected_clef'] and st.session_state['selected_acci']:
        st.session_state['pic']=False
        new_question(st.session_state['selected_clef'],st.session_state['selected_acci'],compound)
        st.rerun()

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
            if st.session_state.get('feedback',None):
                st.write(st.session_state['feedback'])
    

if __name__ == '__main__':
    main()