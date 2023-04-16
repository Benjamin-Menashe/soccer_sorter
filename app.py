import streamlit as st
import numpy as np

def Eval_loss(teams):
    vec_m = (np.mean(teams, axis=1) - (np.mean(teams)))
    loss_m = np.linalg.norm(vec_m)
    vec_s = (np.std(teams, axis=1) - np.mean(np.std(teams, axis=1)))
    loss_s = np.linalg.norm(vec_s)
    loss = loss_m + loss_s
    return loss

def main():
    st.title("Team Optimization App")
    st.write("Enter the names and numbers of 21 players:")

    playing = {}
    player_table = st.beta_container()
    with player_table:
        st.write("Enter player names and numbers:")
        playing = {}
        for i in range(1, 22):
            col1, col2 = st.beta_columns(2)
            with col1:
                name = st.text_input(f"Name {i}")
            with col2:
                number = st.number_input(f"Number {i}", value=int)
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

        st.write("Optimized Teams:")
        for i in range(3):
            st.write('------------------------------')
            st.subheader(f"team {i+1}:")
            IDs_str = " ".join(str(IDs[i][j]) for j in range(7))
            st.subheader(IDs_str)
            st.write(np.round(np.mean(teams[i]),2), np.round(np.std(teams[i]),2))

if __name__ == "__main__":
    main()
