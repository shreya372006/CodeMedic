import os
import json
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

SYSTEM_PROMPT = """You are CodeMedic, an expert code analysis AI.
Your job is to analyse code and find ALL bugs, errors, and issues.

You must respond ONLY with a valid JSON object in this exact format:
{
    "bugs": [
        {
            "line": <line number as integer>,
            "type": <one of: "syntax", "logical", "runtime", "warning", "style">,
            "description": <clear explanation of what is wrong>,
            "fix": <specific suggestion to fix the bug>
        }
    ]
}

Rules:
- Find EVERY single bug, error, warning, and issue in the code
- line must be the exact line number where the bug occurs
- type must be exactly one of: syntax, logical, runtime, warning, style
- description must clearly explain what is wrong and why
- fix must give a specific actionable fix
- If no bugs found, return {"bugs": []}
- Return ONLY the JSON object, no other text, no markdown, no explanation
"""


def analyse_code(code, language):
    language_names = {
        'python': 'Python',
        'c': 'C',
        'cpp': 'C++',
        'java': 'Java',
    }

    lang_name = language_names.get(language, language)
    numbered_code = add_line_numbers(code)

    user_message = f"""Analyse this {lang_name} code and find ALL bugs:

{numbered_code}

Return ONLY a JSON object with all bugs found."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=2000,
        )

        raw = response.choices[0].message.content.strip()
        raw = clean_json_response(raw)
        data = json.loads(raw)

        bugs = data.get('bugs', [])

        validated_bugs = []
        for bug in bugs:
            if all(k in bug for k in ['line', 'type', 'description', 'fix']):
                bug['type'] = validate_bug_type(bug['type'])
                bug['line'] = int(bug['line'])
                validated_bugs.append(bug)

        return validated_bugs, None

    except json.JSONDecodeError as e:
        return [], f"AI response parsing error: {str(e)}"
    except Exception as e:
        return [], f"Analysis error: {str(e)}"


def add_line_numbers(code):
    lines = code.split('\n')
    numbered = []
    for i, line in enumerate(lines, 1):
        numbered.append(f"{i:3} | {line}")
    return '\n'.join(numbered)


def clean_json_response(raw):
    if '```json' in raw:
        raw = raw.split('```json')[1].split('```')[0].strip()
    elif '```' in raw:
        raw = raw.split('```')[1].split('```')[0].strip()

    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1:
        raw = raw[start:end+1]

    raw = raw.replace('\n', ' ')
    raw = raw.replace('\r', ' ')
    raw = ' '.join(raw.split())

    return raw


def validate_bug_type(bug_type):
    valid_types = ['syntax', 'logical', 'runtime', 'warning', 'style']
    bug_type = bug_type.lower().strip()
    if bug_type in valid_types:
        return bug_type
    return 'warning'