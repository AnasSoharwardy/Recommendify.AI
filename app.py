import streamlit as st
import requests
import json

st.set_page_config()
st.title("Recommendify.AI")

st.markdown("""
This is an **AI-powered Product Review Analyzer** that finds YouTube reviews and helps you decide whether to buy a product, with the help of AI Agents & LLM!

No more wasting time browsing countless YouTube videos to find trustworthy product reviews!

How it works:
- Searches YouTube for top review videos
- Filter relevant videos
- Extracts transcripts of the videos  
- Summarizes the overall sentiment by using the pros and cons from transcripts
- Provides a recommendation based on the summaries

Just enter a specific product name below to begin!
""")

query = st.text_input("Enter a specific product name")
st.caption("Examples: Sony PS5, iPhone 15 Pro, Dyson Airwrap, Tesla Model 3 2024, HyperX Cloud 2")

if st.button("Recommendify!"):
    if not query.strip():
        st.warning("Please enter a product name")
    else:
        st.write("⏳ Running analysis...")
        try:
            response = requests.post(
                "http://localhost:8000/analyze",
                json={"query": query}
            )

            if response.status_code != 200:
                st.error(f"Server error: {response.status_code}")
                st.stop()

            data = response.json()

            if not data.get("success"):
                st.warning(f"{data.get('error', 'Unknown error')}")
                st.stop()

            st.success("✅ Analysis complete!")

            st.subheader("Final Verdict")

            try:
                #
                verdict_data = json.loads(data["verdict"])
                recommendation = verdict_data.get("recommendation", "N/A")
                reason = verdict_data.get("reason", "No reason provided.")

                st.markdown(f"**Recommendation:** {recommendation}")
                st.markdown(f"**Reason:** {reason}")

            except Exception:
                st.write(data["verdict"])

        except Exception as e:
            st.error(f"An error occurred: {e}")
