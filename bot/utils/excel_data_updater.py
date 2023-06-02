import logging
import os
import time

from dotenv import load_dotenv
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()


class ExcelDataUpdater:
    def __init__(self):
        self.json_file = '../sheets_google_credentials.json'  # Путь к вашему файлу json с данными аутентификации
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
                ]

                for values in find_values:
                    start = first_values.index(values[1])  # Находим открывающий тег
                    end = first_values.index(values[2])  # Находим закрывающий тег
                    # Создаем DataFrame на отрезке от открывающего тега до закрывающего
                    region_sorted_data[values[0]] = pd.DataFrame(region_data[start+2:end],
                                                                 columns=[name for name in region_data[start+1:end][0]])

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

    def get_available_regions(self) -> list:
        """
        :return: List of available regions
        """
        return [region for region in self.excel_data]


excel_data_updater_obj = ExcelDataUpdater()