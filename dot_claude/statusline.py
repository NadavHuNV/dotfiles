#!/usr/bin/env python3
import sys, json, os, time

CACHE_FILE = os.path.expanduser('~/.claude/.usage_cache.json')
CACHE_TTL = 60
ORG_UUID = 'ae6cdefa-a29d-44f9-af49-72d85aede8c8'

def get_token():
    try:
        creds = os.path.expanduser('~/.claude/.credentials.json')
        return json.load(open(creds))['claudeAiOauth']['accessToken']
    except:
        try:
            import subprocess
            out = subprocess.check_output(
                ['security', 'find-generic-password', '-s', 'Claude Code-credentials', '-w'],
                stderr=subprocess.DEVNULL
            )
            return json.loads(out.decode())['claudeAiOauth']['accessToken']
        except:
            return None

def fetch_usage():
    try:
        import urllib.request
        token = get_token()
        if not token:
            return None, None
        req = urllib.request.Request(
            'https://api.anthropic.com/api/oauth/usage',
            headers={
                'Authorization': f'Bearer {token}',
                'anthropic-beta': 'oauth-2025-04-20',
                'Content-Type': 'application/json',
            }
        )
        with urllib.request.urlopen(req, timeout=3) as r:
            d = json.loads(r.read())
        return d['five_hour']['utilization'], d['seven_day']['utilization']
    except:
        return None, None

def fetch_billing():
    try:
        import urllib.request
        token = get_token()
        if not token:
            return None, None
        req = urllib.request.Request(
            f'https://claude.ai/api/organizations/{ORG_UUID}/usage',
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
        )
        with urllib.request.urlopen(req, timeout=3) as r:
            d = json.loads(r.read())
        eu = d.get('extra_usage') or {}
        used = eu.get('used_credits')
        limit = eu.get('monthly_limit')
        if used is None:
            return None, None
        return used / 100, (limit / 100 if limit else None)
    except:
        return None, None

def get_usage():
    try:
        with open(CACHE_FILE) as f:
            c = json.load(f)
        if time.time() - c['ts'] < CACHE_TTL:
            return c['fh'], c['sd'], c.get('bill'), c.get('bill_limit')
    except:
        pass
    fh, sd = fetch_usage()
    bill, bill_limit = fetch_billing()
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({'ts': time.time(), 'fh': fh, 'sd': sd, 'bill': bill, 'bill_limit': bill_limit}, f)
    except:
        pass
    return fh, sd, bill, bill_limit

data = json.load(sys.stdin)
cwd = data.get('cwd', '')
home = os.path.expanduser('~')
if cwd.startswith(home):
    cwd = '~' + cwd[len(home):]
model = data.get('model', {}).get('display_name', 'Unknown')
ctx_pct = data.get('context_window', {}).get('used_percentage', 0)
cost = data.get('cost', {}).get('total_cost_usd', 0)

def b(n): return f'\x1b[48;5;{n}m'
def f(n): return f'\x1b[38;5;{n}m'
R = '\x1b[0m'
SEP = ''

def seg(txt, bg, fg, next_bg=None):
    s = b(bg) + f(fg) + ' ' + txt + ' '
    if next_bg is not None:
        s += b(next_bg) + f(bg) + SEP
    else:
        s += R + f(bg) + SEP + R
    return s

def usage_color(pct):
    if pct is None: return 239, 245
    if pct < 50:    return 65, 255
    if pct < 80:    return 130, 255
    return 131, 255

def bar(pct, w=15):
    if pct is None: return '▱' * w
    filled = round(w * pct / 100)
    return '▰' * filled + '▱' * (w - filled)

if ctx_pct < 50:   ctx_bg, ctx_fg = 65, 255
elif ctx_pct < 70: ctx_bg, ctx_fg = 130, 255
else:              ctx_bg, ctx_fg = 131, 255

fh, sd, bill, bill_limit = get_usage()
fh_bg, fh_fg = usage_color(fh)
sd_bg, sd_fg = usage_color(sd)

bill_str = '\U0001f4b0 $' + (f'{bill:.0f}' if bill is not None else '--')
if bill is not None and bill_limit:
    bill_str += ' / $' + f'{bill_limit/1000:.0f}K'

next_after_bill = fh_bg if fh is not None else None

out = seg('\U0001f4c2 ' + cwd, 239, 255, 25)
out += seg('★ ' + model, 25, 255, ctx_bg)
out += seg('Ctx ' + bar(ctx_pct) + ' ' + str(ctx_pct) + '%', ctx_bg, ctx_fg, 57)
out += seg('\U0001f4b0 Cost $' + f'{cost:.4f}', 57, 255, 55 if bill is not None else next_after_bill)
if bill is not None:
    out += seg(bill_str, 55, 255, next_after_bill)
if fh is not None:
    out += seg('5h ' + bar(fh) + ' ' + str(int(fh)) + '%', fh_bg, fh_fg, sd_bg)
    out += seg('7d ' + bar(sd) + ' ' + str(int(sd)) + '%', sd_bg, sd_fg, None)

print(out, end='')
