import math
import time

import streamlit as st
from matplotlib import pyplot as plt
from utils.make_tree import make_tree


def run():
    st.title("Christmas Lights Controller")
    st.divider()

    tree_col, _, user_col = st.columns([2, 1, 5])

    with tree_col:
        st.session_state.n_leds = st.number_input(
            label="LEDs: ", min_value=1, value=st.session_state.n_leds, step=1
        )
        tree_fig = st.empty()

        def preview(effects, length: int = 5):
            with tree_fig:
                start = time.time()
                alpha = 1
                pattern = list(st.session_state.pattern["pattern"])
                sparkle = 1
                while time.time() - start < length:
                    if effects["breathing"]:
                        alpha = (math.sin(time.time() * 3) + 1) / 2
                    if effects["chasing"]:
                        last = pattern.pop(-1)
                        pattern = [last] + pattern
                    if effects["sparkle"]:
                        sparkle = 5
                    fig = make_tree(
                        st.session_state.n_leds, pattern, alpha=alpha, sparkle=sparkle
                    )
                    st.pyplot(
                        fig,
                        clear_figure=True,
                    )
                    plt.close(fig)
                    time.sleep(0.02)

        with tree_fig:
            fig = make_tree(
                st.session_state.n_leds,
                st.session_state.pattern["pattern"],
                alpha=1,
            )
            st.pyplot(
                fig,
                clear_figure=True,
            )

    with user_col:
        st.header("Make a pattern")
        details_col, _, effects_col = st.columns([6, 1, 2])
        with details_col:
            pattern_name = st.text_input(
                "Pattern name:", value=f"Pattern{len(st.session_state.patterns)+1}"
            )
            pattern_length = st.number_input(
                label="Pattern length",
                min_value=1,
                max_value=st.session_state.n_leds,
                value=1,
            )

        with effects_col:
            st.subheader("Effects")
            effects = {}
            for eff in st.session_state.effects:
                effects[eff] = st.checkbox(eff, value=False)
        st.divider()

        colours = ["#FFFFFF"] * pattern_length

        with st.container(key="colourbox"):
            colour_cols = st.columns(pattern_length)
            for i in range(pattern_length):
                with colour_cols[i]:
                    colours[i] = st.color_picker(
                        label=" ",
                        label_visibility="hidden",
                        key=f"pattern_colour{i}",
                        value="#FFFFFF",
                    )
        st.divider()

        pattern = {"name": pattern_name, "pattern": colours, "effects": effects}
        st.session_state.pattern = pattern
        st.button("Preview", on_click=preview, args=(effects, 5))


def main():
    st.set_page_config(layout="wide")
    # Set state variables
    st.session_state["n_leds"] = st.session_state.get("n_leds", 100)
    # patterns = hit backend API to retrieve from db
    st.session_state["patterns"] = st.session_state.get(
        "patterns",
        [
            {
                "name": "Candy Cane",
                "pattern": ["#FFFFFF", "#ff2921"],
                "effects": {"breathing": False, "chasing": True, "sparkle": False},
            }
        ],
    )
    st.session_state["pattern"] = st.session_state.get(
        "pattern",
        {
            "name": "Candy Cane",
            "pattern": ["#FFFFFF", "#ff2921"],
            "effects": {"breathing": False, "chasing": True, "sparkle": False},
        },
    )
    st.session_state["effects"] = st.session_state.get(
        "effects", set(st.session_state.pattern["effects"].keys())
    )
    st.html("static/style.css.html")
    run()


if __name__ == "__main__":
    main()
