import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import email
import os
import shutil
import logging
from consts import *


def send_email(sender_email=MAGDAD_MAIL, sender_password=MAGDAD_PASS,
               recipient_email=CLIENT_MAIL, cc_emails=None, subject="", message="",
               attachment_path=None):
    try:
        smtp_server = "smtp.office365.com"
        smtp_port = 587

        # Create the email message
        email = MIMEMultipart()
        email["From"] = sender_email
        email["To"] = recipient_email
        # if cc_emails:
        #   email["Cc"] = ", ".join(cc_emails)  # Join CC emails with comma separator

        email["Subject"] = subject

        # Attach the message to the email
        email.attach(MIMEText(message, "plain"))

        # Attach the file
        if attachment_path:
            attachment_filename = os.path.basename(attachment_path)

            attachment = open(attachment_path, "rb")
            mime_base = MIMEBase("application", "octet-stream")
            mime_base.set_payload((attachment).read())
            encoders.encode_base64(mime_base)
            mime_base.add_header("Content-Disposition", f"attachment; filename= {attachment_filename}")
            email.attach(mime_base)

        # Create a secure SSL/TLS connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        try:
            # Login to the email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, email.as_string())
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error("Failed to send email. "+str(e))
        finally:
        # Close the connection
            server.quit()
    except Exception as e:
        return


def sender():
    # Provide your email credentials and other details
    sender_email = MAGDAD_MAIL
    sender_password = MAGDAD_PASS
    recipient_email = CLIENT_MAIL
    attachment_path = "image.png"
    with open(height_file_path,'r') as f:
        height = f.read()
    subject = f"user report h = {height}"
    with open(LOGG, 'r') as file:
        log_content = file.read()

    # Format the log content
    message = f"Log Content:\n\n{log_content}"
    try:
        # Send the email
        send_email(sender_email=sender_email, sender_password=sender_password, recipient_email=recipient_email,
               subject=subject, message=message, attachment_path=attachment_path)
    except Exception as e:
        return

# recieve data file via mail
def download_attachment_with_subject(username="alinmagdad@outlook.com", password="yogev&0mri", subject=None,
                                     save_folder="PI/Media"):
    """

    :param username:

    :param password:
    :param subject:
    :param save_folder:
    :return:
    """
    # Connect to the Outlook IMAP server
    imap_server = "imap-mail.outlook.com"
    imap_port = 993
    connection = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Login to the email account
    connection.login(username, password)

    # Select the mailbox (e.g., "INBOX")
    mailbox = "INBOX"
    connection.select(mailbox)

    # Search for emails with the specified subject
    _, data = connection.search(None, f'(SUBJECT "{subject}")')
    email_ids = data[0].split()

    # Get the latest email with the specified subject
    latest_email_id = email_ids[-1]
    _, email_data = connection.fetch(latest_email_id, "(RFC822)")
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Iterate over email parts
    for part in email_message.walk():
        if part.get_content_maintype() == "multipart" and part.get("Content-Disposition") is None:
            continue
        if part.get("Content-Disposition") is not None:
            # Check if the part has an attachment
            filename = part.get_filename()
            if filename:
                # Remove the path from the filename
                filename = os.path.basename(filename)

                # Download the attachment
                save_path = os.path.join(save_folder, filename)
                with open(save_path, "wb") as f:
                    f.write(part.get_payload(decode=True))
                    logging.info("Attachment downloaded: "+save_path)
                break

    # Logout and close the connection
    connection.logout()


def receive_data():
    """

    :return:
    """
    # Provide your Outlook email credentials, the subject of the email, and the folder to save the attachment
    username = "alinmagdad@outlook.com"
    password = "yogev&0mri"
    subject = "testsubj"
    save_folder = "/Users/yogev/Desktop"  # todo  change this
    # Download the attachment from the most recent email with the specified subject
    download_attachment_with_subject(username, password, subject, save_folder)


# todo write a file into diskonkey

def check_and_copy_file(file_path, destination_folder):
    """

    :param file_path: file on rpi to copy
    :param destination_folder: where to put in flash
    :return:
    """
    # Get a list of mounted devices
    devices = os.listdir("/media/pi")

    # Iterate through the devices to find a flash drive
    for device in devices:
        device_path = os.path.join("/media/pi", device)
        if os.path.isdir(device_path):
            # Flash drive found, copy the file to the destination folder
            destination_path = os.path.join(device_path, destination_folder)
            shutil.copy2(file_path, destination_path)
            logging.info("File copied successfully.")
            return
    logging.warning("No flash drive found.")


def copy_file():
    # Specify the source file and destination folder
    source_file = "/path/to/source/file.txt"
    destination_folder = "/media/pi"  # Update with the desired destination folder

    # Check and copy the file to the flash drive
    check_and_copy_file(source_file, destination_folder)


# todo recieve input from keyboard
"""
maybe if keyboard conected then it can turn on wifi
send mail
recieve mail
"""

# todo recieve input from mouse and control with it
