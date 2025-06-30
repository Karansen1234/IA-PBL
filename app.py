import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Driver Rating Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("GJ25NS018 Karan Sen data analytics.xlsx", sheet_name="Sheet1")
    return df.iloc[:, :8]  # Keep relevant columns

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
min_rating, max_rating = st.sidebar.slider("Select Driver Rating Range", 1.0, 5.0, (1.0, 5.0), 0.5)
customer_type = st.sidebar.multiselect("Customer Type", df["Customer Type"].unique(), default=df["Customer Type"].unique())
payment_method = st.sidebar.multiselect("Payment Method", df["Payment Method"].unique(), default=df["Payment Method"].unique())

# Apply filters
filtered_df = df[
    (df["Driver Rating"] >= min_rating) &
    (df["Driver Rating"] <= max_rating) &
    (df["Customer Type"].isin(customer_type)) &
    (df["Payment Method"].isin(payment_method))
]

st.title("🚚 Driver Rating Analytics Dashboard")
st.markdown("This interactive dashboard provides insights into driver performance and operational KPIs. Use the filters on the left to explore micro and macro patterns.")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "👥 Customer & Payment", "📈 Performance", "📅 Trends", "📌 Advanced"])

with tab1:
    st.subheader("1. Overall Driver Rating Distribution")
    st.markdown("Shows the count of deliveries by driver ratings.")
    fig1 = px.histogram(filtered_df, x="Driver Rating", nbins=10, color_discrete_sequence=["#4CAF50"])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("2. Average Order Value by Driver Rating")
    st.markdown("Analyzes whether higher-rated drivers get more valuable orders.")
    fig2 = px.box(filtered_df, x="Driver Rating", y="Order Value", color="Driver Rating")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("3. Average Delivery Time by Driver Rating")
    st.markdown("Checks if better-rated drivers deliver faster.")
    fig3 = px.box(filtered_df, x="Driver Rating", y="Delivery Time(Minutes)", color="Driver Rating")
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("4. Order Value by Customer Type")
    fig4 = px.box(filtered_df, x="Customer Type", y="Order Value", color="Customer Type")
    st.markdown("Compares order value patterns between new and repeat customers.")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("5. Payment Method Distribution")
    fig5 = px.histogram(filtered_df, x="Payment Method", color="Payment Method")
    st.markdown("Shows preferred payment modes.")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("6. Driver Rating by Customer Type")
    fig6 = px.box(filtered_df, x="Customer Type", y="Driver Rating", color="Customer Type")
    st.markdown("Do new customers rate differently than repeat ones?")
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("7. Delivery Time by Payment Method")
    fig7 = px.box(filtered_df, x="Payment Method", y="Delivery Time(Minutes)", color="Payment Method")
    st.plotly_chart(fig7, use_container_width=True)

with tab3:
    st.subheader("8. Correlation Heatmap")
    st.markdown("Shows correlations between numeric variables.")
    corr = filtered_df.select_dtypes(include='number').corr()
    fig8, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig8)

    st.subheader("9. Driver Rating vs Delivery Time")
    fig9 = px.scatter(filtered_df, x="Driver Rating", y="Delivery Time(Minutes)", color="Driver Rating")
    st.markdown("Check relationship between rating and delivery time.")
    st.plotly_chart(fig9, use_container_width=True)

    st.subheader("10. Driver Rating vs Distance")
    fig10 = px.scatter(filtered_df, x="Driver Rating", y="Delivery Distance (KM)", color="Driver Rating")
    st.plotly_chart(fig10, use_container_width=True)

    st.subheader("11. Driver Rating vs Order Value")
    fig11 = px.scatter(filtered_df, x="Driver Rating", y="Order Value", color="Driver Rating")
    st.plotly_chart(fig11, use_container_width=True)

with tab4:
    st.subheader("12. Orders Over Time")
    fig12 = px.histogram(filtered_df, x="Date", color="Driver Rating")
    st.markdown("Tracks order volume and driver ratings over time.")
    st.plotly_chart(fig12, use_container_width=True)

    st.subheader("13. Average Rating by Date")
    st.markdown("Shows how ratings trend over time.")
    df_daily = filtered_df.groupby("Date")["Driver Rating"].mean().reset_index()
    fig13 = px.line(df_daily, x="Date", y="Driver Rating")
    st.plotly_chart(fig13, use_container_width=True)

    st.subheader("14. Average Delivery Time by Date")
    df_time = filtered_df.groupby("Date")["Delivery Time(Minutes)"].mean().reset_index()
    fig14 = px.line(df_time, x="Date", y="Delivery Time(Minutes)")
    st.plotly_chart(fig14, use_container_width=True)

with tab5:
    st.subheader("15. Outlier Detection: Order Value")
    fig15 = px.box(filtered_df, y="Order Value", color_discrete_sequence=["#E91E63"])
    st.plotly_chart(fig15, use_container_width=True)

    st.subheader("16. Outlier Detection: Delivery Time")
    fig16 = px.box(filtered_df, y="Delivery Time(Minutes)", color_discrete_sequence=["#9C27B0"])
    st.plotly_chart(fig16, use_container_width=True)

    st.subheader("17. Summary Table")
    st.dataframe(filtered_df.describe(), use_container_width=True)

    st.subheader("18. Raw Data Table")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("19. KPI Summary")
    avg_rating = filtered_df["Driver Rating"].mean()
    avg_time = filtered_df["Delivery Time(Minutes)"].mean()
    avg_value = filtered_df["Order Value"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg. Driver Rating", f"{avg_rating:.2f}")
    col2.metric("Avg. Delivery Time (min)", f"{avg_time:.2f}")
    col3.metric("Avg. Order Value (AED)", f"{avg_value:.2f}")

    st.subheader("20. Delivery Distance Boxplot")
    fig20 = px.box(filtered_df, y="Delivery Distance (KM)", color_discrete_sequence=["#03A9F4"])
    st.plotly_chart(fig20, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Karan Sen using Streamlit. For HR/Logistics Insight.")
