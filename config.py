# settings.py
PASSWORD_CONFIG = {
    'MIN_LENGTH': 10,
    'COMPLEXITY': ['uppercase', 'lowercase', 'digits', 'special_characters'],
    'HISTORY': 3,
    'DICTIONARY': ['password', '123456', 'qwerty'],
    'LOGIN_ATTEMPTS': 3
}