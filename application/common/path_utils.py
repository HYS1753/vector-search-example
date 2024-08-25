import os

class PathUtils:
    def __init__(self, current_dir):
        self.current_dir = current_dir

    def find_resource_dir(self):
        current_path = self.current_dir
        marker = 'resource'
        while current_path != os.path.dirname(current_path):
            if marker in os.listdir(current_path):
                return os.path.join(current_path, marker)
            current_path = os.path.dirname(current_path)
        return None
