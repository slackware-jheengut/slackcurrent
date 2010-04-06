#!/usr/bin/python
import os
import re
import sys
import glob
import time
import types
import string 
import urllib

# some global vars
_slackcurrent_rc_regex = re.compile("rc[0-9_]{1,3}$")
_slackcurrent_ve_regex = re.compile("([a-z])")
_slackcurrent_rc_like  = {"pre":0,"pl":0,"alpha":0,"beta":100,"rel.":0}
_slackcurrent_lowercase= [c for c in string.lowercase]

# app data
__author__ 	= "Eustaquio 'TaQ' Rangel (eustaquiorangel AT yahoo.com)"
__version__	= "0.1.7"
__date__		= "$Date: 2008/03/04 12:00:00$"

# some paths
localpath = "/var/log/packages/"
confpath  = "/etc/slackcurrent/"

#---------------------------------------------------------------------------#
# Class to store info about a package, like name, version, architeture and  #
# build version                                                             #
#---------------------------------------------------------------------------#
class SlackPack:
	""" 
		Create an object with the package info
		The filename MUST have four tokens (returned splitting the file name
		using the '-' delimiter char).
	"""
	def __init__(self,file):
		try:
			self.cversion	= -1
			self.fullpath	= file
			self.file		= file
			self.path		= ""

			# finds the last / position to get the file name
			pos = string.rfind(file,"/")
			if pos>=0:
				self.path = string.strip(file[0:pos])
				self.file = string.strip(file[pos+1:])

			# parse the file name to get it's properties
			tokens = string.split(self.file,"-")

			# needs at least 4 tokens for a valid package
			if(len(tokens)<4):
				throw
			
			self.build		= self.get_build_value(tokens[-1])
			self.arch		= tokens[-2]
			self.version	= tokens[-3]
			self.name		= string.replace(string.join(tokens[0:len(tokens)-3])," ","-")
			self.cversion	= self.make_version()				
			self.valid		= True	
		except StandardError,e:			
			# print "Invalid package path/name: "+self.file
			self.build		= "0"
			self.arch		= "???"
			self.version	= "0"
			self.name		= self.file
			self.cversion	= 0
			self.valid		= False

	"""
		Returns the build value
	"""
	def get_build_value(self,b):
		# remove the extension from the build
		if string.find(b,".")>=0:
			b = b[0:string.find(b,".")]
		versions = [t for t in _slackcurrent_ve_regex.split(b) if len(t)>0]
		val = 0
		for i in range(len(versions)):
			val = val + self.get_char_value(versions[i])
		return val

	"""
		When having some letters, try to make an integer with it. If the char is a 
		number, return its integer value.
	"""
	def get_char_value(self,c):
		idx = c
		try:
			idx = _slackcurrent_lowercase.index(c)
		except:
			idx = int(c)
		return idx	

	"""
		Calculate a version based on the package name.
	"""
	def make_version(self):
		try:
			version = []
			version.append(string.zfill("",36))					# version
			version.append(string.zfill("",3))					# rc
			version.append(string.zfill(self.build,3)[0:3])	# build
			rc = 0
		
			# replace rc like strings to rc
			# here is a little trick for beta versions - they are like rc versions
			# but it's value is added by 100 - I can't imagine more that 99 alpha
			# versions! :-p
			for t,v in _slackcurrent_rc_like.iteritems():
				if string.find(self.version,t)>=0:
					self.version = string.replace(self.version,t,"rc")
					rc = v

			# check if there is a rc version
			rm = _slackcurrent_rc_regex.search(self.version)
			if rm:
				# did you already saw an underline char (_) on the rc? I did. Argh.
				rc_str = string.replace(self.version[rm.start()+2:],"_","")
				# try to convert the rc to an integer number
				version[1] = string.zfill(int(rc_str)+rc,3)[0:3]
				self.version = self.version[0:rm.start()]

			# check if there is more than 4 version numbers - what kind of
			# freak do that? :-) if found more than 4, concatenate the last ones
			vtokens = string.split(self.version,".")
			if len(vtokens)>4:
				self.version = string.join(vtokens[0:4],".")+string.join(vtokens[4:],'')
			
			v = [string.join(self.make_version_token(t),'') for t in string.split(self.version,".")]
			for i in range(4-len(v)):
				v.append("000000000000")
			version[0] = v[0]+v[1]+v[2]+v[3]
			return long(string.join(version,''))
		except StandardError,e:
			return -1

	"""
		Calculate a "version token"
	"""
	def make_version_token(self,token):
		version  = ["000","000","000","000"]
		try:
			versions = [t for t in _slackcurrent_ve_regex.split(token) if len(t)>0]
			for i in range(len(versions)):	
				chr = string.replace(versions[i],"_","")
				version[i] = string.zfill(self.get_char_value(chr),3)
				# try to short the last version number to 3 digits
				if len(version[i])>4:
					diff = len(version[i])-2
					num  = int(version[i][0:4])
					for ex in range(diff):
						num += int(version[i][ex+4])
					version[i] = str(num)
		except StandardError,e:
			pass
		return version

	"""
		Operators overloading for comparison 
	"""
	def __eq__(self,other):
		return self.cversion==other.cversion

	def __gt__(self,other):
		return self.cversion>other.cversion

	def __lt__(self,other):
		return self.cversion<other.cversion
		
	"""
		Return package info as a string
	"""
	def __str__(self):
		return "Package: "+self.name+" Version: "+self.version+"\n"\
				 "Build: "+str(self.build)+" Arch: "+self.arch+"\n"+\
		       "Path   : "+self.path+"\n"+\
				 "Id     : "+str(self.cversion)+"\n"+\
		       "--------------------------------------------------------------------------\n\n"

