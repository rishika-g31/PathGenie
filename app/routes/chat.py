# app/routes/chat.py
import os
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from groq import Groq, RateLimitError, APIError # Import Groq and potential errors
from markdown import markdown

# Define the blueprint, prefix all routes in this file with /chat
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/')
@login_required
def index():
    """Renders the main chat page template."""
    # Template will be located at app/templates/chat/chat.html
    return render_template('chat/chat.html', title="Chat Bot")

@chat_bp.route('/api', methods=['POST'])
@login_required
def chat_api():
    """API endpoint to handle incoming chat messages using Groq."""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'reply': 'Please enter a message.'}), 400

    try:
        # --- Groq API Call ---
        groq_api_key = current_app.config.get('GROQ_API_KEY')
        if not groq_api_key:
            current_app.logger.error("GROQ_API_KEY not configured!")
            return jsonify({'reply': 'Chatbot configuration error.'}), 500

        client = Groq(api_key=groq_api_key)
        model_name = "llama3-8b-8192" # Or another model like mixtral-8x7b-32768
        system_prompt = "You are a helpful assistant for PathGenie, a learning path generator website. Be concise and helpful."

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=model_name,
        )

        reply = chat_completion.choices[0].message.content
        reply_html = markdown(reply)
        # --- End Groq API Call ---

    except RateLimitError:
        current_app.logger.warning("Groq rate limit exceeded.")
        reply = "The chatbot is experiencing high traffic. Please try again later."
    except APIError as e:
        current_app.logger.error(f"Groq API error: {e}")
        reply = f"An error occurred contacting the chatbot service (Code: {e.status_code}). Please try again."
    except Exception as e:
        current_app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        reply = "An unexpected error occurred. Please try again."

    return jsonify({'reply': reply_html})