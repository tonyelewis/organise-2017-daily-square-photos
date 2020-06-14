import json
import pytest

from pathlib import Path

from organise.file_data import FileData, is_up_to_date, scan_file, up_to_datify

TEST_DIR = Path(__file__).parent.absolute() / 'example_data_dir'

LOCAL_FILE = Path( 'subdir/a' )


def test_scan_file():
	a_1 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '1' )
	assert a_1 == FileData( size_in_bytes=5, modification_timestamp=1592120187.7758024, md5='e5828c564f71fea3a12dde8bd5d27063' )
	a_2 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '2' )
	assert a_2 == FileData( size_in_bytes=5, modification_timestamp=1592120187.7758024, md5='225c72ad96dc54ca5ff5829c46b18544' )
	a_3 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '3' )
	assert a_3 == FileData( size_in_bytes=6, modification_timestamp=1592120187.7758024, md5='4c850c5b3b2756e67a91bad8e046ddac' )
	a_4 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '4' )
	assert a_4 == FileData( size_in_bytes=5, modification_timestamp=1592120209.2634983, md5='e5828c564f71fea3a12dde8bd5d27063' )


def test_is_up_to_date():
	a_1 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '1' )
	a_2 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '2' )
	a_3 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '3' )
	a_4 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '4' )

	assert is_up_to_date(a_1, LOCAL_FILE, context_dir=TEST_DIR / '1' )
	assert is_up_to_date(a_1, LOCAL_FILE, context_dir=TEST_DIR / '2' )
	assert not is_up_to_date(a_1, LOCAL_FILE, context_dir=TEST_DIR / '3' )
	assert not is_up_to_date(a_1, LOCAL_FILE, context_dir=TEST_DIR / '4' )


def test_up_to_datify():
	a_1 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '1' )
	a_2 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '2' )
	a_3 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '3' )
	a_4 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '4' )

	assert up_to_datify(a_1, LOCAL_FILE, context_dir=TEST_DIR / '1') == FileData( size_in_bytes=5, modification_timestamp=1592120187.7758024, md5='e5828c564f71fea3a12dde8bd5d27063' )
	assert up_to_datify(a_1, LOCAL_FILE, context_dir=TEST_DIR / '2') == FileData( size_in_bytes=5, modification_timestamp=1592120187.7758024, md5='e5828c564f71fea3a12dde8bd5d27063' )
	assert up_to_datify(a_1, LOCAL_FILE, context_dir=TEST_DIR / '3') == FileData( size_in_bytes=6, modification_timestamp=1592120187.7758024, md5='4c850c5b3b2756e67a91bad8e046ddac' )
	assert up_to_datify(a_1, LOCAL_FILE, context_dir=TEST_DIR / '4') == FileData( size_in_bytes=5, modification_timestamp=1592120209.2634983, md5='e5828c564f71fea3a12dde8bd5d27063' )


# def test_file_list():
# 	a_1 = scan_file( LOCAL_FILE, context_dir=TEST_DIR / '1' )
# 	assert json.dumps( { 'data': a_1 } ) == 'fred'
