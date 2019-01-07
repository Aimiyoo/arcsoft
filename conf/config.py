import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf/config.ini'))

if __name__ == '__main__':
    print(config.get('arcsoft', 'APP_ID'))