#---------------------------------------------------------------------------#
# Class to store info about the local packages                              #
#---------------------------------------------------------------------------#
class SlackLocalPacks:
	"""
		Create an object with a list of all the local valid packages on a directory.
	"""	
	def __init__(self,dir):
		list  = glob.glob(dir+"*-*-*-*")
		list.sort()
		self.packs = [SlackPack(i) for i in list]

	"""
		Return a list of the local valid packages. 
	"""
	def valid(self):
		return [p for p in self.packs if p.valid]
	
	"""
		Return a list of the local invalid packages. 
	"""
	def invalid(self):
		return [p for p in self.packs if not p.valid]
	
	"""
		Search for a package name on the local list
	"""
	def find(self,package):
		return [p for p in self.packs if p.name==package]

#--------------------------------------------------------------------------------#
#	Class to store info about the remote packages											#
#--------------------------------------------------------------------------------#
class SlackRemotePacks:
	"""
		Create an object with a list of all the local valid packages on the 
		remote server.
	"""	
	def __init__(self,remotelistfile):
		list  = file(remotelistfile,"rb").readlines()
		server= getserver()
		if server[-1]=="/":
			server = server[0:len(server)-1]
		remotelist = [server+r.strip() for r in list]
		remotelist.reverse()
		self.packs = [SlackPack(i) for i in remotelist]

	"""
		Return a list of the local valid packages. 
	"""
	def valid(self):
		return [p for p in self.packs if p.valid]
	
	"""
		Return a list of the local invalid packages. 
	"""
	def invalid(self):
		return [p for p in self.packs if not p.valid]
	
	"""
		Search for a package name on the remote list
	"""
	def find(self,package):
		return [p for p in self.packs if p.name==package]

#--------------------------------------------------------------------------------#
#	Local stuff																							#
#--------------------------------------------------------------------------------#
"""
	Return the local list of packages
"""
def getlocallist():
	p = SlackLocalPacks(localpath)
	return p.valid()

"""
	Print the local list of packages
"""
def listlocal(parm):	
	print "Listing local packages:"
	for i in getlocallist():
		print i

"""
	Return the local list of invalid packages
"""
def getlocalinvalidlist():
	p = SlackLocalPacks(localpath)
	return p.invalid()

"""
	Return a string with the local invalid files names
"""
def getlocalinvalidstring():
	list = [p.name for p in getlocalinvalidlist()]
	if len(list)>0:
		list = string.join(list,",")
	return list		

"""
	Print the local list of invalid packages
"""
def listinvalidlocal(parm):	
	print "Listing local invalid packages:\n"
	for i in getlocalinvalidlist():
		print i

#--------------------------------------------------------------------------------#
#	File path stuff																					#
#--------------------------------------------------------------------------------#
"""
	Remote list file path
"""
def remotelistfile():
	return confpath+"remotelist"

"""
	Black list file path
"""	
def blacklistfile():
	return confpath+"blacklist"

"""
	Mirrors list file path
"""	
def mirrorsfile():
	return confpath+"mirrors"

