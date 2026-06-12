import os

# Base directory is where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define folder structure and file contents
FILES = {
    "run.py": """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
""",
    "seed_data.py": """from app import create_app
from app.extensions import db
from app.models import Deal, ICQuestion, TransactionLog

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    deals = [
        Deal(
            project_name='Project Titanium',
            acquirer='JPM',
            target='SQ',
            deal_value=5800,
            enterprise_value=6200,
            equity_value=5800,
            ebitda_multiple=14.5,
            premium_pct=28,
            cash_pct=60,
            stock_pct=40,
            debt_pct=0,
            status='Pending',
            synergy_cost=180,
            synergy_rev=70,
            synergy_realism=65,
            risk_score=38,
            commentary='Bid getting spicy. Street leverage spike se khush nahi hoga.'
        ),
        Deal(
            project_name='Project Nightshade',
            acquirer='PFE',
            target='BNTX',
            deal_value=4200,
            enterprise_value=4500,
            equity_value=4200,
            ebitda_multiple=12.2,
            premium_pct=35,
            cash_pct=40,
            stock_pct=60,
            debt_pct=0,
            status='Rumored',
            synergy_cost=250,
            synergy_rev=110,
            synergy_realism=42,
            risk_score=65,
            commentary='Mgmt adjusted EBITDA kaafi aggressive lag raha hai. Hostile whispers.'
        ),
        Deal(
            project_name='Project Griffin',
            acquirer='XOM',
            target='CVX',
            deal_value=22000,
            enterprise_value=23500,
            equity_value=22000,
            ebitda_multiple=9.8,
            premium_pct=18,
            cash_pct=30,
            stock_pct=70,
            debt_pct=0,
            status='Closed',
            synergy_cost=1200,
            synergy_rev=400,
            synergy_realism=78,
            risk_score=22,
            commentary='Clean mega-merger. Sponsor-backed angle lag raha hai solid.'
        ),
        Deal(
            project_name='Project Falcon',
            acquirer='MSFT',
            target='ATVI',
            deal_value=68700,
            enterprise_value=75000,
            equity_value=68700,
            ebitda_multiple=18.3,
            premium_pct=22,
            cash_pct=100,
            stock_pct=0,
            debt_pct=0,
            status='Closed',
            synergy_cost=800,
            synergy_rev=300,
            synergy_realism=55,
            risk_score=45,
            commentary='Antitrust gauntlet completed. Data room abhi incomplete tha initially.'
        ),
        Deal(
            project_name='Project K2',
            acquirer='BAC',
            target='Regional Bank',
            deal_value=1900,
            enterprise_value=2100,
            equity_value=1900,
            ebitda_multiple=11.5,
            premium_pct=40,
            cash_pct=50,
            stock_pct=50,
            debt_pct=0,
            status='Pending',
            synergy_cost=320,
            synergy_rev=90,
            synergy_realism=28,
            risk_score=72,
            commentary='Deal ka synergy case kaafi stretched lag raha hai. Dumpster fire candidate.'
        )
    ]

    db.session.add_all(deals)
    db.session.commit()

    for deal in deals[:2]:
        questions = [
            ICQuestion(deal_id=deal.id,
                       question=f'Why are we paying {deal.ebitda_multiple}x EBITDA?',
                       answer='Because the target has high growth and strategic synergies that justify a premium.',
                       category='MD'),
            ICQuestion(deal_id=deal.id,
                       question='Walk me through downside protection.',
                       answer='We have a collar agreement, break-up fee, and the target’s intrinsic value is supported by hard assets.',
                       category='PE'),
            ICQuestion(deal_id=deal.id,
                       question='Can this delever fast enough?',
                       answer='Yes, free cash flow generation will reduce leverage to 2.5x within 3 years.',
                       category='Credit'),
            ICQuestion(deal_id=deal.id,
                       question='How does the market react to the premium?',
                       answer='Based on precedents, the premium is within the 25-35% range; we expect neutral to slightly negative initial reaction.',
                       category='MD'),
            ICQuestion(deal_id=deal.id,
                       question='What’s the synergy payback period?',
                       answer='Under conservative assumptions, full cost synergies are realized by year 3, revenue synergies by year 4.',
                       category='PE')
        ]
        db.session.add_all(questions)

    logs = [
        TransactionLog(message='🔥 Project Titanium LOI sent.', deal_id=1),
        TransactionLog(message='💬 Sponsor pushing tighter exclusivity on Nightshade.', deal_id=2),
        TransactionLog(message='✔️ Griffin deal closed – champagne popped.', deal_id=3),
        TransactionLog(message='📉 Market reaction to Falcon premium: acquirer down 1.2%.', deal_id=4),
        TransactionLog(message='🚨 K2 due diligence finds two major customer concentration red flags.', deal_id=5)
    ]
    db.session.add_all(logs)
    db.session.commit()

    print("Database seeded with 5 deals, IC questions, and transaction logs.")
""",
    "requirements.txt": """Flask==3.1.0
Flask-SQLAlchemy==3.1.1
pandas==2.2.3
numpy==1.26.4
yfinance==0.2.43
plotly==5.24.1
requests==2.31.0
""",
    "app/__init__.py": """from flask import Flask
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.routes.dashboard import dashboard_bp
    from app.routes.deals import deals_bp
    from app.routes.ic import ic_bp
    from app.routes.data_room import data_room_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(deals_bp, url_prefix='/deals')
    app.register_blueprint(ic_bp, url_prefix='/ic')
    app.register_blueprint(data_room_bp, url_prefix='/vdr')

    with app.app_context():
        db.create_all()

    return app
""",
    "app/config.py": """import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'change-this-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'manda.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
""",
    "app/extensions.py": """from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
""",
    "app/models.py": """from app.extensions import db
from datetime import datetime

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    acquirer = db.Column(db.String(100), nullable=False)
    target = db.Column(db.String(100), nullable=False)
    deal_value = db.Column(db.Float)
    enterprise_value = db.Column(db.Float)
    equity_value = db.Column(db.Float)
    ebitda_multiple = db.Column(db.Float)
    premium_pct = db.Column(db.Float)
    cash_pct = db.Column(db.Float)
    stock_pct = db.Column(db.Float)
    debt_pct = db.Column(db.Float)
    status = db.Column(db.String(20))
    synergy_cost = db.Column(db.Float)
    synergy_rev = db.Column(db.Float)
    synergy_realism = db.Column(db.Integer)
    risk_score = db.Column(db.Float)
    commentary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ICQuestion(db.Model):
    __tablename__ = 'ic_questions'
    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deals.id'))
    question = db.Column(db.String(300))
    answer = db.Column(db.String(300))
    category = db.Column(db.String(50))

class TransactionLog(db.Model):
    __tablename__ = 'transaction_log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String(200))
    deal_id = db.Column(db.Integer, db.ForeignKey('deals.id'), nullable=True)
""",
    "app/engine.py": """import numpy as np
import pandas as pd
import yfinance as yf
from functools import lru_cache
import time

@lru_cache(maxsize=32)
def _fetch_ticker_data(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        time.sleep(0.2)
        return {
            'name': info.get('shortName', ticker),
            'price': info.get('currentPrice', None),
            'market_cap': info.get('marketCap', None),
            'ebitda': info.get('ebitda', None),
            'net_income': info.get('netIncomeToCommon', None),
            'shares': info.get('sharesOutstanding', None),
            'pe_ratio': info.get('trailingPE', None),
            'ev_to_ebitda': info.get('enterpriseToEbitda', None),
            'sector': info.get('sector', 'Unknown')
        }
    except Exception as e:
        print(f"Failed to fetch {ticker}: {e}")
        return None

def get_peer_comps(ticker):
    data = _fetch_ticker_data(ticker)
    if not data:
        return []
    sector = data['sector']
    comp_map = {
        'Technology': ['MSFT', 'GOOGL', 'ORCL'],
        'Financial Services': ['BAC', 'C', 'WFC'],
        'Healthcare': ['JNJ', 'PFE', 'MRK'],
        'Energy': ['XOM', 'CVX', 'COP'],
        'Unknown': ['AAPL', 'MSFT', 'GOOGL']
    }
    peers = comp_map.get(sector, ['AAPL', 'MSFT', 'GOOGL'])
    comps_data = []
    for p in peers:
        d = _fetch_ticker_data(p)
        if d:
            comps_data.append(d)
    return comps_data

def accretion_dilution(acq_ticker, tgt_ticker, premium_pct, cash_pct, synergy_cost, synergy_rev):
    acq = _fetch_ticker_data(acq_ticker)
    tgt = _fetch_ticker_data(tgt_ticker)
    if not acq or not tgt:
        return {'error': 'Ticker not found'}

    acq_net_income = (acq['net_income'] or 1000e6) / 1e6
    tgt_net_income = (tgt['net_income'] or 200e6) / 1e6
    acq_shares = (acq['shares'] or 500e6) / 1e6
    tgt_shares = (tgt['shares'] or 100e6) / 1e6
    acq_price = acq['price'] or 100
    tgt_price = tgt['price'] or 50

    offer_price = tgt_price * (1 + premium_pct / 100)
    deal_value = offer_price * tgt_shares

    cash_used = deal_value * (cash_pct / 100)
    stock_used = deal_value * (1 - cash_pct / 100)
    new_shares = stock_used / acq_price
    pf_shares = acq_shares + new_shares
    interest = cash_used * 0.06 * (1 - 0.21)
    total_synergies = synergy_cost + synergy_rev
    pf_net_income = acq_net_income + tgt_net_income + total_synergies - interest
    acq_eps = acq_net_income / acq_shares
    pf_eps = pf_net_income / pf_shares
    acc_dil_pct = (pf_eps / acq_eps - 1) * 100

    prems = [10, 20, 30, 40, 50]
    cashes = [0, 25, 50, 75, 100]
    sens = []
    for p in prems:
        row = []
        for c in cashes:
            op = tgt_price * (1 + p/100)
            dv = op * tgt_shares
            cu = dv * (c/100)
            su = dv * (1 - c/100)
            ns = su / acq_price
            pfs = acq_shares + ns
            int_cost = cu * 0.06 * 0.79
            pfn = acq_net_income + tgt_net_income + total_synergies - int_cost
            eps = pfn / pfs
            ad = (eps / acq_eps - 1) * 100
            row.append(round(ad, 2))
        sens.append(row)

    return {
        'acq_eps': round(acq_eps, 2),
        'pf_eps': round(pf_eps, 2),
        'acc_dil_pct': round(acc_dil_pct, 2),
        'deal_value': round(deal_value, 0),
        'offer_price': round(offer_price, 2),
        'sensitivity': sens,
        'premiums': prems,
        'cash_pcts': cashes,
        'acq_name': acq['name'],
        'tgt_name': tgt['name']
    }

def synergy_realism_meter(cost_syn, rev_syn, industry='general'):
    base_score = 50
    if cost_syn > 200:
        base_score -= 20
    if rev_syn > 150:
        base_score -= 25
    if industry == 'Technology':
        base_score -= 10
    base_score += np.random.randint(-5, 5)
    base_score = max(0, min(100, base_score))

    if base_score >= 70:
        level = 'Conservative (Bankable)'
        comment = 'Mgmt presented a realistic plan. Synergies seem achievable.'
    elif base_score >= 40:
        level = 'Achievable with Execution Risk'
        comment = 'Street may buy it, but watch the integration timeline.'
    elif base_score >= 20:
        level = 'Aggressive – "Banker Hopium"'
        comment = 'Mgmt adjusted EBITDA kaafi aggressive lag raha hai. Expect pushback.'
    else:
        level = 'Pure Banker Hopium'
        comment = 'Deal ka synergy case kaafi stretched lag raha hai. Underwrite carefully.'

    return {
        'score': base_score,
        'level': level,
        'comment': comment
    }

def deal_risk_analyzer(deal):
    integration = 30
    leverage = 20
    antitrust = 10
    cultural = 20

    if deal.cash_pct > 70:
        leverage += 30
    if deal.deal_value > 10000:
        antitrust += 25
        integration += 15
    if 'Tech' in deal.acquirer or 'Tech' in deal.target:
        cultural += 15
    if deal.premium_pct > 40:
        integration += 10

    total_risk = (integration * 0.4) + (leverage * 0.3) + (antitrust * 0.2) + (cultural * 0.1)
    total_risk = min(100, total_risk)

    if total_risk < 30:
        category = 'Clean Deal'
        comment = 'Almost no hair on this one. Sponsor-backed angle lag raha hai solid.'
    elif total_risk < 60:
        category = 'Hairy but Manageable'
        comment = 'Need tighter underwriting. Some hair but doable.'
    else:
        category = 'Dumpster Fire Candidate'
        comment = 'Street leverage spike se khush nahi hoga. Avoid unless you’re a distressed fund.'

    return {
        'risk_score': round(total_risk, 1),
        'category': category,
        'comment': comment
    }

def football_field_data(ticker):
    d = _fetch_ticker_data(ticker)
    if not d:
        return None
    price = d['price'] or 100
    dcf_low = round(price * 0.8, 2)
    dcf_high = round(price * 1.3, 2)
    comps_low = round(price * 0.9, 2)
    comps_high = round(price * 1.15, 2)
    fifty2_low = round(price * 0.7, 2)
    fifty2_high = round(price * 1.1, 2)
    return {
        '52-Week': [fifty2_low, fifty2_high],
        'DCF': [dcf_low, dcf_high],
        'Comps': [comps_low, comps_high],
        'Current': [price, price]
    }
""",
    "app/routes/__init__.py": "",
    "app/routes/dashboard.py": """from flask import Blueprint, render_template
from app.models import Deal, TransactionLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    deals = Deal.query.order_by(Deal.created_at.desc()).all()
    logs = TransactionLog.query.order_by(TransactionLog.timestamp.desc()).limit(5).all()
    return render_template('dashboard.html', deals=deals, logs=logs)
""",
    "app/routes/deals.py": """from flask import Blueprint, render_template, request, jsonify
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
    realism = synergy_realism_meter(deal.synergy_cost, deal.synergy_rev)
    risk = deal_risk_analyzer(deal)
    football = football_field_data(deal.target) if deal.target else None
    return render_template('deal.html', deal=deal,
                           acc_dil=acc_dil,
                           realism=realism,
                           risk=risk,
                           football=football)

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
""",
    "app/routes/ic.py": """from flask import Blueprint, render_template, request, jsonify
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
""",
    "app/routes/data_room.py": """from flask import Blueprint, render_template

data_room_bp = Blueprint('data_room', __name__)

@data_room_bp.route('/')
def index():
    sections = [
        {'name': 'Financial Statements', 'files': ['Income Statement Q1', 'Balance Sheet', 'Cash Flow']},
        {'name': 'Debt Schedule', 'files': ['Term Loan A', 'Revolver', 'Senior Notes']},
        {'name': 'Legal Risks', 'files': ['Litigation Summary', 'IP Portfolio']},
        {'name': 'Customer Concentration', 'files': ['Top 10 Customers', 'Revenue by Region']},
        {'name': 'Operational KPIs', 'files': ['Headcount Trend', 'Utilization Rates']}
    ]
    return render_template('data_room.html', sections=sections)
""",
    "app/templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IBD Terminal | {% block title %}M&A Simulator{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="terminal-container">
        <nav class="sidebar">
            <div class="logo">IBD<span class="blink">_</span></div>
            <ul>
                <li><a href="{{ url_for('dashboard.index') }}">🏦 Dashboard</a></li>
                <li><a href="{{ url_for('deals.deal_list') }}">📁 Deal Room</a></li>
                <li><a href="{{ url_for('ic.ic_select') }}">🧠 IC Simulator</a></li>
                <li><a href="{{ url_for('data_room.index') }}">🔒 Data Room</a></li>
            </ul>
            <div class="sidebar-footer">
                <div class="user">Analyst <span class="green">ONLINE</span></div>
                <div class="time" id="live-time"></div>
            </div>
        </nav>
        <main class="content">
            <div class="ticker-wrap">
                <div class="ticker">
                    {% for log in logs %}
                    <div class="ticker-item">{{ log.message }}</div>
                    {% endfor %}
                    {% if not logs %}
                    <div class="ticker-item">🔥 DEAL ALERT: Project Titanium – JPM / FinTech – Bid getting spicy</div>
                    <div class="ticker-item">💬 Sponsor-backed angle lag raha hai on Griffin.</div>
                    <div class="ticker-item">🚨 Data room abhi incomplete hai – mgmt pushing for early close.</div>
                    {% endif %}
                </div>
            </div>
            {% block content %}{% endblock %}
        </main>
    </div>
    <div class="humor-panel" id="humor-panel">
        <div class="humor-title">BANKER MOOD</div>
        <div id="humor-quote">Associate hasn’t slept in 48 hours.</div>
    </div>
    <script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>""",
    "app/templates/dashboard.html": """{% extends "base.html" %}
{% block title %}Live Deal Dashboard{% endblock %}

{% block content %}
<div class="dashboard">
    <div class="header">
        <h1>LIVE DEAL DASHBOARD <span class="blink">█</span></h1>
        <div class="stats-bar">
            <span>Active Deals: {{ deals|length }}</span>
            <span>Sponsor Heat: <span class="amber">HIGH</span></span>
        </div>
    </div>

    <div class="kpi-grid">
        {% for deal in deals %}
        <div class="kpi-card">
            <div class="card-header">{{ deal.project_name }}</div>
            <div class="card-body">
                <div><strong>Acquirer:</strong> {{ deal.acquirer }}</div>
                <div><strong>Target:</strong> {{ deal.target }}</div>
                <div><strong>Value:</strong> ${{ "{:,.0f}M".format(deal.deal_value) }}</div>
                <div><strong>Status:</strong> <span class="status-{{ deal.status.lower() }}">{{ deal.status }}</span></div>
                <div class="card-footer">
                    <a href="{{ url_for('deals.deal_detail', deal_id=deal.id) }}" class="btn">View Deal →</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="commentary-feed">
        <h2>📡 BANKER COMMENTARY</h2>
        <div class="comment-box">
            {% for deal in deals %}
            <div class="comment-item">
                <span class="time">{{ deal.created_at.strftime('%H:%M') }}</span>
                <strong>{{ deal.project_name }}</strong>: {{ deal.commentary | safe }}
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}""",
    "app/templates/deal.html": """{% extends "base.html" %}
{% block title %}{{ deal.project_name }} Analysis{% endblock %}

