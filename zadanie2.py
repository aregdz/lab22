import argparse
from pathlib import Path


COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "DIR": "\033[94m",  # Синий
    "EXEC": "\033[92m",  # Зеленый
    "FILE": "\033[0m",  # Сброс цвета
    "SIZE": "\033[93m",  # Желтый
}


def format_size(size):
    """Форматирование размера файла/каталога для вывода."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / 1024 / 1024:.2f} MB"
    else:
        return f"{size / 1024 / 1024 / 1024:.2f} GB"


def tree(directory, max_depth=None, ignore=None, depth=0):
    """Отображение дерева каталогов."""
    directory_path = Path(
        directory
    )  # Преобразуем путь к каталогу в объект Path

    for item in sorted(
        directory_path.iterdir()
    ):  # Итерируемся по содержимому каталога
        if ignore and item.name in ignore:
            continue

        prefix = "|   " * (depth - 1) + "|-- " if depth > 0 else ""
        print(prefix, end="")

        if item.is_dir():  # Проверяем, является ли элемент каталогом
            print(
                f"{COLORS['DIR']}{COLORS['BOLD']}{item.name}{COLORS['RESET']}"
            )
            if max_depth is None or depth < max_depth:
                tree(
                    item, max_depth, ignore, depth + 1
                )  # Рекурсивно вызываем функцию для каталога
        else:
            size = item.stat().st_size
            print(
                f"{COLORS['FILE']}{item.name}{COLORS['RESET']}  ({COLORS['SIZE']}{format_size(size)}{COLORS['RESET']})"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Отображение дерева каталогов с использованием библиотеки pathlib"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Каталог для отображения дерева (по умолчанию текущий каталог)",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        help="Максимальная глубина отображения дерева",
    )
    parser.add_argument(
        "-i", "--ignore", nargs="+", help="Игнорируемые каталоги или файлы"
    )
    args = parser.parse_args()

    directory = args.directory
    max_depth = args.max_depth
    ignore = args.ignore

    tree(directory, max_depth, ignore)


if __name__ == "__main__":
    main()
