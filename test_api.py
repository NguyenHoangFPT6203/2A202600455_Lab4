import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Khong tim thay OPENAI_API_KEY trong .env")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
    response = llm.invoke("Tra loi ngan gon: ket noi API da thanh cong.")
    print(response.content)


if __name__ == "__main__":
    main()
