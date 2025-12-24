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
