from helpers.utils.decoder import check
from helpers.fileFormatters.fileHandler import dataToDict
from helpers.info.regexConditions import interface
def intFormatter(data, infc):
  (_,s) = check(data, interface["start"]).span()
  (e,_) = check(data, interface["end"]).span()
  value = dataToDict(interface["header"],data[s:e])
  result = list(filter(lambda interface: interface['Interface'] == infc, value))[0]
  return result