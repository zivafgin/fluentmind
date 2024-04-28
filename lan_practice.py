from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with your actual secret key

openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('lan_practice.html', datetime=datetime.now())

@app.route('/submit', methods=['POST'])
def submit():
    if 'profile' not in session:
        return jsonify({'message': 'You need to log in first!'})

    data = request.form.to_dict()
    data_list = [data['date'], data['words'], data['wpm'], data['duration']]
    # Your logic here
    return jsonify({'message': 'Data received'})

@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms_of_service', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/get_feedback', methods=['POST'])
def get_feedback():
    try:
        text = request.form['text']
        role = request.form['role']  # 'coach', 'psychologist', or 'teacher'

        # Check word count
        word_count = len(text.split())
        if word_count > 2000:
            return jsonify({'message': 'Text exceeds 2000 word limit'}), 400
    
        # Dictionary to hold different system messages for each role
        system_prompts = {
            'coach': "You're an inspiring coach. offer concise suggestions, make it short and to the point, no longer than the amount of words the user has written",
            'psychologist': "You're a world-leading psychologist. Help the user identify patterns in their thinking and writing that could reveal blind spots or self-sabotaging behaviors. make it short and to the point, no longer than the user writing text",
            'teacher': "You're an expert as a language teacher, Your task is to provide a numerical rating between 1 to 10 on : 1)clarity, 2) Ease of understanding  3) Grammarly ONLY -  Important, Ignore all spelling mistakes, being short and to the point, giving general short sum and suggestions at the end"

        }

        # Create a system message based on the role
        system_message = {"role": "system", "content": system_prompts[role]}

        # User message stays the same, just reference the role now
        user_message = {
            "role": "user",
            "content": f"This is a conversation with a {role}. Please do the following: 1) Share your general thoughts on what I've written. 2) Depending on your role, evaluate my skills or provide feedback accordingly. {text}"
        }

        summary_response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            temperature=0.5,
            messages=[system_message, user_message]
        )
        summary = summary_response['choices'][0]['message']['content'].strip()

        return jsonify({'feedback': summary})
    except Exception as e:
        print("Error:", e)
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
