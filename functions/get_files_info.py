import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(os.path.abspath(working_dir_abs), directory))
        valid_target_directory = os.path.commonpath([working_dir_abs, target_directory]) == working_dir_abs

        if not valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
    
        lines = []
        for name in os.listdir(target_directory):
            file_path = os.path.join(target_directory, name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            lines.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"