from flask import Blueprint, render_template

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
