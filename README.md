# OpenWeatherMap API

## Synopsis 

Give the today, tomorrow weather or a forecast for a specific day of the week with the related data (humidity, temperature, etc ...) for a given location. 

## Installation
```
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_openweathermap.git
```

## Options

| parameter | required | default | choices                     | comment                                                                                                    |
|-----------|----------|---------|-----------------------------|------------------------------------------------------------------------------------------------------------|
| api_key   | YES      | None    |                             | User API key of the OWM API get one [here](https://home.openweathermap.org/users/sign_up)                  |
| location  | YES      | None    |                             | The location                                                                                               |
| lang      | No       | en      |                             | Look for the supported languages [here](https://openweathermap.org/current#multi)                          |
| temp_unit | No       | celsius | celsius, kelvin, fahrenheit |                                                                                                            |                                                      
| country   | No       | None    |                             | [ISO-3166 Country Code](https://en.wikipedia.org)                                                           |
| 12h_format| no       | False   | True/False                  | To get 12 hour format for sunrise and sunset return value                                                  |                
| day       | No       | None    | today or a weekday          | Only needed if you want a single synapse to catch the day and translate it in a file_template (required)   |


## Return Values

| name                        | Description                                | Type   | sample                 |
|-----------------------------|--------------------------------------------|--------|------------------------|
| location                    | The current location                       | String | Grenoble               |
| longitude                   | The current longitude                      | Float  | 5.73                   |
| latitude                    | The current latitude                       | Float  | 45.18                  |
| sunset_today                | The sunset time for today                  | Time   | 20:52                  |            
| sunrise_today               | The sunrise time for today                 | Time   | 06:31                  | 
|-----------------------------|--------------------------------------------|--------|------------------------|
| current['weather_status']   | The current weather conditions             | String | moderate rain          |
| current['temp']             | The current temperature                    | Int    | 20                     |
| current['max_temp']         | The current max. temperature               | Int    | 20                     |
| current['min_temp']         | The current min. temperature               | Int    | 19                     |
| current['pressure']         | The current pressure in hectopascals       | Float  | 1017                   |
| current['sea_level']        | The current sea level pressure in hpa      | Float  | None                   |
| current['wind_deg']         | The current wind directions in degree      | Float  | 90                     |
| current['wind_speed']       | The current wind speed in meter/seconds    | Float  | 0.69                   |
| current['humidity']         | The current humidity in percent            | Float  | 28                     |
| current['snowfall']         | The current snowfall volume                | Float  | None                   |
| current['rainfall']         | The current rainfall volume                | Float  | None                   |
| current['clouds_coverage']  | The current cloud coverage in percent      | Float  | 64                     |
|-----------------------------|--------------------------------------------|--------|------------------------|
| tomorrow['weather_status']  | The current weather conditions             | String | light rain             |
| tomorrow['temp']            | The tomorrow temperature                   | Int    | 16                     |            
| tomorrow['max_temp']        | The tomorrow max. temperature              | Int    | 17                     |            
| tomorrow['min_temp']        | The tomorrow min. temperature              | Int    | 8                      |
| tomorrow['morning_temp']    | The tomorrow temperature at the morning    | Int    | 8                      |
| tomorrow['evening_temp']    | The tomorrow temperature at the evening    | Int    | 14                     |
| tomorrow['night_temp']      | The tomorrow temperature at the night      | Int    | 11                     |
| tomorrow['pressure']        | The tomorrow pressure in hectopascals      | Float  | 859.78                 |            
| tomorrow['sea_level']       | The tomorrow sea level pressure in hpa     | Float  | None                   |            
| tomorrow['humidity']        | The tomorrow humidity in percent           | Float  | 61                     |            
| tomorrow['wind_deg']        | The tomorrow wind directions in degree     | Float  | None                   |            
| tomorrow['wind_speed']      | The tomorrow wind speed in meter/seconds   | Float  | 0.71                   |            
| tomorrow['snowfall']        | The tomorrow snowfall volume               | Float  | None                   |            
| tomorrow['rainfall']        | The tomorrow rainfall volume               | Float  | 26.88                  |            
| tomorrow['clouds_coverage'] | The tomorrow cloud coverage in percent     | Float  | 0                      |  
|-----------------------------|--------------------------------------------|--------|------------------------|
| today['weather_status']     | The weather conditions for the given day   | String | heavy intensity rain   |            
| today['temp']               | The expected temperature                   | Int    | 17                     |
| today['max_temp']           | The expected max. temperature              | Int    | 20                     |
| today['min_temp']           | The expected min. temperature              | Int    | 11                     |
| today['morning_temp']       | The expected temperature at the morning    | Int    | 20                     |
| today['evening_temp']       | The expected temperature at the evening    | Int    | 16                     |
| today['night_temp']         | The expected temperature at the night      | Int    | 11                     |
| today['humidity']           | The expected humidity in percent           | Float  | 63                     |
| today['wind_speed']         | The expected wind speed in meter/seconds   | Float  | 0.87                   |
| today['wind_deg']           | The expected wind directions in degree     | Float  | 163                    |
| today['pressure']           | The expected pressure in hectopascals      | Float  | 857.32                 |
| today['sea_level']          | The expected sea level pressure in hpa     | Float  | None                   |
| today['rainfall']           | The expected rainfall volume               | Float  | 13.76                  |
| today['snowfall']           | The expected snowfall volume               | Float  | None                   |

## Forecast
To get the forecast for each day of the week, replace today with: monday, tuesday, wednesday, thursday, friday, saturday or sunday

## Note:
It is possible that some data's are not available in this case it returns None


## Synapses example


```
  - name: "get-the-weather"
    signals:
      - order: "quel temps fait-il"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "fr"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template:
          - "Aujourd'hui a {{ location }} le temps est {{ today['weather_status'] }} avec une température de {{ today['temp'] }} degrés et demain le temps sera {{ tomorrow['weather_status'] }} avec une température de {{ tomorrow['temp']}} degrés"
```
Load the location from your order
```
  - name: "getthe-weather"
    signals:
      - order: "what is the weather in {{ location }}"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location: "{{ location }}"
          say_template:
          - "Today in {{ location }} the weather is {{ current['weather_status'] }} with a temperature of {{ current['temp'] }} degree and tomorrow the weather will be {{ tomorrow['weather_status'] }}  with a temperature of  {{ tomorrow['temp'] }} degree"
          
```
Forecast example for Monday
```
  - name: "weather-forecast-daily"
    signals:
      - order: "How is the weather on Monday"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          location: "{{ location }}"
          say_template: "The weather on Monday will be {{ monday['weather_status'] }} with temperatures from  {{ monday['min_temp'] }}  to  {{ monday['max_temp'] }} degree"
```
Forecast example for today at a given location
```
  - name: "weather-forecast-daily"
    signals:
      - order: "How will be the weather be today"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template: "The weather today will be {{ today['weather_status'] }} with temperatures from  {{ today['min_temp'] }}  to  {{ today['max_temp'] }} degree"
```

## Templates example 

```
Today in {{ location }} the weather is {{ current['weather_status'] }} with a temperature of  {{ current['temp'] }} degree
```

## Template and synapse example to get the forecast of a specific day with a single synapse

You need to translate all the days in the left column to your language in lowercase

```
{% set day_of_week = {
    "your_day_translation": "today",
    "your_day_translation": "monday",
    "your_day_translation": "tuesday",
    "your_day_translation": "wednesday", 
    "your_day_translation": "thursday",
    "your_day_translation": "friday",
    "your_day_translation": "saturday", 
    "your_day_translation": "sunday"
    }[day] | default("")
-%}


{% if "today" == day_of_week %} 
The weather today will be {{ today['weather_status'] }} with temperatures from {{ today['min_temp'] }} to {{ today['max_temp'] }} degree

{% elif "monday" == day_of_week %} 
The weather on Monday will be {{ monday['weather_status'] }} with temperatures from {{ monday['min_temp'] }} to {{ monday['max_temp'] }} degree

{% elif "tuesday" == day_of_week %} 
The weather on Tuesday will be {{ tuesday['weather_status'] }} with temperatures from {{ tuesday['min_temp'] }} to {{ tuesday['max_temp'] }} degree

{% elif "wednesday" == day_of_week  %} 
The weather on Wednesday will be {{ wednesday['weather_status'] }} with temperatures from {{ wednesday['min_temp'] }} to {{ wednesday['max_temp'] }} degree

{% elif "thursday" == day_of_week  %} 
The weather on Thursday will be {{ thursday['weather_status'] }} with temperatures from {{ thursday['min_temp'] }} to {{ thursday['max_temp'] }} degree

{% elif "friday" == day_of_week  %} 
The weather on Friday will be {{ friday['weather_status'] }} with temperatures from {{ friday['min_temp'] }} to {{ friday['max_temp'] }} degree

{% elif "saturday" == day_of_week  %} 
The weather on Saturday will be  {{ saturday['weather_status'] }} with temperatures from {{ saturday['min_temp'] }} to {{ saturday['max_temp'] }} degree

{% elif "sunday" == day_of_week  %} 
The weather on Sunday will be {{ sunday['weather_status'] }} with temperatures from {{ sunday['min_temp'] }} to {{ sunday['max_temp'] }} degree

{%else %}
    I could not find that day
{% endif %}

```

```
  - name: "wetter-forecast-daily"
    signals:
      - order: "what is the weather on {{ day }}"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          country: "FR"
          location: "Grenoble"
          day: "{{ day }}"
          file_template: "templates/daily_weather.j2" 
```

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
