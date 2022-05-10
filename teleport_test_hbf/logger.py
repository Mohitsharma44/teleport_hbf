import os
import logging

def logger(logname, filename, level=logging.DEBUG, console=True):
    """
    Get logger object to stream logs to console and to the file

    Parameters
    ----------
    logname : str
        name for the logger
    filename : str
        path to the file to store the logs in
    level : logging.<levels>, optional
        logging level to use by default, by default logging.DEBUG
    console : bool, optional
        stream logs to console, by default True

    Returns
    -------
    _type_
        _description_
    """
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-5s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        filename=filename,
                        filemode='a')

    logger = logging.getLogger(logname)
    if console:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)-5s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M')
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger