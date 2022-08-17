import os
from alib3 import afile


## Please download ExifTool from https://exiftool.org/
if os.name == "nt":
	PATH_EXIFTOOL = "exiftool"
else:
	PATH_EXIFTOOL = "./exiftool"
KEY = {1: "DateTimeOriginal",
		2: "FileModifyDate",
		3: "CreationDate"}

def getImgPathList(folder_name, filter_=None):
	if filter_ == None:
		return afile.fileLstMaker(folder_name, deep=False)
	return afile.fileLstMaker(folder_name, deep=False, filter_=filter_)


def getEXIFfromImg(img_path, key):
	p = os.popen("%s -s -FileTypeExtension -%s \"%s\"" % (PATH_EXIFTOOL, key, img_path))
	raw_exif = p.read()
	p.close()
	return raw_exif


def getSpecificEXIFfromEXIF(raw_exif):
	try:
		extension, specific_exif = raw_exif.split("\n")[:-1]
		extension = "." + extension.split(" : ")[1]
		specific_exif = specific_exif.split(" : ")[1]
	except:
		return None
	return extension, specific_exif


def exif2FileName(date_exif):
	## date_exif = '2020:01:23 21:36:24'
	idx_char_plus = date_exif.find("+")
	if idx_char_plus >= 0:
		date_exif = date_exif[:idx_char_plus]
	d, t = date_exif.split(" ")
	d = d[2:].replace(":", "")
	t = t.replace(":", "-")
	return d + " " + t


def previewAndNewPath(img_path, key):
	raw_exif = getEXIFfromImg(img_path, key)
	_ = getSpecificEXIFfromEXIF(raw_exif)
	folder, fname = os.path.split(img_path)

	if _ == None:
		print(fname + " -> *** UNABLE TO GET EXIF INFO ***")
		return None
	
	ext = _[0]
	specific_exif = _[1]

	rename = exif2FileName(specific_exif) + ext

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