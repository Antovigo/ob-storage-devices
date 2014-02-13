#!/usr/bin/python2.7
#-*-coding:utf-8-*-
import os
import commands

def item ( lab, cmd ):
	print("<item label='{0}'>\
	<action name='execute'>\
	<execute>{1}</execute>\
	</action>\
	</item>".format (lab,cmd) )

print ("<openbox_pipe_menu>")

lsblk = commands.getoutput('lsblk -l').split('\n')
dev = []

def filtre(nom): # You can filter out the peripheral you don't want here.
	if 'sda' in nom or nom == 'sr0' or nom == 'mmcblk0' or nom == 'mmcblk0p1':
		return False
	elif nom[-1].isdigit() : # Assuming only the partitions ending with a digit can be mounted
		return True
	else:
		return False

for i in lsblk[1:] :
	k = i.split()
	if filtre(k[0]):
		dev.append (k)

if dev == []: # Aucun périph
	print("<separator label='No storage device!' />")
	
elif len(dev) == 1: # Un seul périph
	k = dev[0]
	if len(k) >= 7:
		item ( 'Browse', 'xdg-open '+k[6] )
		item ('Eject', 'sh -c "udevil umount '+k[6]+"; notify-send 'You can now tear your usb stick away.' -i ~/.config/openbox/content.png" + '"')
	else:
		emp = "/media/" + k[0]
		item ( k[0] + ' (' + k[3] + ') ', 'sh -c "udevil mount /dev/'+k[0]+" "+emp+'; thunar '+emp+'"')
		
else:
	for k in dev: # Plusieurs périphs
		if len(k) >= 7:
			print( '<menu id="'+k[0] + ' (' + k[3] + ')" label="' +k[0] + ' (' + k[3] + ')">')
			item ( 'Browse', 'xdg-open '+k[6] )
			item ('Eject', 'sh -c "udevil umount '+k[6]+"; notify-send 'You can now tear your usb stick away.' -i ~/.config/openbox/content.png" + '"')
			print( '</menu>')
		else:
			emp = "/media/" + k[0]
			item ( k[0] + ' (' + k[3] + ') ', 'sh -c "udevil mount /dev/'+k[0]+" "+emp+'; thunar '+emp+'"')

print ("</openbox_pipe_menu>")
