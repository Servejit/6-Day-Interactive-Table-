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
    "💹I'day 

https://colab.research.google.com/drive/1eiD96FMKbxOcqnY55PcA6yYJY5LbLzlV


https://colab.research.google.com/drive/1Ftd318NU5cQvBy28-u16_G3daf5JWYug

############################
6thSense+6thAlert 
ETERNAL, "264.19"
TRENT, "4029.90" + "4019.80"
TECHM, "1426.43" + "1422.85"
MOTHERSON, "128.16" + "127.84"
ADANIGREEN, "959.60" + "957.19"
LTIM, "4753.09" + "4741.18"
NAUKRI, "1051.76" + "1049.13"
PERSISTENT, "4903.71"
DIXON, "10540.58"
MPHASIS, "2288.17"
NHPC, "73.53" + "73.34"
SUZLON, "43.72" + "43.61"
INDUSINDBK, "909.67" + "907.39"
SRF, "2615.94" + "2609.39"
PHOENIXLTD, "1697.75" + "1693.49"



Extra 
INFY, "1314.71" + "1311.41"



############################
Yesterday 
TECHM, "1449.47" + "1445.83"
ETERNAL, "267.18" + "266.51"
NAUKRI, "1062.34" + "1059.68"
LTIM, "4849.85" + "4837.69"
INDHOTEL, "663.34" + "661.68"
AMBUJACEM, "507.38" + "506.11"
DLF, "614.46" + "612.92"
PERSISTENT, "5057.33"
HDFCAMC, "2694.65" + "2687.89"
PRESTIGE, "1468.32" + "1464.64"
NHPC, "73.77" + "73.58"
MANKIND, "2009.86" + "2004.83"
DIXON, "10979.48" + "10951.97"
BHEL, "250.07" + "249.45"
OBEROIRLTY, "1490.27" + "1486.53"
MPHASIS, "2315.40" + "2309.59"
SRF, "2653.65" + "2647.00"




Extra 
ULTRACEMCO, "12546.56" + "12515.11"
TRENT, "4031.60" + "4021.49"
BHARTIARTL, "1966.07" + "1961.15"
LODHA, "1054.71" + "1052.06"
MUTHOOTFIN, "3356.59" + "3348.18"
PAGEIND, "32383.84" + "32302.68"




############################
Yesterday 
ETERNAL, "269.18" + "268.50"
LTIM, "4908.70" + "4896.40"
NAUKRI, "1087.28" + "1084.55"
SRF, "2657.24" + "2650.58"

Extra 
INDHOTEL, "666.43" + "664.76"
HDFCAMC, "2718.19" + "2711.38"
MPHASIS, "2356.10" + "2350.19"
DIXON, "11098.19" + "11070.37"
OBEROIRLTY, "1490.76" + "1487.03"

############################
Yesterday 
SRF, "2689.06" + "2682.32"

############################
Yesterday 
HINDALCO, "878.80"
M&M, "3453.35" + "3444.69"
HINDZINC, "573.56"
BOSCHLTD, "35131.95" + "35043.90"
MUTHOOTFIN, "3431.50"
BSE, "2718.29"
HEROMOTOCO, "5432.88" + "5419.27"
PIIND, "3007.46" + "2999.93"



############################
Yesterday 
HINDUNILVR, "2282.38"
HINDALCO, "887.28"
JIOFIN, "258.90" + "258.25"
M&M, "3460.33" + "3451.66"
RELIANCE, "1405.78" + "1402.25"
ADANIPORTS, "1491.56" + "1487.82"
TATACONSUM, "1114.31" + "1111.51"
COALINDIA, "405.58" + "404.57"
ADANIENT, "2097.94" + "2092.68"
KOTAKBANK, "417.20" + "416.16"
DLF, "620.45"
BAJAJHFL, "88.45" + "88.23"
PNB, "117.26" + "116.96"
IRFC, "110.29" + "110.02"
SOLARINDS, "12819.87" + "12787.74"
GODREJCP, "1168.87" + "1165.94"
CANBK, "139.80" + "139.45"
DMART, "3832.69" + "3823.09"
PFC, "396.26" + "395.26"
BPCL, "368.13" + "367.20"
AMBUJACEM, "511.92" + "510.63"
MUTHOOTFIN, "3441.38"
BSE, "2719.48"
OIL, "451.02"
PAGEIND, "33146.93" + "33063.85"
NHPC, "74.46" + "74.28"
UPL, "714.61" + "712.82"
IRCTC, "604.63" + "603.12"
POLYCAB, "7517.16" + "7498.32"
YESBANK, "20.65" + "20.60"





Extra
TATASTEEL, "200.05" + "199.55"
SUZLON, "45.23" + "45.11"
BHEL, "252.37" + "251.74"




############################
Yesterday 
INFY, "1278.30"
TCS, "2578.54"
HCLTECH, "1392.51"
HDFCBANK, "898.75" + "896.50"
KOTAKBANK, "418.50" + "417.45"
JIOFIN, "262.19" + "261.54"
COALINDIA, "407.08" + "406.06"
HINDALCO, "898.75" + "896.50"
DLF, "621.99"
LTIM, "4975.53"
JSWENERGY, "467.68" + "466.51"
SOLARINDS, "12902.66" + "12870.33"
RECLTD, "338.95" + "338.10"
IRFC, "110.77" + "110.49"
BAJAJHFL, "88.68" + "88.46"
SHREECEM, "25685.63" + "25621.25"
PNB, "118.00" + "117.71"
VBL, "444.49" + "443.37"
CANBK, "141.07" + "140.71"
NAUKRI, "1101.44" + "1098.68"
COFORGE, "1330.67"
OIL, "451.17"
OFSS, "6384.00"
PERSISTENT, "5196.98"
MPHASIS, "2349.31"
SRF, "2758.69"
PRESTIGE, "1478.39" + "1474.69"
NHPC, "75.01" + "74.82"
PAGEIND, "33216.75" + "33133.50"
JUBLFOOD, "523.94" + "522.62"
YESBANK, "20.66" + "20.61"
IDFCFIRSTB, "79.81" + "79.61"
GMRAIRPORT, "93.30" + "93.06"





Extra 
TATACONSUM, "1122.59" + "1119.77"
ADANIENT, "2118.89" + "2113.58"
AXISBANK, "1312.81" + "1309.52"
M&M, "3511.50" + "3502.70"
RELIANCE, "1412.76" + "1409.22"
AMBUJACEM, "515.96" + "514.66"
PFC, "398.40" + "397.40"
BPCL, "372.02" + "371.09"
UPL, "719.15" + "717.35"





############################
       ______  Finish Line _______




",
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
