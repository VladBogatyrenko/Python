import os.path
import sys
from stats import *
from multiprocessing import Pool
sys.stdout.reconfigure(encoding="utf-8")


def process_file_chunk(args) -> dict:
    local_dict = {}
    file_path, start_byte, end_byte = args
    get = local_dict.get  ##TODO: рассказать почему ускоряет
    with open(file_path, "rb", buffering=8 * 1024 * 1024) as file:
        if start_byte > 0:
            file.seek(start_byte - 1)
            if file.read(1) != b"\n":
                file.readline()
        cur_pos = file.tell()
        while cur_pos < end_byte:
            line = file.readline()
            if not line:
                break
            city, _, temperature = line.partition(b";")
            temperature = int(temperature.replace(b".", b""))
            data = get(city)
            if data is None:
                local_dict[city] = StationStats(temperature)
            else:
                data.update(temperature)
            cur_pos += len(line)
    return local_dict


def divide_file_to_chunks(file_path: str, num_chunks: int = 4) -> list:
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_chunks
    chunks = [0] * 4
    for i in range(num_chunks):
        start = i * chunk_size
        end = file_size if i == num_chunks - 1 else (i + 1) * chunk_size
        chunks[i] = (file_path, start, end)
    return chunks


def merge_two_dict(dict1: dict, dict2: dict) -> dict:
    if len(dict1) < len(dict2):
        dict1, dict2 = dict2, dict1

    for key, record in dict2.items():
        if key in dict1:
            dict1[key].merge(record)
        else:
            dict1[key] = record
    return dict1


def main(file_path: str)->None:
    cities_dict = {}
    try:
        f = open(file_path, 'r')
        f.close()
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return
    chuncks = divide_file_to_chunks(file_path)
    with Pool(processes=4) as pool:
        for temp_dict in pool.imap_unordered(process_file_chunk, chuncks):
            cities_dict = merge_two_dict(cities_dict, temp_dict)
    cities_dict = {
        city.decode("utf-8"): data
        for city, data in cities_dict.items()
    }
    output = '\n'.join(
        f"{key};{cities_dict[key]}"
        for key in sorted(cities_dict))
    print(output)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        main(file_path)
    else:
        print(f"Ошибка: Файл не указан")