#--------------------------------------------------------------------------------#
#	Remote stuff																						#
#--------------------------------------------------------------------------------#
"""
	Update the list of remote files 
"""
def updatelist(parms):
	print "Updating the list ..."
	remotelist = downloadremotelist()
	if remotelist == None:
		return

	# if exists, save the previous list for later comparisons		
	if os.path.exists(remotelistfile()):
		os.rename(remotelistfile(),remotelistfile()+".old")	
			
	open(remotelistfile(),"w").writelines(remotelist)
	print len(remotelist),"items updated"

"""
	Return the list of remote valid files
"""
def getremotelist():
	p = SlackRemotePacks(remotelistfile())
	return p.valid()

"""
	Check if the remote list exists
"""
def checkremotelist():
	if os.path.exists(remotelistfile()):
		# check if the remote list is older than one week
		ftime = os.path.getmtime(remotelistfile())
		ltime = time.time()
		days  = int((ltime-ftime)/(60*60*24))
		if days>7:
			answer = raw_input("The list with the remotefiles is older than one week ("+str(days)+" days).\nDo you want to upgrade it now? (Y/n) ")
			if string.upper(answer) == "Y":
				updatelist(None)
		return True
	
	answer = raw_input("The list with the remotefiles does not exists.\nDo you want to download it now? (Y/n) ")
	if string.upper(answer) == "Y":
		updatelist(None)
		return True
	return False

"""
	Print the list of remote files
"""
def listremote(parms):
	if not checkremotelist():
		print "Please download the remote list first"	
		return
	print "Listing remote packages:\n"
	remotelist = getremotelist()
	for i in remotelist:
		print i

"""
	Return the list of remote invalid files
"""
def getremoteinvalidlist():
	p = SlackRemotePacks(remotelistfile())
	return p.invalid()

"""
	Return a string with the remote invalid files names
"""
def getremoteinvalidstring():
	list = [p.name for p in getremoteinvalidlist()]
	if len(list)>0:
		list = string.join(list,",")
	return list		

"""
	Print the list of remote invalid files
"""
def listinvalidremote(parms):
	if not checkremotelist():
		print "Please download the remote list first"	
		return
	print "Listing remote invalid packages:\n"
	remotelist = getremoteinvalidlist()
	for i in remotelist:
		print i

"""
	Download the remote list from the selected server
"""
def downloadremotelist():	
	url = getserver()+"FILELIST.TXT"
	print "Downloading\n",url
	expr = re.compile("t[gx]z$")
	pref = re.compile("^http|^ftp")
	try:
		if pref.search(url)!=None:
			oper = urllib.urlopen
		else:	
			oper = open
		remotelist = [r[string.find(r,"/"):] for r in oper(url).readlines() if expr.search(r)!=None]
	except:
		print "Impossible to reach file"
		return None
	return remotelist

#--------------------------------------------------------------------------------#
#	Upgrade stuff, including the testing serie												#
#--------------------------------------------------------------------------------#
def upgradetesting(parms):
	upgrade(parms,True)

#--------------------------------------------------------------------------------#
#	Upgrade stuff																						#
#--------------------------------------------------------------------------------#
"""
	Get local and remote lists, compares it, write to a file and if the user wants,
	show on the screen
"""
def upgrade(parms,testing=False):
	if not checkremotelist():
		print "Upgrade canceled."
		return
	
	print "Checking packages for upgrade"
	limit = ""
	
	if len(parms)>2:
		limit = parms[2]
		print "Limited on",limit		
		
	list = getupgradelist(limit,testing)
	if len(list)==0:
		print "No packages for upgrade"
		return
	
	iv = False
	il = getlocalinvalidstring()
	if len(il)>0:
		print "\n*** WARNING! ***"
		print "There are some LOCAL packages that are invalid."
		print "The packages are: "+il
		iv = True
	
	ir = getremoteinvalidstring()
	if len(ir)>0:
		print "\n*** WARNING! ***"
		print "There are some REMOTE packages that are invalid."
		print "The packages are: "+ir
		iv = True

	if iv:
		print "\nThe invalid packages WONT BE checked for newer versions because their"
		print "names does not follow the default and standard name format that "
		print "Slackcurrent works with. If you think that the names are ok (with name,"
		print "up to 4 version numbers, an optional rc string and the build number),"
		print "maybe there is a bug on Slackcurrent. Please use the Sourceforge forums"
		print "to let me know about it, thank you!\n"
	
	try:		
		open("slackcurrent.list","w").writelines(list)
		print len(list)/2,"item(s) written to slackcurrent.list"
		print "Now use a download manager to get it all, for example, wget:"
		print "wget <your options for wget here> -i slackcurrent.list"
		
		answer= raw_input("Do you want to see the list now on the screen? (y/N) ")
		if string.upper(answer) == "Y":
			expr = re.compile("t[gx]z$")
			for i in [p for p in list if expr.search(p)!=None]: print i
	except StandardError,e:
		print "Could not create the file list."
		print e

