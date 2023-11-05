from flask import Flask, render_template, request
from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load the BART model and tokenizer
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None  

    if request.method == 'POST':
        text = request.form.get('text')
        url = request.form.get('url')  

        if text:
            
            input_text = text
        elif url:

            input_text = summarize_url(url)

        if input_text:
            
            input_ids = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return render_template('webpage.html', summary=summary)

def summarize_url(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()

    return text

if __name__ == '__main__':
    app.run()
