import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import altair as alt  # type: ignore


st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")


# Load data
df = pd.read_csv("data/marketing_campaign_cleaned.csv")

# Titre du dashboard
st.title("📊 Dashboard Analyse de Campagne Marketing")

# Layout en colonnes
col1, col2 = st.columns(2)

with col1:
    # Graphique du taux d'acceptation global
    total_customers = len(df)
    customers_accepted = len(df[df["accepted_campaigns"] > 0])
    acceptance_rate = (customers_accepted / total_customers) * 100

    fig_acceptance = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=acceptance_rate,
            title={"text": "Taux d'acceptation global"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 50], "color": "lightblue"},
                    {"range": [50, 100], "color": "slategray"},
                ],
            },
        )
    )
    st.plotly_chart(fig_acceptance)

with col2:
    # Distribution des âges pour les clients ayant accepté une campagne
    fig_age = px.histogram(
        df[df["accepted_campaigns"] > 0],
        x="age_group",
        title="Distribution des âges - Clients ayant accepté une campagne",
        color_discrete_sequence=["darkblue"],
    )
    fig_age.update_layout(showlegend=False)
    st.plotly_chart(fig_age)

# Nouvelle ligne
col3, col4 = st.columns(2)

with col3:
    # Dépenses totales par groupe d'âge
    spending_by_age = df.groupby("age_group")["Total_Amount_Spent"].sum().reset_index()
    fig_spending = px.bar(
        spending_by_age,
        x="age_group",
        y="Total_Amount_Spent",
        title="Dépenses totales par groupe d'âge",
        color_discrete_sequence=["darkblue"],
    )
    st.plotly_chart(fig_spending)

with col4:
    # Achats en ligne vs en magasin
    online_vs_store = pd.DataFrame(
        {
            "Type": ["Achats en ligne", "Achats en magasin"],
            "Nombre": [df["NumWebPurchases"].sum(), df["NumStorePurchases"].sum()],
        }
    )

    fig_purchases = px.pie(
        online_vs_store,
        values="Nombre",
        names="Type",
        title="Répartition des achats en ligne vs en magasin",
        color_discrete_sequence=["darkblue", "lightblue"],
        hole=0.5,
    )
    st.plotly_chart(fig_purchases)

# Métriques additionnelles
st.subheader("📈 Métriques clés")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Nombre total de clients", total_customers)
with metric_col2:
    st.metric("Clients ayant accepté une campagne", customers_accepted)
with metric_col3:
    avg_spending = df["Total_Amount_Spent"].mean()
    st.metric("Dépense moyenne par client", f"{avg_spending:.2f} €")
with metric_col4:
    response_rate = df["Response"].mean() * 100
    st.metric("Taux de réponse dernière campagne", f"{response_rate:.1f}%")
