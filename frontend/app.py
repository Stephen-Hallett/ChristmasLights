import os
import time

import requests
import streamlit as st
from matplotlib import pyplot as plt
from utils.make_tree import make_tree
from utils.utilities import effects2backend, effects2frontend, get_alpha


def save_pattern() -> None:
    res = requests.post(
        f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/save",
        json=st.session_state.pattern,
    )
    if res.status_code == 200:
        st.success(res.text)
    else:
        st.error(
            f"Error {'Updat' if 'id' in st.session_state.pattern else 'Sav'}ing pattern \"{st.session_state.pattern["name"]}\""
        )


def run():
    # patterns = hit backend API to retrieve from db
    st.session_state["patterns"] = requests.get(
        f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/list"
    ).json()
    st.session_state.patterns.append(st.session_state.blank_pattern)

    st.session_state["active"] = requests.get(
        f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/active"
    ).json()

    st.title("Christmas Lights Controller")
    st.divider()

    tree_col, _, user_col = st.columns([2, 1, 5])

    with tree_col:
        tree_fig = st.empty()

        def preview(effects: dict, length: int = 5):
            with tree_fig:
                effect_pattern = list(st.session_state.pattern["pattern"])
                start = time.time()
                while time.time() - start < length:
                    if effects["chasing"] > 0:
                        effect_pattern.insert(0, effect_pattern[-1])
                        effect_pattern.pop(-1)
                    if effects["breathing"] > 0:
                        alpha = get_alpha(effects["breathing"], time.time() - start)
                    else:
                        alpha = 1
                    fig = make_tree(
                        st.session_state.n_leds,
                        effect_pattern,
                        alpha=alpha,
                        sparkle=effects["sparkle"],
                    )
                    st.pyplot(fig, clear_figure=True)
                    plt.close(fig)
                    current = time.time() - start
                    if effects["chasing"]:
                        time.sleep(effects["chasing"] - (current % effects["chasing"]))

    time.sleep(0.08)

    with user_col:
        st.header("Pattern Menu")
        st.session_state.pattern = st.selectbox(
            "Pattern to edit",
            options=st.session_state.patterns,
            index=st.session_state.patterns.index(st.session_state.active),
            format_func=lambda x: x["name"] if len(x["name"]) else "+ Create New",
        )

        details_col, _, effects_col = st.columns([6, 1, 2])
        with details_col:
            current = st.session_state.pattern
            ui_effects = effects2frontend(current["effects"])
            current["name"] = st.text_input("Pattern name:", value=current["name"])
            pattern_length = st.number_input(
                label="Pattern length",
                min_value=1,
                max_value=st.session_state.n_leds,
                value=len(current["pattern"]),
            )

            st.html("<br/>")
            current["active"] = st.toggle("Activate pattern", value=current["active"])
        with effects_col:
            st.subheader("Effects")
            for eff in st.session_state.effects:
                ui_effects[eff] = st.slider(
                    eff,
                    min_value=st.session_state.slider_values[eff][0],
                    value=ui_effects[eff],
                    help=st.session_state.help_messages[eff],
                    max_value=st.session_state.slider_values[eff][1],
                    step=st.session_state.slider_values[eff][2],
                )
            current["effects"] = effects2backend(ui_effects)
        st.divider()

        current["pattern"] = [
            current["pattern"][i] if i < len(current["pattern"]) else "#000000"
            for i in range(pattern_length)
        ]
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

        st.button(
            f"{'Update' if 'id' in current else 'Save'} pattern",
            use_container_width=True,
            type="primary",
            on_click=save_pattern,
        )

    with tree_col:
        with tree_fig:
            fig = make_tree(
                st.session_state.n_leds, st.session_state.pattern["pattern"], alpha=1
            )
            st.pyplot(fig, clear_figure=True)
        _, stump, _ = st.columns([3, 4, 3])
        with stump, st.container(key="stump_button"):
            st.button(
                "Preview",
                on_click=preview,
                args=(current["effects"], 5),
                use_container_width=True,
            )


def main():
    st.set_page_config(layout="wide")
    # Set state variables
    st.session_state["n_leds"] = int(
        st.session_state.get("n_leds", os.environ.get("N_LEDS", 100))
    )
    st.session_state["blank_pattern"] = st.session_state.get(
        "blank_pattern",
        {
            "name": "",
            "pattern": ["#000000"],
            "active": False,
            "effects": {"breathing": 0.0, "chasing": 0.0, "sparkle": 0.0},
        },
    )
    st.session_state["pattern"] = st.session_state.get(
        "pattern",
        requests.get(
            f"{os.environ.get("BACKEND_URL", "http://localhost:80")}/patterns/active"
        ).json(),
    )
    st.session_state["effects"] = st.session_state.get(
        "effects", set(st.session_state.pattern["effects"].keys())
    )
    st.session_state["help_messages"] = st.session_state.get(
        "help_messages",
        {
            "breathing": "Number of complete pulses to occur per minute",
            "chasing": "Number of pattern steps per minute",
            "sparkle": "The approximate proportion of lights which should be randomly turned off at any given time.",
        },
    )
    st.session_state["slider_values"] = st.session_state.get(
        "slider_values",
        {"breathing": (0, 100, 1), "chasing": (0, 1000, 1), "sparkle": (0, 100, 1)},
    )
    st.html("static/style.css.html")
    run()


if __name__ == "__main__":
    main()
