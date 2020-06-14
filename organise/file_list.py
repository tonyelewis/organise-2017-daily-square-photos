import datetime
import logging
import os
import pickle
import shutil

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, KeysView, Optional, Set, Tuple
# from typing import Dict, Iterable, KeysView, List, Optional, Set, Tuple

from .file_data import FileData, scan_file, up_to_datify


class FileList:
	'''Class for TODOCUMENT'''

	def __init__(self):
		self.files_data: Dict[Path, FileData] = {}
		# if file_data_entries is not None:
		# 	self.files_data = list(file_data_entries)

	def __len__(self):
		return len(self.files_data.keys())

	def files(self) -> KeysView[Path]:
		return self.files_data.keys()

	def file_data_of_file(self, file: Path) -> FileData:
		return self.files_data[file]

	def insert_or_update(self, file: Path, file_data: FileData):
		self.files_data[file] = file_data

	def remove_file(self, file: Path):
		del self.files_data[file]


def remove_excess(*,
                  files: Set[Path],
                  file_list: FileList):
	excess_files = file_list.files() - files
	for excess_file in excess_files:
		file_list.remove_file(excess_file)


def check_and_update(file_list: FileList,
                     context_dir: Path,
					 ) -> FileList:
	for file in file_list.files():
		orig = file_list.file_data_of_file(file)
		fresh = up_to_datify(orig, file, context_dir=context_dir)
		if fresh != orig:
			file_list.insert_or_update(file, fresh)


def print_file_list(file_list: FileList):
	the_files = sorted(list(file_list.files()))
	index_width = len( f'{len(the_files)}' )
	for index, file in enumerate( the_files ):
		file_data = file_list.file_data_of_file( file )
		print( f'{index:>{index_width}} { file_data.md5 } {file_data.size_in_bytes:>8} {datetime.datetime.fromtimestamp(file_data.modification_timestamp)} {file}' )

def flag_duplicates(file_list: FileList):
	file_of_md5 = {}
	the_files = sorted(list(file_list.files()))
	for file in the_files:
		file_data = file_list.file_data_of_file( file )
		if file_data.md5 not in file_of_md5:
			file_of_md5[ file_data.md5 ] = []
		file_of_md5[ file_data.md5 ].append( file )

	dup_groups = []
	for md5, files in file_of_md5.items():
		if len( files ) > 1:
			dup_groups.append( files )
	dup_groups.sort( key=lambda x: (len(x), x[0]))

	for dup_group in dup_groups:
		for dup in dup_group:
			print(dup)
		print('')

	print('')
	print('')
	
	num_dups_per_dir = {}
	for dup_group in dup_groups:
		for dup in dup_group:
			if dup.parent not in num_dups_per_dir:
				num_dups_per_dir[ dup.parent ] = 0
			num_dups_per_dir[ dup.parent ] = num_dups_per_dir[ dup.parent ] + 1

	num_files_per_dir = {}
	for file in the_files:
		if file.parent in num_dups_per_dir:
			if file.parent not in num_files_per_dir:
				num_files_per_dir[ file.parent ] = 0
			num_files_per_dir[ file.parent ] = num_files_per_dir[ file.parent ] + 1
	
	frac_dups_per_dir_with_dups = {}
	for dir, num_dups in num_dups_per_dir.items():
		frac_dups_per_dir_with_dups[dir] = num_dups / num_files_per_dir[dir]
	
	sorted_dup_dirs = sorted(list(num_dups_per_dir.keys()), key=lambda x: frac_dups_per_dir_with_dups[x])
	for sorted_dup_dir in sorted_dup_dirs:
		print( f'{frac_dups_per_dir_with_dups[sorted_dup_dir]:5.3f} {sorted_dup_dir}' )

	for dup_group in dup_groups:
		dirs = set([ x.parent for x in dup_group])
		if ( len(list(dirs)) == 1):
			print( f'AAAAAAARRRRRRRGGGGGGGHHHHHHHH')
			for dup in dup_group:
				print( f"\t{dup}" )
			print( f'AAAAAAARRRRRRRGGGGGGGHHHHHHHH')
			print( f'')
			print( f'')
			# exit()

def file_list_from_files(files: Set[Path],
                         *,
                         context_dir: Path,
                         store_pickle_file: Optional[Path] = None,
                         checkpoint_frequency: Optional[int] = 200,
                         ) -> FileList:
	'''TODOCUMENT'''

	the_file_list = FileList()
	if store_pickle_file is not None and store_pickle_file.exists():
		with open(store_pickle_file, 'rb') as store_pickle_fh:
			the_file_list = pickle.load(store_pickle_fh)

	def checkpoint():
		if store_pickle_file is not None:
			logging.info( 'Checkpointing' )
			temp_pickle_file = store_pickle_file.parent / ( store_pickle_file.name + '.temp' )

			with open( temp_pickle_file, 'wb' ) as temp_pickle_fh:
				pickle.dump(the_file_list, temp_pickle_fh)

			shutil.move( temp_pickle_file, store_pickle_file )
			print_file_list( the_file_list )
			print('')
			print('')
			flag_duplicates( the_file_list )

	remove_excess(files=files, file_list=the_file_list)
	check_and_update(file_list=the_file_list, context_dir=context_dir)
	checkpoint()

	missing_files = files - the_file_list.files()
	counter = 0
	for missing_file in missing_files:
		the_file_list.insert_or_update(missing_file,scan_file(missing_file, context_dir=context_dir))
		counter = counter + 1
		if checkpoint_frequency is not None and counter % checkpoint_frequency == 0:
			checkpoint()

			print('')
			
			print( f'{100.0 * counter / len(missing_files):6.2f}% [ {counter} / {len(missing_files)} ]' )
			# exit()

	checkpoint()

	return the_file_list


def files_in_dir(dir: Path) -> Set[Path]:
	return set(
		Path(recurse_dir).relative_to(dir) / file
		for
		recurse_dir, _, files
		in
		os.walk(dir)
		for
		file
		in
		files
	)


def file_list_from_dir(dir: Path,
                       *,
                       store_pickle_file: Optional[Path] = None,
                       checkpoint_frequency: int = 200,
                       ) -> FileList:
	'''TODOCUMENT'''

	return file_list_from_files(
		files=files_in_dir(dir),
		context_dir=dir,
            store_pickle_file=store_pickle_file,
            checkpoint_frequency=checkpoint_frequency,
	)
