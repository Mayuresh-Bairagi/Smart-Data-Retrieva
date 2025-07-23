import streamlit as st
from sql_agent import SQLReviewAnalyzer

# Set up your SQLite DB path
DB_PATH = r"D:\Gen AI\Saurabh\reviews.db"

# Initialize SQL Agent
@st.cache_resource
def get_sql_agent():
    return SQLReviewAnalyzer(db_path=DB_PATH)

sql_agent = get_sql_agent()

# Streamlit UI
st.set_page_config(page_title="Shopify Review Analyst", layout="wide")
st.title("📊 Shopify Review SQL Analyst")

st.markdown("Ask questions in natural language, and get answers from the review database!")

# Input box for question
question = st.text_input("Enter your question:", placeholder="e.g. What are the top 5 highest-rated reviews?")

# Submit button
if st.button("Get Answer") and question.strip():
    with st.spinner("Generating SQL and running the query..."):
        try:
            # Get SQL + Answer
            sql_query = sql_agent.generate_sql(question)
            result_df = sql_agent.run_sql_query(sql_query)
            final_answer = sql_agent.format_answer(question, sql_query, result_df)

            # Display SQL
            with st.expander("🧠 Generated SQL Query"):
                st.code(sql_query, language="sql")

            # Display Table
            if result_df is not None and not result_df.empty:
                st.subheader("📋 Query Results")
                st.dataframe(result_df)
            else:
                st.warning("No results found for this query.")

            # Display final answer
            st.subheader("🧾 Final Answer")
            st.markdown(final_answer)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
else:
    st.info("Enter a question above and click 'Get Answer'.")

# Footer
st.markdown("---")
st.caption("Built by Mayuresh with ❤️ using Streamlit, LangChain & Groq")
