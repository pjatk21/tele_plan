from dataclasses import dataclass
from datetime import datetime, time, timezone, tzinfo
import os
from typing import List, Dict, Optional
from aiogram import utils
import pytz


def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])


def bold(text):
    return f"\033[1m{text}\033[0m"

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
    tutors: Optional[List[str]] = None

    @classmethod
    def from_json(self, json: Dict):
        # Acknowledge timezones
        try:
            tz_str = os.getenv("TIMEZONE")
        except:
            raise Exception("No TIMEZONE env found!")
        set_tz = pytz.timezone(tz_str)

        utc_begin: datetime = datetime.fromisoformat(json['begin'][:-1]).astimezone(timezone.utc)
        utc_end: datetime = datetime.fromisoformat(json['end'][:-1]).astimezone(timezone.utc)

        tz_begin = utc_begin.astimezone(tz=set_tz)
        tz_end = utc_end.astimezone(tz=set_tz)

        return self(
            begin=tz_begin,
            building=json['building'],
            code=json['code'],
            end=tz_end,
            groups=json['groups'],
            name=json['name'],
            room=json['room'],
            type=json['type'],
            tutors=json['tutors']
        )


    def to_markdown(self) -> str:
        current_time = datetime.now().astimezone(timezone.utc)
        if self.type == "Wykład":
            markdown = "{} - {} | {}: {} (zdalny wykład na Teams)\n".format(
                time.isoformat(self.begin.time(), timespec='minutes'),
                time.isoformat(self.end.time(), timespec='minutes'),
                self.code,
                self.name
            )
        else:
            markdown = "{} - {} | {}: {} (sala {} w budynku {})\n".format(
                time.isoformat(self.end.time(), timespec='minutes'),
                time.isoformat(self.end.time(), timespec='minutes'),
                self.code,
                self.name,
                self.room,
                self.building
            )

        if current_time > self.end:
            markdown = utils.markdown.strikethrough(markdown)
            return markdown
        elif self.begin <= current_time <= self.end:
            markdown = "⭐ " + markdown
            markdown = utils.markdown.bold(markdown)
            return markdown

        return utils.markdown.escape_md(markdown)