"""
	Return the upgrade list
"""
def getupgradelist(limit="",testing=False):	
	black		= getblacklist()
	local		= [p for p in SlackLocalPacks(localpath).valid() if p.name not in black]
	remote	= SlackRemotePacks(remotelistfile())
	expr		= re.compile("^"+getserver()+limit)	
	test		= re.compile("^"+getserver()+"testing")
	list		= []
	
	for p in local:
		rmt = remote.find(p.name)
		try:
			if rmt==None or len(rmt)<1:
				continue
			for r in rmt:
				if len(limit)>0 and expr.match(r.fullpath)==None:
					continue
				if not testing and test.match(r.fullpath):
					continue
				if r>p:
					list.append(r.fullpath+"\n")
					list.append(r.fullpath+".asc\n")
		except:
			print "ERROR:",p.name,rmt			
	return list		

#--------------------------------------------------------------------------------#
#	New stuff																							#
#--------------------------------------------------------------------------------#
def listnew(parms):
	print "Listing new packages"
	new = getnewlist()

	if new == None or len(new)==0:
		print "No new packages"
		return
	open("slackcurrent.new","w").writelines(new)
		
	print len(new)/2,"item(s) written to slackcurrent.new"
	print "Now use a download manager to get it all, for example, wget:"
	print "wget <your options for wget here> -i slackcurrent.list"
	
	answer= raw_input("Do you want to see the list now on the screen? (y/N) ")
	if string.upper(answer) == "Y":
		expr = re.compile("t[gx]z$")
		for i in [p for p in new if expr.search(p)!=None]: print i

"""
	Get the list of new packages added since the latest list update
"""
def getnewlist():
	if not os.path.exists(remotelistfile()+".old"):
		print "There is no previous package list for comparison."
		print "It will be available on the next list update."
		return None

	cur = SlackRemotePacks(remotelistfile()).valid()
	old = SlackRemotePacks(remotelistfile()+".old")
	new = []
	for p in cur:
		o = old.find(p.name)
		if o==None or len(o)<1:
			new.append(p.fullpath+"\n")
			new.append(p.fullpath+".asc\n")
	return new

"""
	Download your packages from some place you already downloaded them
"""
def download_from(parms):
	if(len(parms)<4):
		print "Usage: <user> <host> <remote directory>"
		return

	user = parms[2]
	host = parms[3]
	dir  = parms[4]

	# here we use SSH to get the list of files on the remote directory
	print "Checking",host,"on",dir,"using user",user
	os.system("ssh "+user+"@"+host+" ls "+dir+" > /tmp/slackcurrent.rl")

	# check the files
	if not os.path.exists("/tmp/slackcurrent.rl"):
		print "Could not find the remote list. Did the SSH connection worked?"
		return
	
	if not os.path.exists("slackcurrent.list"):
		print "Could not find the list with the required new packages."
		print "Did you run slackcurrent.py -ul and slackcurrent.py -u to create the list?"
		return
	
	# read the list
	dl = open("/tmp/slackcurrent.rl","rb").readlines()
	ll = open("slackcurrent.list","rb").readlines()

	# prepare an empty list for the packages to get from there
	gl = []
	nf = []

	# we just want the .t[gx]z files
	tgz_regex = re.compile("t[gx]z$")

	# check what package we need there and have there
	for t in ll:
		if not tgz_regex.search(t):
			continue
		pos	= string.rfind(t,"/")
		file	= t
		if pos>0:
			file = string.strip(t[pos+1:])
		print "  Checking",file,"...",
		ok = [r for r in dl if string.find(r,file)>=0]
		if ok:
			print "found!"
			gl.append(user+"@"+host+":"+dir+"/"+file)
		else:
			print "NOT found!"
			nf.append(file)
	
	com = "scp "+string.join(gl," ")+" ."
	print "Downloading files ..."
	os.system(com)
	if len(nf)>0:
		print "Done, but",len(nf),"packages are missing:\n"
		for i in nf:
			print "  ",i
		print "\nPlease download the missing packages from another place (your slackcurrent.list file contains your preferred mirror path for those packages)."
	else:	
		print "Done. Now install the packages."
	os.unlink("/tmp/slackcurrent.rl")

