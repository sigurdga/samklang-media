from django.core.files.storage import FileSystemStorage

import os

class UpdateIgnoreStorage(FileSystemStorage):

    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        """Replaces last part of filename with "original", saves it if it is
        not already saved, and makes a symlink to the intended filename. This
        way, a folder will have one real file, and one symlink for each
        uniquely given filename."""

        # replace basename with "original"
        filename = os.path.join(name.rsplit("/", 1)[0], "original")

        # save the file if it has not already been saved
        if not self.exists(filename):
            super(UpdateIgnoreStorage, self)._save(filename, content)

        # make symlink to the intended filename
        symlink_path = os.path.join(self.location, name)
        file_path = os.path.join(self.location, filename)
        if not os.path.exists(symlink_path):
            os.symlink(file_path, symlink_path)

        # return the symlink name given as method parameter: this is used in the database
        return name
