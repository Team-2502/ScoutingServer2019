TEMP_TIMD_COMP_KEYS = {
    'A': 'matchNumber',
    'B': 'teamNumber',
    'C': 'assignmentMode',
    'D': 'scoutKey',
    'E': 'driversStation',
    'F': 'isReplay',
    'G': 'isNoShow',
    'H': 'startLevel',
    'I': 'preloadPiece',
    'J': 'leftHab',
    'K': 'actionType',
    'L': 'actionPlace',
    'M': 'actionTime',
    'N': 'actionPiece',
    'O': 'placeLevel',
    'P': 'wasDefended',
    'Q': 'cargoShipSide',
    'R': 'actualClimb',
    'S': 'attemptedClimb',
    'T': 'isDoubleClimb',
    'U': 'isTripleClimb',
    'V': 'assistedAnotherClimb',
    'W': 'wasAssistedClimb',
    'X': 'cause'
}
TEMP_TIMD_COMP_VALUES = {
    't': True,
    'f': False,
    'a': 'file',
    'b': 'override',
    'c': 'red1',
    'd': 'red2',
    'e': 'red3',
    'g': 'blue1',
    'h': 'blue2',
    'i': 'blue3',
    'j': 'hab1',
    'k': 'hab2',
    'l': 'cargo',
    'm': 'hatch',
    'n': 'none',
    'o': 'humanPlayerStation',
    'p': 'ground',
    'q': 'intake',
    'r': 'place',
    's': 'level1',
    'u': 'level2',
    'v': 'level3',
    'w': 'front',
    'x': 'side',
    'y': 'rocket',
    'z': 'cargoShip',
    'aa': 'drop',
    'ab': 'middleField',
    'ac': 'incap',
    'ad': 'recap',
    'ae': 'climb',
    'af': 'offense',
    'ag': 'defense',
    "ah": 'double placed',
    "ai": 'stuckOnCargo',
    "aj": 'disabled',
    "ak": 'tippedOver',
    "al": 'other'
}
SCOUT_NAME_VALUES = {
    "a": "Adhi",
    "v": "Aedin",
    "b": "Big Chief",
    "c": "Christian",
    "d": "Christopher",
    "e": "Danny",
    "f": "Drew",
    "g": "Evan",
    "s": "Isaac A",
    "y": "Isaac W",
    "p": "Ishan",
    "x": "Josie",
    "r": "Justin",
    "h": "Kyle",
    "q": "Michael",
    "t": "Miguel",
    "i": "Nathan",
    "j": "Neel",
    "k": "Nigel",
    "l": "Ravisha",
    "w": "Rahul",
    "m": "Riley",
    "n": "Ritik",
    "o": "Ryan",
    "u": "Other"
}


def decompress_timd(temp_timd):
    header, timeline = temp_timd.split("|")
    decompressed_header = decompress_header(header)
    team_number = decompressed_header.get('teamNumber')
    match_number = decompressed_header.get('matchNumber')
    if decompressed_header.get('isNoShow'):
        decompressed_timd = {'header': decompressed_header, 'team_number': team_number, 'match_number': match_number}
    else:
        decompressed_timeline = decompress_timeline(timeline)
        decompressed_timd = {'header': decompressed_header, 'timeline': decompressed_timeline, 'team_number': team_number, 'match_number': match_number}
    return decompressed_timd


def decompress_header(header):
    return decompress_action(header)


def decompress_timeline(timeline):
    compressed_timeline = timeline.split(",")
    decompressed_timeline = []
    for action in compressed_timeline:
        decompressed_action = decompress_action(action)
        decompressed_timeline.append(decompressed_action)
    return decompressed_timeline


def decompress_value(compressed_value):
    # Value is a compressed string
    if compressed_value.isalpha():
        return TEMP_TIMD_COMP_VALUES[compressed_value]
    # Value is a number, usually a time
    else:
        try:
            return int(compressed_value)
        # TODO Value is '', don't know what this is
        except ValueError:
            return compressed_value


def decompress_action(action):
    decompressed_action = {}
    last_key_index = 0
    for index, character in enumerate(action):
        # First character
        if index == 0:
            last_key_index = 0
        # Last character
        if index == len(action) - 1:
            compressed_value = action[last_key_index + 1:]
            value = decompress_value(compressed_value)
            compressed_key = action[last_key_index]
            key = TEMP_TIMD_COMP_KEYS[compressed_key]
            decompressed_action[key] = value
            last_key_index = index
        # TODO Prepare for having keys that are longer than one character
        # Next capital letter key
        elif character.isupper():
            compressed_key = action[last_key_index]
            key = TEMP_TIMD_COMP_KEYS[compressed_key]

            # Value from end of last key to this key
            compressed_value = action[last_key_index + 1:index]
            # Scout names stored in separate dictionary
            if key == 'scoutKey':
                value = SCOUT_NAME_VALUES[compressed_value]
            else:
                value = decompress_value(compressed_value)

            decompressed_action[key] = value
            last_key_index = index
    return decompressed_action
