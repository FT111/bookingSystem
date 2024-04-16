from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template


class EmailFuncs:
    def __init__(self, emailAddress: str, emailAuth: str, emailProvider: str, emailPort: int) -> None:
        self.emailAddress = emailAddress
        self.emailAuth = emailAuth
        self.emailProvider = emailProvider
        self.emailPort = emailPort

    def sendHTMLMail(self, toAddress, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.emailAddress
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(self.emailProvider, self.emailPort) as server:
            server.starttls()
            server.login(self.emailAddress, self.emailAuth)
            server.sendmail(self.emailAddress, toAddress, msg.as_string())

    def sendBookingConfirmation(self, email, booking: object, viewing: object, seats: list, tickets: list):

        # Renders the email body from Jinja template
        emailBody = render_template('./emailFormats/bookingConfirmed.html', booking=booking,
                                    seats=seats, tickets=tickets, viewing=viewing)

        self.sendHTMLMail(email, 'Booking Confirmation', emailBody)
