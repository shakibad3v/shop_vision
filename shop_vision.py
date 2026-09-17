import pandas as pd
import matplotlib.pyplot as plt
import json

# ۱. بارگذاری و ترکیب
employees = pd.read_csv('datapulse_employees.csv')
sales = pd.read_csv('datapulse_sales.csv')
df = pd.merge(sales, employees, on='employee_id', how='left')

# ۲. محاسبه مقادیر
sales_summary = {
    "total_revenue": float(df['revenue_usd'].sum()),
    "avg_unit_price": float(df['unit_price_usd'].mean()),
    "total_quantity": int(df['quantity'].sum()),
    "revenue_by_payment": df.groupby('payment_method')['revenue_usd'].sum().to_dict(),
    "revenue_by_category": df.groupby('category')['revenue_usd'].sum().to_dict()
}

emp_summary = df.groupby('employee_name_x').agg({
    'monthly_salary_usd': 'first',
    'hours_per_day': 'first',
    'revenue_usd': 'sum',
    'performance_score': 'mean'
}).rename(columns={'revenue_usd': 'total_sales_generated'})

# ۳. ذخیره داده‌های JSON برای سایت
final_output = {
    "sales": sales_summary,
    "employees": emp_summary.to_dict(orient='index')
}
with open('dashboard_data.json', 'w') as f:
    json.dump(final_output, f)

# ۴. تولید نمودارها برای نمایش در سایت
# نمودار ۱: عملکرد کارمندان
plt.figure(figsize=(10, 6))
emp_summary['total_sales_generated'].plot(kind='bar', color='skyblue')
plt.title('Employee Sales Performance')
plt.savefig('chart_employee_performance.png')

# نمودار ۲: روش پرداخت
plt.figure(figsize=(7, 7))
pd.Series(sales_summary['revenue_by_payment']).plot(kind='pie', autopct='%1.1f%%')
plt.title('Revenue by Payment Method')
plt.savefig('chart_payment_methods.png')

# نمودار ۳: فروش دسته‌بندی
plt.figure(figsize=(10, 6))
pd.Series(sales_summary['revenue_by_category']).plot(kind='bar', color='salmon')
plt.title('Revenue by Product Category')
plt.savefig('chart_category_sales.png')

print("همه چیز آماده شد! فایل json و ۳ تا عکس نمودار در پوشه پروژه ذخیره شدند.")
