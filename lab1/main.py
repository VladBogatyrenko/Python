import sys

sys.stdout.reconfigure(encoding="utf-8")
def BillionLinesTask(file_path: str, cities_dict: dict):
    try:
        get = cities_dict.get
        with open(file_path, "rb", buffering=8 * 1024 * 1024) as file:
            for line in file:
                city, _, temperature = line.partition(b";")
                temperature = int(temperature.replace(b".", b""))
                data = get(city)
                if data is None:
                    cities_dict[city] = [temperature, temperature, temperature, 1]
                else:
                    if temperature < data[0]:
                        data[0] = temperature
                    if temperature > data[2]:
                        data[2] = temperature
                    data[1] += temperature
                    data[3] += 1
        cities_dict = {
            city.decode("utf-8"): data
            for city, data in cities_dict.items()
        }
        output = '\n'.join(
            f"{key};{cities_dict[key][0] / 10};{round(cities_dict[key][1] / cities_dict[key][3] / 10, 1)};{cities_dict[key][2] / 10}"
            for key in sorted(cities_dict))
        print(output)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")

try:
    file_path = sys.argv[1]
except IndexError:
    print(f"Ошибка: Файл не указан")
cities_dict = {}
BillionLinesTask(file_path, cities_dict)
