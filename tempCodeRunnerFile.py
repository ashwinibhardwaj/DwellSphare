app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email
        subject = 'Contact Form Submission'
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_email(subject, body)

        flash('Thank you for your message. We will get back to you soon.', 'success')

    return render_template('contact.html')

def send_email(subject, body):
    msg = Message(subject, recipients=['ashwini.10521@gmail.com'])
    msg.body = body
    mail.send(msg)