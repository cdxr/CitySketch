# run setup of Flask app

def setup_env(app):
    # general
    app.secret_key = 'A0Zasdfsafdsjlfjadfs9892834234[,;234'

    # email
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USERNAME'] = 'citysketch@outlook.com'
    app.config['MAIL_PASSWORD']= '495team3'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
