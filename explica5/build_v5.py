import json, sys
key = sys.argv[1]  # busy | batt
src = {'busy': 'obusy_en', 'batt': 'obatt_en'}[key]
J = json.load(open(f'../explica/tl_{src}.json'))
H = lambda a, b: f'{a}<br><span class="g2">{b}</span>'
E = lambda x: f'<em>{x}</em>'
ACP = ['Accounts payable', 'The bills you still owe your suppliers.']
if key == 'busy':
    chn = ['SETUP', 'CONNECT', 'INVOICES', 'MARGINS', 'BRIEFING']
    steps = [
        dict(t=5.0, ch=0, scr='import', h=H('Easy setup.', 'Start with one file.'),
             you=f'Upload your {E("price list")}, menu or catalog.', does=f'Creates your {E("products, prices and categories")}.'),
        dict(t=7.1, ch=0, scr='hours', h=H('Documents ready?', 'Get started in hours.'),
             you='Review what OneTap imported.', does=f'Guides you step by step until you are {E("ready to sell")}.'),
        dict(t=10.1, ch=0, scr='support', h=H('Set it up yourself.', 'Support when you need it.'),
             you='Follow the guided setup at your own pace.', does=f'{E("No implementation")} meetings or team needed.',
             term=['What it means', 'Implementation: a long setup project run by consultants before you can start.']),
        dict(t=15.1, ch=1, scr='connected', h=H('Your business.', 'Connected.'),
             does=f'Keeps {E("sales, inventory, costs, team and finances")} in one place.',
             term=['Why it matters', 'No more copying numbers between apps and spreadsheets.']),
        dict(t=21.5, ch=2, scr='invoice', h=H('Feed it your invoices.', 'Let the data flow.'),
             you=f'Snap a photo of a {E("supplier invoice")}.', does=f'Updates {E("stock, costs and bills")} together.', term=ACP, gap=.5),
        dict(t=25.8, ch=3, scr='margin', h=H('Spot waste.', 'Protect your margins.'),
             does=f'Shows {E("price, cost and margin")} for every product.',
             term=['Margin', '(Price − cost) ÷ price<br><b>$2.50 − $0.62 = $1.88</b><br><b>$1.88 ÷ $2.50 ≈ 75%</b>']),
        dict(t=29.9, ch=4, scr='brief', h=H('Know what needs attention.', 'Your AI morning briefing.'),
             you=f'Read {E("3 actions")} each morning.', does='Ranks what needs attention. You set the AI limits.')]
    chap = [[0, 2.95, 1, 'THE PROBLEM'], [2.95, 4.95, 2, 'THE SOLUTION'], [33.6, 35.9, 4, 'THE RESULT']]
    recap = ['Upload one file', 'Feed your invoices', 'Watch your margins', 'Read your briefing']
else:
    chn = ['SETUP', 'INVOICES', 'BRIEFING', 'CONTROL']
    steps = [
        dict(t=39.6, ch=0, scr='import', h=H('One file.', 'Your business, connected.'),
             you=f'Upload one {E("PDF or spreadsheet")}.', does=f'Builds your {E("products, prices and categories")}.'),
        dict(t=43.75, ch=1, scr='invoice', h=H('Feed OneTap.', 'Your documents do the work.'),
             you=f'Snap a photo of a {E("supplier invoice")}.', does=f'Updates {E("stock, costs and accounts payable")}.', term=ACP),
        dict(t=50.0, ch=2, scr='brief', h=H('Know your next move.', 'Your morning briefing.'),
             you=f'Open your {E("morning briefing")}.', does=f'Gives you {E("3 concrete actions")} for the day.', gap=.45),
        dict(t=53.1, ch=3, scr='chat', h=H('AI that helps you act.', 'You stay in control.'),
             you='Choose how much the AI can do.', does=f'It acts only {E("within your limits")}.',
             term=['4 levels', 'From only suggesting to approving on its own, within limits you set.'], gap=.45)]
    chap = [[0, 28.4, 1, 'THE PROBLEM'], [28.4, 39.55, 2, 'THE SOLUTION'], [56.75, 71.3, 4, 'THE RESULT']]
    recap = ['Upload one file', 'Feed your invoices', 'Read your briefing', 'Set the AI limits']
ui = next(b for b in J['beats'] if b['type'] == 'ui')
ui['steps'] = steps; ui['chn'] = chn; ui['nonum'] = True
J['chap'] = chap; J['recap'] = recap; J['words'] = json.load(open(f'words_{key}.json')); J['segs'] = []
json.dump(J, open(f'tl_{key}5.json', 'w'), ensure_ascii=False)
print('ok', key, J['total'], J['end'])
