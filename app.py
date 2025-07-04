from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SITE_NAME'] = 'HAVA DURUMU'

# OpenWeatherMap API configuration
API_KEY = os.getenv("MY_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # Using HTTPS

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        
        if not city:
            error_message = "Lütfen bir şehir adı girin."
            return render_template('index.html', 
                                weather=None, 
                                error=error_message, 
                                site_name=app.config['SITE_NAME'])
        
        # API parameters
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'tr'  # Turkish language support
        }
        
        try:
            response = requests.get(BASE_URL, params=params, timeout=10)  # Added timeout
            print(f"API Response Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city,
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'feels_like': round(data['main']['feels_like']),  # Added feels like temperature
                    'datetime': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
            elif response.status_code == 404:
                error_message = "Şehir bulunamadı! Lütfen geçerli bir şehir adı girin."
            else:
                error_message = f"Hava durumu bilgisi alınamadı. (Hata kodu: {response.status_code})"
        except requests.Timeout:
            error_message = "API yanıt vermedi. Lütfen daha sonra tekrar deneyin."
        except requests.RequestException as e:
            error_message = "Bağlantı hatası oluştu. Lütfen internet bağlantınızı kontrol edin."
            print(f"Error details: {str(e)}")
        except Exception as e:
            error_message = "Beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            print(f"Error details: {str(e)}")
    
    return render_template('index.html', 
                         weather=weather_data, 
                         error=error_message,
                         site_name=app.config['SITE_NAME'])

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

