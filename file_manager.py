from file_organizer import organize_files
from analyzer import analyze_folder


# Parent Class
class FileManager:

    def __init__(self, folder_path):
        # Public member
        self.folder_path = folder_path

        # Private member
        self.__last_analysis = None

    def organize(self):
        """Organize files inside the selected folder."""
        organize_files(self.folder_path)

    def analyze(self):
        """Analyze files inside the selected folder."""
        self.__last_analysis = analyze_folder(self.folder_path)

        return self.__last_analysis

    def get_total_files(self):
        """Return total number of files."""
        if self.__last_analysis is None:
            self.analyze()

        return self.__last_analysis[0]

    def get_analysis(self):
        """Return the complete analysis."""
        if self.__last_analysis is None:
            self.analyze()

        return self.__last_analysis


# Child Class
class AdvancedFileManager(FileManager):

    def organize(self):
        """Organize files using the inherited FileManager."""
        print("Advanced FileManager: Organizing files...")
        super().organize()
        print("Advanced FileManager: Organization completed.")