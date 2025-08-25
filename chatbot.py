import streamlit as st
from exercise_info import exercise_info

# Generate a formatted response based on user input
def get_response(user_input: str):
    user_input = user_input.strip().lower()

    # Check if the input matches any known exercise name
    if user_input in exercise_info:
        info = exercise_info[user_input]
        return (
            f"### {user_input.title()}\n\n"
            f"**✅ Correct Form:**\n{info['form']}\n\n"
            f"**⚠️ Common Mistakes:**\n{info['common_mistakes']}\n\n"
            f"**💪 Benefits:**\n{info['benefits']}"
        )
    else:
        return (
            "🤖 Sorry, I couldn't find information on that exercise.\n"
            "Try something like: `barbell biceps curl`, `squat`, `push up`, or `shoulder press`."
        )

# Chatbot Streamlit UI
def run_chatbot():
    st.title("🏋️ FitX AI Chatbot")
    st.markdown("Ask me about an exercise to get tips on form, mistakes to avoid, and benefits.")

    # Chat history (session state)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Text input
    user_input = st.text_input("Type your question here...")

    if user_input:
        response = get_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("FitX Bot", response))

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧍 {sender}:** {message}")
        else:
            st.markdown(f"**🤖 {sender}:**\n\n{message}")

# If run directly
if __name__ == "__main__":
    run_chatbot()
