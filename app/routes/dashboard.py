from flask import Blueprint, render_template
from app.models import Deal, TransactionLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    deals = Deal.query.order_by(Deal.created_at.desc()).all()
    logs = TransactionLog.query.order_by(TransactionLog.timestamp.desc()).limit(5).all()
    return render_template('dashboard.html', deals=deals, logs=logs)
