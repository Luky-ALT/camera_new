import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "jcaviirqsyunanvl" # The both are constants that cannot be changed
SENDER = "andrejovskylukas@gmail.com"
RECEIVER = "andrejovskylukas@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()    # thats the object equal to the class emailMessage
    email_message["Subject"] = "We showed up it"   # the subject of the sent email
    email_message.set_content("Hey, just somobody came to the room")  # it will shown in the email body

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content)) # imghrd defines the type of image contained in a file or byte stream

    # a need to create a gmail server

    gmail = smtplib.SMTP("smtp.gmail.com", 587)  #587 is a port for the server
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ =="__main__":
    send_email(image_path="images/19.png")