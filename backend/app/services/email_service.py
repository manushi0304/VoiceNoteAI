import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:
    @staticmethod
    def is_configured() -> bool:
        return bool(settings.SMTP_HOST and settings.SMTP_FROM)

    @staticmethod
    def _send_sync(
        to_email: str,
        subject: str,
        body_text: str,
        body_html: str,
    ) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg.attach(MIMEText(body_text, "plain", "utf-8"))
        msg.attach(MIMEText(body_html, "html", "utf-8"))

        if settings.SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            if settings.SMTP_USE_TLS:
                server.starttls()

        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())
        server.quit()

    @staticmethod
    async def send_reminder_email(
        to_email: str,
        user_name: str | None,
        reminder_time_display: str,
        reminder_id: str,
    ) -> bool:
        if not EmailService.is_configured():
            print(
                "EMAIL SKIPPED | SMTP not configured "
                f"(set SMTP_HOST and SMTP_FROM in .env) | to={to_email}"
            )
            return False

        greeting = user_name or "there"
        subject = f"{settings.APP_NAME} — Reminder due"
        body_text = (
            f"Hi {greeting},\n\n"
            f"Your scheduled reminder is due ({reminder_time_display}).\n\n"
            f"Open VoiceNote AI to review your notes and todos.\n\n"
            f"— {settings.APP_NAME}"
        )
        body_html = f"""
        <html><body style="font-family:Segoe UI,Arial,sans-serif;color:#111;">
          <h2 style="color:#2563eb;">⏰ Reminder due</h2>
          <p>Hi {greeting},</p>
          <p>Your scheduled reminder for <strong>{reminder_time_display}</strong> is due now.</p>
          <p style="color:#64748b;font-size:13px;">Reminder ID: {reminder_id}</p>
          <p>— {settings.APP_NAME}</p>
        </body></html>
        """

        try:
            await asyncio.to_thread(
                EmailService._send_sync,
                to_email,
                subject,
                body_text,
                body_html,
            )
            print(f"EMAIL SENT | to={to_email} | reminder={reminder_id}")
            return True
        except Exception as exc:
            print(f"EMAIL FAILED | to={to_email} | error={exc}")
            return False
