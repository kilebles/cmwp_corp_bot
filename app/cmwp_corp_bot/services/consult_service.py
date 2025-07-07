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

    body = f"""\
        site^^
        og-bot.cmwp.ru
        ^^^^

        form-name^^
        plan
        ^^^^

        name^^
        {full_name}
        ^^^^

        phone^^
        {phone}
        ^^^^

        profile_tg^^
        {tg_link}
        ^^^^

        company^^
        {company}
        ^^^^

        comment^^
        {context_text}
        ^^^^
        """

    msg.set_content(body)

    await send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        start_tls=True,
    )
