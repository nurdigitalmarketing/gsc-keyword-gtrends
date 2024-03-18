import streamlit as st
import pandas as pd
import base64
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import time

st.title("Google Trends For Top GSC Keywords")

st.markdown("""
**Istruzioni:**
1. Esporta i dati dal [report sul rendimento](https://search.google.com/search-console/performance/search-analytics) (impressioni, CTR, posizione) in Google Search Console. Carica poi il file `Queries.csv` dal file zip.
2. Il numero massimo di query da eseguire è limitato a 200 per evitare il timeout dell'applicazione o il blocco da parte di Google.
""")

st.markdown("---")

sortby = st.selectbox('Ordina keyword per',('Clic', 'Impressioni','CTR','Posizione'))
cutoff = st.number_input('Numero di queries', min_value=1, max_value=200, value=10)
pause = st.number_input('Pausa tra le chiamate', min_value=1, max_value=60, value=30)  # Aumentato il limite massimo
timeframe = st.selectbox('Timeframe',('today 1-m', 'today 3-m', 'today 12-m'))
geo = st.selectbox('Geo',('World', 'US'))

if geo == 'World':
    geo = ''

get_gsc_file = st.file_uploader("Carica il file CSV di GSC",type=['csv'])  

if get_gsc_file is not None:
    st.write("Caricamento dei dati riuscito, elaborazione... :sunglasses:")
    
    df = pd.read_csv(get_gsc_file, encoding='utf-8')
    df.sort_values(by=[sortby], ascending=False, inplace=True)
    df = df[:cutoff]
    
    d = {'Keyword': [], sortby:[], 'Trend': []}
    df3 = pd.DataFrame(data=d)
    keywords = []
    trends = []
    metric = df[sortby].tolist()
    up =0
    down =0
    flat =0
    na = 0

    def fetch_trends_with_retry(keyword, pytrends, attempts=5, sleep_duration=60):
        for attempt in range(attempts):
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
                return pytrends.interest_over_time()
            except TooManyRequestsError:
                if attempt < attempts - 1:
                    time.sleep(sleep_duration)  # Aumenta la pausa per evitare il blocco
                    continue
                else:
                    return pd.DataFrame()  # Restituisce un DataFrame vuoto in caso di fallimento
        return pd.DataFrame()  # Precauzione

    pytrends = TrendReq(hl='en-US', tz=360)
    
    for keyword in df['Query più frequenti'].head(cutoff):
        df2 = fetch_trends_with_retry(keyword, pytrends, attempts=3, sleep_duration=pause)
        if not df2.empty:
            # Il tuo codice per elaborare i dati e aggiornare df3
            keywords.append(keyword)
            try:
                trend1 = int((df2[keyword][-5] + df2[keyword][-4] + df2[keyword][-3])/3)
                trend2 = int((df2[keyword][-4] + df2[keyword][-3] + df2[keyword][-2])/3)
                trend3 = int((df2[keyword][-3] + df2[keyword][-2] + df2[keyword][-1])/3)

                if trend3 > trend2 and trend2 > trend1:
                    trends.append('UP')
                    up+=1
                elif trend3 < trend2 and trend2 < trend1:
                    trends.append('DOWN')
                    down+=1
                else:
                    print(keyword + " is flat")
                    trends.append('FLAT')
                    flat+=1
            except:
                trends.append('N/A')
                na+=1
        else:
            keywords.append(keyword)
            trends.append('N/A')
            na+=1
        time.sleep(pause)
      
    df3['Keyword'] = keywords
    df3['Trend'] = trends
    df3[sortby] = metric
    
    def colortable(val):
        color = 'white'
        if val == 'DOWN':
            color="lightcoral"
        elif val == 'UP':
            color = "lightgreen"
        elif val == 'FLAT':
            color = "lightblue"
        return 'background-color: %s' % color

    df3 = df3.style.applymap(colortable)
    
    def get_csv_download_link(df, title):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{title}">Scarica il file CSV</a>'
    
    total = len(trends)
    st.write("Up: " + str(up) + " | " + str(round((up/total)*100,0)) + "%")
    st.write("Down: " + str(down) + " | " + str(round((down/total)*100,0)) + "%")
    st.write("Flat: " + str(flat) + " | " + str(round((flat/total)*100,0)) + "%")
    st.write("N/A: " + str(na) + " | " + str(round((na/total)*100,0)) + "%")
    
    st.markdown(get_csv_download_link(df3.data,"gsc-keyword-trends.csv"), unsafe_allow_html=True)
    st.dataframe(df3)

st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [importSEM](https://www.importsem.com) and [Physics Forums](https://www.physicsforums.com)')