{% block content %}
<div class="deal-room">
    <h1>{{ deal.project_name }} <span class="status-{{ deal.status.lower() }}">{{ deal.status }}</span></h1>
    <div class="deal-meta">
        <span>Acquirer: {{ deal.acquirer }}</span> | 
        <span>Target: {{ deal.target }}</span> |
        <span>Deal Value: ${{ "{:,.0f}M".format(deal.deal_value) }}</span> |
        <span>Premium: {{ deal.premium_pct }}%</span> |
        <span>Funding: {{ deal.cash_pct }}% Cash / {{ deal.stock_pct }}% Stock / {{ deal.debt_pct }}% Debt</span>
    </div>

    {% if football %}
    <div class="chart-container">
        <h2>🏈 FOOTBALL FIELD</h2>
        <div id="football-chart"></div>
    </div>
    {% endif %}

    <div class="analysis-grid">
        <div class="metric-box">
            <h3>ACCRETION / DILUTION</h3>
            <div class="kpi">
                <span class="label">Acquirer EPS</span>
                <span class="value">${{ acc_dil.acq_eps }}</span>
            </div>
            <div class="kpi">
                <span class="label">Pro‑Forma EPS</span>
                <span class="value">${{ acc_dil.pf_eps }}</span>
            </div>
            <div class="kpi big {% if acc_dil.acc_dil_pct > 0 %}green{% else %}red{% endif %}">
                <span class="label">Acc/Dil</span>
                <span class="value">{{ acc_dil.acc_dil_pct }}%</span>
            </div>
            <p class="verdict">
                {% if acc_dil.acc_dil_pct > 0 %}Mildly accretive – street may like it.
                {% elif acc_dil.acc_dil_pct > -1 %}Breakeven-ish. No fireworks.
                {% else %}Existing shareholders getting smoked. Dilution alert.{% endif %}
            </p>
        </div>

        <div class="sensitivity-box">
            <h3>SENSITIVITY TABLE (Acc/Dil %)</h3>
            <table class="sens-table">
                <tr>
                    <th>Premium \\ Cash %</th>
                    {% for c in acc_dil.cash_pcts %}<th>{{ c }}%</th>{% endfor %}
                </tr>
                {% for i in range(acc_dil.premiums|length) %}
                <tr>
                    <td>{{ acc_dil.premiums[i] }}%</td>
                    {% for j in range(acc_dil.cash_pcts|length) %}
                    <td class="{% if acc_dil.sensitivity[i][j] > 0 %}green{% else %}red{% endif %}">{{ acc_dil.sensitivity[i][j] }}%</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>

    <div class="synergy-meter">
        <h3>🧪 SYNERGY REALISM METER</h3>
        <div class="meter-bar">
            <div class="meter-fill" style="width: {{ realism.score }}%; background: {% if realism.score >= 70 %}#00ff88{% elif realism.score >= 40 %}#ffaa00{% else %}#ff3333{% endif %};"></div>
        </div>
        <span class="meter-label">{{ realism.level }} ({{ realism.score }}/100)</span>
        <p class="commentary">{{ realism.comment }}</p>
    </div>

    <div class="risk-analyzer">
        <h3>⚠️ DEAL RISK ANALYZER</h3>
        <div class="risk-score">
            <span class="big-number">{{ risk.risk_score }}</span>/100
            <span class="risk-category">{{ risk.category }}</span>
        </div>
        <p>{{ risk.comment }}</p>
        <div class="risk-radar" id="risk-radar"></div>
    </div>

    <div class="timeline">
        <h3>📅 DEAL PROCESS TIMELINE</h3>
        <div class="timeline-steps">
            <div class="step done">Teaser</div>
            <div class="step done">NDA</div>
            <div class="step active">CIM out</div>
            <div class="step">IOI due</div>
            <div class="step">DD</div>
            <div class="step">Financing</div>
            <div class="step">Sign</div>
            <div class="step">Close</div>
        </div>
        <p class="commentary">Data room abhi incomplete hai – Legal ne phir markup bhej diya.</p>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    {% if football %}
    var ffData = [{
        type: 'bar',
        x: [{{ football['52-Week'][0] }}, {{ football['52-Week'][1] }}],
        y: ['52-Week', '52-Week'],
        orientation: 'h',
        marker: {color: '#00d4ff'},
        width: 0.4
    }, {
        type: 'bar',
        x: [{{ football['DCF'][0] }}, {{ football['DCF'][1] }}],
        y: ['DCF', 'DCF'],
        orientation: 'h',
        marker: {color: '#ffaa00'},
        width: 0.4
    }, {
        type: 'bar',
        x: [{{ football['Comps'][0] }}, {{ football['Comps'][1] }}],
        y: ['Comps', 'Comps'],
        orientation: 'h',
        marker: {color: '#00ff88'},
        width: 0.4
    }];
    Plotly.newPlot('football-chart', ffData, {
        barmode: 'overlay',
        plot_bgcolor: '#0f1216',
        paper_bgcolor: '#0f1216',
        font: {color: '#e0e0e0'},
        height: 250,
        margin: {l:100, r:20, t:20, b:20}
    });
    {% endif %}

    var riskCtx = document.getElementById('risk-radar').getContext('2d');
    new Chart(riskCtx, {
        type: 'radar',
        data: {
            labels: ['Integration', 'Leverage', 'Antitrust', 'Cultural'],
            datasets: [{
                label: 'Risk',
                data: [{{ risk.risk_score * 0.4 }}, {{ risk.risk_score * 0.3 }}, {{ risk.risk_score * 0.2 }}, {{ risk.risk_score * 0.1 }}],
                backgroundColor: 'rgba(255, 51, 51, 0.2)',
                borderColor: '#ff3333',
                pointBackgroundColor: '#ff3333'
            }]
        },
        options: { scale: { ticks: { beginAtZero: true, max: 100 } } }
    });
