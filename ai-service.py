import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def classify_event(self, title: str, description: str) -> str:

        categories = {"Music": 1, "Technology": 2, "Food & Drink": 3, "Art & Culture": 4,
                      "Sports": 5, "Travel": 6, "Education": 7, "Health": 8, "Business": 9, "Other": 10}


        prompt = f"""
            Etkinlik başlığı: {title}
            Etkinlik açıklaması: {description}

            Aşağıda etkinlik kategorileri listelenmiştir:
            - Music
            - Technology
            - Food & Drink
            - Art & Culture
            - Sports
            - Travel
            - Education
            - Health
            - Business
            - Other

            Bu etkinlik birden fazla kategoriyle örtüşebilir. Lütfen etkinliğin içeriğine göre en uygun olan TÜM kategorileri belirle.

            Cevap yalnızca virgülle ayrılmış kategori adlarından oluşmalıdır.  
            Açıklama, yorum veya ekstra bilgi verme.  
            Başına "Bu etkinlik şuna aittir" gibi cümle yazma.  
            Sadece şu formatta cevap ver:

            Food & Drink, Art & Culture, Travel

            Eğer hiçbir kategoriye uygun değilse yalnızca:
            Other
            """

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost", 
            "X-Title": "EventClassifier"
        }

        data = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status() # HTTP hatalarını yakalar ve hata fırlatır

        result = response.json()
    
        content = result["choices"][0]["message"]["content"].strip()

        content = content.split(",")
        content = [categories[category.strip()] for category in content if category.strip() in categories]

        return content

def main():
    api_key = os.getenv("open_router_api_key")
    model = os.getenv("model")
    llm = LLMService(api_key, model)

    while True:
        title = input("Etkinlik başlığı: ")
        description = input("Etkinlik açıklaması: ")

        category = llm.classify_event(title, description)
        print(category)


if __name__ == "__main__":
    main()