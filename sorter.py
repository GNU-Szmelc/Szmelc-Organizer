import os
import shutil
import yaml

# Load configuration from config.yml file
config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

# Get source directory from config
source_dir = config.get('source_directory')

if not source_dir:
    print("Source directory not specified in config.yml.")
    exit(1)

# Create target directories if they don't exist
for file_format, target_dir in config.items():
    if file_format != 'source_directory' and isinstance(target_dir, str):
        target_path = os.path.join(os.path.dirname(__file__), target_dir)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

# Helper function to resolve naming conflicts
def resolve_conflict(target_path):
    """
    Resolves naming conflicts by adding a numbering scheme to the target file.
    """
    base_name, file_format = os.path.splitext(target_path)
    counter = 1
    while os.path.exists(target_path):
        target_path = f"{base_name}-{counter}{file_format}"
        counter += 1
    return target_path

# Log recent activity
log = []

# Supported file formats and target directories from config
supported_formats = config.get('formats', [])
target_dirs = config
special_rules = config.get('special_rules', {})

# Function to search for files in directory and its subdirectories
def search_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_format = os.path.splitext(filename)[1]
            if file_format in supported_formats:
                target_dir = target_dirs.get(file_format)
                if target_dir is not None and isinstance(target_dir, str):
                    target_path = os.path.join(os.path.dirname(__file__), target_dir, filename)
                    if os.path.exists(target_path):
                        target_path = resolve_conflict(target_path)
                        log.append(f"Resolved naming conflict: {filename} -> {target_path}")
                    shutil.move(file_path, target_path)
                    log.append(f"Moved {filename} to {target_path}")
                else:
                    log.append(f"No target directory specified for file format: {file_format}")
            else:
                log.append(f"Ignored {filename} (unsupported file format)")

# Search for files in source directory and its subdirectories
search_files(source_dir)

# Delete empty directories inside source directory
for dirpath, dirnames, filenames in os.walk(source_dir, topdown=False):
    for dirname in dirnames:
        dir_path = os.path.join(dirpath, dirname)
        if not os.listdir(dir_path):
            os.rmdir(dir_path)
            log.append(f"Deleted empty directory: {dir_path}")

# Create logs folder if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Create new log file with unique name
log_file_path = os.path.join(logs_dir, 'log-1.txt')
counter = 1
while os.path.exists(log_file_path):
    counter += 1
    log_file_path = os.path.join(logs_dir, f'log-{counter}.txt')

# Save log to log file
with open(log_file_path, 'w') as log_file:
    log_file.write('\n'.join(log))

print("File sorting completed.")
