# check-google-ip-ranges

<p>The Script checks every hour for changes in the official google ip list: https://www.gstatic.com/ipranges/goog.json
and sents an email with differences.</p>

<p>Just fill in your SMTP credentials in check_google_ip_changes.py and set 4 secrets in github settings: RECIPIENT_EMAIL, SENDER_EMAIL, SMTP_PASSWORD, SMTP_USERNAME</p>
