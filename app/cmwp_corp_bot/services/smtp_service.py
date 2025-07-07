from aiosmtplib import send
from email.message import EmailMessage

from app.cmwp_corp_bot.settings import config


async def send_consult_email(
    full_name: str,
    tg_link: str,
    phone: str,
    company: str,
    context_text: str,
) -> None:
    msg = EmailMessage()
    msg["From"] = config.SMTP_USER
    msg["To"] = config.EMAIL_ADRESS
    msg["Subject"] = f"Запрос консультации от {full_name}"

    html = f"""
    <h3>💬 Запрос консультации</h3>
    <p><b>Имя:</b> {full_name}<br>
    <b>Телефон:</b> {phone or "—"}<br>
    <b>Компания:</b> {company or "—"}<br>
    <b>Профиль TG:</b> <a href="{tg_link}">{tg_link}</a></p>
    <hr>
    <h4>Сообщение клиента:</h4>
    <pre>{context_text}</pre>
    """

    msg.set_content("Ваш почтовый клиент не поддерживает HTML-формат.")
    msg.add_alternative(html, subtype="html")

    await send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        start_tls=True,
    )