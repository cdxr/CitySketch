# run setup of Flask app

def setup_env(app):
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USERNAME'] = 'citysketch@outlook.com'
    app.config['MAIL_PASSWORD']= '495team3'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
