import requests
import logging
import json

API_URL = 'https://api.perplexity.ai/chat/completions'
API_KEY = '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'

logging.basicConfig(level=logging.INFO)

def query_ai(input_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": f'Ты топовый финансовый директор с опытом работы более 10 лет с финансами и бухгалтерией. Ответь на мои запросы: {input_text}'
            }
        ],
        "max_tokens": 123,
        "temperature": 0.2,
        "top_p": 0.9,
        "search_domain_filter": None,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": None,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": None
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"AI response received: {response.json()}")
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка подключения: {e}")
        return 'Ошибка подключения'
