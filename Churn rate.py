import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("D:/DATA ANALYST/Mind X/II. Business Intelligence Analyst/Project/E-commerce Dataset_cleaned.csv")

df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df = df[['Customer_Id', 'Order_Date']]
df['Order_Date'] = df['Order_Date'].dt.month
df['min_Order_Date'] = df.groupby('Customer_Id')['Order_Date'].transform('min')
df['date_diff'] = df['Order_Date'] - df['min_Order_Date']

cohort_data = df.groupby(['min_Order_Date', 'Customer_Id']).size().reset_index(name='CustomerCount')
initial_cohort = cohort_data[cohort_data['min_Order_Date'] == cohort_data['min_Order_Date'].min()]
initial_cohort_counts = initial_cohort['Customer_Id'].value_counts()

df['min_Order_Date'] = df.groupby('Customer_Id')['Order_Date'].transform('min')
# Tính toán các cột Month 1, Month 2, Month 3 dựa trên date_diff
df['Month 1'] = (df['date_diff'] == 1).astype(int)
df['Month 2'] = (df['date_diff'] == 2).astype(int)
df['Month 3'] = (df['date_diff'] == 3).astype(int)
df['Month 4'] = (df['date_diff'] == 4).astype(int)
df['Month 5'] = (df['date_diff'] == 5).astype(int)
df['Month 6'] = (df['date_diff'] == 6).astype(int)
df['Month 7'] = (df['date_diff'] == 7).astype(int)
df['Month 8'] = (df['date_diff'] == 8).astype(int)
df['Month 9'] = (df['date_diff'] == 9).astype(int)
df['Month 10'] = (df['date_diff'] == 10).astype(int)
df['Month 11'] = (df['date_diff'] == 11).astype(int)
df['Month 12'] = (df['date_diff'] == 12).astype(int)


# Tính toán số lượng khách hàng mới
result = df.groupby('min_Order_Date').agg(
    new_customer_count=('Customer_Id', 'nunique'),
    Month_1=('Month 1', 'sum'),
    Month_2=('Month 2', 'sum'),
    Month_3=('Month 3', 'sum'),
    Month_4=('Month 4', 'sum'),
    Month_5=('Month 5', 'sum'),
    Month_6=('Month 6', 'sum'),
    Month_7=('Month 7', 'sum'),
    Month_8=('Month 8', 'sum'),
    Month_9=('Month 9', 'sum'),
    Month_10=('Month 10', 'sum'),
    Month_11=('Month 11', 'sum'),
    Month_12=('Month 12', 'sum'),
).reset_index()

new_columns = [f'Month_{i}/new_customer_count' for i in range(1, 13)]
new_df = result[['min_Order_Date'] + ['new_customer_count'] + [f'Month_{i}' for i in range(1, 13)]].copy()
for i in range(1, 13):
    new_df[new_columns[i - 1]] = new_df[f'Month_{i}'] / new_df['new_customer_count']

selected_columns = ['min_Order_Date', 'new_customer_count']
for month in range(1, 13):
    selected_columns.append(f'Month_{month}/new_customer_count')
cohort_table = new_df[selected_columns]

cohort_table = cohort_table.rename(columns={
    'min_Order_Date': 'Month',
    'new_customer_count': 'Customers'
})
for month in range(1, 13):
    old_column_name = f'Month_{month}/new_customer_count'
    new_column_name = f'Month {month}'
    cohort_table = cohort_table.rename(columns={old_column_name: new_column_name})
print(cohort_table)


cohort_table.loc[:, 'Month 1':'Month 12'] *= 100
print(cohort_table)


data_for_heatmap = cohort_table.loc[:, 'Month 1':'Month 12']
plt.figure(figsize=(10, 6))
sns.heatmap(data_for_heatmap, annot=True, fmt=".1f", cmap="YlGnBu", yticklabels=range(1, len(data_for_heatmap) + 1))
plt.title("Cohort Table (%)")
plt.ylabel("Month")
plt.show()


