import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://hop_bo:!2345hopbo0005432!@178.128.93.105/uta_hop_dev_db_000'
    MONGO_DBNAME = 'uta_mongo_hop_dev_db_000'
    MONGO_URI = 'mongodb://hop_bo:!2345hopbo0005432!@178.128.93.105/uta_mongo_hop_dev_db_000'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://hop_bo:!2345hopbo0005432!@178.128.93.105/uta_hop_dev_db_000'
    MONGO_DBNAME = 'uta_mongo_hop_dev_db_000'
    MONGO_URI = 'mongodb://hop_bo:!2345hopbo0005432!@178.128.93.105/uta_mongo_hop_dev_db_000'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://hop_bo:!2345hopbo0005432!@178.128.93.105/uta_hop_db_000'
    MONGO_DBNAME = 'uta_mongo_hop_db_000'
    MONGO_URI = 'mongodb://hop_bo:!2345hopbo0005432!@178.128.93.105/uta_mongo_hop_db_000'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.SANIC_MAIL_SENDER,
            toaddrs=[cls.SANIC_ADMIN],
            subject=cls.SANIC_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
