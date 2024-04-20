import os

def create_levels(base_path):
    # Убедимся, что базовый путь существует
    if not os.path.exists(base_path):
        print(f"Указанный путь {base_path} не существует.")
        return

    # Создаем папки с названием от level1 до level16
    for i in range(1, 17):
        folder_path = os.path.join(base_path, f'level{i}')
        os.makedirs(folder_path, exist_ok=True)
        print(f"Папка {folder_path} создана.")

# Укажите здесь желаемый путь
base_path = 'assets'
create_levels(base_path)
