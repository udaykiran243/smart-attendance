import smtplib
from email.message import EmailMessage
from .config import SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER

def send_verification_email(to_email: str, verification_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email for Smart Attendance"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    
    msg.set_content(
        f"""
Hi,

Click the link below to verify your email:

    {verification_link}
    
If you did not create this account, you can ignore this email.

Thanks,
Smart Attendance
      
      """  
    )
    
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)