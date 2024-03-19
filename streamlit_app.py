import streamlit as st
import pandas as pd
import base64
import time
from pytrends.request import TrendReq

st.title("Google Trends For Top GSC Keywords")

st.markdown("""
**Istruzioni:**
1. Esporta i dati dal [report sul rendimento](https://search.google.com/search-console/performance/search-analytics) (impressioni, CTR, posizione) in Google Search Console. Carica poi il file `Queries.csv` dal file zip.
2. Il numero massimo di query da eseguire è limitato a 200 per evitare il timeout dell'applicazione o il blocco da parte di Google.
""")

st.markdown("---")

sortby = st.selectbox('Ordina keyword per', ('Clic', 'Impressioni', 'CTR', 'Posizione'))
cutoff = st.number_input('Numero di queries', min_value=1, max_value=200, value=10)
pause = st.number_input('Pausa tra le chiamate', min_value=1, max_value=5, value=2)
timeframe = st.selectbox('Timeframe', ('today 1-m', 'today 3-m', 'today 12-m'))
geo = st.selectbox('Geo', ('World', 'US'))

if geo == 'World':
    geo = ''

get_gsc_file = st.file_uploader("Carica il file CSV di GSC", type=['csv'])

def fetch_trends_with_retry(pytrends, kw_list, timeframe, geo, retries=3, backoff_factor=2):
    for attempt in range(retries):
        try:
            pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
            return pytrends.interest_over_time()
        except Exception as e:
            print(f"Errore: {e}. Tentativo {attempt + 1} di {retries}.")
            time.sleep((backoff_factor ** attempt) * pause)
    raise Exception("Max retries reached, unable to fetch trends")

if get_gsc_file is not None:
    st.write("Caricamento dei dati riuscito, elaborazione... 😎")
    
    df = pd.read_csv(get_gsc_file, encoding='utf-8')
    df.sort_values(by=[sortby], ascending=False, inplace=True)
    df = df[:cutoff]
    
    d = {'Keyword': [], sortby: [], 'Trend': []}
    df3 = pd.DataFrame(data=d)
    keywords = []
    trends = []
    metric = df[sortby].tolist()
    up, down, flat, na = 0, 0, 0, 0

    for index, row in df.iterrows():
        keyword = row['Query più frequenti']
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [keyword]
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
        df2 = pytrends.interest_over_time()
        keywords.append(keyword)
        try:
            df2 = fetch_trends_with_retry(pytrends, kw_list, timeframe, geo)
            trend1 = int((df2[keyword][-5] + df2[keyword][-4] + df2[keyword][-3])/3)
            trend2 = int((df2[keyword][-4] + df2[keyword][-3] + df2[keyword][-2])/3)
            trend3 = int((df2[keyword][-3] + df2[keyword][-2] + df2[keyword][-1])/3)

            if trend3 > trend2 and trend2 > trend1:
                trends.append('UP')
                up += 1
            elif trend3 < trend2 and trend2 < trend1:
                trends.append('DOWN')
                down += 1
            else:
                trends.append('FLAT')
                flat += 1
        except Exception as e:
            print(f"Impossibile recuperare i trend per {keyword}: {e}")
            trends.append('N/A')
            na += 1
        time.sleep(pause)

    df3['Keyword'] = keywords
    df3['Trend'] = trends
    df3[sortby] = metric

    def colortable(val):
        color = 'white'
        if val == 'DOWN':
            color = "lightcoral"
        elif val == 'UP':
            color = "lightgreen"
        elif val == 'FLAT':
            color = "lightblue"
        return 'background-color: %s' % color

    df3 = df3.style.applymap(colortable)

    def get_csv_download_link(df, title):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{title}.csv">Scarica il file CSV</a>'
        return href

    total = up + down + flat + na
    st.write(f"Up: {up} | {round((up/total)*100,0)}%")
    st.write(f"Down: {down} | {round((down/total)*100,0)}%")
    st.write(f"Flat: {flat} | {round((flat/total)*100,0)}%")
    st.write(f"N/A: {na} | {round((na/total)*100,0)}%")

    st.markdown(get_csv_download_link(df3.data, "gsc-keyword-trends"), unsafe_allow_html=True)
    st.dataframe(df3.data)

st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [importSEM](https://www.importsem.com) and [Physics Forums](https://www.physicsforums.com)')
