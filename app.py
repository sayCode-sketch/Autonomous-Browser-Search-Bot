import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from search_bot import ddg_search

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Autonomous Browser Search Bot", page_icon="🔍")
st.title("🔍 Autonomous Browser Search Bot")

query = st.text_input("Enter your search query:")
max_results = st.slider("Number of results", 1, 10, 5)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        # Search DuckDuckGo
        with st.spinner("Searching DuckDuckGo..."):
            results = ddg_search(query, max_results)

        if not results:
            st.error("No results found.")
        else:
            st.success(f"Found {len(results)} results.")

            # Display raw results
            for i, res in enumerate(results, 1):
                st.markdown(f"### {i}. [{res['title']}]({res['link']})")
                st.write(res['snippet'])

            # Summarize results with OpenAI
            with st.spinner("Summarizing results with AI..."):
                summary_prompt = "Summarize the following search results:\n\n"
                for r in results:
                    summary_prompt += f"Title: {r['title']}\nSnippet: {r['snippet']}\nLink: {r['link']}\n\n"

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summary_prompt}],
                    temperature=0.5
                )
                summary = response.choices[0].message.content

                st.subheader("AI Summary")
                st.write(summary)