</script>
{% endblock %}""",
    "app/templates/ic_simulator.html": """{% extends "base.html" %}
{% block title %}IC Simulator – {{ deal.project_name }}{% endblock %}

{% block content %}
<div class="ic-room">
    <h1>🧠 INVESTMENT COMMITTEE: {{ deal.project_name }}</h1>
    <p>You are presenting to the IC. Answer the MD’s, PE Partner’s, and Credit Committee’s questions.</p>

    <div class="ic-question-box" id="question-container">
        <h3 id="question-text">Click "Start IC Grilling"</h3>
        <input type="text" id="answer-input" placeholder="Your answer..." disabled>
        <button id="submit-answer" class="btn" disabled>Submit</button>
        <div id="feedback"></div>
    </div>

    <div class="ic-progress">
        <span id="progress-text">Questions remaining: {{ questions|length }}</span>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    const questions = [
        {% for q in questions %}
        { id: {{ q.id }}, question: "{{ q.question|escape }}", answer: "{{ q.answer|escape }}" },
        {% endfor %}
    ];
    let currentIndex = 0;
    const questionEl = document.getElementById('question-text');
    const answerInput = document.getElementById('answer-input');
    const submitBtn = document.getElementById('submit-answer');
    const feedbackEl = document.getElementById('feedback');
    const progressText = document.getElementById('progress-text');

    function loadQuestion() {
        if (currentIndex < questions.length) {
            questionEl.innerText = questions[currentIndex].question;
            answerInput.disabled = false;
            submitBtn.disabled = false;
            answerInput.value = '';
            feedbackEl.innerHTML = '';
            progressText.innerText = `Question ${currentIndex+1} of ${questions.length}`;
        } else {
            questionEl.innerText = '🎉 IC GRIND COMPLETE. You survived. Maybe your bonus will survive too.';
            answerInput.style.display = 'none';
            submitBtn.style.display = 'none';
            progressText.innerText = 'Finished';
        }
    }

    submitBtn.addEventListener('click', async () => {
        const answer = answerInput.value;
        const q = questions[currentIndex];
        const res = await fetch('/ic/api/answer', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ question_id: q.id, answer: answer })
        });
        const data = await res.json();
        feedbackEl.innerHTML = data.message;
        if (data.correct) {
            currentIndex++;
            setTimeout(loadQuestion, 1000);
        } else {
            feedbackEl.innerHTML += ' <br> Try again.';
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        if (questions.length > 0) {
            loadQuestion();
        } else {
            questionEl.innerText = 'No questions loaded. Seed the database first.';
        }
    });
