__all__ = ["data_updater_th", "ExcelDataUpdater", "excel_data_updater_obj", "generate_preview_text", "send_email"]

from threading import Thread

from bot.utils.generate_preview import generate_preview_text
from bot.utils.excel_data_updater import ExcelDataUpdater, excel_data_updater_obj
from bot.utils.send_email import send_email


data_updater_th = Thread(target=excel_data_updater_obj.start_update)
data_updater_th.daemon = True
