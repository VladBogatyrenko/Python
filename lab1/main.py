##from multiprocessing import Pool
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")
def BillionLinesTask(file_path: str, cities_dict: dict):
    try:
        with open(file_path, "r",encoding="utf-8") as file:
            for line in file:
                splited_str = line.split(";")
                city = splited_str[0]
                temperature = splited_str[1]
                fTemperature = float(temperature)
                if cities_dict.get(city) == None:
                    cities_dict[city] = [fTemperature, fTemperature, fTemperature, 1]
                else:
                    if fTemperature < cities_dict[city][0]:
                        cities_dict[city][0] = fTemperature
                    if fTemperature > cities_dict[city][2]:
                        cities_dict[city][2] = fTemperature
                    cities_dict[city][1] += fTemperature
                    cities_dict[city][3] += 1
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")


def PrintCities(cities_dict: dict):
    for key in cities_dict:
        print(
            f"{key};{cities_dict[key][0]};{round(cities_dict[key][1] / cities_dict[key][3], 1)};{cities_dict[key][2]}")


file_path = sys.argv[1]
cities_dict = {}
start_time = time.perf_counter()
BillionLinesTask(file_path, cities_dict)
end_time = time.perf_counter()
elapsed_time = end_time - start_time
PrintCities(cities_dict)
print(f"Прошло времени: {elapsed_time:.6f} сек.")
##"measurements_10m.txt"