</script>
{% endblock %}""",
    "app/templates/data_room.html": """{% extends "base.html" %}
{% block title %}Virtual Data Room{% endblock %}

{% block content %}
<div class="data-room">
    <h1>🔒 VIRTUAL DATA ROOM</h1>
    <p class="warn">Access Restricted – For Authorized Bidders Only</p>
    <div class="vdr-grid">
        {% for section in sections %}
        <div class="vdr-folder">
            <h3>📁 {{ section.name }}</h3>
            <ul>
                {% for file in section.files %}
                <li>📄 {{ file }} <span class="lock">🔒</span></li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}""",
    "app/templates/deal_list.html": """{% extends "base.html" %}
{% block title %}Deal Room{% endblock %}

{% block content %}
<div class="deal-list">
    <h1>📁 DEAL ROOM</h1>
    <div class="kpi-grid">
        {% for deal in deals %}
        <div class="kpi-card">
            <div class="card-header">{{ deal.project_name }}</div>
            <div class="card-body">
                <p>{{ deal.acquirer }} / {{ deal.target }}</p>
                <p>${{ "{:,.0f}M".format(deal.deal_value) }} | {{ deal.status }}</p>
                <a href="{{ url_for('deals.deal_detail', deal_id=deal.id) }}" class="btn">Open Deal →</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}""",
    "app/templates/ic_select.html": """{% extends "base.html" %}
{% block title %}IC Simulator – Select Deal{% endblock %}

