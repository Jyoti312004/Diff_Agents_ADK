import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        I like to play Pickleball, Disc Golf, and Tennis.
        My favorite food is Mexican.
        My favorite TV show is Game of Thrones.
        Loves it when people like and subscribe to his YouTube channel.
    """,
}

# Create a NEW session
APP_NAME = "Brandon Bot"
USER_ID = "brandon_hancock"
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

# List of questions
questions = [
    "What is Brandon's favorite TV show?",
    "What food does Brandon like?",
    "What are Brandon’s favorite sports?",
]

# Get session and prepare message history
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

if "message_history" not in session.state:
    session.state["message_history"] = []

# Ask each question
for question in questions:
    print(f"\n🤔 Asking: {question}")

    # Create content message
    new_message = types.Content(
        role="user", parts=[types.Part(text=question)]
    )

    # Save user message
    session.state["message_history"].append({
        "role": "user",
        "text": question
    })

    # Run the agent
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = event.content.parts[0].text
                print(f"🎯 Answer: {response_text}")

                # Save assistant response
                session.state["message_history"].append({
                    "role": "assistant",
                    "text": response_text
                })

# Show session info
print("\n==== 🗂 Final Session State ====")
for key, value in session.state.items():
    if key != "message_history":
        print(f"{key}: {value.strip() if isinstance(value, str) else value}")

print("\n==== 📝 Message History ====")
for msg in session.state["message_history"]:
    print(f"{msg['role'].capitalize()}: {msg['text']}")
