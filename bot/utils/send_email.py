import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from bot.utils import excel_data_updater_obj


async def send_email(data: dict) -> None:
    """
    Отправка письма на электронную почту
    :param data:  Словарь с данными пользователя
    :return: None
    """
    # Авторизация на почтовом сервере
    smtp = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=465, use_tls=True)
    await smtp.connect()
    await smtp.login(os.getenv("GOOGLE_EMAIL"), os.getenv("GOOGLE_PASSWORD"))

    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = 'rentbotcar@gmail.com'
    msg['To'] = excel_data_updater_obj.get_region_email(region=data['REGION'])
    msg['Subject'] = 'Заявка на аренду!'

    # Создание текста сообщения
    body = f"""
    Регион:                 {data['REGION']}
    Имя пользователя:       {data['USER_REAL_NAME']}
    Номер телефона:         {data['PHONE_NUMBER']}
    Дата начала аренды:     {data['START_DATE']}
    Дата окончания аренды:  {data['END_DATE']}
    Кол-во дней аренды:     {data['RENT_DAYS']}
    Класс авто:             {data['CAR_CLASS'][1]}
    Модель авто:            {data['CAR_MODEL']}
    Стоимость аренды:       {data['RENT_PRICE']} rub.
    
    """
    msg.attach(MIMEText(body, 'plain'))

    # Отправка сообщения
    await smtp.send_message(msg)

    # Закрытие соединения с почтовым сервером
    await smtp.quit()
