"""Generated class for event_mapping.json"""
from .common import Entry
from .building_config import BuildingConfig


class MappingEvent:
  """Generated schema class"""

  def __init__(self):
    self.timestamp = None
    self.version = None
    self.guid = None
    self.status = None
    self.translation = None

  @staticmethod
  def from_dict(source):
    if not source:
      return None
    result = MappingEvent()
    result.timestamp = source.get('timestamp')
    result.version = source.get('version')
    result.guid = source.get('guid')
    result.status = Entry.from_dict(source.get('status'))
    result.translation = BuildingTranslation.map_from(source.get('translation'))
    return result

  @staticmethod
  def map_from(source):
    if not source:
      return None
    result = {}
    for key in source:
      result[key] = MappingEvent.from_dict(source[key])
    return result

  @staticmethod
  def expand_dict(input):
    result = {}
    for property in input:
      result[property] = input[property].to_dict() if input[property] else {}
    return result

  def to_dict(self):
    result = {}
    if self.timestamp:
      result['timestamp'] = self.timestamp # 5
    if self.version:
      result['version'] = self.version # 5
    if self.guid:
      result['guid'] = self.guid # 5
    if self.status:
      result['status'] = self.status.to_dict() # 4
    if self.translation:
      result['translation'] = BuildingTranslation.expand_dict(self.translation) # 2
    return result
