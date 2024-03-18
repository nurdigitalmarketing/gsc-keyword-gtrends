
# Google Trends for Top GSC Keywords Automator v.1

## 👉🏼 Description
This Streamlit tool was developed to integrate Google Trends analysis with Google Search Console (GSC) performance data, enabling users to visualize trends for their top-performing GSC keywords. By leveraging Google's Trend API through the `pytrends` library, this application processes up to 200 keywords, comparing their performance over specified timeframes and geographical settings. This unique approach provides valuable insights into keyword popularity trends, aiding in strategic decision-making for SEO and content marketing.

## 👉🏼 Features
- Upload CSV files containing Google Search Console performance data.
- Customize analysis by selecting the number of queries, pause duration between calls, timeframe, and geographical focus.
- Automatically sorts keywords based on selected performance metrics (Clicks, Impressions, CTR, Position).
- Visual representation of keyword trends (Up, Down, Flat, N/A) based on historical data.
- Downloadable CSV file with the trend analysis results.

## 👉🏼 How to Use
1. Export your Google Search Console performance data (Impressions, CTR, Position) and prepare a `Queries.csv` file from the zip file.
2. Ensure all dependencies are installed from `requirements.txt`.
3. Launch the Streamlit application using the command:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Upload your `Queries.csv` file through the Streamlit user interface.
5. Customize your analysis parameters and click on "Run Analysis" to view and download the trend analysis.

## 👉🏼 Technologies Used
- `pytrends`: A Python library for accessing Google Trends API for keyword trend data.
- `pandas`: An open-source data manipulation and analysis library.
- `streamlit`: An open-source app framework for Machine Learning and Data Science projects.

## 👉🏼 Installation
To install the necessary dependencies, run:
```bash
pip install -r requirements.txt
```

## Credits

This tool extends the capabilities of Google Search Console data analysis by integrating with Google Trends, offering a streamlined way to monitor keyword performance trends over time. Developed with the aim of enhancing SEO strategies and content planning, this application stands as a practical solution for digital marketers and content creators.

Author: Greg Bernhardt | Friends: [importSEM](https://www.importsem.com) and [Physics Forums](https://www.physicsforums.com)

