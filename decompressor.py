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
    'U': 'isTripleClimb'
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
    'af': 'defenseStart',
    'ag': 'defenseEnd',
}

very_cool_timd = 'A37B1923CaDaEcFfGfHkIlJt|KrLyM146NlOvPf,KqLpM140Nl,KrLyM138NlOuPt,KqLoM135Nl,KrLyM134NlOsPf,KqLpM132Nm,KrLzM130NmOsQwPt,KqLoM128Nm,KaaLoM120NnPt,KqLoM116Nm,KrLzM115NmOsQxPt,KacM112,KadM110|M108RvSvTt'
def decompress_timd(temp_timd):
    header, timeline, climb = temp_timd.split("|")
    print(header)
    print(timeline)
    decompress_timeline(timeline)
    print(climb)

def decompress_timeline(timeline):
    compressed_timeline = timeline.split(",")
    print(compressed_timeline)
    decompressed_timeline = []
    for action in compressed_timeline:
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
                # Value from end of last key to this key
                compressed_value = action[last_key_index + 1:index]
                value = decompress_value(compressed_value)
                compressed_key = action[last_key_index]
                key = TEMP_TIMD_COMP_KEYS[compressed_key]
                decompressed_action[key] = value
                last_key_index = index
        decompressed_timeline.append(decompressed_action)
    print(decompressed_timeline)


def decompress_value(compressed_value):
    # Value is a compressed string
    if compressed_value.isalpha():
        return TEMP_TIMD_COMP_VALUES[compressed_value]
    # Value is a number, usually a time
    else:
        return compressed_value


def main():
    decompress_timd(very_cool_timd)

main()