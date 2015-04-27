import os.path
import sys
import yaml

from yclient.utils import a_logger, LOG_LEVELS

import yclient.biobank
import yclient.galaxy
import yclient.yrods


def load_config(config_file):
    with open(config_file) as cfg:
        conf = yaml.load(cfg)
    return conf


class ConfigurationFromYamlFile(object):
    """

    """
    def __init__(self, yaml_file, loglevel='INFO'):
        self.logger = a_logger(self.__class__.__name__, level=loglevel)
        if os.path.isfile(yaml_file):
            self.conf = load_config(yaml_file)
        else:
            self.logger.critical('{} not exists'.format(yaml_file))
            sys.exit()

    def get_aus_section(self, subsection=None):
        aus_section = self.get_section('aus')
        if subsection:
            if subsection in aus_section:
                return aus_section[subsection]
            else:
                self.logger.warning('section {} not found'.format(subsection))
                return ''
        else:
            return aus_section

    def get_galaxy_section(self, subsection=None):
        g_section = self.get_section('galaxy')
        if subsection:
            if subsection in g_section:
                return g_section[subsection]
            else:
                self.logger.warning('section {} not found'.format(subsection))
                return ''
        else:
            return g_section

    def get_io_section(self):
        io_section = self.get_section('io')
        if io_section:
            if 'opaths' in io_section:
                for op in io_section['opaths']:
                    if not os.path.isdir(op):
                        self.logger.critical('section {} not found'.format(op))
        return io_section

    def get_irods_section(self):
        return self.get_section('irods')

    def get_omero_section(self):
        return self.get_section('omero')

    def get_section(self, section_label):
        if self.is_section_present(section_label):
            return self.conf[section_label]
        else:
            self.logger.warning('section {} not found'.format(section_label))
            return ''

    def is_section_present(self, section_label):
        if section_label in self.conf:
            return True
        else:
            return False