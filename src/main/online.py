#  Switcher, a tool for managing graphics and keymap profiles in games.
#  Copyright (C) 2020 Sam McCormack
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import Tuple, List

from github import Github

whitelist = ["TheGreatCabbage"]
g = Github()
template = "Switcher plugin for "


def find_online_plugins() -> Tuple[List, List]:
    plugins = search_plugins()
    for p in plugins:
        description = p.description

        if len(description) > len(template):
            game = description[len(template) : -1]
        else:
            game = description

        p.game = game

    trusted = [p for p in plugins if p.owner in whitelist]
    untrusted = [p for p in plugins if p not in trusted]

    _sort = lambda f: f.game
    trusted.sort(key=_sort)
    untrusted.sort(key=_sort)

    return trusted, untrusted


def search_plugins():
    repos = g.search_repositories(query="topic:switcher-plugin")
    return repos
