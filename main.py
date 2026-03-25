#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from navigation import Navigator
from file_operations import FileOperations
from commands import CommandHandler

class FileManager:
    def __init__(self):
        """Инициализация файлового менеджера"""
        print("Загрузка файлового менеджера...")
        
        # Загрузка конфигурации
        self.config = Config()
        
        # Инициализация навигации
        self.navigator = Navigator(
            self.config.working_directory,
            self.config.restrict_to_workspace
        )
        
        # Инициализация файловых операций
        self.file_ops = FileOperations(self.navigator)
        
        # Инициализация обработчика команд
        self.command_handler = CommandHandler(self.navigator, self.file_ops)
        
        print(f"Рабочая директория: {self.navigator.get_current_path()}")
        print("Введите 'help' для справки")
    
    def run(self):
        """Запуск основного цикла программы"""
        running = True
        
        while running:
            try:
                # Отображение приглашения
                prompt = f"\n{self.navigator.get_current_path()}> "
                
                # Ввод команды
                command = input(prompt).strip()
                
                # Выполнение команды
                running = self.command_handler.execute(command)
                
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                running = False
            except Exception as e:
                print(f"Непредвиденная ошибка: {e}")
                running = False

def main():
    """Точка входа"""
    try:
        manager = FileManager()
        manager.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()