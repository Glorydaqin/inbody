#-*-coding:utf-8-*-
import os
import sys
import ConfigParser

def get_current_path():
    return os.path.split(os.path.realpath( sys.argv[0] ))[0]


def get_config(config_name):
    filepath = get_current_path() + "\license.ini"
    conf = ConfigParser.ConfigParser()
    res = conf.read(filepath)
    config_val = conf.get("config", config_name)

    return config_val