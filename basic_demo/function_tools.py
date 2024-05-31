import requests
import json
import datetime
import function_api


def get_weather(city_name):

    amap_key = 'your_amap_api'
    try:
        addr_resp = requests.get(f"https://restapi.amap.com/v3/geocode/geo?address={city_name}&key={amap_key}")
        adcode = addr_resp.json()['geocodes'][0]['adcode']
        response = requests.get(f"https://restapi.amap.com/v3/weather/weatherInfo?city={adcode}&key={amap_key}")
        data = response.json()

        lives = data["lives"][0]
        temperature = lives["temperature_float"]
        wind_direction = lives["winddirection"]
        windpower = lives["windpower"]
        humidity = lives["humidity_float"]
        weather_report_time = lives["reporttime"]

        response_text = f"Function calling result: The current weather in {city_name} is {temperature} degrees Celsius, {wind_direction}, {windpower}, and humidity is {humidity}%. The above data is valid until {weather_report_time}."

    except requests.RequestException as e:
        print(f"get_weather function calling failed: {e}")
        return None

    return json.dumps(response_text)

def convert_currency(base_num, base_currency, target_currency):

    ex_api = "your_ex_api"
    url = f"https://v6.exchangerate-api.com/v6/{ex_api}/latest/{base_currency}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        
        if target_currency in data['conversion_rates']:
            exchange_rate = data['conversion_rates'][target_currency]
            target_num = base_num * exchange_rate
            response_text = f"Function calling result: According to the current exchange rate, {base_num} {base_currency} can be exchanged for {target_num} {target_currency}"

            return json.dumps(response_text)

        else:
            return None

    except requests.RequestException as e:
        print(f"convert_currency function calling failed: {e}")
        return None

def get_date():
    now = datetime.datetime.now()
    weekday = now.weekday()
    weekday_str = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday]
    response_text = f"The current time is {now}. Today is {weekday_str}"
    return json.dumps(response_text)

def main():

    print(get_weather("深圳"))
    # print(convert_currency(100,"USD","CNY"))
    # print(get_date())


if __name__ == "__main__":
    main()
