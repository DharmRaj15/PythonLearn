import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_question_confidence(rating, remarks):
    # ... (same confidence calculation logic as before) ...
    if not rating or not remarks:
        return 0.5 # Neutral confidence if no rating or remark.

    # Example keyword-based confidence logic (can be customized)
    positive_keywords = ["excellent", "good", "satisfied", "positive", "strong", "effective"]
    negative_keywords = ["poor", "bad", "unsatisfied", "negative", "weak", "ineffective","terrible","broke"]

    positive_count = sum(1 for keyword in positive_keywords if keyword in remarks)
    negative_count = sum(1 for keyword in negative_keywords if keyword in remarks)

    if rating >= 4 and negative_count > 0:
      return 0.25 #If high rating but negative remarks, low confidence.
    elif rating <= 2 and positive_count > 0:
      return 0.25 #If low rating but positive remarks, low confidence.
    elif rating >= 4 and positive_count > 0:
      return 0.9 #High rating, positive remarks.
    elif rating <= 2 and negative_count > 0:
      return 0.9 #low rating, negative remarks.
    elif positive_count > negative_count:
        return 0.75
    elif negative_count > positive_count:
        return 0.25
    else:
        return 0.5 # Neutral confidence if no strong keywords

def assess_rating_confidence(assessment_data):
    # ... (same assessment logic as before) ...
    questions = assessment_data.get("questions", [])
    total_confidence = 0
    num_questions = len(questions)
    misaligned_questions = []

    for question in questions:
        rating = question.get("rating")
        remarks = question.get("remarks", "").lower()
        question_text = question.get("question", "")

        confidence = calculate_question_confidence(rating, remarks)
        total_confidence += confidence

        if confidence < 0.5:  # Arbitrary threshold to indicate misalignment
            misaligned_questions.append({
                "question": question_text,
                "rating": rating,
                "remarks": remarks,
                "confidence": confidence
            })

    overall_confidence = total_confidence / num_questions if num_questions > 0 else 1.0

    return {
        "overall_confidence": overall_confidence,
        "misaligned_questions": misaligned_questions
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            json_data = request.files['json_file'].read()
            assessment_data = json.loads(json_data)
            result = assess_rating_confidence(assessment_data)

        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            result = {"error": f"Error processing JSON: {str(e)}"}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)