#--------------------------------------------------------------------------------#
#	Config stuff																						#
#--------------------------------------------------------------------------------#
"""
	Check the ASC packages signatures
"""
def checksign(parms):
	list  = glob.glob("*.t[gx]z")
	list.sort()
	for p in list:
		print "checking",p
		if not os.path.exists(p+".asc"):
			print "ASC signature not found, skipping ..."
			continue
		r = os.spawnlp(os.P_WAIT,"gpg","gpg","--verify",p+".asc",p)
		if r != 0:
			print "Checking FAILED!"
			print "Please confirm that the package and the signature as downloaded ok."
			return
		else:
			print "Signature OK."			
		print

"""
	Main method when running from the console
"""
def main(argv):		
	header()
	msgs = {}
	msgs["-v" ]	= "Show Slackcurrent header with current version"
	msgs["-ul"] = "Update your local list with references of remote files"
	msgs["-ll"] = "List all your local packages"
	msgs["-li"] = "List all your local invalid packages"
	msgs["-lr"] = "List remote packages"
	msgs["-ri"] = "List all remote invalid packages"
	msgs["-lb"] = "List the black list"
	msgs["-ln"] = "List new packages"
	msgs["-cs"] = "Check the packages ASC signatures"
	msgs["-um"] = "Update the mirrors list file"
	msgs["-cl"] = "Show the latest i386 current changelog"
	msgs["-u" ] = "Get the list of packages for upgrade"
	msgs["-ut"] = "Get the list of packages for upgrade, including testing"
	msgs["-df"] = "Download packages from a previous downloaded place"
	
	# available commands	
	commands= {"-ll"							:[listlocal				,msgs["-ll"]],\
				  "--list-local"				:[listlocal				,msgs["-ll"]],\
				  "-li"							:[listinvalidlocal	,msgs["-li"]],\
				  "--list-invalid-local"	:[listinvalidlocal	,msgs["-li"]],\
				  "-lr"							:[listremote			,msgs["-lr"]],\
				  "--list-remote"				:[listremote			,msgs["-lr"]],\
				  "-ri"							:[listinvalidremote	,msgs["-ri"]],\
				  "--list-invalid-remote"	:[listinvalidremote	,msgs["-ri"]],\
				  "-lb"							:[listblacklist		,msgs["-lb"]],\
				  "--list-blacklist"			:[listblacklist		,msgs["-lb"]],\
				  "-ul"							:[updatelist			,msgs["-ul"]],\
				  "--update-list"				:[updatelist			,msgs["-ul"]],\
				  "-u"							:[upgrade				,msgs["-u" ]],\
				  "--upgrade"					:[upgrade				,msgs["-u" ]],\
				  "-ut"							:[upgradetesting		,msgs["-ut"]],\
				  "--upgrade-testing"		:[upgradetesting		,msgs["-ut"]],\
				  "-ln"							:[listnew				,msgs["-ln"]],\
				  "--list-new"					:[listnew				,msgs["-ln"]],\
				  "-cs"							:[checksign				,msgs["-cs"]],\
				  "--check-sign"				:[checksign				,msgs["-cs"]],\
				  "-um"							:[updatemirrors		,msgs["-um"]],\
				  "--update-mirrors"			:[updatemirrors		,msgs["-um"]],\
				  "-cl"							:[changelog				,msgs["-cl"]],\
				  "--changelog"				:[changelog				,msgs["-cl"]],\
				  "-df"							:[download_from		,msgs["-df"]],\
				  "--download-from"			:[download_from		,msgs["-df"]],\
				  "-v"							:[void					,msgs["-v" ]],\
				  "--version"					:[void					,msgs["-v" ]]}

	# nothing asked to do, get out!
	if(len(argv)<2):
		help(commands)
		return
	
	command = argv[1]
	# execute the desired command	
	if command in commands:
		commands[command][0](argv)
	else:
		print command,"is not a valid command"
		help()

"""
	Do nothing
"""
def void(void):
	pass

"""
	Prints the program header info
"""
def header():
	print "\nSlackcurrent "+__version__+" - Slackware current packages maintenance program"
	print "This software is GPL. More about it on: http://slackcurrent.sf.net"
	print "Get the latest code on http://github.com/taq/slackcurrent"
	print "Current server is "+getserver(False)
	print

