import math
import time

import streamlit as st
from matplotlib import pyplot as plt
from utils.make_tree import make_tree
import requests
import os

def save_pattern() -> None:
    res = requests.post(f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/save", json=st.session_state.pattern)
    if res.status_code == 200:
        st.success(res.text)
    else:
        st.error(f"Error {'Updat' if 'id' in st.session_state.pattern else 'Sav'}ing pattern \"{st.session_state.pattern["name"]}\"")

def run():
    # patterns = hit backend API to retrieve from db
    st.session_state["patterns"] = requests.get(f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/list").json()
    st.session_state.patterns.append(st.session_state.blank_pattern)

    st.session_state["active"] = requests.get(f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/active").json()

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

    with user_col:
        st.header("Pattern Menu")

        st.session_state.pattern = st.selectbox("Pattern to edit", 
                                                options=st.session_state.patterns, 
                                                index = st.session_state.patterns.index(st.session_state.active),
                                                format_func = lambda x: x["name"])

        details_col, _, effects_col = st.columns([6, 1, 2])
        with details_col:
            current = st.session_state.pattern
            current["name"] = st.text_input(
                "Pattern name:", value=current["name"]
            )
            pattern_length = st.number_input(
                label="Pattern length",
                min_value=1,
                max_value=st.session_state.n_leds,
                value=len(current["pattern"]),
            )

        with effects_col:
            st.subheader("Effects")
            for eff in st.session_state.effects:
                current["effects"][eff] = st.number_input(eff, min_value=0 if isinstance(current["effects"][eff], int) else 0.0, value=current["effects"][eff])
        st.divider()

        current["pattern"] = [current["pattern"][i] if i < len(current["pattern"]) else "#000000" for i in range(pattern_length)]

        with st.container(key="colourbox"):
            colour_cols = st.columns(pattern_length)
            for i in range(pattern_length):
                with colour_cols[i]:
                    current["pattern"][i] = st.color_picker(
                        label=" ",
                        label_visibility="hidden",
                        key=f"pattern_colour{i}",
                        value=current["pattern"][i],
                    )
        st.divider()

        st.button(f"{'Update' if 'id' in current else 'Save'} pattern", use_container_width=True, type="primary", on_click=save_pattern)

    with tree_col:
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
        _, stump, _ = st.columns([3,4,3])
        with stump, st.container(key="stump_button"):
            st.button("Preview", on_click=preview, args=(current["effects"], 5), use_container_width=True)


def main():
    st.set_page_config(layout="wide")
    # Set state variables
    st.session_state["n_leds"] = int(st.session_state.get("n_leds", os.environ.get("N_LEDS", 100)))
    st.session_state["blank_pattern"] = st.session_state.get("blank_pattern", {"name": "New Pattern",
                                                                               "pattern": ["#000000"],
                                                                               "active": False,
                                                                               "effects": {
                                                                                   "breathing": 0,
                                                                                   "chasing": 0,
                                                                                   "sparkle": 0
                                                                               }})
    st.session_state["pattern"] = st.session_state.get(
        "pattern",
        requests.get(f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/active").json(),
    )
    st.session_state["effects"] = st.session_state.get(
        "effects", set(st.session_state.pattern["effects"].keys())
    )
    st.html("static/style.css.html")
    run()


if __name__ == "__main__":
    main()
