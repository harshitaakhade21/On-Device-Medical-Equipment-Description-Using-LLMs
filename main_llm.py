import ollama

def ask_openai(prompt):
    response = ollama.chat(
        model="gemma:2b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']





