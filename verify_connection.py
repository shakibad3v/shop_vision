import json, re

with open('dashboard_data.js', encoding='utf-8') as f:
    js = f.read()
assert js.startswith('const DASHBOARD_DATA = {') and js.rstrip().endswith(';')
payload = json.loads(js[len('const DASHBOARD_DATA = '):-1].strip())
assert set(payload) == {'sales', 'employees', 'recent_sales', 'total_orders'}
print('dashboard_data.js OK:', payload['sales']['total_revenue'], '| orders:', payload['total_orders'])

with open('index.html', encoding='utf-8') as f:
    html = f.read()

ids = set(re.findall(r"getElementById\('([^']+)'\)", html))
missing = [i for i in sorted(ids) if f'id="{i}"' not in html]
print('IDs referenced:', len(ids), '| missing:', missing or 'none')

for src in ['dashboard_data.js', 'style.css', 'chart_employee_performance.png',
            'chart_payment_methods.png', 'chart_category_sales.png']:
    assert f'{src}' in html, f'{src} not referenced'
    import os
    assert os.path.exists(src), f'{src} file missing'
print('All referenced assets exist.')
