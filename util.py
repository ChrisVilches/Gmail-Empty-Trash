import os


class Util:
    @staticmethod
    def file_lines_to_set(relative_filename):
        absolute_path = os.path.join(os.getcwd(), relative_filename)
        lines = open(absolute_path, encoding='UTF-8').read().split('\n')
        lines = list(filter(None, lines))  # Remove empty lines.
        return set(lines)

    @staticmethod
    def substring_of_any(sender, patterns):
        for pattern in patterns:
            if pattern in sender:
                return True
        return False
