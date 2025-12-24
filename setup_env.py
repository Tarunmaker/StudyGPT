import os

def create_env():
    print("🔑 OpenAI API key setup tool 🔑")
    key = input("Paste your OpenAI API key (starts with 'sk-'): ").strip()

    if not key.startswith("sk-"):
        print("❌ Invalid key format! It should start with 'sk-'.")
        return

    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={key}\n")

    print("✅ .env file created successfully!")
    print("You can now run: python3 app.py")

if __name__ == "__main__":
    create_env()
