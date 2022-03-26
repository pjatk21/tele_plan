from dataclasses import dataclass
from datetime import datetime, time
from typing import List,Dict, Optional
from aiogram import utils

@dataclass
class Entry:
    begin: datetime
    building: str
    code: str
    end: datetime
    groups: List[str]
    name: str
    room: str
    type: str
    tutor: Optional[str] = None
    

def to_markdown(entry: Entry) -> str:
    if entry.type == "Wykład":
        markdown = "{} - {} | {}: {} (zdalny wykład na Teams)\n".format(
            time.isoformat(entry.begin.time(),timespec='minutes'),
            time.isoformat(entry.end.time(),timespec='minutes'),
            entry.code,
            entry.name
            )
    else:
        markdown = "{} - {} | {}: {} (sala {} w budynku {})\n".format(
            time.isoformat(entry.begin.time(),timespec='minutes'),
            time.isoformat(entry.end.time(),timespec='minutes'),
            entry.code,
            entry.name,
            entry.room,
            entry.building
            )
    return utils.markdown.escape_md(markdown)

def from_json(json: Dict) -> Entry:
    value = Entry(
        begin=datetime.fromisoformat(json['begin'][:-1]),
        building=json['building'],
        code = json['code'],
        end=datetime.fromisoformat(json['end'][:-1]),
        groups=json['groups'],
        name=json['name'],
        room=json['room'],
        type=json['type'],
        tutor=json['tutor']
        )
    return value