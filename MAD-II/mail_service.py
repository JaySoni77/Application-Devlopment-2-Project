from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = "JAYYSONI@YAHOO.IN"
SENDER_PASSWORD = ""

def send_message (to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'plain'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()

def send_html_email(to, subject, html_content, attachment_path=None):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL

    # Attach the HTML content
    html_part = MIMEApplication(html_content, 'html')
    msg.attach(html_part)

    # Optionally, attach a file
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment_file:
                attachment = MIMEApplication(attachment_file.read(), _subtype="pdf")
                attachment.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
                msg.attach(attachment)
        except Exception as e:
            print(f"there is error in sending pdf{e}")

    # Connect to the SMTP server and send the email
    with SMTP(host=SMTP_HOST, port=SMTP_PORT) as client:
        client.send_message(msg)

# Example usage
# to_address = "recipient@example.com"
# email_subject = "HTML Report Email"
# html_report = "<html><body><h1>Your HTML Report</h1><p>This is the content of your HTML report.</p></body></html>"
# attachment_path = "/path/to/your/report/file.txt"

# send_html_email(to_address, email_subject, html_report)
# send_message("jaythadeshwar0@gmail.com", 'test', "plain msg testing")