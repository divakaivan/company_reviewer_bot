import streamlit as st
from openai import OpenAI

st.title("기업 평가 챗봇")

# Sidebar for API key input
api_key = st.sidebar.text_input("OpenAI API 키:", type="password")

if api_key:

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def generate_response(messages):
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:movie-reviewer-v2:AI7hIoND",
            messages=[
                {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": "Your task is to summarize. You are a helpful assistant who will help me evaluate Korean company's reviews. Up to 50 reviews are provided for each company in the \"Input\". Analyze the reviews by each 12 dimension described below and return a dimension-specific rating (1-10) and a summary description. The 12 dimensions to summarize company culture are as follows:\n1) Strategic Direction and Intent: Evaluate the long-term goals and direction of the organization.\n2) Goals and Objectives: Evaluate the specific goals set by the organization and the plan to achieve them.\n3) Vision: Evaluate the vision for the future of the organization and the extent to which it is shared with its members.\n4) Core Values: Evaluate the shared values of the organization and the extent to which they are internalized by its members.\n5) Agreement: Evaluate the level of agreement in the decision-making process within the organization.\n6) Coordination and Integration: Evaluate the level of consistency and integration of systems and processes within the organization.\n7) Team Orientation: Evaluate the degree of teamwork and cooperation.\n8) Capability Development: Evaluate the extent to which the organization supports the development and growth of the capabilities of its members.\n9) Empowerment: Evaluates the extent to which members are empowered and given autonomy.\n10) Creating Change: Evaluates how effectively the organization manages change and innovation.\n11) Customer Focus: Evaluates how well it responds to customer needs and expectations.\n12) Organizational Learning: Evaluates the extent to which the organization learns and shares knowledge.\n\nTo do the task, please perform the following steps:\n1. First, for each review, determine which dimension it is related to.\n2. Assign a dimension-specific rating (1-10) to each review.\n3. Aggregate the ratings of each individual review by dimension to generate a final dimension-specific rating and summary for the movie.\n4. Translate the final dimension-specific summary for each movie into Korean and return it with dimension-specific rating (1-10).\n"
                    }
                ]
                },
                messages
            ],
            temperature=0,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )
        
        return response.choices[0].message.content

    # User input
    user_input = st.text_input("You:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        assistant_response = generate_response({"role": "user", "content": user_input})
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        for message in st.session_state.messages[1:]:
            if message["role"] == "user":
                # st.markdown(f"**You:** {message['content']}")
                pass
            else:
                st.markdown(f"**Assistant:** {message['content']}")

else:
    st.warning("OpenAI API 키를 입력해 주세요.")
