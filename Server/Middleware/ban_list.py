from dataclasses import dataclass, field
from typing import List


@dataclass
class BanList(object):
    target_ban_list: List[str] = field(default_factory=list)

    async def add_ban(self, target: str):
        if target in self.target_ban_list:
            pass
        else:
            self.target_ban_list += str.split(target)

    async def remove_ban(self, target: str):
        if target in self.target_ban_list:
            self.target_ban_list.remove(target)
        else:
            pass


ban_list = BanList()


