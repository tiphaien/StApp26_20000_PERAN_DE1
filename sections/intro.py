# context, objectives, data caveats
import streamlit as st

from utils.io import URL_JEU


def render():
    st.subheader("Why this topic is important")
    st.markdown("""
    Tap water is the most controlled food item in France: hundreds of thousands of samples
    are analyzed each year by the Regional Health Agencies. **But is this water of the same
    quality everywhere, and throughout the year?**

    **Target audience :** residents, local elected officials and water services who want to know where to act as a priority.

    **Questions this dashboard answers:**
    1. Do water quality issues vary throughout the year? → *Over time* tab
    2. Are some departments more affected than others? → *Where?* tab
    3. Can these figures be trusted? → *Data quality* tab
    """)
    st.subheader("How to read the data")
    st.markdown("""
    - **A sample** = a water sample collected from the distribution network.
    - **Bacteriology** : presence of microbes that can cause illness (e.g., E. coli).
    - **Chemistry** : substances like nitrates or pesticides.
    - **Non-conforming** = at least one value exceeds a **quality limit** set by regulations.
      This signals a problem to be corrected, without necessarily indicating an immediate danger.
    """)
    st.info(f"Data: [Tap water health monitoring results]({URL_JEU}) (2024), "
            "Ministry of Health — Open Licence. File used: UDI_PLV "
            "(samples collected from distribution networks).")