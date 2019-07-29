def avg(lis, exception=0.0):
    """
    Shamelessly stolen almost verbatim from 1678
    Copyright (c) 2019 FRC Team 1678: Citrus Circuits

    Calculates the average of a list.

    lis is the list that is averaged.
    exception is returned if there is a divide by zero error. The
    default is 0.0 because the main usage in in percentage calculations.
    """
    lis = [item for item in lis if item is not None]
    if len(lis) == 0:
        return exception
    else:
        return round(sum(lis) / len(lis), 1)
