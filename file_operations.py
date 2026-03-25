import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class FileOperations:
    def __init__(self, navigator):
        self.navigator = navigator
    
    def get_absolute_path(self, path):
        """Получение абсолютного пути"""
        if os.path.isabs(path):
            target = Path(path).resolve()
        else:
            target = (self.navigator.current_path / path).resolve()
        
        if self.navigator.restricted:
            try:
                target.relative_to(self.navigator.root_path)
                return target
            except ValueError:
                return None
        return target
    
    def create_directory(self, name):
        """Создание директории"""
        path = self.get_absolute_path(name)
        if path and not path.exists():
            path.mkdir(parents=True)
            return True, f"Директория '{name}' создана"
        return False, f"Не удалось создать директорию '{name}'"
    
    def delete_directory(self, name):
        """Удаление директории"""
        path = self.get_absolute_path(name)
        if path and path.is_dir():
            try:
                shutil.rmtree(path)
                return True, f"Директория '{name}' удалена"
            except Exception as e:
                return False, f"Ошибка удаления: {str(e)}"
        return False, f"Директория '{name}' не найдена"
    
    def create_file(self, name, content=""):
        """Создание файла"""
        path = self.get_absolute_path(name)
        if path and not path.exists():
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, f"Файл '{name}' создан"
            except Exception as e:
                return False, f"Ошибка создания: {str(e)}"
        return False, f"Файл '{name}' уже существует или путь недоступен"
    
    def read_file(self, name):
        """Чтение файла"""
        path = self.get_absolute_path(name)
        if path and path.is_file():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return True, content
            except Exception as e:
                return False, f"Ошибка чтения: {str(e)}"
        return False, f"Файл '{name}' не найден"
    
    def write_file(self, name, content):
        """Запись в файл"""
        path = self.get_absolute_path(name)
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, f"Данные записаны в файл '{name}'"
            except Exception as e:
                return False, f"Ошибка записи: {str(e)}"
        return False, f"Не удалось записать в файл '{name}'"
    
    def delete_file(self, name):
        """Удаление файла"""
        path = self.get_absolute_path(name)
        if path and path.is_file():
            try:
                path.unlink()
                return True, f"Файл '{name}' удален"
            except Exception as e:
                return False, f"Ошибка удаления: {str(e)}"
        return False, f"Файл '{name}' не найден"
    
    def copy_file(self, source, dest):
        """Копирование файла"""
        src_path = self.get_absolute_path(source)
        dest_path = self.get_absolute_path(dest)
        
        if src_path and src_path.is_file() and dest_path:
            try:
                if dest_path.is_dir():
                    dest_path = dest_path / src_path.name
                shutil.copy2(src_path, dest_path)
                return True, f"Файл скопирован в '{dest_path.name}'"
            except Exception as e:
                return False, f"Ошибка копирования: {str(e)}"
        return False, "Исходный файл не найден"
    
    def move_file(self, source, dest):
        """Перемещение файла"""
        src_path = self.get_absolute_path(source)
        dest_path = self.get_absolute_path(dest)
        
        if src_path and src_path.is_file() and dest_path:
            try:
                if dest_path.is_dir():
                    dest_path = dest_path / src_path.name
                shutil.move(str(src_path), str(dest_path))
                return True, f"Файл перемещен в '{dest_path.name}'"
            except Exception as e:
                return False, f"Ошибка перемещения: {str(e)}"
        return False, "Исходный файл не найден"
    
    def rename(self, old_name, new_name):
        """Переименование файла/директории"""
        old_path = self.get_absolute_path(old_name)
        new_path = self.get_absolute_path(new_name)
        
        if old_path and old_path.exists() and new_path and not new_path.exists():
            try:
                old_path.rename(new_path)
                return True, f"'{old_name}' переименован в '{new_name}'"
            except Exception as e:
                return False, f"Ошибка переименования: {str(e)}"
        return False, "Невозможно переименовать"