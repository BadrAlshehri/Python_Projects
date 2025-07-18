import yfinance as yf
import pandas as pd
import datetime 
import csv 
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)


def grab_year(datetime):
    return datetime.year

def grab_month(datetime):
    return datetime.month

spy = yf.Ticker("SPY")
df = spy.history(start="2015-01-01", end=datetime.date.today())

df.to_csv("spy_data.csv")


df2 = pd.read_csv('spy_data.csv')

for index, row in df2.iterrows():
    if row["Close"] > row["Open"]:
        df2.at[index, "Capital Gain"] = 1.0
    elif row["Close"] < row["Open"]:
        df2.at[index, "Capital Gain"] = -1.0
    else:
        df2.at[index, "Capital Gain"] = 0

df2["Date"] =pd.to_datetime(df2["Date"])
#print(df2['Date'])

df2["Year"] = df2['Date'].apply(grab_year)
df2['Month'] = df2['Date'].apply(grab_month)

df2.drop(columns=["Capital Gains"], inplace=True)

df2 = df2[['Date','Year','Month','Open','High','Low','Close','Volume','Dividends','Stock Splits','Capital Gain']]

target_year = int(input('Enter your target year: '))
target_month = int(input('Enter your target month(jan:1, feb:2...): '))

filtered_df2 = df2[(df2["Year"] == target_year) & (df2['Month'] == target_month)]

monthly_sum_Capital_gains = filtered_df2['Capital Gain'].sum()

filtered_df2["monthly_sum_Capital_gains"] = monthly_sum_Capital_gains

df2["Monthly Capital Gain"] = df2.groupby(['Year', 'Month'])["Capital Gain"].transform('sum')

monthly_capital_list = []

'''q5 = print(filtered_df2.index[0])
value = filtered_df2.at[q5, "monthly_sum_Capital_gains"]'''

q5 = filtered_df2.index[0]

value = filtered_df2.at[q5, "monthly_sum_Capital_gains"]

monthly_capital_list.append(value)

target_gain = monthly_capital_list[0]

q6 = df2[df2['Year'] == target_year]
q7 = q6.groupby('Month').first().reset_index()
#print(q7[['Year','Month','Monthly Capital Gain']])

Monthly_review = q7['Monthly Capital Gain']
months_of_the_year = ['January','February','March','April','May','June','July','August','September','October','November','December']
plt.plot(months_of_the_year[0:len(Monthly_review)], Monthly_review)
plt.ylabel('Monthly Split')
plt.xlabel('Months')
plt.title('SPY index value')
plt.yticks(range(int(min(Monthly_review)) - 2, int(max(Monthly_review)) + 2))

print(f'The monthly sum of your target month is {target_gain}')

#Target gain is the sum of the gain of our targeted month / year so in this case it would be 2.0

matching_values = (df2['Monthly Capital Gain'] == target_gain)

matching_df = df2[matching_values]

unique_months = matching_df[['Year', 'Month']].drop_duplicates()

next_dates = []

for index, row in unique_months.iterrows():
    current_month = row['Month']
    current_year = row['Year']

    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    next_dates.append((next_year, next_month))

next_both_df = pd.DataFrame(next_dates, columns=(['Year', 'Month']))

next_month_gains = []

for index, row in next_both_df.iterrows():
    year = row['Year']
    month = row['Month']
    matching_rows = df2[(df2['Year'] == year) & (df2['Month'] == month)]
    gain = matching_rows['Capital Gain'].sum()
    next_month_gains.append(gain)

next_both_df['Capital Gain 2'] = next_month_gains

#print(next_both_df['Capital Gain 2'])

total = len(next_both_df['Capital Gain 2'])
negative = len(next_both_df[next_both_df['Capital Gain 2'] < 0])
positive = len(next_both_df[next_both_df['Capital Gain 2'] > 0])

q6 = positive / total * 100
q7 = 100 - q6

print(f"The chance of the price going up the month after your targeted date is {q6:.2f}% and the chance it might go down is {q7:.2f}%")

plt.show()
#unique_months.to_csv('matching_months3.csv')

#print(next_month_gains)

#q6.to_csv('filtered_dates8.csv')



'''
unique_months = Months capital gain that = our target capital gain
next_both_df = Months after the original matching capital gain months, with their corresponding capital gain value
df2 = the whole dataframe of the index from chosen start date
filtered_df2 = the chosen date with their corresponsding values'''