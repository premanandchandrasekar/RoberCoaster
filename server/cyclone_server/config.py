# coding: utf-8

import sys
import ConfigParser
import os
from cyclone.util import ObjectDict
import json

CONFIG_FILE_PATH = None


# FIXME: A better dirty hack
CONFIG_FILE_MAP = {'development': 'cyclone_server.conf'}


def config_file_path():
    if CONFIG_FILE_PATH is not None:
        return CONFIG_FILE_PATH
    cnt = 0
    dir_name = os.path.dirname(os.path.abspath(__file__))
    while True:
        l = os.listdir(dir_name)
        conf_name = CONFIG_FILE_MAP.get('development')
        
        if conf_name in l:
            return os.path.join(dir_name, conf_name)
        dir_name = os.path.abspath(os.path.join(dir_name, os.pardir))
        cnt += 1
        if dir_name == '/' or cnt > 4:
            break


def xget(func, section, option, default=None):
    try:
        return func(section, option)
    except:
        return default


def parse_config(filename=None):
    if filename is None:
        filename = config_file_path()
    global CONFIG_FILE_PATH
    if CONFIG_FILE_PATH is None and os.path.isfile(filename):
        CONFIG_FILE_PATH = os.path.abspath(filename)
    cfg = ConfigParser.RawConfigParser()
    with open(filename) as fp:
        cfg.readfp(fp)

    settings = {}

    # web server settings
    settings["debug"] = xget(cfg.getboolean, "server", "debug", False)
    settings["xheaders"] = xget(cfg.getboolean, "server", "xheaders", False)
    settings["enable_logging"] = xget(cfg.getboolean, "server",
                                      "enable_logging", False)

    settings["enable_caching"] = xget(cfg.getboolean, "server",
            "enable_caching", False)
    settings["base_url"] = cfg.get("server", "base_url")


    # get project's absolute path
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print root
    getpath = lambda k, v: os.path.join(root, xget(cfg.get, k, v))

    # locale, template and static directories' path
    settings["locale_path"] = getpath("frontend", "locale_path")
    settings["static_path"] = getpath("frontend", "static_path")
    settings["template_path"] = getpath("frontend", "template_path")
    settings["project_selection"] = cfg.get("frontend", "project_selection")

    # postgresql support
    if xget(cfg.getboolean, "postgresql", "enabled", False):
        settings["postgresql_settings"] = ObjectDict(
            host=cfg.get("postgresql", "host"),
            port=cfg.getint("postgresql", "port"),
            database=cfg.get("postgresql", "database"),
            poolsize=cfg.getint("postgresql", "poolsize"),
            username=cfg.get("postgresql", "username"),
            password=cfg.get("postgresql", "password")
        )
    else:
        settings["postgresql_settings"] = None

    # redis support
    if xget(cfg.getboolean, "redis", "enabled", False):
        settings["redis_settings"] = ObjectDict(
            host=cfg.get("redis", "host"),
            port=cfg.getint("redis", "port"),
            dbid=cfg.getint("redis", "dbid"),
            poolsize=cfg.getint("redis", "poolsize"),
        )
    else:
        settings["redis_settings"] = None

    settings['search_engine'] = ObjectDict(
        host=cfg.get('search_engine', 'host'),
        port=cfg.get('search_engine', 'port'),
        index=cfg.get('search_engine', 'index')     
        )


    return settings
