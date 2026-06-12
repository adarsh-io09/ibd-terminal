from app import create_app
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
