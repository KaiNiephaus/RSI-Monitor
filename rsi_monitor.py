import yfinance as yf
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fetch RSI (Relative Strength Index)
def get_latest_rsi(ticker):
    try:
        data = yf.download(ticker, period='1mo', interval='1d')
        if data.empty or 'Close' not in data:
            return None  # Ensure valid data
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1]) if not rsi.empty else None
    except Exception as e:
        print(f"Error calculating RSI: {e}")
        return None

def monitor_rsi():
    ticker = 'MSTR'
    rsi_value = get_latest_rsi(ticker)
    if rsi_value is None:
        print(f"RSI for {ticker} could not be calculated.")
        return

    print(f'Current RSI for {ticker}: {rsi_value:.2f}')
    if rsi_value < 70:
        send_email_notification(rsi_value)

# Send an email alert
def send_email_notification(rsi_value):
    sender_email = 'your email@domain.com'
    receiver_email = 'receiver_email@domain.com' 
    password = 'your dedicated app password, not your general account password'

    subject = f'MSTR RSI Alert: RSI is now {rsi_value:.2f}'
    body = f'The RSI for MSTR has dropped below 70. Current RSI: {rsi_value:.2f}.'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

# Main program to monitor RSI
def monitor_rsi():
    ticker = 'MSTR'
    rsi_value = get_latest_rsi(ticker)
    if rsi_value is not None and isinstance(rsi_value, (int, float)):
        print(f'Current RSI for {ticker}: {rsi_value:.2f}')
    else:
        print(f'RSI for {ticker} could not be calculated.')
    if rsi_value is not None and isinstance(rsi_value, (int, float)) and rsi_value < 70:
        send_email_notification(rsi_value)

if __name__ == '__main__':
    monitor_rsi()