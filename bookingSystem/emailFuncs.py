from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from flask import render_template
import base64


class EmailFuncs:
    def __init__(self, emailAddress: str, emailAuth: str, emailProvider: str, emailPort: int) -> None:
        self.emailAddress = emailAddress
        self.emailAuth = emailAuth
        self.emailProvider = emailProvider
        self.emailPort = emailPort

    def sendHTMLMail(self, toAddress, subject, body, imageLocs: list[str] = None):
        msg = MIMEMultipart()
        msg['From'] = self.emailAddress
        msg['To'] = toAddress
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        if imageLocs is not None:
            for count, imageLoc in enumerate(imageLocs):
                with open(imageLoc, 'rb') as imageFile:
                    msgImage = MIMEImage(imageFile.read())
                    msgImage.add_header('Content-ID', f'<Attachment{count}>')

                    msg.attach(msgImage)

        try:
            with smtplib.SMTP(self.emailProvider, self.emailPort) as server:
                server.starttls()
                server.login(self.emailAddress, self.emailAuth)
                server.sendmail(self.emailAddress, toAddress, msg.as_string())
        except smtplib.SMTPRecipientsRefused:  # Catches test data addresses refusing the email - Removed in production
            pass

    def sendBookingConfirmation(self, toAddress: str, bookingObj: object, customer: object,
                                viewing: object, tickets: list):

        customer.Name = customer.getName()
        booking = vars(bookingObj)
        seats = bookingObj.getSelectedSeats()
        priceSum = bookingObj.getPriceSum()
        dateFormatted = viewing.getFormattedDate()

        qrLocs = [f'./static/assets/codes/{ticket.getID()}.png' for ticket in tickets]

        # imageEncodings = []
        # for qrLoc in qrLocs:
        #     with open(qrLoc, 'rb') as qrFile:
        #         encoded_string = base64.b64encode(qrFile.read()).decode('utf-8')
        #         imageEncodings.append(f'data:image/png;base64,{encoded_string}')

        # Renders the email body from Jinja template
        emailBody = render_template('./emailFormats/bookingConfirmed.html', booking=booking,
                                    dateFormatted=dateFormatted, seats=seats, tickets=tickets, viewing=viewing,
                                    customer=customer, priceSum=priceSum, qrLocs=qrLocs)

        self.sendHTMLMail(toAddress, 'Booking Confirmation', emailBody, qrLocs)
