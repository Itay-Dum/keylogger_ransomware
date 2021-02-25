import os

SEND_REPORT_EVERY = 10  # 10 minutes
EMAIL_ADDRESS = os.environ.get('EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')