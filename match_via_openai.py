import openai

# Set your OpenAI API key
openai.api_key = "sk-proj-3Gj8MtJdQqdfEvxGCRoDT3BlbkFJBZb8Fex5I0PZFXpy8dbN"

def chat_with_model(messages):
    """Sends a message to the OpenAI Chat Completion API and returns the response."""

    response = openai.chat.completions.create(
        model="gpt-4o",  # Or another suitable model
        messages=messages
    )

    return response.choices[0].message.content

def main(search_article,articles):
    """Starts an interactive chat session with the model."""

    messages = [
        {"role": "system", "content": f"""You are a helpful assistant and your task is to read all articles from {articles} and compare with '{search_article}', then find most matched article.
        """}
    ]

    messages.append({"role": "user", "content": "Do not give any wrong match. If you found more then one match then give only top two results."})

    response = chat_with_model(messages)
    print("Assistant:", response)

    return response