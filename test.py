import json
filters_dir = "D:/Inventory-System/app/resources/config/filters.json"
try:
    with open(filters_dir, 'r') as f:
        settings = json.load(f)
        data = settings['backup_file_format']

        for format_key in data:
            for key, value in format_key.items():
                print(f'Key: {key} Value: {value}')
except Exception as e:
    print('Error')
