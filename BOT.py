import openai
import requests
import re
# Set up API credentials
openai.api_key = 'YOUR_openai_API_KEY'
openweather_api_key = 'YOUR_openweather_API'
messages = [
            {"role": "system", "content": "You are a kind helpful assistant."},
            ]


# Function to interact with the OpenAI language model
def generate_openai_response(user_input):
    message = user_input
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply


# Function to fetch weather data using the OpenWeather API
def get_weather_data(location):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={openweather_api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extract the relevant weather information from the response
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return f"The weather in {location} is {weather_description}. The temperature is {temperature}°C, and the humidity is {humidity}%."
    #else:
        #return "Failed to fetch weather data. Please try again later."

# Main logic of the chatbot
while True:
    user_input = input("User: ")

    # Check if the user's input contains weather-related keywords
    if re.search(r'\bweather\b|\btemperature\b|\bforecast\b', user_input, re.IGNORECASE):
        # Extract the location from the user's input (e.g., "What's the weather in Mumbai?")
        location = re.findall(r'in\s+([a-zA-Z\s]+)|of\s+([a-zA-Z\s]+)|for\s+([a-zA-Z\s]+)', user_input, re.IGNORECASE)
        if location:
            # Find the first non-empty group from the location match
            location = next(filter(None, location[0]))
            response = get_weather_data(location)
        else:
            response = "Invalid location. Please provide a valid location."
    else:
        response = generate_openai_response(user_input)

    print("shoaib's Bot:", response)