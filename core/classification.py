from openai import OpenAI
import json
import yake


def classify_message(message: str, open_ai_client: OpenAI, model: str) -> dict:
    chat = [
        {
            "role": "system",
            "content": """"You are a support message classifier. 
Your task is to classify messages into one of the following categories:

1. **Assistance Request** – When a user asks for support with a specific problem.  
2. **Error Report** – When a user reports a malfunction or bug.  
3. **Information Request** – When a user asks for details about a service, product, or functionality.  
4. **Other** – Any message that does not fit into the above categories.  

### Output Rules:
- You must return **only** a JSON object **without any additional text**.  
- Do not include introductions, explanations, or any other information in your output.  
- The JSON format must be exactly one of the following:

- For an assistance request:
    { "category": "assistance" }

- For an error report:
    { "category": "error" }

- For an information request:
    { "category": "information" }

- For any other category:
    { "category": "other" }

Example of a correct output:

{ "category": "error" }

**IMPORTANT:** Return only the JSON, with no additional text, explanations, or extra information."
""",
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    print("Classifiyng the message...")

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "categorization",
            "schema": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["assistance", "error", "information", "other"],
                    }
                },
                "required": ["category"],
            },
        },
    }

    response = open_ai_client.chat.completions.create(
        model=model,
        messages=chat,
        response_format=schema,
    )

    response_content = response.choices[0].message.content

    response = json.loads(response_content)

    print(json.dumps(response, indent=2))

    return response


def extract_keyword_llm(message: str, open_ai_client: OpenAI, model: str) -> dict:
    chat = [
        {
            "role": "system",
            "content": """You are a keyword extractor. 
Your task is to extract the most relevant keyword from a given message. 
The keyword should be a single word or a short phrase that best represents the main topic or subject of the message.
""",
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    print("Extracting the keywords...")

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "keyword_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                    }
                },
                "required": ["keywords"],
            },
        },
    }

    response = open_ai_client.chat.completions.create(
        model=model,
        messages=chat,
        response_format=schema,
    )

    response_content = response.choices[0].message.content

    response = json.loads(response_content)

    print(json.dumps(response, indent=2))

    return response


def extract_keyword(message: str) -> dict:
    kw_extractor = yake.KeywordExtractor(lan="it", n=4, dedupLim=0.5, top=5)

    keywords = kw_extractor.extract_keywords(message)

    print(keywords)

    return keywords
