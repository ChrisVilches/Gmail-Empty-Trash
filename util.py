import os


class Util:
    @staticmethod
    def file_lines_to_set(relative_filename):
        absolute_path = os.path.join(os.getcwd(), relative_filename)
        lines = open(absolute_path, encoding='UTF-8').read().split('\n')
        lines = list(filter(None, lines))  # Remove empty lines.
        return set(lines)

    @staticmethod
    def contains_any(long_string, str_array):
        long_string = long_string.lower()
        for s in str_array:
            if s.lower() in long_string:
                return True
        return False
