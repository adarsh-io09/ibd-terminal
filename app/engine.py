import numpy as np
import pandas as pd
import yfinance as yf
from functools import lru_cache
import time
import json
import os

# --- CACHE SETUP ---
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def _get_cache_path(ticker):
    return os.path.join(CACHE_DIR, f'{ticker}.json')

def _cache_get(ticker):
    path = _get_cache_path(ticker)
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        # Invalidate after 6 hours
        if time.time() - data.get('timestamp', 0) < 6 * 3600:
            return data['info']
    return None

def _cache_set(ticker, info):
    path = _get_cache_path(ticker)
    with open(path, 'w') as f:
        json.dump({'timestamp': time.time(), 'info': info}, f)

# --- STATIC FALLBACK DATA (for offline / rate-limited) ---
STATIC_DATA = {
    'JPM':  {'name': 'JPMorgan Chase & Co.', 'price': 190, 'market_cap': 550e9, 'ebitda': 80e9, 'net_income': 50e9, 'shares': 2.9e9, 'pe_ratio': 12, 'ev_to_ebitda': None, 'sector': 'Financial Services'},
    'SQ':   {'name': 'Block, Inc.', 'price': 75, 'market_cap': 46e9, 'ebitda': 2.5e9, 'net_income': 1.2e9, 'shares': 620e6, 'pe_ratio': 35, 'ev_to_ebitda': None, 'sector': 'Technology'},
    'PFE':  {'name': 'Pfizer Inc.', 'price': 28, 'market_cap': 160e9, 'ebitda': 30e9, 'net_income': 15e9, 'shares': 5.7e9, 'pe_ratio': 11, 'ev_to_ebitda': None, 'sector': 'Healthcare'},
    'BNTX': {'name': 'BioNTech SE', 'price': 100, 'market_cap': 24e9, 'ebitda': 4e9, 'net_income': 3e9, 'shares': 240e6, 'pe_ratio': 8, 'ev_to_ebitda': None, 'sector': 'Healthcare'},
    'XOM':  {'name': 'Exxon Mobil Corporation', 'price': 110, 'market_cap': 490e9, 'ebitda': 85e9, 'net_income': 55e9, 'shares': 4.5e9, 'pe_ratio': 9, 'ev_to_ebitda': None, 'sector': 'Energy'},
    'CVX':  {'name': 'Chevron Corporation', 'price': 155, 'market_cap': 290e9, 'ebitda': 50e9, 'net_income': 35e9, 'shares': 1.9e9, 'pe_ratio': 8, 'ev_to_ebitda': None, 'sector': 'Energy'},
    'MSFT': {'name': 'Microsoft Corporation', 'price': 420, 'market_cap': 3120e9, 'ebitda': 130e9, 'net_income': 85e9, 'shares': 7.4e9, 'pe_ratio': 37, 'ev_to_ebitda': None, 'sector': 'Technology'},
    'ATVI': {'name': 'Activision Blizzard, Inc.', 'price': 94, 'market_cap': 74e9, 'ebitda': 4.5e9, 'net_income': 2.8e9, 'shares': 780e6, 'pe_ratio': 26, 'ev_to_ebitda': None, 'sector': 'Technology'},
    'BAC':  {'name': 'Bank of America Corporation', 'price': 33, 'market_cap': 260e9, 'ebitda': 45e9, 'net_income': 27e9, 'shares': 7.9e9, 'pe_ratio': 10, 'ev_to_ebitda': None, 'sector': 'Financial Services'},
}

def _fetch_ticker_data(ticker):
    # Check cache first
    cached = _cache_get(ticker)
    if cached:
        return cached

    # Check static fallback
    if ticker.upper() in STATIC_DATA:
        return STATIC_DATA[ticker.upper()]

    # Try yfinance
    try:
        t = yf.Ticker(ticker)
        info = t.info
        time.sleep(0.5)  # Slightly longer pause to respect rate limits
        data = {
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
        _cache_set(ticker, data)
        return data
    except Exception as e:
        print(f"Failed to fetch {ticker}: {e}")
        # Fallback to static if available, else None
        return STATIC_DATA.get(ticker.upper(), None)


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

    # Fallback to default data if None
    if not acq:
        acq = {'name': acq_ticker, 'price': 100, 'market_cap': 100e9, 'ebitda': 20e9, 'net_income': 10e9, 'shares': 1e9, 'pe_ratio': 15, 'ev_to_ebitda': None, 'sector': 'Unknown'}
    if not tgt:
        tgt = {'name': tgt_ticker, 'price': 50, 'market_cap': 20e9, 'ebitda': 5e9, 'net_income': 2e9, 'shares': 400e6, 'pe_ratio': 20, 'ev_to_ebitda': None, 'sector': 'Unknown'}

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