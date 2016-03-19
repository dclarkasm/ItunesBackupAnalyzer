import os
import binascii
import sys
import string

f_types = {
	"sqlite":["SQLite format 3"],
	"plist":["bplist00", "plist", "PLIST"],
	"JPG":["ExifMM"],
	"png":["PNG"],
	"mov":["ftypqt"],
	"gif":["GIF89"],
	"jpg":["JFIF"],
}

t_count = {
	"sqlite":0,
	"plist":0,
	"JPG":0,
	"png":0,
	"mov":0,
	"gif":0,
	"jpg":0,
	"unknown":0
}

working_dir = os.path.dirname(__file__)

backup_path = os.path.join(working_dir, "85bd37e44606302177ba0ec6a21cd80b69b97637")
result_path = os.path.join(working_dir, "resulting_files")

f_list = os.listdir(backup_path)
print(backup_path)
total = 0
for f in f_list:
	file = open(os.path.join(backup_path, f), "rb")
	l = file.read()

	bs = ""
	for c in l:
		if chr(c) in string.printable:
			bs += chr(c)

	ffts = {}
	for t in f_types:
		for s in range(0, len(f_types[t])):
			fr = bs.find(f_types[t][s])
			if fr != -1:
				ffts[fr] = t

	print(f + ": " + str(ffts))
	file.close()
	total += 1

	restype = "unknown"
	rescnt = 9999999999999 	# an insanly high starting pos, so there is nowhere to go but down :)
	for t in ffts:
		if t < rescnt:
			restype = ffts[t]
			rescnt = t

	t_count[restype] += 1

	resdir = os.path.join(result_path, restype)
	if not os.path.exists(resdir):
		os.makedirs(resdir)
	rfile = None
	if restype == "unknown":
		rfile = open(os.path.join(resdir, f), "wb")
	else:
		rfile = open(os.path.join(resdir, f + "." + restype), "wb")
	rfile.write(l)
	rfile.close()

print("total files processed: " + str(total))
print("demographics:")
for t in t_count:
	print("\t" + t + ": " + str(t_count[t]))