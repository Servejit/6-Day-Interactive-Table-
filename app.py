import streamlit as st
import re
import pandas as pd
from collections import defaultdict
from io import BytesIO


# ============================================
# Page Config
# ============================================

st.set_page_config(
    page_title="6thSense Stock Analyzer",
    layout="wide"
)

st.title("📊 6thSense Stock Analyzer")


# ============================================
# Function
# ============================================

def analyze_stock_data(raw_text, total_days=6, main4_days=4):

    days_raw = [d.strip() for d in raw_text.split("############################") if d.strip()]

    days = days_raw[:total_days]

    main6 = defaultdict(int)
    main4 = defaultdict(int)
    extra6 = defaultdict(int)

    for day_index, day in enumerate(days):

        lines = day.split("\n")

        extra_mode = False

        main_set = set()
        extra_set = set()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if line.upper().startswith("EXTRA"):
                extra_mode = True
                continue

            match = re.match(r'^([A-Z0-9]+),', line)

            if match:

                stock = match.group(1)

                if extra_mode:
                    extra_set.add(stock)
                else:
                    main_set.add(stock)

        for stock in main_set:
            main6[stock] += 1

        for stock in extra_set:
            extra6[stock] += 1

        if day_index < main4_days:
            for stock in main_set:
                main4[stock] += 1


    all_stocks = set(main6) | set(extra6)

    result = []

    for stock in all_stocks:

        m6 = main6[stock]
        m4 = main4[stock]
        e6 = extra6[stock]
        total = m6 + e6

        result.append([stock, m6, m4, e6, total])


    df = pd.DataFrame(
        result,
        columns=["Stock", "Main6", "Main4", "Extra6", "Total"]
    )

    df = df.sort_values(
        by=["Main6", "Main4", "Extra6"],
        ascending=False
    )

    df = df.reset_index(drop=True)

    return df


# ============================================
# Input Box
# ============================================

raw_data = st.text_area(
    "📥 Paste Raw Data Here",
    height=300
)


# ============================================
# Analyze Button
# ============================================

if st.button("Analyze"):

    if raw_data.strip() == "":
        st.warning("Please paste data first")
    else:

        df = analyze_stock_data(raw_data)

        st.success("Analysis Complete")

        st.dataframe(df, use_container_width=True)


        # Excel Download
        output = BytesIO()

        df.to_excel(output, index=False)

        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name="6thSense_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
