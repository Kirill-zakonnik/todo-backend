import os
import json
from typing import List

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, value):
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        with open(f"{path}/{self.title}.json", 'w', encoding='utf-8') as f:
            json.dump(self.json(), f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return cls.from_json(content)


def print_with_indent(value, indent=0):
    indentation = "\t" * indent
    print(indentation + str(value))


def entry_from_json(value: dict) -> Entry:
    new_entry = Entry(value['title'])
    for item in value.get('entries', []):
        new_entry.add_entry(entry_from_json(item))
    return new_entry


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []
        os.makedirs(self.data_path, exist_ok=True)

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)



    def load(self):
        for file_name in os.listdir(self.data_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.data_path, file_name)
                entry = Entry.load(file_path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)