from dataclasses import dataclass
from datetime import datetime, time, timezone, tzinfo
import os
from typing import List, Dict, Optional
from aiogram import utils
import pytz


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

    @classmethod
    def from_json(self, json: Dict):
        # Acknowledge timezones
        try:
            tz_str = os.getenv("TIMEZONE")
        except:
            raise Exception("No TIMEZONE env found!")
        tz = pytz.timezone(tz_str)

        return self(
            begin=tz.fromutc(datetime.fromisoformat(json['begin'][:-1]).astimezone(timezone.utc)),
            building=json['building'],
            code=json['code'],
            end=tz.fromutc(datetime.fromisoformat(json['end'][:-1]).astimezone(timezone.utc)),
            groups=json['groups'],
            name=json['name'],
            room=json['room'],
            type=json['type'],
            tutor=json['tutor']
        )


    def to_markdown(self) -> str:
        if self.type == "Wykład":
            markdown = "{} - {} | {}: {} (zdalny wykład na Teams)\n".format(
                time.isoformat(self.begin.time(), timespec='minutes'),
                time.isoformat(self.end.time(), timespec='minutes'),
                self.code,
                self.name
            )
        else:
            markdown = "{} - {} | {}: {} (sala {} w budynku {})\n".format(
                time.isoformat(self.begin.time(), timespec='minutes'),
                time.isoformat(self.end.time(), timespec='minutes'),
                self.code,
                self.name,
                self.room,
                self.building
            )
        return utils.markdown.escape_md(markdown)
