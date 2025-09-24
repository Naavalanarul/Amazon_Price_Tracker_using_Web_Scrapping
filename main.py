import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
import os

AMAZON_ENDPOINT = "https://www.amazon.in/Anker-Charging-PowerCore-Microsoft-MacBook/dp/B0CXDXP8VR/ref=sr_1_4?crid=166SHZTFSEKU8&dib=eyJ2IjoiMSJ9.b1qpF_CitUbn9azf2f_81rwApXPqtjIivuL3k5pqaMlLK2NHHqCu2HRFO77MjhY5RnPJE5ROSw37pNJcuuhRJ-VT2rJ2DSn8s6P3_GauuS2xolSOGXoKBZ3oeedcxBkskxWclG4uuMgH5ZELWU8b-b-0Mv1w2BKjj66PqfbC3GtW175-620kpKOYphcl3Rn7gw3b9SAtqwAhkTtB533AKKnAL5rQ0aCJJMIDXTVWVCPjlDBMiAmrXcugfBrHAAT-_r4hRRODxdNkH0DwOCpw6cmeFGEf4DXQGyUHcgq2RUM.F1ZjMw9HqjEg3XaRjOhV0C2Ebdw5yWusSFQbbcxz9Hc&dib_tag=se&keywords=powerbanks&qid=1758468574&refinements=p_36%3A420000-640000&rnid=1318502031&s=electronics&sprefix=pow%2Celectronics%2C263&sr=1-4&xpid=T0YPo5SGi00I6&th=1"
AMAZON_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
ALERT_PRICE = 4000
PRICE_TRACKER = []
CONNECTION_MAIL = os.environ.get("PERSONAL_MAIL")
CONNECTION_PASSWORD = os.environ.get("PERSONAL_PASSWORD")
TO_ADDRESS = os.environ.get("COLLEGE_MAIL")

response = requests.get(AMAZON_ENDPOINT, headers = AMAZON_HEADER)
soup = BeautifulSoup(response.text, 'html.parser')

product_name = soup.find('span', id = 'productTitle').get_text().strip()
price = soup.find('span', class_ = 'a-price-whole')
web_cost = ""
price_str = price.get_text()
for digit in price_str:
    if digit.isdigit():
        web_cost += digit

difference_percent = ((ALERT_PRICE - int(web_cost))/int(web_cost)) * 100

MAIN_MESSAGE = f"""Subject: 🎉 Price Drop Alert: Your watched item is now cheaper!

Body:

Hello User,

Good news! The price of the product you were tracking has just dropped.

📌 Product: {product_name}
🔥 New Price: ₹{web_cost}

👉 Grab it now before the offer ends: {AMAZON_ENDPOINT}

Happy Shopping!"""

MSG = MIMEText(MAIN_MESSAGE, _charset="utf-8")
MSG["From"] = CONNECTION_MAIL
MSG["To"] = TO_ADDRESS

if difference_percent < 10:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user = CONNECTION_MAIL, password = CONNECTION_PASSWORD)
        connection.sendmail(CONNECTION_MAIL, TO_ADDRESS, MSG.as_string())
        connection.close()

print("Program executed successfully.")