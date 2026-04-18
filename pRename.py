import os
import re
from datetime import datetime
import exifread
from alib3 import afile

KEY = {1: "DateTimeOriginal",
		2: "FileModifyDate",
		3: "CreationDate"}

def getImgPathList(folder_name, filter_=None):
	if filter_ == None:
		return afile.fileLstMaker(folder_name, deep=False)
	return afile.fileLstMaker(folder_name, deep=False, filter_=filter_)

def exif2FileName(date_exif):
	"""
	Accepts a datetime or a string like:
	  - "2021:11:20 16:47:13"
	  - "2021-11-20 16:47:13"
	  - "20211120 16:47:13"
	  - with optional timezone suffix like "+08:00"
	Returns formatted string: "YYMMDD HH-MM-SS"
	"""
	if isinstance(date_exif, datetime):
		dt = date_exif
	else:
		s = str(date_exif).strip()
		# remove timezone like +08:00, +0800 or trailing 'Z'
		s = re.sub(r'([+-]\d{2}:?\d{2})$','', s)
		s = s.rstrip('Z').strip()
		dt = None
		for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y%m%d %H:%M:%S"):
			try:
				dt = datetime.strptime(s, fmt)
				break
			except Exception:
				continue
		if dt is None:
			nums = re.findall(r'\d+', s)
			if len(nums) >= 6:
				try:
					y, m, d, H, M, S = map(int, nums[:6])
					dt = datetime(y, m, d, H, M, S)
				except Exception:
					dt = None
		if dt is None:
			return s
	return dt.strftime("%y%m%d %H-%M-%S")


def previewAndNewPath(img_path, key):
	if key == "DateTimeOriginal":
		with open(img_path, "rb") as f:
			tags = exifread.process_file(f, details=False)
		specific_exif = tags.get("EXIF DateTimeOriginal")
	elif key == "FileModifyDate":
		specific_exif = datetime.fromtimestamp(os.path.getmtime(img_path))
	elif key == "CreationDate":
		specific_exif = datetime.fromtimestamp(os.path.getctime(img_path))

	folder, fname = os.path.split(img_path)

	if specific_exif == None:
		print(fname + " -> *** UNABLE TO GET EXIF INFO ***")
		return None

	ext = os.path.splitext(img_path)[1]
	rename = exif2FileName(str(specific_exif)) + ext

	print("%s -> %s" % (fname, rename))
	new_path = os.path.join(folder, rename)
	return new_path


def execRename(origin_path, new_path):
	ctr = 2
	new_path_sure = new_path
	fpath, ext = os.path.splitext(new_path)
	while True:
		if os.path.exists(new_path_sure) and origin_path != new_path_sure:
			new_path_sure = fpath + "(%d)" % ctr + ext
			ctr += 1
		else:
			break
	if ctr > 2:
		print("<!> %s has been renamed as %s." % (os.path.split(new_path)[1], os.path.split(new_path_sure)[1]))
	os.rename(origin_path, new_path_sure)

def main():
	folder = input("Folder\n> ")
	extension = input("Extension (.jpg, .png, ...)\n> ")
	key = int(input('''Rename as
1. Date/Time Original
2. File Modify Date
3. CreationDate (for .MOV files)
> '''))
	if key not in KEY.keys():
		print("Unknown rule...")
		exit(0)

	img_path_list = getImgPathList(folder, [extension])

	renameDict = {}
	for i in img_path_list:
		new_path = previewAndNewPath(i, KEY[key])
		if new_path == None:
			continue
		renameDict[i] = new_path

	input("Press any key to rename...")
	for k in renameDict.keys():
		execRename(k, renameDict[k])
	input("Press any key to exit...")

if __name__ == '__main__':
	main()