from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# In-memory chat history
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_prompt = request.form['prompt']
        chat_history.append({'role': 'user', 'content': user_prompt})

        api_url = 'https://api.cerebras.ai/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer csk-kcn4jh4mkmywc54c9nvethhfkj6ncenhy4cf2kf5452ex2hk'
        }
        
        # Add a system prompt to guide the model
        system_prompt = "You are a helpful assistant that generates detailed and realistic video prompts."
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(chat_history)

        data = {
            "model": "qwen-3-235b-a22b-instruct-2507",
            "stream": False, # Changed to False for simpler response handling
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.8,
            "messages": messages
        }

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for bad status codes
            
            api_response = response.json()
            ai_message = api_response['choices'][0]['message']['content']
            
            chat_history.append({'role': 'assistant', 'content': ai_message})
            return jsonify({'history': chat_history})

        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    return render_template('index.html', history=chat_history)
