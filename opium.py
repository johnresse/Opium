#!/usr/bin/python


import subprocess
import os
import optparse
import sys

#testing on apk -------->   Superdry_v2.0_apkpure.com.apk

#path where the tools are located
jadx_path = "/usr/local/bin/jadx/bin"

#getting the arguments from the terminal
def get_argument():

	parser=optparse.OptionParser()	
	parser.add_option("-a","--apk",dest="android_file",help="Add a apkfile with the path")
	parser.add_option("-o","--output",dest="output_file",help="Add a output file")
	(options,arguments) = parser.parse_args()

	if not options.android_file:
		parser.error("\n[-] Specify an apk file to scan --help for more details")
	elif not options.output_file:
		parser.error("\n[-] Specify an output file for storing the decompiled file --help for more details")

	return options

options = get_argument()
#print(options)


#Decompiling the android app
def Decompile(input, output):

	if not os.path.exists(jadx_path):
		print("[-] Decompiling Failed, Please Install Jadx")
		sys.exit()

	else:

		path = os.path.join(jadx_path, options.output_file)
		#check for the existence of the diretory that is used for the output.
		if os.path.isdir(path) == True:
			print("[-] The Directory already exists, please select another output Directory" )
			sys.exit()


		else:
			os.mkdir(path)
			os.chdir("/usr/local/bin/jadx/bin")
			print('\n\n')
			print("[+] Please wait Decompiling....\n")
			subprocess.call(["./jadx","-d",options.output_file, options.android_file])
			print("\n\n[+] Decompiling Complete!")
			path_manifest = os.path.join(path, 'resources/AndroidManifest.xml')
			#print(path_manifest)

			manifest = open(path_manifest)
			#printing the manifest.xml file to the terminal
			#print(manifest.read())
			lines = manifest.readlines()
			#print(lines)
			#word = ['android:name','activity']

			print('[+] Analysing the AndroidManifest file\n')

			print('[+] Extracting the Activities...\n\n')

			print('[+] Activities: \n\n')

			for line in lines:
				if 'android:name' in line:
					if 'activity' in line:
						print(line,end="")


			print("\n\n")
			print('[+] Now Extracting the recivers...')

			print('[+]  Receivers: \n')

			Rec = 0
			for line in lines:
				if 'android:name' in line:
					if 'recevier' in line:
						print(line,end='')
						Rec = Rec+1

			if Rec == 0:
				print('[-] No Receivers Found')


			print('[+] Now Extracting Services...')

			print('[+] Services: \n')

			ser = 0
			for line in lines:
				if 'android:name' in line:
					if 'service' in line:
						print(line,end='')
						ser = ser+1


			if ser ==0:
				print('[-] No Services Found')




			print('[+] Extracting the exported Activities...\n')
			l = 0
			for line in lines:
				if 'exported=true' in line:
					if 'activity' in line:
						print(line,end='')
						l = l+1


			if l==0:
				print('[-] No exported actvites found\n')


			print("[+]Now Checking for fbtoken stealing...\n")

			fb = ['fbconnect', '@string/fb']
			test = 0
			print('\n\n')
			for line in lines:
				for name in fb:
					if name in line:
						print('[+] The App may be vulernable to fb Token stealing' )
						test = test+1
					

			if test == 0:
				print('[-]Not vulernable to Fbtoken stealing\n')	


			
			strings_path = os.path.join(path, 'resources/res/values/strings.xml')

			print('[+] Checking for the hardcoded secrets\n')
			secret = ['key', 'secret', 'token', 'oauth']
			sec = 0
			strings = open(strings_path)
			strings_line = strings.readlines()

			for sl in strings_line:
				for s in secret:
					if s in sl:
						print(sl,end='')
						sec = sec+1


			if sec == 0:
				print('[-] No Hardcoded Secrets are found\n\n')

			print('\n\n')

			print('For Exploitation of Keys please refer to the gmapscanner and keyhacks\n\n')




		
Decompile(options.android_file, options.output_file)	

print('HAPPY HUNTING!!')






































