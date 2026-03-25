import os
import configparser
from pathlib import Path

class Config:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Загрузка конфигурации из файла"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Создание конфигурации по умолчанию"""
        if not os.path.exists('workspace'):
            os.makedirs('workspace')
        
        self.config['Paths'] = {
            'working_directory': os.path.abspath('workspace')
        }
        self.config['Security'] = {
            'restrict_to_workspace': 'true'
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    @property
    def working_directory(self):
        return self.config['Paths']['working_directory']
    
    @property
    def restrict_to_workspace(self):
        return self.config.getboolean('Security', 'restrict_to_workspace')