{% block content %}
<div class="ic-select">
    <h1>🧠 INVESTMENT COMMITTEE SIMULATOR</h1>
    <p>Select a deal to present to the IC.</p>
    <div class="kpi-grid">
        {% for deal in deals %}
        <div class="kpi-card">
            <div class="card-header">{{ deal.project_name }}</div>
            <div class="card-body">
                <p>{{ deal.acquirer }} → {{ deal.target }}</p>
                <a href="{{ url_for('ic.ic_simulator', deal_id=deal.id) }}" class="btn">Start Grilling →</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}""",
    "app/static/css/style.css": """/* Base terminal look */
:root {
    --bg-primary: #0a0c10;
    --bg-secondary: #0f1216;
    --border-color: #1f2937;
    --text-primary: #d1d5db;
    --text-bright: #ffffff;
    --accent-cyan: #00d4ff;
    --accent-green: #00ff88;
    --accent-red: #ff3333;
    --accent-amber: #ffaa00;
    --font-mono: 'Courier New', Courier, monospace;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.5;
}

.terminal-container {
    display: flex;
    height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 220px;
    background-color: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    padding: 20px 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.logo {
    font-size: 1.8rem;
    color: var(--accent-cyan);
    text-align: center;
    letter-spacing: 2px;
    font-weight: bold;
}

.sidebar ul {
    list-style: none;
    margin-top: 30px;
}

.sidebar ul li a {
    display: block;
    padding: 10px 20px;
    color: var(--text-primary);
    text-decoration: none;
    transition: 0.2s;
}

.sidebar ul li a:hover {
    background-color: #1e2632;
    color: var(--accent-cyan);
}

.sidebar-footer {
    padding: 20px;
    font-size: 0.8rem;
}

.user .green { color: var(--accent-green); }

/* Main content */
.content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background-color: var(--bg-primary);
}

