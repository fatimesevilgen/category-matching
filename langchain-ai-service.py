import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_community.chat_models import ChatOpenAI 

load_dotenv()

categories = {
    "Music": 1, "Technology": 2, "Food & Drink": 3, "Art & Culture": 4,
    "Sports": 5, "Travel": 6, "Education": 7, "Health": 8, "Business": 9, "Other": 10
}

prompt = PromptTemplate(
    template="""
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
        )

llm = ChatOpenAI(
    model=os.getenv("model"),
    openai_api_key=os.getenv("open_router_api_key"),
    base_url="https://openrouter.ai/api/v1",
)

output_parser = CommaSeparatedListOutputParser()

chain = ( prompt | llm | output_parser | RunnableLambda(lambda categories_list: [categories[c.strip()] for c in categories_list if c.strip() in categories]))

def main():
    while True:
        title = input("Etkinlik başlığı: ")
        description = input("Etkinlik açıklaması: ")

        result = chain.invoke({"title": title, "description": description})
        print(result)

if __name__ == "__main__":
    main()