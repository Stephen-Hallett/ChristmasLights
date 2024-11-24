import streamlit as st
from utils.make_tree import make_tree


def run():
    st.set_page_config(layout="wide")

    st.title("Christmas Lights Controller")
    st.divider()

    tree_col, _, user_col = st.columns([2, 1, 5])

    with tree_col:
        st.session_state.n_leds = st.number_input(
            label="LEDs: ", min_value=1, value=st.session_state.n_leds, step=1
        )
        st.pyplot(
            make_tree(st.session_state.n_leds, st.session_state.pattern["pattern"])
        )

    with user_col:
        st.header("Make a pattern")


def main():
    # Set state variables
    st.session_state["n_leds"] = st.session_state.get("n_leds", 100)
    # patterns = hit backend API to retrieve from db
    st.session_state["patterns"] = st.session_state.get(
        "patterns", [{"pattern": ["#FFFFFF", "#ff2921"], "effects": {"chasing": True}}]
    )
    st.session_state["pattern"] = st.session_state.get(
        "pattern", {"pattern": ["#FFFFFF", "#ff2921"], "effects": {"chasing": True}}
    )
    run()


if __name__ == "__main__":
    main()
