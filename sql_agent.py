import os
import pandas as pd
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()


class SQLReviewAnalyzer:
    def __init__(self, db_path: str, groq_model: str = "gemma2-9b-it", temperature: float = 0):
        # Set up LLM
        self.llm = ChatGroq(
            model=groq_model,
            temperature=temperature
        )

        # Setup SQL DB connection
        sqlite_uri = f"sqlite:///{db_path}"
        self.db = SQLDatabase.from_uri(sqlite_uri)

        # Setup SQL generation prompt
        self.prompt_generate_sql_query = PromptTemplate(
            template=self._get_sql_prompt_template(),
            input_variables=["user_question"]
        )

        # Setup answer formatting prompt
        self.prompt_format_answer = PromptTemplate(
            template=self._get_answer_prompt_template(),
            input_variables=["question", "sql_query", "sql_query_result"]
        )

        # Output parser
        self.parser = StrOutputParser()

        # SQL chain
        self.sql_chain = (
            {"user_question": RunnablePassthrough()}
            | self.prompt_generate_sql_query
            | self.llm
            | self.parser
        )

        # Answer chain
        self.answer_chain = (
            self.prompt_format_answer
            | self.llm
            | self.parser
        )

    def _get_sql_prompt_template(self):
        return """
You are an expert SQLite SQL query generator.

Your job is to generate correct and optimized **SQLite SQL queries** based on natural language questions.

Use only the following table: `shopify_reviews`

Its columns are:
- "Review ID" (text)
- "Product Name" (text)
- "Rating" (numeric, 1 to 5)
- "Review Content" (text)
- "Timestamp" (datetime)
- "Customer Email" (text)
- "Product Category" (text)
- "Order Value" (numeric)
- "Fulfillment Status" (text)
- "Shipping Country" (text)

### Rules:
- Use only valid SQLite-compatible SQL syntax
- Do not use `ORDER BY` or `LIMIT` directly before or after `UNION` or `UNION ALL`; wrap each SELECT in a subquery if needed
- Always wrap subqueries when using `ORDER BY` with `LIMIT` inside `UNION`, `UNION ALL`, or `JOIN`
- Output only the final SQL query — no explanations
- Enclose all column names in double quotes (`"Column Name"`)
- If the query involves sentiment, use `"Rating"` as a proxy (1 = negative, 5 = positive)
- Do not use unsupported SQLite features (e.g., ILIKE, FULL OUTER JOIN)
- Do not use aggregate functions (AVG(), SUM(), etc.) in the WHERE clause.
    → Use them in the HAVING clause after a GROUP BY.
- Use HAVING to filter on aggregate results (e.g., AVG(rating) < 3) after grouping.
- Do not use ORDER BY or LIMIT directly before or after UNION or UNION ALL.
    → Instead, wrap each SELECT in a subquery if ordering or limiting is required.
- To apply ORDER BY or LIMIT to the final result of a union, wrap the entire union in a subquery.
- Always alias aggregate columns (e.g., AVG(rating) AS avg_rating) to improve readability and usability in outer queries.
- When using nested subqueries, always use clear aliases for both the subquery and its columns.
- Avoid ambiguity in grouped queries by ensuring all non-aggregated columns are included in the GROUP BY clause.

Question:
{user_question}
"""

    def _get_answer_prompt_template(self):
        return """ 
You are a data analyst assistant.

You are given:
1. A user question.
2. The SQL query used to answer that question.
3. The result of the SQL query in table format.

Your task is to:
- Understand the user’s question.
- Analyze the table data.
- Provide a clear, human-readable answer based on the result.
- Highlight important patterns, anomalies, or insights if present.

Question:{question}
SQL Query:{sql_query}
SQL Result:{sql_query_result}

if the SQL query result is empty or None, return "No results found "
"""

    def generate_sql(self, user_question: str) -> str:
        return self.sql_chain.invoke({"user_question": user_question})

    def run_sql_query(self, query: str) -> pd.DataFrame:
        try:
            df = pd.read_sql_query(query, self.db._engine)
            return df
        except SQLAlchemyError as e:
            print("❌ SQL Execution Error:", str(e))
            return None
        except Exception as ex:
            print("❌ Unexpected Error:", str(ex))
            return None

    def format_answer(self, question: str, sql_query: str, sql_result_df: pd.DataFrame) -> str:
        formatted_result = (
            sql_result_df.to_markdown(index=False)
            if sql_result_df is not None
            else "No results found or query failed."
        )
        input_data = {
            "question": question,
            "sql_query": sql_query,
            "sql_query_result": formatted_result
        }
        return self.answer_chain.invoke(input_data)

    def answer_question(self, question: str) -> str:
        print(f"🔍 Question: {question}")
        sql_query = self.generate_sql(question)
        print(f"🧠 Generated SQL:\n{sql_query}\n")
        result_df = self.run_sql_query(sql_query)
        final_answer = self.format_answer(question, sql_query, result_df)
        return final_answer
