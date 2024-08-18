from dataclasses import fields, asdict
import logging

logger = logging.getLogger(__name__)

def from_dict(klass, d):
    try:
        fieldtypes = {f.name:f.type for f in fields(klass)}
        return klass(**{f:from_dict(fieldtypes[f],d[f]) for f in d})
    except Exception as e:
        logger.debug(f'Error converting dict to dataclass: {e}')
        return d # Not a dataclass field


def to_dict(object):
    return asdict(object)
