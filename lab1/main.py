##from multiprocessing import Pool
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")
def BillionLinesTask(file_path: str, cities_dict: dict):
    try:
        with open(file_path, "r",encoding="utf-8", buffering=1024*1024) as file:
            for line in file:
                city,temperature =  line.split(";")
                fTemperature = float(temperature)
                if not(city in cities_dict):
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
    output='\n'.join(f"{key};{cities_dict[key][0]};{round(cities_dict[key][1] / cities_dict[key][3], 1)};{cities_dict[key][2]}" for key in sorted(cities_dict))
    print(output)


file_path = sys.argv[1]
cities_dict = {}
start_time = time.perf_counter()
BillionLinesTask(file_path, cities_dict)
PrintCities(cities_dict)
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Прошло времени: {elapsed_time:.6f} сек.")
##"measurements_10m.txt"
