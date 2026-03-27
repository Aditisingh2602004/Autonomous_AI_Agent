from dotenv import load_dotenv
from agent import build_agent

load_dotenv(override=True)


def main():
    agent = build_agent()

    task = """
Read instructions from ./instructions/platform.md

Then:

1. Login to frontend UI using login_frontend
2. Ensure login is successful

IMPORTANT:
- Do NOT call backend login
- Do NOT repeat steps
- Stop after success

Return FINAL ANSWER.
""".strip()

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": task}, #task is called here 
            ]
        },
        config={"recursion_limit": 5},
    )

    print("\n✅ FINAL RESULT: Login Successful\n")

    
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            print(msg.content)
            break


if __name__ == "__main__": #runs only when file is executed.
    main()
