import sys
from stats import *

sys.stdout.reconfigure(encoding="utf-8")
def main(file_path: str, cities_dict: dict):
    try:
        get = cities_dict.get ##TODO: рассказать почему ускоряет
        with open(file_path, "rb", buffering=8 * 1024 * 1024) as file:
            for line in file:
                city, _, temperature = line.partition(b";")
                temperature = int(temperature.replace(b".", b""))
                data = get(city)
                if data is None:
                    cities_dict[city] = StationStats(temperature)
                else:
                    data.update(temperature)
        cities_dict = {
            city.decode("utf-8"): data
            for city, data in cities_dict.items()
        }
        output = '\n'.join(
            f"{key};{cities_dict[key]}"
            for key in sorted(cities_dict))
        print(output)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")

if len(sys.argv)>1:
    file_path = sys.argv[1]
    cities_dict = {}
    main(file_path, cities_dict)
else:
    print(f"Ошибка: Файл не указан")

