import os

DEPT_ARRAY = []
DEPT_FILE_PATH = os.environ.get('BASE_DIR') + "/deptcodes.txt"

try:
    with open(DEPT_FILE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                DEPT_ARRAY.append(parts)
except FileNotFoundError:
    print('Unable to load deptcodes.txt')
    # If the file doesn't exist, DEPT_ARRAY will be empty,
    # and lookupcode will return '\n'.
    pass

def lookupcode(search_string: str) -> str:
    """
    Looks for a department code within the search_string and returns the
    corresponding department name.

    Args:
        search_string: The string to search within.

    Returns:
        The department name if found, otherwise a newline character.
    """
    for item in DEPT_ARRAY:
        code = item[0]
        name = item[1]
        if code in search_string:
            return name

    return "\n"
