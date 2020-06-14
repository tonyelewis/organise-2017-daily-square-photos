import hashlib
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

# from dataclasses_json import dataclass_json

@dataclass
class FileData:
	'''Class for TODOCUMENT'''

	# # TODOCUMENT
	# file: Path

	# TODOCUMENT
	size_in_bytes: int

	# TODOCUMENT
	modification_timestamp: float

	# TODOCUMENT
	md5: str

	# def total_cost(self) -> float:
	# 	return self.unit_price * self.quantity_on_hand


def size_and_time_of_file(file: Path) -> Tuple[int, float]:
	stat_info = os.stat(file)
	return (stat_info.st_size, stat_info.st_mtime)


def hash_of_file(file: Path) -> str:
	hasher = hashlib.md5()
	with open(file, 'rb') as afile:
		buf = afile.read()
		hasher.update(buf)
	return hasher.hexdigest()


def is_up_to_date(file_data: FileData, file: Path, *, context_dir: Path) -> bool:
	file_size, file_time = size_and_time_of_file(context_dir/file)
	return file_size == file_data.size_in_bytes and file_time == file_data.modification_timestamp


def up_to_datify(file_data: FileData, file: Path, *, context_dir: Path) -> FileData:
	file_size, file_time = size_and_time_of_file(context_dir/file)
	if file_size == file_data.size_in_bytes and file_time == file_data.modification_timestamp:
		return file_data
	return FileData(
		size_in_bytes=file_size,
		modification_timestamp=file_time,
		md5=hash_of_file(context_dir/file),
	)


def scan_file(file: Path, *, context_dir: Path) -> FileData:
	file_size, file_time = size_and_time_of_file(context_dir/file)
	return FileData(
		size_in_bytes=file_size,
		modification_timestamp=file_time,
		md5=hash_of_file(context_dir/file),
	)
