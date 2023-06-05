import logging
import os
import time

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class ExcelDataUpdater:
    def __init__(self):
        self.json_file = '../sheets_google_credentials.json'  # Путь к вашему файлу json с данными аутентификации
        # self.json_file = "sheets_google_credentials.json"
        self.file_id = os.getenv('GOOGLE_SHEETS_ID')  # Указываем айди документа на sheets.google.com
        self.scope = ['https://spreadsheets.google.com/feeds',  # Устанавливаем права доступа
                      'https://www.googleapis.com/auth/drive']

        # Авторизация
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.json_file, self.scope)
        self.client = gspread.authorize(self.creds)
        self.excel_data: dict = {}

    def __get_data_from_excel(self) -> dict:
        """
        :return: Возвращает соварь, в котором ключом является название региона, а значением - полная таблица
        региона из sheets.google
        """
        # Получаем гугл-документ.
        sheet = self.client.open_by_url(f'https://docs.google.com/spreadsheets/d/{self.file_id}')

        # Получаем список листов в таблице
        worksheet_list = sheet.worksheets()

        # Генерируем список регионов по названиям таблиц, исключая таблицу <rules>, в которой описаны правила.
        regions = [worksheet.title for worksheet in worksheet_list if worksheet.title != '<rules>']

        regions_data = {}

        # Читаем данные из каждого листа
        for worksheet in worksheet_list:
            # Читаем только данные, из выбранных регионов
            if worksheet.title in regions:
                # Заносим данные в один словарь, ключом к которому будет название региона
                regions_data[worksheet.title] = worksheet.get_all_values()

        return regions_data

    def __process_data(self, regions_data: dict):
        """
        Обрабатываем полученные данные.
        :param regions_data:  Полученные данные в виде словаря, которые уже отсортированы по регионам
        :return: Отсоритрованный словарь, по ключу региона определяется данные с каждой таблицы в виде словаря,
        словарь имеет три ключа: "tarriff_limit", "tariff_unlimit", "available_cars" подходящие под конкретный регион.
        """
        sorted_data = {}
        for region in regions_data:  # Проходимся циклом по каждому региону
            try:
                region_sorted_data = {}
                region_data = regions_data[region]
                first_values = [value[0] for value in region_data]  # Получаем первый столбик в каждой строчке, чтобы
                # в дальнейшем искать по ним теги <> и </> которыми я разделил таблицу на подтаблицы

                find_values = [  # Список кортежей для сортировки информации.
                    ("tarriff_limit", "<tariff_limit>", "</tariff_limit>"),
                    ("tariff_unlimit", "<tariff_unlimit>", "</tariff_unlimit>"),
                    ("available_cars", "<available_cars>", "</available_cars>"),
                    ("email", "<email>", "</email>")
                ]

                for values in find_values:
                    start = first_values.index(values[1])  # Находим открывающий тег
                    end = first_values.index(values[2])  # Находим закрывающий тег
                    # Создаем DataFrame на отрезке от открывающего тега до закрывающего
                    region_sorted_data[values[0]] = pd.DataFrame(region_data[start + 2:end],
                                                                 columns=[name for name in
                                                                          region_data[start + 1:end][0]])

                sorted_data[region] = region_sorted_data  # Добавляем данные в общий словарь

            except Exception as error:
                logging.error(f"Ошибка при добавлении региона {region}: {error}")

        self.excel_data = sorted_data

    def start_update(self, refresh_time: int or float = 600) -> None:
        """
        Updates table every {refresh_time} seconds.
        :param refresh_time: int or float, data refresh rate
        :return: None
        """
        while True:
            regions_data = self.__get_data_from_excel()
            self.__process_data(regions_data)
            time.sleep(refresh_time)

    def get_available_models(self, region: str, car_class: list, affiliated_brand: str = "Европкар"):
        """
        Функция, которая возвращает список доступных машин для выбранного региона.
        :param region: Выбранный пользователем регион, совпадает с названием гугл таблицы.
        :param car_class:  Список искомых классов авто, например ["EXMR", "PDAR", "FDAR"]
        :param affiliated_brand: Название аффилированного бренда
        :return: Список доступных машин для выбранного региона и класса авто. El: (car_model, spec, transmission,)
        """
        region_available_cars: pd.DataFrame = self.excel_data[region]['available_cars']
        # Выбор строки с нужным аффилированным брендом
        result = region_available_cars.loc[region_available_cars['Аffiliated brand'] == affiliated_brand]

        cars_list = []
        for spec in car_class:
            if spec[2] == "M":
                transmission = "MT"
            elif spec[2] == "A":
                transmission = "AT"

            table_cell = result.loc[0, spec]
            cars = table_cell.split(',')
            for car in cars:
                car_model = car.strip()
                if car_model != 'n/a':
                    cars_list.append((car_model, spec, transmission,))  # Очищаем строчку от пробелов, добавляем
                # информацию о категории авто и трансмиссии

        return cars_list

    def get_available_tariffs(self, region: str, tariff_type: str = "tarriff_limit") -> list:
        """
        Получение списка доступных тариффов
        :param region: Поиск таррифа в регионе
        :param tariff_type: Выбор типа тариффа, с лимитом пробега или без
        :return: Список доступных тариффов
        """
        region_tariff: pd.DataFrame = self.excel_data[region][tariff_type]
        return region_tariff.iloc[:, 0].values.tolist()

    def get_available_regions(self) -> list:
        """
        :return: List of available regions
        """
        return [region for region in self.excel_data]

    def get_price_by_options(self, region: str, car_class: str, tariff: int,
                             tariff_type: str = "tarriff_limit") -> float:
        """
        Возвращает цену аренды авто по выбранным параметрам
        :param region: Выбранный регион
        :param car_class:  Класс машины
        :param tariff: Выбранный тарифф
        :param tariff_type:  Тип тариффа (По названию таблицы)
        :return:
        """
        tariff_table: pd.DataFrame = self.excel_data[region][tariff_type]  # Получаем таблицу с тариффами
        tariff_table_dict = tariff_table.to_dict()["Tariffs"]
        for t in tariff_table_dict:
            tariff_index = t
            tariff_range: list = eval(tariff_table_dict[t])  # Преобразуем строку в список
            tariff_range_min = min(tariff_range)
            tariff_range_max = max(tariff_range)

            if tariff_range_min <= tariff <= tariff_range_max:
                break
        else:
            raise Exception('Wrong tariff!')
        # tariff_index = tariff_table.loc[tariff_table["Tariffs"] == tariff].index[0]  # Получаем индекс строчки
        # выбранного тариффа
        class_slice = tariff_table[car_class]  # Срезаем столбец с выбранным классом автомобиля
        price: str = class_slice[tariff_index]  # Получаем цену среза по индексу тариффа
        price = price.replace(',', '.').replace(' ', '')  # Убираем пробел и заменяем запятую на точку, чтобы
        # можно было преобразовать str в float

        return float(price) * tariff

    def get_region_email(self, region: str) -> str:
        """
        Returns region email
        :param region: Region name
        :return: region email
        """
        email: pd.DataFrame = self.excel_data[region]["email"]
        return email.columns.tolist()[0]


excel_data_updater_obj = ExcelDataUpdater()

if __name__ == '__main__':
    from threading import Thread

    Thread(target=excel_data_updater_obj.start_update).start()
    time.sleep(3)
    # excel_data_updater_obj.get_available_models(region="Москва", car_class=["EXMR", "PDAR", "FDAR"])
    # excel_data_updater_obj.get_available_tariffs(region='Москва')
    excel_data_updater_obj.get_price_by_options(region="Москва", car_class="EDMR", tariff='Сутки')
