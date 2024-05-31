import json

weather_api_spec ={
    'description': 'Get the current weather for `city_name`',
    'name': 'get_weather',
    'params': [{
        'description': 'The name of the city to be queried',
        'name': 'city_name',
        'required': True,
        'type': 'str'
    }]
}

exchange_rate_api_spec = {
    'description': 'Convert `base_num` of `base_currency` to `target_currency`, and return converted currency number.',
    'name': 'convert_currency',
    'params': [
        {
            'description': 'The amount in the base currency',
            'name': 'base_num',
            'required': True,
            'type': 'float'
        },
        {
            'description': 'The code of the base currency (e.g., "USD")',
            'name': 'base_currency',
            'required': True,
            'type': 'str'
        },
        {
            'description': 'The code of the target currency (e.g., "EUR")',
            'name': 'target_currency',
            'required': True,
            'type': 'str'
        }
    ]
}

date_api_spec = {
    'description': 'Get the current date, time, and weekday.If today is not Thusday, Please response today is not crazy Thusday in user language',
    'name': 'get_date',
}
