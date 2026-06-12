from flask import Blueprint, render_template, request, jsonify
from app.models import Deal, ICQuestion

ic_bp = Blueprint('ic', __name__)

@ic_bp.route('/')
def ic_select():
    deals = Deal.query.all()
    return render_template('ic_select.html', deals=deals)

@ic_bp.route('/<int:deal_id>')
def ic_simulator(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    questions = ICQuestion.query.filter_by(deal_id=deal_id).all()
    return render_template('ic_simulator.html', deal=deal, questions=questions)

@ic_bp.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    answer = data.get('answer', '').strip().lower()
    question = ICQuestion.query.get(question_id)
    if not question:
        return jsonify({'correct': False, 'message': 'Question not found.'})
    if question.answer.lower() in answer:
        return jsonify({'correct': True, 'message': 'You survived this round. Next!'})
    else:
        return jsonify({'correct': False, 'message': f'Wrong. The correct answer was: {question.answer}'})
