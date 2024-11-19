import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from function import DataAnalyzer

sns.set(style='dark')

# Prepare Dataset
day_df = pd.read_csv('https://raw.githubusercontent.com/aismaanly/bikesharing-analysis/refs/heads/main/dashboard/day_clean.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/aismaanly/bikesharing-analysis/refs/heads/main/dashboard/hour_clean.csv')

# Ensure the date column are of type datetime
datetime_columns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Create filter components
min_date = day_df["date"].min()
max_date = day_df["date"].max()

# Sidebar
with st.sidebar:
    # Adding a logo
    st.image("https://raw.githubusercontent.com/aismaanly/bikesharing-analysis/main/dashboard/logo.jpg", width=150 )

    # Data range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = day_df[(day_df["date"] >= str(start_date)) &
                (day_df["date"] <= str(end_date))]

function = DataAnalyzer(main_df)

daily_orders_df = function.create_daily_orders_df()
sum_casual_user_df = function.create_sum_casual_user_df()
sum_registered_user_df = function.create_sum_registered_user_df()
byweather_df = function.create_byweather_df()
byseason_df = function.create_byseason_df()
rfm_df = function.create_rfm_df()

# Create title dashboard
st.title('Bike Share Dashboard :sparkles:')

# Add text or descriptions
st.write("**This is a dashboard for analyzing Bike Sharing Dataset**")

# Daily Users
st.subheader('Daily Users')
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_orders_df.casual_user.sum()
    st.metric("Total Casual User", value=f'{total_casual:,}')

with col2:
    total_registered = daily_orders_df.registered_user.sum()
    st.metric("Total Registered User", value=f'{total_registered:,}')

with col3:
    total_users = daily_orders_df.total_user.sum()
    st.metric("Total Users", value=f'{total_users:,}')


fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders_df.index,  
    y=daily_orders_df['total_user'],  
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)  
ax.tick_params(axis="y", labelsize=15) 
ax.set_xlabel(None) 
ax.set_ylabel(None)  
st.pyplot(fig)


# Daily User Distribution by User Type in Bike Sharing
st.subheader("Daily User Distribution by User Type in Bike Sharing")
col1, col2 = st.columns(2)

with col1:
    total_users = daily_orders_df.total_user.sum()
    st.markdown(f"Total Users: **{total_users}**")

with col2:
    total_users = daily_orders_df.total_user.mean()
    st.markdown(f"Averange Users: **{total_users}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="casual_user", y="day", data=sum_casual_user_df, palette="viridis", hue="day", legend=False, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Casual User", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis ='x', labelsize=30, rotation=45)

sns.barplot(x="registered_user", y="day", data=sum_registered_user_df, palette="viridis", hue="day", legend=False, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Registered User", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis ='x', labelsize=30, rotation=-45)

st.pyplot(fig)

# Impact of Weather and Seasons on Bike Sharing Usage
st.subheader("Impact of Weather and Seasons on Bike Sharing Usage")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(y="total_user", x="weather", data=byweather_df.sort_values(by="total_user", ascending=False), palette="viridis", hue="weather", legend=False, ax=ax[0])
ax[0].set_title("Number of User by Weather", loc="center", fontsize=50)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis ='x', labelsize=30)
ax[0].ticklabel_format(style='plain', axis='y')

sns.barplot(y="total_user", x="season", data=byseason_df.sort_values(by="total_user", ascending=False), palette="viridis", hue="season", legend=False, ax=ax[1])
ax[1].set_title("Number of User by Season", loc="center", fontsize=50)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis ='x', labelsize=30)
ax[1].ticklabel_format(style='plain', axis='y')

st.pyplot(fig)

# RFM Analysis
st.subheader("Best Customer Based on RFM Parameters (day)")
tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

# Colors for visualizations
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

# Tab 1: Recency
with tab1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y="recency", x="day", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax)
    ax.set_title("By Recency (days)", loc="center", fontsize=20)
    ax.set_ylabel("Recency")
    ax.set_xlabel("Day")
    st.pyplot(fig)

# Tab 2: Frequency
with tab2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y="frequency", x="day", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax)
    ax.set_title("By Frequency", loc="center", fontsize=20)
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Day")
    st.pyplot(fig)

# Tab 3: Monetary
with tab3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO')
    st.metric("Average Monetary", value=avg_monetary)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y="monetary", x="day", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax)
    ax.set_title("By Monetary", loc="center", fontsize=20)
    ax.set_ylabel("Monetary")
    ax.set_xlabel("Day")
    st.pyplot(fig)

st.caption('Copyright (C) Aisma Nurlaili 2024')
