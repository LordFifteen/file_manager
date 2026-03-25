import os
from pathlib import Path

class CommandHandler:
    def __init__(self, navigator, file_ops):
        self.navigator = navigator
        self.file_ops = file_ops
        self.commands = {
            'help': self.help,
            'ls': self.list_dir,
            'pwd': self.pwd,
            'cd': self.change_dir,
            'mkdir': self.make_dir,
            'rmdir': self.remove_dir,
            'touch': self.touch_file,
            'cat': self.cat_file,
            'echo': self.echo_file,
            'rm': self.remove_file,
            'cp': self.copy_file,
            'mv': self.move_file,
            'rename': self.rename_item,
            'home': self.go_home,
            'exit': self.exit_shell,
            'clear': self.clear_screen,
            'info': self.file_info
        }
    
    def execute(self, command_line):
        """Выполнение команды"""
        if not command_line.strip():
            return True
        
        parts = command_line.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in self.commands:
            try:
                return self.commands[cmd](*args)
            except Exception as e:
                print(f"Ошибка: {e}")
                return True
        else:
            print(f"Неизвестная команда: {cmd}. Введите 'help' для справки.")
            return True
    
    def help(self, *args):
        """Справка по командам"""
        print("\n=== Файловый менеджер - Справка ===\n")
        print("Навигация:")
        print("  pwd                 - показать текущую директорию")
        print("  ls [path]          - показать содержимое директории")
        print("  cd <path>          - перейти в директорию")
        print("  home                - перейти в рабочую директорию")
        print("\nРабота с директориями:")
        print("  mkdir <name>        - создать директорию")
        print("  rmdir <name>        - удалить директорию")
        print("\nРабота с файлами:")
        print("  touch <name>        - создать пустой файл")
        print("  cat <name>          - показать содержимое файла")
        print("  echo <name> <text>  - записать текст в файл")
        print("  rm <name>           - удалить файл")
        print("  cp <src> <dest>     - копировать файл")
        print("  mv <src> <dest>     - переместить файл")
        print("  rename <old> <new>  - переименовать файл/директорию")
        print("\nИнформация:")
        print("  info <name>         - информация о файле/директории")
        print("\nПрочее:")
        print("  clear               - очистить экран")
        print("  help                - показать эту справку")
        print("  exit                - выйти из программы")
        print()
        return True
    
    def list_dir(self, *args):
        """Вывод содержимого директории"""
        path = args[0] if args else "."
        items = self.navigator.list_directory()
        
        print(f"\nСодержимое: {self.navigator.get_current_path()}\n")
        print(f"{'Имя':<30} {'Тип':<6} {'Размер':<10} {'Изменен'}")
        print("-" * 70)
        
        for item in items:
            size = f"{item['size']} B" if item['size'] < 1024 else f"{item['size']/1024:.1f} KB"
            print(f"{item['name']:<30} {'[DIR]' if item['type'] == 'dir' else 'FILE':<6} {size:<10} {item['modified']}")
        print()
        return True
    
    def pwd(self, *args):
        """Показать текущую директорию"""
        print(self.navigator.get_current_path())
        return True
    
    def change_dir(self, *args):
        """Смена директории"""
        if not args:
            print("Укажите путь")
            return True
        
        if self.navigator.change_directory(args[0]):
            print(f"Перешли в: {self.navigator.get_current_path()}")
        else:
            print("Не удалось перейти в указанную директорию")
        return True
    
    def make_dir(self, *args):
        """Создание директории"""
        if not args:
            print("Укажите имя директории")
            return True
        
        success, message = self.file_ops.create_directory(args[0])
        print(message)
        return True
    
    def remove_dir(self, *args):
        """Удаление директории"""
        if not args:
            print("Укажите имя директории")
            return True
        
        confirm = input(f"Вы уверены, что хотите удалить директорию '{args[0]}'? (y/n): ")
        if confirm.lower() == 'y':
            success, message = self.file_ops.delete_directory(args[0])
            print(message)
        return True
    
    def touch_file(self, *args):
        """Создание файла"""
        if not args:
            print("Укажите имя файла")
            return True
        
        success, message = self.file_ops.create_file(args[0])
        print(message)
        return True
    
    def cat_file(self, *args):
        """Чтение файла"""
        if not args:
            print("Укажите имя файла")
            return True
        
        success, content = self.file_ops.read_file(args[0])
        if success:
            print("\n" + "="*50)
            print(content)
            print("="*50 + "\n")
        else:
            print(content)
        return True
    
    def echo_file(self, *args):
        """Запись в файл"""
        if len(args) < 2:
            print("Использование: echo <имя_файла> <текст>")
            return True
        
        filename = args[0]
        content = ' '.join(args[1:])
        success, message = self.file_ops.write_file(filename, content)
        print(message)
        return True
    
    def remove_file(self, *args):
        """Удаление файла"""
        if not args:
            print("Укажите имя файла")
            return True
        
        confirm = input(f"Вы уверены, что хотите удалить файл '{args[0]}'? (y/n): ")
        if confirm.lower() == 'y':
            success, message = self.file_ops.delete_file(args[0])
            print(message)
        return True
    
    def copy_file(self, *args):
        """Копирование файла"""
        if len(args) < 2:
            print("Использование: cp <источник> <назначение>")
            return True
        
        success, message = self.file_ops.copy_file(args[0], args[1])
        print(message)
        return True
    
    def move_file(self, *args):
        """Перемещение файла"""
        if len(args) < 2:
            print("Использование: mv <источник> <назначение>")
            return True
        
        success, message = self.file_ops.move_file(args[0], args[1])
        print(message)
        return True
    
    def rename_item(self, *args):
        """Переименование"""
        if len(args) < 2:
            print("Использование: rename <старое_имя> <новое_имя>")
            return True
        
        success, message = self.file_ops.rename(args[0], args[1])
        print(message)
        return True
    
    def go_home(self, *args):
        """Переход в домашнюю директорию"""
        self.navigator.go_home()
        print(f"Перешли в рабочую директорию: {self.navigator.get_current_path()}")
        return True
    
    def file_info(self, *args):
        """Информация о файле/директории"""
        if not args:
            print("Укажите имя файла/директории")
            return True
        
        path = self.file_ops.get_absolute_path(args[0])
        if path and path.exists():
            print(f"\nИнформация о: {path}")
            print(f"Тип: {'Директория' if path.is_dir() else 'Файл'}")
            print(f"Размер: {path.stat().st_size} байт")
            print(f"Создан: {path.stat().st_ctime}")
            print(f"Изменен: {path.stat().st_mtime}")
            if path.is_file():
                print(f"Расширение: {path.suffix}")
            print()
        else:
            print("Объект не найден")
        return True
    
    def clear_screen(self, *args):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
        return True
    
    def exit_shell(self, *args):
        """Выход из программы"""
        print("До свидания!")
        return False