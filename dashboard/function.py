class DataAnalyzer:
    def __init__(self,df):
        self.df = df

# Helper functions
    def create_daily_orders_df(self):
        orders_df = self.df.resample(rule='D', on='date').sum()
        return orders_df
    
    def create_sum_casual_user_df(self):
        sum_casual_user_df = self.df.groupby("day").casual_user.sum().sort_values(ascending=False).reset_index()
        return sum_casual_user_df

    def create_sum_registered_user_df(self):
        sum_registered_user_df = self.df.groupby("day").registered_user.sum().sort_values(ascending=False).reset_index()
        return sum_registered_user_df

    def create_byweather_df(self):
        byweather_df = self.df.groupby("weather").total_user.sum().sort_values(ascending=False).reset_index()
        return byweather_df

    def create_byseason_df(self):
        byseason_df = self.df.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()
        return byseason_df

    def create_rfm_df(self):
        rfm_df = self.df.groupby(by="day", as_index=False).agg({
            "date": "max",
            "instant": "nunique",
            "total_user": "sum"
        })
        rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]
        rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
        recent_date = self.df["date"].dt.date.max()
        rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
        rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
        return rfm_df