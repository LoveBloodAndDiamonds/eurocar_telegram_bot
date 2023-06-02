__all__ = ["data_updater_th", "ExcelDataUpdater"]

from bot.utils.excel_data_updater import ExcelDataUpdater
from threading import Thread

excel_data_updater_obj = ExcelDataUpdater()
data_updater_th = Thread(target=excel_data_updater_obj.start_update)
data_updater_th.daemon = True
