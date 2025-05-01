import streamlit as st
import re

st.set_page_config(page_title="Subtract Times", layout="centered")
st.title("⏱️ Time Subtraction Calculator")

def validate_and_format(time_str):
    time_str = re.sub(r"[^\d:]", "", time_str)

    if len(time_str) == 4 and ":" not in time_str:
        time_str = time_str[:2] + ":" + time_str[2:]

    if re.fullmatch(r"\d{1,2}:\d{2}", time_str):
        h, m = map(int, time_str.split(":"))
        if 0 <= h <= 23 and 0 <= m <= 59:
            return f"{h:02}:{m:02}"
    return ""

def subtract_times(start, times):
    results = []
    try:
        h1, m1 = map(int, start.split(":"))
        start_minutes = h1 * 60 + m1

        for t in times:
            if t:
                h2, m2 = map(int, t.split(":"))
                target_minutes = h2 * 60 + m2
                diff = target_minutes - start_minutes

                if diff < 0:
                    diff += 1440  # rollover midnight

                hours = diff // 60
                minutes = diff % 60
                results.append(f"{hours}:{minutes:02d}")
            else:
                results.append("")
        return results
    except:
        return ["⚠️ Invalid time format"] * len(times)

# Input fields
st.subheader("Enter Times")
start_time = st.text_input("Start Time (HH:MM or HHMM)", key="start")
start_time = validate_and_format(start_time)

time_inputs = []
for i in range(1, 4):
    t = st.text_input(f"Time {i} (HH:MM or HHMM)", key=f"time_{i}")
    time_inputs.append(validate_and_format(t))

if st.button("Calculate"):
    if not start_time or not re.fullmatch(r"\d{2}:\d{2}", start_time):
        st.error("Start time must be in HH:MM format.")
    else:
        results = subtract_times(start_time, time_inputs)
        st.success("Subtracted Times:")
        for i, r in enumerate(results):
            st.write(f"Time {i+1} - Start = **{r}**")

if st.button("Clear"):
    st.session_state["start"] = ""
    for i in range(1, 4):
        st.session_state[f"time_{i}"] = ""
    st.experimental_rerun()
