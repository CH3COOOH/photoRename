# -*- coding: utf-8 -*-
# <-- AZLIBRARY PROJECT (Python2, 3) -->
# Started: 2018.02.02
# Latest: 2020.02.02

import os

# --- EXAMPLE ---
# <INPUT>
# fl = fileLstMaker('.', ['.jpg'])
# <OUTPUT>
# ['./a.jpg', './b.jpg', './test/c.jpg', './test/test2/d.jpg', ...]
# ---------------
def fileLstMaker(folder, deep=True, ext_filter=None, match_case=False, include_dir=True):
	# print('[Info] Building the file list of folder %s...' % folder)
	fileLst = []
	if deep:
		for root, dirs, files in os.walk(folder):
			for f in files:
				full_path = os.path.join(root, f)
				if include_dir == False and os.path.isfile(full_path) == False:
					continue
				fileLst.append(full_path)
	else:
		files = os.listdir(folder)
		for f in files:
			full_path = os.path.join(folder, f)
			if include_dir == False and os.path.isfile(full_path) == False:
				continue
			fileLst.append(full_path)

	if ext_filter != None:
		if match_case:
			fileLst = filter((lambda x: os.path.splitext(x)[-1] in ext_filter), fileLst)
		else:
			filter_lo = list(map((lambda p: p.lower()), ext_filter))
			fileLst = filter((lambda x: os.path.splitext(x)[-1].lower() in filter_lo), fileLst)
	return sorted(fileLst)

# --- EXAMPLE ---
# <INPUT>
# fl = multiFileLstMaker(['.', './test'], ['.jpg'])
# <OUTPUT>
# {'.': [fileLstMaker1], './test': [fileLstMaker2], ...}
# ---------------
def multiFileLstMaker(folders, filter_=None):
	fileLst = {}
	for folder in folders:
		fileLst[folder] = fileLstMaker(folder, filter_)
	return fileLst

# --- EXAMPLE ---
# <INPUT>
# fl = classifiedFileLst('.', ['.jpg'])
# <OUTPUT>
# {'.': [fLst1],
# './001': [fLst2],
# ...}
# ---------------
def classifiedFileLst(folder, filter_=None):
	fl = fileLstMaker(folder, filter_)
	csf = {}
	for p in fl:
		[folder, fname] = os.path.split(p)
		if folder in csf.keys():
			csf[folder].append(fname)
		else:
			csf[folder] = [fname]
	return csf