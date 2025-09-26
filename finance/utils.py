# finance/utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

# Function to generate a PDF invoice
def generate_invoice_pdf(invoice_obj):
    file_name = f"invoice_{invoice_obj.invoice_id}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # --- Simple Invoice Layout ---
    c.drawString(inch, height - inch, f"Invoice ID: {invoice_obj.invoice_id}")
    c.drawString(inch, height - 1.25*inch, f"Student: {invoice_obj.student}")
    c.drawString(inch, height - 1.5*inch, f"Amount: ${invoice_obj.amount}")
    c.drawString(inch, height - 1.75*inch, f"Status: {invoice_obj.status}")
    c.drawString(inch, height - 2.0*inch, f"Due Date: {invoice_obj.due_date.strftime('%Y-%m-%d')}")

    c.save()
    print(f"Generated {file_name}")
    return file_name

# Function to send an email (placeholder)
def send_email(to_address, subject, body):
    # IMPORTANT: Use environment variables for credentials in a real app
    from_address = "your_email@example.com"
    password = "your_email_password"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587) # Replace with your SMTP server
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")