/* Live Ticker */
.ticker-wrap {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    overflow: hidden;
    margin-bottom: 20px;
    height: 30px;
    position: relative;
}
.ticker {
    display: flex;
    animation: ticker-scroll 20s linear infinite;
    white-space: nowrap;
}
.ticker-item {
    padding: 0 30px;
    color: var(--accent-amber);
    font-size: 0.85rem;
}
@keyframes ticker-scroll {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 15px;
    margin-bottom: 30px;
}
.kpi-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 15px;
}
.kpi-card .card-header {
    color: var(--accent-cyan);
    font-weight: bold;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 5px;
    margin-bottom: 10px;
}
.kpi-card .card-footer { margin-top: 10px; }

.status-closed { color: var(--accent-green); }
.status-pending { color: var(--accent-amber); }
.status-rumored { color: var(--accent-red); }

.btn {
    background: transparent;
    border: 1px solid var(--accent-cyan);
    color: var(--accent-cyan);
    padding: 5px 10px;
    text-decoration: none;
    font-weight: bold;
    display: inline-block;
    transition: 0.2s;
}
.btn:hover { background: var(--accent-cyan); color: black; }

/* Chart containers */
.chart-container {
    margin: 25px 0;
}

/* Sensitivity table */
.sens-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}
.sens-table th, .sens-table td {
    border: 1px solid var(--border-color);
    padding: 5px;
    text-align: center;
}
.sens-table th { background: #161b22; }
.green { color: var(--accent-green); }
.red { color: var(--accent-red); }

/* Synergy meter */
.synergy-meter {
    margin: 25px 0;
}
.meter-bar {
    background: #2d2d2d;
    height: 20px;
    border-radius: 3px;
    overflow: hidden;
}
.meter-fill {
    height: 100%;
    width: 0;
    transition: width 1s;
}

/* Risk radar */
.risk-radar { max-width: 300px; margin: 20px auto; }

/* Timeline */
.timeline-steps {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
}
.step {
    padding: 8px 12px;
    background: #1e2632;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 0.8rem;
}
.step.done { border-color: var(--accent-green); color: var(--accent-green); }
.step.active { border-color: var(--accent-cyan); color: var(--accent-cyan); animation: pulse 1.5s infinite; }

@keyframes pulse {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
}

/* Banker Humor Panel */
.humor-panel {
    position: fixed;
    bottom: 10px;
    right: 10px;
    background: #1a1a1a;
    border: 1px solid var(--accent-amber);
    padding: 10px 15px;
    font-size: 0.7rem;
    color: var(--accent-amber);
    max-width: 200px;
    z-index: 999;
}
.humor-title { font-weight: bold; margin-bottom: 4px; }

.blink { animation: blinker 1s step-start infinite; }
@keyframes blinker { 50% { opacity: 0; } }
""",
    "app/static/js/scripts.js": """// Live time in sidebar
setInterval(() => {
    const now = new Date();
    document.getElementById('live-time').innerText = now.toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// Humor quotes rotation
const quotes = [
    "Associate hasn’t slept in 48 hours.",
    "Model broke before MD review.",
    "Client wants upside with zero dilution.",
    "This comp set looks trash.",
    "Mgmt adjusted EBITDA kaafi aggressive lag raha hai.",
    "Sponsor pushing tighter exclusivity.",
    "Legal ne phir markup bhej diya.",
    "Data room abhi incomplete hai."
];
let i = 0;
setInterval(() => {
    document.getElementById('humor-quote').innerText = quotes[i % quotes.length];
    i++;
}, 8000);
"""
}

def create_project():
    # Create directories and write files
    for filepath, content in FILES.items():
        full_path = os.path.join(BASE_DIR, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {filepath}")

    print("\n✅ All files created! Now follow the next steps.")

if __name__ == "__main__":
    create_project()