from app.extensions import db
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
