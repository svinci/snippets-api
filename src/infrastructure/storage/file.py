from pathlib import Path
import os, errno

def remove_file(directory_path: str, file_name: str) -> None:
    try:
        os.remove(f'{directory_path}/{file_name}')
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def file_exists(directory_path: str, file_name: str) -> bool:
    return os.path.exists(f'{directory_path}/{file_name}')


def ensure_file_exists(directory_path: str, file_name: str) -> None:
    if file_exists(directory_path, file_name):
        return

    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    
    path.joinpath(file_name).touch()


def get_files_in_directory(directory_path: str) -> list[str]:
    if not file_exists(directory_path, ''):
        return []

    return [
        f
        for f in os.listdir(directory_path) 
        if os.path.isfile(os.path.join(directory_path, f))
    ]
