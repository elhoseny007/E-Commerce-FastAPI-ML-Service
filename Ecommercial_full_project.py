import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('rainbow')
import plotly.express as px
import warnings
#path
df=pd.read_csv('E:/1.1 ecommerce-purchases.csv')
#meta_data
df.info()
head=df.head()
df.tail()
describe=df.describe().round(3)
columns=df.columns
meta_data=df.shape
num_rows=df.shape[0]
num_columns=df.shape[1]
#------------
#KPIs
Total_revenue=df.iloc[:,-1].sum()
Average_Purchase=df.iloc[:,-1].mean().round(2)
purchase_Date=df['AM or PM'].value_counts()

#charts
companies = df['Company'].str.split(',').value_counts().reset_index().rename(columns={'count': 'Companies'})
company=(df['Company'].str.split(',').explode().str.strip().value_counts())

#date# date parsing fix
df['CC Exp Date'] = pd.to_datetime(df['CC Exp Date'], format='%m/%d', errors='coerce')
df['CC Exp Date'] = df['CC Exp Date'].apply(lambda x: x.replace(year=2026) if pd.notnull(x) else x)
df_time = df.set_index('CC Exp Date')

# --- 2. daily Plot ---
Daily_data = df_time['Purchase Price'].resample('D').count() 
top30_daiys=Daily_data.sort_values(ascending=False).head(30)
top30_daiys=top30_daiys.sort_index()
plt.figure(figsize=(20,10))
plt.plot(top30_daiys.index,top30_daiys.values,color='green',marker='o',markersize=6)
#plt.fill_between(top30_daiys.index,top30_daiys.values,color='green',alpha=0.3)
plt.title('purchase_per_dayes')
plt.xlabel('Date')
plt.ylabel('Purchase')
plt.show()
#----------------
#sum purchase per emails
purchase_per_emails=df.groupby('Email')["Purchase Price"].sum().nlargest(10)
plt.figure(figsize=(20,10))
ax=purchase_per_emails.plot(kind='bar',color='brown')
plt.title('sum purchase per emails')
plt.xlabel('Emails')
plt.ylabel('Purchase')
plt.show()
#----------------
#count of purchase per browsers
df['Browser Info']=df['Browser Info'].str.split('/').str[0]
pie_browser=df['Browser Info'].value_counts()

colors = ['#A04000', '#007ACC'] 

plt.figure(figsize=(6, 6))
plt.pie(pie_browser,labels=pie_browser.index,startangle=90,autopct='%1.2f',
        colors=colors, pctdistance=0.85, textprops={'color':"black"})

centre_circle = plt.Circle((0,0), 0.70, fc='white') 
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# 4. اللمسات النهائية
plt.title('Count of Purchase Price by Browser Info', loc='left', fontsize=14)
plt.axis('equal')
plt.legend(title="Browser Info", loc="center right", bbox_to_anchor=(1, 0, 0.5, 1))

plt.tight_layout()
plt.show()
#----------
#count of activation per Time(am,pm)

AM_PM=df['AM or PM'].value_counts()
time=AM_PM.plot(kind='bar',color='#A04000')
labels='PM', 'AM'
plt.bar_label(time.containers[0], padding=3, labels=[f'{v/1000:.1f}K' for v in AM_PM.values], fontsize=10, fontweight='bold')
plt.title('operations per AM,PM')
plt.xlabel('operations')
plt.ylabel('AM,PM')
plt.legend()
plt.tight_layout()
plt.show()
#--------------
#jobs
plt.figure(figsize=(20,10))
top_10_jobs_purchase_total=df.groupby('Job')['Purchase Price'].sum().nlargest(10)
colors = plt.cm.rainbow(np.linspace(0, 1, 10))
job1 = plt.barh(top_10_jobs_purchase_total.index, top_10_jobs_purchase_total.values, color=colors)
plt.bar_label(job1, padding=3, labels=[f'{v/1000:.1f}K' for v in top_10_jobs_purchase_total.values], 
              fontsize=10, fontweight='bold')

plt.title('Most Jobs by Total Purchase Value')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

plt.figure(figsize=(20,10))
top_10_jobs_purchase_count = df.groupby('Job')['Purchase Price'].count().nlargest(10)
colors2 = plt.cm.viridis(np.linspace(0, 1, 10)) 
job2 = plt.barh(top_10_jobs_purchase_count.index, top_10_jobs_purchase_count.values, color=colors2)
plt.bar_label(job2, padding=3, labels=[f'{int(v)}' for v in top_10_jobs_purchase_count.values], 
              fontsize=10, fontweight='bold')

plt.title('Operation Purchase Count by Job')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
#-----------------
#count of purchase per language
plt.figure(figsize=(20,10))
top5_lang=df.groupby('Language')['Purchase Price'].count().nlargest(5)
tl=plt.barh(top5_lang.index,top5_lang.values,color='blue' )
plt.bar_label(tl,padding=3,labels=[f'{int(v)}'for v in top5_lang.values],fontsize=10, fontweight='bold')
plt.title('top5_lang')
plt.tight_layout()
plt.show()

plt.figure(figsize=(20,10))
lowest5_lang=df.groupby('Language')['Purchase Price'].count().sort_values(ascending=True).head(5)
ll=plt.barh(lowest5_lang.index,lowest5_lang.values,color='skyblue')
plt.bar_label(ll,padding=3,labels=[f'{int(v)}'for v in lowest5_lang.values],fontsize=10, fontweight='bold')
plt.title('lowest5_lang')
plt.tight_layout()
plt.show()

#---------------
#count of address by browser info
browser_counts = df['Browser Info'].str.split('/').str[0].value_counts()

plt.figure(figsize=(10, 6))
ax = plt.gca()

colors = ['#E57373', '#F8BBD0'] 
ab = plt.barh(browser_counts.index, browser_counts.values, color=colors)

plt.bar_label(ab, padding=10, labels=[f'{v/1000:.2f}K' for v in browser_counts.values], 
              fontsize=11, fontweight='bold', color='#555555')

plt.title('Count of Address by Browser Info', loc='left', fontsize=14, pad=20, color='#333333')
plt.xlabel('Count of Address', fontsize=10, color='#666666')
plt.ylabel('Browser Info', fontsize=10, color='#666666')

plt.grid(axis='x', linestyle=':', alpha=0.7)
plt.xticks([0, 5000], ['0K', '5K'])

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()

#crdit card with providers
providers_card=df.groupby('CC Provider')['Credit Card'].count().nlargest(10)
plt.figure(figsize=(20,10))
pc=providers_card.plot(kind='bar',color='green')
plt.bar_label(pc,padding=10, labels=[f'{v/1000:.2f}K' for v in providers_card.values], 
              fontsize=11, fontweight='bold', color='#555555')
plt.title('crdit card with providers')
plt.xlabel('providers')
plt.ylabel('credit card')
plt.tight_layout()
plt.show()


