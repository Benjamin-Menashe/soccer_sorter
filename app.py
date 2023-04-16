import streamlit as st
import numpy as np
import pyperclip

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


def Eval_loss(teams):
    vec_m = (np.mean(teams, axis=1) - (np.mean(teams)))
    loss_m = np.linalg.norm(vec_m)
    vec_s = (np.std(teams, axis=1) - np.mean(np.std(teams, axis=1)))
    loss_s = np.linalg.norm(vec_s)
    loss = loss_m + loss_s
    return loss

def main():
    st.title("Soccer Team Sorter App")
    st.write("*Created by Benjamin Menashe*")
    st.subheader("This app will randomly sort 21 players into 3 fair teams based on their number rankings.")

    IDs = []
    playing = {}
    names_list = st.text_area("Paste a list of names here, separated by a new line, and press 'ctrl+enter' or click anywhere, or else enter names manually into the table below. make sure there are no repeating names.")
    names_list = names_list.split("\n")
    player_table = st.container()
    with player_table:
        st.write("Rank players:")
        playing = {}
        for i in range(1, 22):
            col1, col2 = st.columns(2)
            with col1:
                if (i-1) < len(names_list):
                    cur_name = names_list[(i-1)].strip()
                    name = st.text_input(f"Name {i}", value=cur_name)                    
                else:
                    name = st.text_input(f"Name {i}")
            with col2:
                number = st.number_input(f"Rank {i} {name}", value=0)
            if name:
                playing[name] = number

    if st.button("Optimize Teams"):
        ps = np.random.permutation(21)
        IDs = np.reshape(np.array(list(playing.keys()))[ps],(3,7))
        teams = np.reshape(np.array(list(playing.values()))[ps],(3,7))
        loss_pre = Eval_loss(teams)
        jj = 0

        while jj < 1000:   
            tm_ind = np.random.choice(3, 2, replace=False)
            plr_ind = np.random.choice(7, 2)
            teams2 = np.copy(teams)
            teams2[tm_ind[0]][plr_ind[0]],teams2[tm_ind[1]][plr_ind[1]] = teams[tm_ind[1]][plr_ind[1]],teams[tm_ind[0]][plr_ind[0]]
            loss_post = Eval_loss(teams2)
            if loss_post < loss_pre:
                teams = teams2
                loss_pre = loss_post
                IDs[tm_ind[0]][plr_ind[0]],IDs[tm_ind[1]][plr_ind[1]] = IDs[tm_ind[1]][plr_ind[1]],IDs[tm_ind[0]][plr_ind[0]]
            jj += 1
            
        st.write("Sort into teams:")
        for i in range(3):
            st.write('------------------------------')
            st.write(f"**team {i+1}:**")
            IDs_str = ", ".join(str(IDs[i][j]) for j in range(7))
            st.write(f"**{IDs_str}**")
            st.write(f"mean={np.round(np.mean(teams[i]),2)} sd={np.round(np.std(teams[i]),2)}")
        st.write('------------------------------')
        
        IF st.button("Copy Team IDs"):
            text_to_be_copied = "Some text"
            copy_dict = {"content": text_to_be_copied}
            
            copy_button = Button(label="Copy Text")
            copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""navigator.clipboard.writeText(content);"""))
            
            no_event = streamlit_bokeh_events(
                copy_button,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=True,
                override_height=75,
                debounce_time=0)

if __name__ == "__main__":
    main()
