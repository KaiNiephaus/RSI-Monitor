# RSI Monitor
 Small app that tracks RSI of a Stock and sends an email


# EStep by Step Guide: Monitor RSI and Create a Custom GPT for RSI Monitoring

This guide explains how to monitor the Relative Strength Index (RSI) for MicroStrategy Incorporated (MSTR), receive email alerts, and extend this functionality into a custom GPT using OpenAI’s GPT API.

---

## **1. What You Need**

### **1.1 Install Python**

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Download Python and install it. During installation, check the box that says "Add Python to PATH."
3. To confirm it works:
   - Open the Terminal (search "Terminal" on your Mac).
   - Type:
     ```bash
     python3 --version
     ```
   - If it shows a version number, you’re good to go.

### **1.2 Install Required Tools**

1. Open the Terminal.
2. Type the following command and press Enter:
   ```bash
   pip3 install yfinance pandas openai
   ```
3. This will set up tools needed to fetch financial data and interact with the OpenAI API.

---

## **2. Create the Email Notification System**

### **2.1 Write the Script**

1. Open Visual Studio Code (VS Code) and create a new file by clicking **File > New File**.
2. Copy and paste the following code into the file:

```python
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

# Send an email alert
def send_email_notification(rsi_value):
    sender_email = 'your_email@gmail.com'
    receiver_email = 'receiver_email@gmail.com'
    password = 'your_email_password'

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
    if rsi_value is None:
        print(f"RSI for {ticker} could not be calculated.")
        return

    print(f'Current RSI for {ticker}: {rsi_value:.2f}')
    if rsi_value < 70:
        send_email_notification(rsi_value)

if __name__ == '__main__':
    monitor_rsi()
```

3. Save this file as `rsi_monitor.py` on your desktop or a folder you can easily access.

---

### **2.2 Add Your Details**

1. Open the file `rsi_monitor.py` in VS Code.
2. Replace `your_email@gmail.com` with your Gmail address.
3. Replace `receiver_email@gmail.com` with the email where you want to receive alerts.
4. Replace `your_email_password` with your Gmail App Password. **Do not use your regular Gmail password**; instead, [generate an App Password](https://support.google.com/accounts/answer/185833?hl=en).
5. Save the file.

Now your script is ready to monitor RSI and send email notifications!

---

## **3. Extend the Functionality into a Custom GPT**

### **3.1 Set Up OpenAI API Access**

1. Go to [OpenAI](https://platform.openai.com/signup/) and create an account if you don’t already have one.
2. Generate an API key:
   - Log in to OpenAI and go to the API section.
   - Click **Create New Secret Key**.
   - Copy the key (you’ll need it in the next step).

### **3.2 Install Required Libraries**

Ensure you have the OpenAI Python library installed:

```bash
pip3 install openai
```

### **3.3 Modify the Script to Use OpenAI GPT API**

Update your script to include functionality for querying OpenAI’s GPT API. Add the following code to your script:

```python
import openai

def ask_gpt(prompt):
    openai.api_key = 'your_openai_api_key'
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error with GPT API: {e}")
        return None

# Example GPT prompt integration
def monitor_rsi_with_gpt():
    ticker = 'MSTR'
    rsi_value = get_latest_rsi(ticker)
    if rsi_value is not None and isinstance(rsi_value, (int, float)):
        print(f'Current RSI for {ticker}: {rsi_value:.2f}')
        if rsi_value < 70:
            send_email_notification(rsi_value)
            gpt_prompt = f"The RSI for {ticker} is {rsi_value:.2f}, below 70. What advice would you give an investor?"
            gpt_response = ask_gpt(gpt_prompt)
            print("GPT Response:", gpt_response)
    else:
        print(f'RSI for {ticker} could not be calculated.')
```

### **3.4 Test GPT Integration**

1. Save the script as `rsi_monitor_with_gpt.py`.
2. Run the script:
   ```bash
   python3 rsi_monitor_with_gpt.py
   ```
3. Check the output. If the RSI is below 70, the script will query OpenAI GPT for advice and print the response.

---

## **4. Deploy Your Custom GPT**

### **4.1 Use Flask to Create a Web Interface**

To make your custom GPT accessible, use Flask to create a simple web interface.

1. Install Flask:

   ```bash
   pip3 install flask
   ```

2. Create a new Python file `app.py` with the following code:

   ```python
   from flask import Flask, request, jsonify
   import openai

   app = Flask(__name__)

   openai.api_key = 'your_openai_api_key'

   @app.route('/ask', methods=['POST'])
   def ask():
       data = request.json
       prompt = data.get('prompt', '')
       try:
           response = openai.Completion.create(
               engine="text-davinci-003",
               prompt=prompt,
               max_tokens=150
           )
           return jsonify({'response': response.choices[0].text.strip()})
       except Exception as e:
           return jsonify({'error': str(e)})

   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. Run the Flask app:

   ```bash
   python3 app.py
   ```

4. Use a tool like Postman or cURL to send POST requests to `http://127.0.0.1:5000/ask` with a JSON body containing a `prompt` field.

### **4.2 Deploy on a Cloud Service**

- **Heroku**: Deploy your Flask app using Heroku for free cloud hosting.
- **AWS**: Use AWS Lambda with API Gateway to deploy serverless functions.
- **Google Cloud**: Deploy using Google Cloud Run for managed containers.

---

## **4.1 Automate GPT Monitoring Script**

### Using macOS Automator

1. Open the **Automator** app on your Mac (search for "Automator" in Spotlight).
2. Click **File > New**, then select **Application**.
3. In the search bar, type **Run Shell Script** and double-click it.
4. In the script box, type:
   ```bash
   python3 /path/to/rsi_monitor_with_gpt.py
   ```
   Replace `/path/to/rsi_monitor_with_gpt.py` with the full path to your script file.
5. Save the Automator application as `RSIMonitorGPT` on your desktop.
6. Open the **Calendar** app.
7. Create a new event at the time you want the script to run.
8. In the event, set **Alert > Custom > Open File**, then select the `RSIMonitorGPT` application you created.
9. Save the event, and your script will now run automatically at the scheduled time.

### Using a Cron Job (macOS/Linux)

1. Open your terminal.
2. Edit your crontab file:
   ```bash
   crontab -e
   ```
3. Add a new line to schedule the script. For example, to run the script daily at 9 AM:
   ```bash
   0 9 * * * python3 /path/to/rsi_monitor_with_gpt.py
   ```
   Replace `/path/to/rsi_monitor_with_gpt.py` with the full path to your script.
4. Save and exit the crontab editor.
5. Confirm the job was added:
   ```bash
   crontab -l
   ```

Your script will now run daily at 9 AM.

---

## **5. Automate GPT Responses**

Schedule the GPT-enhanced RSI monitoring script using macOS Automator (see step 4.1 in the main guide).
Alternatively, use a cron job or cloud scheduler to run the script periodically.

- Schedule the GPT-enhanced RSI monitoring script using macOS Automator (see step 4.1 in the main guide).
- Alternatively, use a cron job or cloud scheduler to run the script periodically.

---

## **6. Keep Things Running Smoothly**

- Regularly update your OpenAI library to access the latest features:
  ```bash
  pip3 install --upgrade openai
  ```
- Monitor GPT responses to ensure they align with your needs.
- Adjust your GPT prompts for better, more specific advice.

---

Congratulations! You’ve extended your RSI monitoring system into a custom GPT-powered assistant using OpenAI’s GPT API. 







