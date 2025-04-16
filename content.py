from transformers import pipeline
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename='app.log')

def generate_content(prompt="GDPR compliance tips for small businesses"):
    try:
        generator = pipeline("text-generation", model="gpt2")
        content = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
        conn = sqlite3.connect("content.db")
        conn.execute("INSERT INTO posts (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()
        logging.info("Content generated and stored")
        return content
    except Exception as e:
        logging.error(f"Content generation failed: {str(e)}")
        return None
