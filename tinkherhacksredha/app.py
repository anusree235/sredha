from flask import Flask, render_template, request, jsonify
from together import Together

app = Flask(__name__)

# Initialize the Together client
client = Together(api_key='ffb32b9b4eb0e3996bd99e5a8b3e44b4c7f6721c070841cd4053c1cb61246c42')

@app.route('/')
def home():
    return render_template('index.html')  # Ensure this matches the template name

@app.route('/check-grammar', methods=['POST'])
def check_grammar():
    try:
        data = request.json
        
        # Get the input text from the request
        if 'inputText' not in data or not data['inputText'].strip():
            return jsonify({'error': 'Please enter some text to check.'}), 400

        input_text = data['inputText']

        # Create a prompt for grammar checking
        prompt = f"Please correct the following text for grammar and spelling:\n\n{input_text}\n\nCorrected Text:"

        # Generate corrected text using Together API
        messages = [{"role": "user", "content": prompt}]
        
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=messages
        )

        if completion and hasattr(completion, 'choices') and len(completion.choices) > 0:
            corrected_text = completion.choices[0].message.content.strip()
            return jsonify({'corrected_text': corrected_text})
        
        return jsonify({'error': 'No corrections found. Please try again.'}), 500

    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': 'An error occurred while checking grammar.'}), 500

if __name__ == '__main__':
    app.run(debug=True)