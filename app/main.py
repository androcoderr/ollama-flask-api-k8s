import os
import re
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

app = Flask(__name__)

# Ollama API URL (örn: http://ollama:11434)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

# Job sınıfı
JOB_CLASS = """
class Job:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        
    def execute(self):
        # Base execution method
        pass
"""

def generate_code_with_ollama(prompt):
    """
    Ollama API kullanarak kod üretir
    """
    system_prompt = f"""
    Sen bir kod üretme asistanısın. Kullanıcının isteğine göre Python kodu üretmelisin.
    Kodun, aşağıda verilen Job sınıfını genişleten bir yapıda olmalı.

    {JOB_CLASS}

    Çıktını şu formatta ver:
    ### BAŞLIK: [Kısa açıklayıcı başlık]

    ```python
    [Python kodu buraya]
    ```
    """

    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={
                "model": "codellama:13b-instruct-q4_K_M",
                "prompt": f"{system_prompt}\n\nKullanıcı İsteği: {prompt}",
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.RequestException as e:
        return f"API Hatası: {str(e)}"

def parse_response(response):
    """
    LLM yanıtından başlık ve kodu ayıklar
    """
    title_match = re.search(r"### BAŞLIK: (.*?)$", response, re.MULTILINE)
    title = title_match.group(1) if title_match else "Oluşturulan Kod"

    code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
    code = code_match.group(1) if code_match else "Kod bulunamadı."

    return title, code

@app.route('/', methods=['GET', 'POST'])
def index():
    title = code = prompt = error = None

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            response = generate_code_with_ollama(prompt)
            if response.startswith("API Hatası"):
                error = response
            else:
                title, code = parse_response(response)

    return render_template('index.html', title=title, code=code, prompt=prompt, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)
