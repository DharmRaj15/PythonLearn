import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_question_confidence(rating, remarks):
    # ... (same confidence calculation logic as before) ...
    if not rating or not remarks:
        return rating # Neutral confidence if no rating or remark.

    # Example keyword-based confidence logic (can be customized)
    positive_keywords = ["excellent", "good", "satisfied", "positive", "strong", "effective","well","meet expectations","great","awesome","reliably","dependable","superb","fantastic","outstanding","exceptional","wonderful","amazing","impressive","satisfactory","pleased","happy","like","love","recommend","best","better","improved","super","terrific","fabulous","marvelous","brilliant","perfect","ideal","superior","quality","high","top","favorite","nice","fine","cool","fun","enjoy","beautiful","attractive","appealing","good-looking","gorgeous","handsome","pretty","cute","charming","lovely","stunning","fascinating","delightful","wonderful","amazing","awesome","excellent","fantastic","great","terrific","superb","outstanding","impressive","exceptional","brilliant","perfect","ideal","superior","quality","high","top","favorite","nice","fine","cool","fun","enjoy","beautiful","attractive","appealing","good-looking","gorgeous","handsome","pretty","cute","charming","lovely","stunning","fascinating","delightful","wonderful","amazing","awesome","excellent","fantastic","great","terrific","superb","outstanding","impressive","exceptional","brilliant","perfect","ideal","superior","quality","high","top","favorite","nice","fine","cool","fun","enjoy","beautiful","attractive","appealing","good-looking","gorgeous","handsome","pretty","cute","charming","lovely","stunning","fascinating","delightful","wonderful","amazing","awesome","excellent","fantastic","great","terrific","superb","outstanding","impressive","exceptional","brilliant","perfect","ideal","superior","quality","high","top","favorite","nice","fine","cool","fun","enjoy","beautiful","attractive","appealing","good-looking","gorgeous","handsome","pretty","cute","charming","lovely","stunning","fascinating","delightful","wonderful","amazing","awesome","excellent","fantastic","great","terrific","superb","outstanding","impressive","exceptional","brilliant","perfect","ideal","superior","quality","high","top","favorite","nice","fine","cool","fun","enjoy","beautiful"]
    negative_keywords = ["poor", "bad", "unsatisfied", "negative", "weak", "ineffective","terrible","broke","not meet expectations","not good","not satisfied","not happy","not like","not love","not recommend","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory","disappointed","unhappy","unlike","dislike","hate","worst","worse","declined","inferior","low","bad","poor","negative","weak","ineffective","unsatisfactory"]

    positive_count = sum(1 for keyword in positive_keywords if keyword in remarks)
    negative_count = sum(1 for keyword in negative_keywords if keyword in remarks)

    if rating >= 4 and negative_count > 0:
      return 1 #If high rating but negative remarks, low rating.
    elif rating <= 2 and positive_count > 0:
      return 5 #If low rating but positive remarks, high rating.
    elif rating >= 4 and positive_count > 0:
      return rating #High rating, positive remarks.
    elif rating <= 2 and negative_count > 0:
      return rating #low rating, negative remarks.
    elif positive_count > negative_count:
        return max(rating,3) # if more positive keywords, return rating or 3, whichever is higher
    elif negative_count > positive_count:
        return min(rating,3) #if more negative keywords, return rating or 3, whichever is lower
    else:
        return rating # Neutral confidence if no strong keywords.

def assess_rating_confidence(assessment_data):
    # ... (same assessment logic as before) ...
    questions = assessment_data.get("questions", [])
    total_rating = 0
    num_questions = len(questions)
    misaligned_questions = []

    for question in questions:
        rating = question.get("rating")
        remarks = question.get("remarks", "").lower()
        question_text = question.get("question", "")

        calculated_rating = calculate_question_confidence(rating, remarks)
        total_rating += calculated_rating

        if calculated_rating != rating:  # Identify misalignments
            misaligned_questions.append({
                "question": question_text,
                "original_rating": rating,
                "remarks": remarks,
                "calculated_rating": calculated_rating
            })
    actual_rating = total_rating / num_questions if num_questions > 0 else 0
    overall_rating = total_rating / num_questions if num_questions > 0 else 0
    

    return {
        "overall_rating": overall_rating,
        "actual_rating": actual_rating,
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