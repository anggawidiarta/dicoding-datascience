import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import streamlit as st

warnings.simplefilter("ignore")

st.set_page_config(
    page_title="Air Quality Index", page_icon=":earth_asia:", layout="wide"
)


def create_sidebar():
    # set start date & end date
    st.sidebar.image('dashboard\Real_Madrid_logo_PNG19.png',caption='Created By : I Putu Angga Purnama Widiarta')
    
    min_date = df["datetime"].min()
    max_date = df["datetime"].max()
    try:
        start_date, end_date = st.sidebar.date_input(
            label="Pilih Periode Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
        )

        if end_date is not None:
            # Lakukan sesuatu dengan start_date dan end_date
            # Contoh: tampilkan rentang waktu yang dipilih
            st.write(f"Rentang Waktu Yang Dipilih: {start_date} - {end_date}")
    except NameError:
        st.stop()
    except ValueError:
        st.stop()

    return start_date, end_date


def create_byyear_df(df):
    df_byyear = (
        df.resample(rule="Y", on="datetime")
        .agg({"pm2.5": ["min", "max", "mean"], "pm10": ["min", "max", "mean"]})
        .sort_values(by="datetime", ascending=True)
        .reset_index()
    )
    return df_byyear


def create_byair_df(df):
    df_air_category = (
        df.groupby("category")["id"].count().sort_values(ascending=False).reset_index()
    )
    return df_air_category


def create_bystation_df(df):
    df_air_bystation = (
        df.groupby("station")["pm2.5"].mean().sort_values(ascending=False).reset_index()
    )
    return df_air_bystation


def set_main_df(df):
    start_date, end_date = create_sidebar()
    df = df[(df["datetime"] >= str(start_date)) & (df["datetime"] <= str(end_date))]
    return df


