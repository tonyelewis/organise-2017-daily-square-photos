#!/usr/bin/env python3


# find ~/pictures -name Thumbs.db -o -name ZbThumbnail.info -o -iname .picasa.ini -print0 | xargs -0 -I VAR rm -f  VAR

# rm -rf volume1_tony_pictures/Photos/2012.08-KateAndMatthewAndTonyAndSandraWithMarnie
# rm -rf volume1_tony_pictures/Photos/2013.03-Cora


import datetime
import exifread
import hashlib
import json
import logging
import os
import sys

from os import walk
from pathlib import Path
from typing import Callable, List, Tuple

from organise.file_list import file_list_from_dir, print_file_list



# exit()

# profile_list_json_file = Path( 'profile-list.json' )

# profile_list_json_file = Path( 'profile-list.json' )

# with open( root_dir/image_file, 'rb') as image_filehd:
# 	tags = exifread.process_file(image_filehd)
# 	# print( repr( tags.keys() ) )
# 	print( tags[ 'Image DateTime'        ] )
# 	# print( tags[ 'EXIF DateTimeOriginal' ] )


# def recurse_get_matching_files(prm_root_dir: Path, prm_filter: Callable[[Path], bool]) -> List[Path]:
# 	def make_to_file(recurse_dir_and_file: Tuple[Path, str]) -> Path:
# 		(recurse_dir, file) = recurse_dir_and_file
# 		return Path(recurse_dir).relative_to(prm_root_dir) / file

# 	return sorted(
# 		filter(prm_filter,
# 					map(make_to_file,
# 						((Path(recurse_dir), file) for recurse_dir, _,
# 						 files in walk(prm_root_dir) for file in files)
# 						)
# 		 )
# 	)


# def is_a_picture_file(x: Path):
# 	if str(x).lower().endswith('.jpg'):
# 		return True
# 	return False


# def size_and_time_of_file(file: Path) -> Tuple[int, float]:
# 	stat_info = os.stat(file)
# 	return (stat_info.st_size, stat_info.st_mtime)


# def hash_of_file(file: Path) -> str:
# 	hasher = hashlib.md5()
# 	with open(file, 'rb') as afile:
# 		buf = afile.read()
# 		hasher.update(buf)
# 	return hasher.hexdigest()


# def profile_of_file(root_dir: Path, local_file: Path):
# 	file_size, file_time = size_and_time_of_file(root_dir/local_file)
# 	hash_str = hash_of_file(root_dir/local_file)
# 	return {
# 		'file_size': file_size,
# 		'file_time': file_time,
# 		'hash_str': hash_str,
# 		'local_file': str(local_file),
# 	}

# def updated_profile_list(profile_list:List[dict], root_dir: Path) -> List[dict]:
# 	image_files = recurse_get_matching_files(root_dir, is_a_picture_file)
# 	pass



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [ %(levelname)s ] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# data = []
# # image_files

# try:
# 	with open(profile_list_json_file) as read_profiles_fh:
# 		data = json.loads( read_profiles_fh.read() )
# except IOError:
# 	pass



root_dir = Path('/home/lewis/pictures')
# image_files = recurse_get_matching_files(root_dir, is_a_picture_file)


the_file_list = file_list_from_dir(
    root_dir,
    store_pickle_file=Path('/home/lewis/pictures.p'),
    checkpoint_frequency=500,
)
# print_file_list( the_file_list )


# for image_file in image_files:
# 	# hasher = hashlib.md5()
# 	# with open( root_dir/image_file, 'rb' ) as afile:
# 	# 	buf = afile.read()
# 	# 	hasher.update(buf)
# 	# hash_str = hasher.hexdigest()
# 	# data.append({
# 	# 	'path': image_file,
# 	# 	'hash': hash_str,
# 	# })
# 	# print( f'{hash_str} {image_file}' )

# 	file_size, file_time = size_and_time_of_file(root_dir/image_file)
# 	hash_str = hash_of_file(root_dir/image_file)

# 	profile = profile_of_file( root_dir, image_file )

# 	# print(
# 	# 	f'file_time={datetime.datetime.fromtimestamp(file_time)}, file_size={file_size}, {root_dir/image_file}')
# 	# print( json.dumps(os.stat(root_dir/image_file), indent=4, sort_keys=True))
# 	print(json.dumps(profile))
# 	data.append(profile)
# 	if len(data) > 15:
# 		break
# 	# exit()

# with open( profile_list_json_file, 'w' ) as write_profiles_fh:
# 	write_profiles_fh.write( json.dumps( data, indent=4, sort_keys=True ) )


# # datetime.datetime.fromtimestamp(file_time)


