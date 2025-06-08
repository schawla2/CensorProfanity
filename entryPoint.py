from openai import OpenAI
import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

def ask_gpt_to_capitalize_profanity(prompt):
    system_prompt = (
        "You are a text annotator.\n"

        "Given a sentence, return the same sentence, but:\n"
        "- If an offensive word is detected, capitalize exactly one letter in that word.\n"
        "- DO NOT capitalize more than one letter per word.\n"
        "- DO NOT capitalize anything unless the word matches the list exactly.\n"
        "- DO NOT censor or modify words that are not in the list.\n"
        "- DO NOT guess. Only act on exact matches from the provided list.\n"

        "All offensive word detection is case-insensitive. Preserve the original casing of all other text.\n"

        "Do NOT add punctuation, asterisks, or replacements. DO NOT censor words like 'bro' or 'bruh' or 'dumb'. These are not offensive.\n"

        "Only act if a word **exactly matches** one of these offensive words:\n"
        "fuck, fucker, fucking, shit, bitch, asshole, bastard, damn, dick, crap, slut, whore, pussy, rape, raped, rapist, retard\n"

        "Examples:\n"
        "- 'you're a piece of shit' → 'you're a piece of shIt'\n"
        "- 'fuck you bitch' → 'fUck you bItch'\n"
        "- 'he's such a dick' → 'he's such a dIck'\n"
        "- 'bro you're dumb' → 'bro you're dumb'  ← no change\n"
        "- 'bruhh' → 'bruhh'  ← no change\n"
        "- 'she got raped' → 'she got rAped'\n"

        "NEVER capitalize more than one letter. NEVER censor or guess.\n"

    
    )    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT API error:", e)
        return prompt

def extract_filter_chars_and_format_input(filtered_response):
    seen = set()
    filters = ''
    for c in filtered_response:
        if c.isupper() and c not in seen:
            seen.add(c)
            filters += c
    return f"{filters}|{filtered_response}" if len(filters) > 0 else filtered_response

def run_brainfuck_via_subprocess(bf_file_path: str, input_str: str) -> str:
    process = subprocess.Popen(
        ["python", "brainfuck.py", bf_file_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        output, error = process.communicate(input=input_str, timeout=30)
        if error:
            print("Brainfuck Error:", error)
        return output.strip()
    except subprocess.TimeoutExpired:
        process.kill()
        return "[Timed out]"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")

        words = user_input.lower().split()
        final_output = ""

        for word in words:
            gpt_output = ask_gpt_to_capitalize_profanity(word)
            formatted_input = extract_filter_chars_and_format_input(gpt_output)

            if '|' in formatted_input:
                output = run_brainfuck_via_subprocess("sample.bf", formatted_input)
                final_output += output + " "
            else:
                final_output += word + " "

        return jsonify({"response": final_output.strip()})
    except Exception as e:
        print("Error in /chat route:", e)
        return jsonify({"response": "[Server error]"}), 500


if __name__ == "__main__":
    app.run(debug=True)