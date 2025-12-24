import openai

# 👇 Apni OpenAI API key yahan daalo
openai.api_key = "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"

# Simple test query
try:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello! How are you?"}
        ]
    )

    print("\n✅ AI Response:\n")
    print(resp.choices[0].message["content"])

except Exception as e:
    print("\n❌ Error:", e)
