import os
import shutil
from pathlib import Path

class Navigator:
    def __init__(self, root_path, restricted=True):
        self.root_path = Path(root_path).resolve()
        self.current_path = self.root_path
        self.restricted = restricted
        self.ensure_root_exists()
    
    def ensure_root_exists(self):
        """Создание корневой директории если не существует"""
        if not self.root_path.exists():
            self.root_path.mkdir(parents=True)
    
    def normalize_path(self, path):
        """Нормализация пути с учетом ограничений"""
        if os.path.isabs(path):
            target = Path(path).resolve()
        else:
            target = (self.current_path / path).resolve()
        
        if self.restricted:
            try:
                target.relative_to(self.root_path)
                return target
            except ValueError:
                return None
        return target
    
    def change_directory(self, path):
        """Смена текущей директории"""
        target = self.normalize_path(path)
        if target and target.is_dir():
            self.current_path = target
            return True
        return False
    
    def get_current_path(self):
        """Получение текущего пути"""
        return str(self.current_path)
    
    def list_directory(self):
        """Список содержимого директории"""
        items = []
        for item in self.current_path.iterdir():
            items.append({
                'name': item.name,
                'type': 'dir' if item.is_dir() else 'file',
                'size': self.get_size(item) if item.is_file() else 0,
                'modified': item.stat().st_mtime
            })
        return sorted(items, key=lambda x: (x['type'] != 'dir', x['name']))
    
    def get_size(self, path):
        """Получение размера файла"""
        return path.stat().st_size
    
    def go_home(self):
        """Переход в корневую директорию"""
        self.current_path = self.root_path
        return True
    
    def go_up(self):
        """Переход на уровень выше"""
        parent = self.current_path.parent
        if not self.restricted or parent.resolve() == self.root_path.resolve() or parent.resolve().is_relative_to(self.root_path):
            if parent.resolve() != self.current_path.resolve():
                self.current_path = parent
                return True
        return False