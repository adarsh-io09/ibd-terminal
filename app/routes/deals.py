from flask import Blueprint, render_template, request, jsonify
from app.models import Deal
from app.engine import accretion_dilution, synergy_realism_meter, deal_risk_analyzer, football_field_data

deals_bp = Blueprint('deals', __name__)

@deals_bp.route('/')
def deal_list():
    deals = Deal.query.all()
    return render_template('deal_list.html', deals=deals)

@deals_bp.route('/<int:deal_id>')
def deal_detail(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    acc_dil = accretion_dilution(deal.acquirer, deal.target,
                                 deal.premium_pct, deal.cash_pct,
                                 deal.synergy_cost, deal.synergy_rev)
    # Check if engine returned an error (shouldn't happen with the new engine, but safeguard)
    if 'error' in acc_dil:
        return render_template('deal.html', deal=deal,
                               acc_dil=None,
                               realism=None,
                               risk=None,
                               football=None,
                               error=acc_dil['error'])

    realism = synergy_realism_meter(deal.synergy_cost, deal.synergy_rev)
    risk = deal_risk_analyzer(deal)
    football = football_field_data(deal.target) if deal.target else None
    return render_template('deal.html', deal=deal,
                           acc_dil=acc_dil,
                           realism=realism,
                           risk=risk,
                           football=football,
                           error=None)

@deals_bp.route('/api/accretion', methods=['POST'])
def api_accretion():
    data = request.get_json()
    premium = data.get('premium', 30)
    cash = data.get('cash', 50)
    cost_syn = data.get('cost_syn', 250)
    rev_syn = data.get('rev_syn', 100)
    deal = Deal.query.first()
    if not deal:
        return jsonify({'error': 'No deals in DB'})
    result = accretion_dilution(deal.acquirer, deal.target,
                               premium, cash, cost_syn, rev_syn)
    return jsonify(result)