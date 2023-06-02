__all__ = ["data_updater_th", "ExcelDataUpdater", "excel_data_updater_obj"]

from bot.utils.excel_data_updater import ExcelDataUpdater, excel_data_updater_obj
from threading import Thread


data_updater_th = Thread(target=excel_data_updater_obj.start_update)
data_updater_th.daemon = True