if __name__ == "__main__":
    df = pd.read_csv("dashboard/fixed_dataset.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = set_main_df(df)
    st.header("Beijing Station Index Air Quality :earth_asia:")
    met1, met2 = st.columns(2)
    with met1:
        st.metric("Total Data", value=df["id"].count())
    with met2:
        st.metric("Total Station", value=df["station"].nunique())

    st.markdown(
        f"<h1 style='text-align: left; font-size: 32px; color:#2192FF'>Average Particulate Matter</h1>",
        unsafe_allow_html=True,
    )

    # rows 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"<h1 style='font-size: 20px;  text-align: center'>PM2.5 : {df['pm2.5'].mean():.2f}</h1>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<h1 style='font-size: 20px;  text-align: center'>PM10 : {df['pm10'].mean():.2f}</h1>",
            unsafe_allow_html=True,
        )

    # st.markdown(
    # st.markdown(
    #     f"<h1 style='text-align: left; font-size: 32px; color:#2192FF'>Average Another Metric</h1>",
    #     unsafe_allow_html=True,
    # )
    # rows 2
    col01, col02, col03, col04 = st.columns(4)
    with col01:
        st.markdown(
            f"<h1 style='font-size: 20px; text-align: center'>SO2 : {df['so2'].mean():.2f}</h1>",
            unsafe_allow_html=True,
        )
    with col02:
        st.markdown(
            f"<h1 style='font-size: 20px;  text-align: center'>NO2 : {df['no2'].mean():.2f}</h1>",
            unsafe_allow_html=True,
        )
    with col03:
        st.markdown(
            f"<h1 style='font-size: 20px;  text-align: center'>CO : {df['co'].mean():.2f}</h1>",
            unsafe_allow_html=True,
        )
    with col04:
        st.markdown(
            f"<h1 style='font-size: 20px;  text-align: center'>O3 : {df['o3'].mean():.2f}</h1>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    chart1, chart2 = st.columns(2)
    with chart1:
        byair_df = create_byair_df(df)
        fig, ax = plt.subplots(figsize=(8, 4.48))
        colors = ["#00bfa0", "#0bb4ff", "#0bb4ff", "#0bb4ff", "#0bb4ff", "#0bb4ff"]
        sns.barplot(
            x="id",
            y="category",
            data=byair_df.sort_values(by="id", ascending=False),
            ax=ax,
            palette=colors,
        )
        sns.despine(bottom=True, left=True)
        ax.set(xticklabels=[])
        ax.yaxis.set_ticks_position("none")
        ax.xaxis.set_ticks_position("none")
        plt.yticks(fontsize=8)
        plt.title("Amount Of Data By Air Quality Category", loc="center", fontsize=12)
        plt.xlabel(None)
        plt.ylabel(None)
        plt.tick_params(axis="x", labelsize=12)

        for p in ax.patches:
            ax.annotate(
                f"{int(p.get_width()):,}",
                (p.get_width(), p.get_y() + p.get_height() / 2),
                ha="center",
                va="center",
                fontsize=8,
                color="black",
            )

        st.pyplot(fig)

    with chart2:
        byyear_df = create_byyear_df(df)
        fig, ax = plt.subplots(figsize=(8, 4))
        byyear_df["datetime"] = byyear_df["datetime"].dt.strftime("%Y")
        years = byyear_df["datetime"]
        pm2_5_mean = byyear_df["pm2.5"]["mean"]

        ax.plot(
            byyear_df["datetime"],
            byyear_df["pm2.5"]["mean"],
            color="b",
            linestyle="-",
            marker="o",
            markersize=5,
            label="PM2.5 Mean",
        )

        # menampilkan nilai pada titik data di setiap tahunnya
        for i in range(len(years)):
            ax.text(
                years[i],
                pm2_5_mean[i],
                f"{pm2_5_mean[i]:.2f}",
                ha="center",
                va="bottom",
            )

        ax.set_ylim(0, max(byyear_df["pm2.5"]["mean"]) * 1.1)

        ax.set_ylabel("PM2.5 Mean")
        ax.set_title("PM2.5 Mean Over Time")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(
            axis="both", which="both", bottom=False, top=False, left=False, right=False
        )
        st.pyplot(fig)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # chart 3
    chart01, chart02 = st.columns(2)

    with chart01:
        bystation_df = create_bystation_df(df)
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
        sns.barplot(
            x="pm2.5",
            y="station",
            data=bystation_df.sort_values(by="pm2.5", ascending=False).head(3),
            palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
            linewidth=0,
            ax=ax[0],
        )

        sns.despine(left=True, bottom=True)

        for p in ax[0].patches:
            ax[0].annotate(
                f"{p.get_width():.2f}",
                (p.get_width(), p.get_y() + p.get_height() / 2),
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
        ax[0].set_xlabel(None)
        ax[0].set_ylabel(None)
        ax[0].set_title("Top 3 Stations by pm2.5", loc="center")

        sns.barplot(
            x="pm2.5",
            y="station",
            data=bystation_df.sort_values(by="pm2.5", ascending=True).head(3),
            palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"],
            linewidth=0,
            ax=ax[1],
        )
        for p in ax[1].patches:
            ax[1].annotate(
                f"{p.get_width():.2f}",
                (p.get_width(), p.get_y() + p.get_height() / 2),
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Worst 3 Stations by pm2.5 ", loc="center")

        st.pyplot(fig)

    with chart02:
        fig, ax = plt.subplots(figsize=(8, 3.05))
        # sns.lmplot(x="pm2.5", y="pm10", data=df)
        sns.scatterplot(ax=ax, x="pm2.5", y="pm10", data=df)
        sns.despine(right=True, top=True)
        ax.set_title("Correlation Between PM2.5 & PM10", loc="center")
        st.pyplot(fig)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        f"<h1 style='text-align: left; font-size: 32px; color:#2192FF'>Dataframe</h1>",
        unsafe_allow_html=True,
    )
    st.dataframe(df, hide_index=True, use_container_width=True)
