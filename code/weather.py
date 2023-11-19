from datetime import datetime, timedelta
import requests
import re
import tkinter as tk


def get_city():
    res = requests.get(r'https://myip.ipip.net', timeout=5).text
    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', res)
    ip = ip_match.group(0)
    res = requests.get(rf'http://ip-api.com/json/{ip}?lang=zh-CN')
    if res.status_code == 200:
        data = res.json()
        # lat = data['lat']
        # lon = data['lon']
        city = data['country'] + ' ' + data['city']
        address = str(data['lon']) + ',' + str(data['lat'])
    return city, address


def get_weather(add):
    token = 'KKTjOwOohyGGeLGw'
    url = rf'https://api.caiyunapp.com/v2.6/{token}/{add}/weather?alert=true&dailysteps=1&hourlysteps=24'
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        # data = json.loads(data)
        des = data['result']['hourly']['description']
        temp = data['result']['hourly']['temperature'][0]['value']
        temp_later = data['result']['hourly']['temperature'][12]['value']
        humidity = data['result']['hourly']['humidity'][0]['value']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:00:00')
        twelve_hours_later = datetime.now() + timedelta(hours=12)
        time_later = twelve_hours_later.strftime('%Y-%m-%d %H:00:00')
        # print(f'当前天气：{des}')
        # print(f'{timestamp} 气温：{temp}摄氏度')
        # print(f'{timestamp} 湿度：{humidity}')
        # print(f'{time_later} 气温：{temp_later}摄氏度')
        weather_info = f'当前天气：{des}\n' \
                       f'{timestamp} 气温：{temp}摄氏度\n' \
                       f'{timestamp} 湿度：{humidity}\n' \
                       f'{time_later} 气温：{temp_later}摄氏度'
        return weather_info
    else:
        return '访问失败'


# if __name__ == '__main__':
#     city, address = get_city()
#     print(f'当前城市：{city}')
#     get_weather(address)
def show_weather():
    city, address = get_city()
    if city and address:
        city_label.config(text=f'当前城市：{city}')
        weather_info = get_weather(address)
        if weather_info:
            weather_label.config(text=weather_info)


root = tk.Tk()
root.title("Weather App")
root.geometry("400x200")  # 设置窗口初始大小为400x200像素
root.minsize(400, 200)  # 设置窗口最小尺寸为400x200像素

# Create a label for city
city_label = tk.Label(root, text="当前城市：")
city_label.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

# Create a label for weather
weather_label = tk.Label(root, text="天气信息将显示在这里", anchor='w', justify=tk.LEFT)
weather_label.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

# Create a button
weather_button = tk.Button(root, text="获取天气信息", command=show_weather)
weather_button.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

# Configure the grid
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Run the application
root.mainloop()
