import os

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    msg['To'] = 'ayaz2000@mail.ru'
    msg['Subject'] = 'Заявка на аренду!'

    body = str(data)
    msg.attach(MIMEText(body, 'plain'))

    # Отправка сообщения
    await smtp.send_message(msg)

    # Закрытие соединения с почтовым сервером
    await smtp.quit()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email())
