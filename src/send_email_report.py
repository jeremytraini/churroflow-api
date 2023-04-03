import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(pdf_bytes, email):
    message = MIMEMultipart()
    churros_email = "churrotastic2021@gmail.com"
    churros_pass = "mupkteuwvswyyuxx"
    message['From'] = churros_email
    message['To'] = email
    message['Subject'] = 'Your PDF report'

    pdf = MIMEApplication(pdf_bytes, _subtype='pdf')
    pdf.add_header('Content-Disposition', 'attachment', filename='invoice.pdf')
    message.attach(pdf)
    text = f"""\
Hello,

Attached is the requested pdf of your validated invoice report by Churros.

Regards,
The Churros Team.
        """
    email_text = MIMEText(text, "plain")
    message.attach(email_text)

    context = ssl.create_default_context()
    port = 465
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(churros_email, churros_pass) 
        server.sendmail(churros_email, email, message.as_string())
    return




