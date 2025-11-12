import requests
import os
def get_weather(city="北京"):
    # api_key = st.secrets["WEATHER_API_KEY"]  # 推荐用 https://www.tianqiapi.com （免费）
    api_key = "7952f0543749fe21298320bc5c58ccdf"
    url = f"https://v1.yiketianqi.com/api?appid={appid}&appsecret={appsecret}&city={city}"
    r = requests.get(url).json()
    return f"{r['date']} {r['wea']} {r['tem2']}~{r['tem1']} {r['win']} {r['air']}"
