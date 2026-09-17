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

# چند فروش برتر برای جدول سایت
top_sales = [
    {
        "product": str(r.product),
        "category": str(r.category),
        "quantity": int(r.quantity),
        "unit_price_usd": float(r.unit_price_usd),
        "payment_method": str(r.payment_method),
        "revenue_usd": float(r.revenue_usd),
    }
    for r in df.nlargest(8, 'revenue_usd').itertuples()
]

# ۳. ذخیره داده‌های JSON برای سایت
final_output = {
    "sales": sales_summary,
    "employees": emp_summary.to_dict(orient='index'),
    "recent_sales": top_sales,
    "total_orders": int(len(df))
}
with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2)


with open('dashboard_data.js', 'w', encoding='utf-8') as f:
    f.write('const DASHBOARD_DATA = ')
    json.dump(final_output, f, ensure_ascii=False)
    f.write(';')

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

# ... (بعد از بخش محاسبه emp_summary)

# ۱. اضافه کردن منطق تصمیم‌گیری (مثلاً میانگین عملکرد و فروش)
performance_threshold = emp_summary['performance_score'].mean()
sales_threshold = emp_summary['total_sales_generated'].mean()

def evaluate_employee(row):
    # اگر امتیاز عملکرد یا فروش از میانگین پایین‌تر باشد -> نیاز به بررسی
    if row['performance_score'] < performance_threshold or row['total_sales_generated'] < sales_threshold:
        return 'Needs Review'
    return 'Top Performer'

emp_summary['status'] = emp_summary.apply(evaluate_employee, axis=1)

# ۲. خروجی جدید برای نمایش در سایت (تعداد وضعیت‌ها)
status_counts = emp_summary['status'].value_counts().to_dict()

# ۳. آپدیت کردن دیکشنری نهایی برای JSON
final_output = {
    "sales": sales_summary,
    "employees": emp_summary.to_dict(orient='index'),
    "status_counts": status_counts # این را اضافه کردیم
}