"""
	Return the selected server
"""
def getserver(resolv=True):
	server = []
	# check if there is a mirrors file
	if not os.path.exists(mirrorsfile()) and resolv:
		print "ERROR! The mirrors file "+mirrorsfile()+" does not exists."
		answer = raw_input("Do you want to download it now? (Y/n)")
		if string.upper(answer) != "Y":
			print "Please install it at",confpath,"or use the -um option to download it."
			sys.exit(1)
		updatemirrors("")	

	if os.path.exists(mirrorsfile()):		
		server = [r.strip() for r in file(mirrorsfile(),"r") if r[0]!="#" and len(r.strip())>0]

	if len(server)<1:
		if resolv:
			print "ERROR! There is no mirror selected."
			print "Please uncomment just ONE mirror line on "+mirrorsfile()
			sys.exit(1)
		else:
			return "NO SERVER DEFINED YET."
	return server[0]

"""
	Return the black list
"""
def getblacklist():
	if not os.path.exists(blacklistfile()):
		return []
	return [r.strip() for r in open(blacklistfile(),"rb").readlines()]	

"""
	List the black list
"""
def listblacklist(parms):
	print "Listing the black list:"
	for i in getblacklist():
		print i		

"""
	Check the latest current changelog
"""
def changelog(parms):
	print "Checking the latest current changelog ...\n"
	main_lines	= urllib.urlopen("http://www.slackware.com/changelog/current.php?cpu=i386").readlines()
	date_re		= re.compile("[A-Z][a-z]{2} [A-Z][a-z]{2} [0-9 ]")
	date_end		= re.compile("^\+--")
	newline_re	= re.compile("<br.?/?>",re.IGNORECASE)
	nbsp_re		= re.compile("&nbsp;",re.IGNORECASE)
	print_line	= False
	for line in main_lines:
		# search for a date
		found_date = date_re.search(line)
		# if found, printing starts here
		if found_date:
			print "Found changes on ",
			print_line = True
			line = line + "\n"
		# but if is the date termination row, ends here	
		if date_end.search(line):
			break
		# if it's allowed to print the line ...
		if print_line:	
			line = newline_re.sub("",line[:-1])
			line = nbsp_re.sub("",line)
			print line

"""
	Update the mirror list. Get it from the Slackware official website.
"""
def updatemirrors(parms):
	print "Updating the mirrors list ..."
	main_re		= re.compile("list\.php\?.*\"")		# find the current countries lists
	mirror_re	= re.compile("<TD><A HREF=\".*\">")	# find the url from the country mirror list
	mirrors		= []											# stores the mirrors found 
	main_lines	= urllib.urlopen("http://www.slackware.com/getslack/").readlines()

	# check if it was called from the command line or from inside this program
	# if from the command line, does not tries to resolve the default server if it was
   # not selected (this could leads to another call to this function from inside getserver()
	# and we'll be on an infinite loop
	default = "no server selected yet"
	if type(parms) is types.ListType:
		default = getserver(False)

	# let's check the available countries ...
	for country in main_lines:
		found = main_re.search(country)
		if found:
			country_url = country[found.start():found.end()-1]		# get the country url
			country		= country_url[country_url.index("=")+1:]	# get the country name
			print "Retrieving mirrors from",country,"..."		
			mirrors.append("### --- mirrors from "+country+" --- ###\n")	# append a comment line on the mirrors file
			country_url = "http://www.slackware.com/getslack/"+country_url	# get the country mirrors
			mirror_lines = urllib.urlopen(country_url).readlines()
			for mirror in mirror_lines:
				mfound = mirror_re.search(mirror)
				# if found, get the mirror url
				if mfound:
					mirror = mirror[mfound.start():mfound.end()]		
					mirror = mirror[mirror.index("=")+2:-2]
					if mirror[-1]!="/":				
						mirror = mirror + "/"
					mirror += "slackware-current/"
					print mirror
					if mirror != default:
						mirror = "#"+mirror
					mirrors.append(mirror+"\n")
			print "--------------------------------------------------------------------------------\n"					
	# write the results to the mirrors file			
	open(mirrorsfile(),"w").writelines(mirrors)					

def help(commands):
	p = {}
	for key,val in commands.iteritems():
		msg = val[1]
		key = string.ljust(key,3)
		if p.has_key(msg):
			if len(p[msg])>len(key):
				p[msg] = key+", "+p[msg]
			else:	
				p[msg] = p[msg]+", "+key
		else:
			p[msg] = key
	
	print "Valid commands:\n"
	v = []
	for key,val in p.iteritems():
		v.append(string.ljust(val,22)+" "+key)
	v.sort()
	for i in v:
		print i
	print

if __name__== "__main__":
	main(sys.argv)
