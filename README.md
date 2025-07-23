# Smart-Data-Retrieva 🧠📊

A smart system that analyzes customer review data from databases and provides insights using SQL-based queries, NLP models, and an interactive interface.

---

## 🔧 Features

- 🗃️ Import and store customer reviews in a SQLite database  
- 🧠 Analyze reviews using sentiment analysis & NLP  
- 🤖 Use an AI SQL agent (`sql_agent.py`) to run natural language queries  
- 📈 Interactive dashboard via `app.py`  
- 📦 Well-organized codebase and Jupyter notebook for model experimentation

---

## 📁 Project Structure

```
├── app.py                         # Main app (Streamlit or Flask)
├── model.ipynb                    # Jupyter notebook for NLP model
├── sql_agent.py                   # Converts user queries to SQL
├── reviews.db                     # Sample review database
├── shopify_reviews.db            # Shopify review database
├── sample_customer_reviews_raw   # Sample raw customer data
├── requirement.txt               # Python dependencies
└── .gitignore                    # Files to be ignored by Git
```

---

## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/Mayuresh-Bairagi/Smart-Data-Retrieva.git
cd Smart-Data-Retrieva
```

2. **Install required packages**
```bash
pip install -r requirement.txt
```

3. **Run the app**
```bash
python app.py
```

---

## 📊 Example Use Cases

- Ask questions like:
  - “Show all negative reviews from the last month”
  - “Which product has the most 5-star reviews?”
  - “Give me the average sentiment per product”

- Get SQL queries generated automatically from natural language  
- Visualize review sentiment trends and keyword clouds

---

## 🧠 Tech Stack

- Python
- Streamlit / Flask
- SQLite
- pandas, NumPy
- NLP libraries (NLTK, spaCy, or transformers)
- SQLAlchemy

---

## 👨‍💻 Author

**Mayuresh Bairagi**  
📧 mayureshbairagi2004@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/mayuresh-bairagi)  
🔗 [GitHub](https://github.com/Mayuresh-Bairagi)

---

## 📌 License

This project is open-source and free to use under the [MIT License](LICENSE).

---

Feel free to contribute, fork, or raise an issue if you have ideas to improve the project!
