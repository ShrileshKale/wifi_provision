import os
import json
# from bson import json_util
import os.path
from shutil import copyfile
import sys
import subprocess
from subprocess import Popen, PIPE, STDOUT, check_output
from time import sleep
from flask import Response, render_template, request
from app import app, db, socketio


filename = "/etc/wpa_supplicant/wpa_supplicant.conf"
header0 = 'country=IN'
header1 = 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev'
header2 = 'update_config=1'
host_to_client = 'hostapd.service'


def wpa_supplicant_new():
    print 'Try to create file wpa_supplicant.conf'
    sleep(2)
    f = open(filename, "w")
    f.write(header0 + '\n')
    f.write(header1 + '\n')
    f.write(header2 + '\n')
    f.close()
    subprocess.call('sudo chown root:root ' + filename , shell=True)
    subprocess.call('sudo chmod 600 ' + filename , shell=True)
    if os.path.isfile(filename):
        print 'File created successfully'
        sleep(2)

def main(ssid,passwd):
    filename_bkp = filename + ".bkp"
    priority = "2"
    replace = True
    interface = 'wlan0'
    error = False
    print('\nSSID: ' + ssid)
    print('Password: ' + passwd)
    print('Priority: ' + priority)
    print('Replace: ' + str(replace))
    print('Interface: ' + interface)
    sleep(2)
    if os.path.isfile(filename):
        index0 = 0
        while True:
            if not os.path.isfile(filename_bkp + str(index0)):
                print "Trying to backup the file..."
                sleep(2)
                copyfile(filename, filename_bkp + str(index0))
                subprocess.call('sudo chown root:root ' +
                            filename_bkp + str(index0) , shell=True)
                subprocess.call('sudo chmod 600 ' +
                            filename_bkp + str(index0), shell=True)
                if os.path.isfile(filename_bkp + str(index0)):
                    print "Backup complete"
                    print "Saved as: " + filename_bkp + str(index0)
                    sleep(2)

                    if replace is True:
                        print "Trying to delete the file"
                        sleep(2)
                        os.system('sudo rm ' + filename)
                        if not os.path.isfile(filename):
                            print "File deleted"
                            sleep(2)
                        else:
                            print 'Error, file not deleted'
                            sleep(2)
                    break
            else:
                index0 += 1

    if ((not os.path.isfile(filename)) | (replace is True)):
        wpa_supplicant_new()

    print 'Get wpa passphrase and append to file'
    sleep(2)

    command_txt = ('sudo wpa_passphrase "' + ssid + '" "' + passwd + '"')
    result = check_output(command_txt, shell=True)

    f = open(filename, 'a')
    for line in result:
        if ((priority != "") & ("}" in line)):
            f.write('\tpriority=' + priority + '\n')
        f.write(line)
    f.close()

    print('\n' + filename)
    print('\nFile content:')
    f = open(filename, "r")
    for line in f:
        sys.stdout.write(line)
        sys.stdout.flush()
        sleep(0.5)
    f.close()
    print 'Reconfigure ' + interface
    sleep(2)
    print('sudo wpa_cli -i ' + interface + ' reconfigure')
    command_txt = "sudo wpa_cli -i " + interface + " reconfigure"
    sts = os.system(command_txt)
    if sts != 0:
        print 'Error, please try reboot your system'
        sleep(2)
        if query_yes_no("Reboot system now?"):
            print 'Trying reboot your system'
            sleep(2)
            os.system('sudo reboot')
        else:
            print 'Please check your system and try again.'
            sys.exit(0)


@app.route('/control-panel', methods=["GET"])

def controlPanel():

	return render_template('test.html')


@app.route('/wifi/update_config', methods=["POST"])
def wifiConfiguration():
    try:
        response = request.get_json(force=True)
        ssid = response['ssid']
        passwd = response['passwd']
        main(ssid, passwd)
        subprocess.call('sudo systemctl stop ' + host_to_client , shell=True)
        # sys.exit(0)
        return Response(json.dumps(
        	{
        		"status": "success",
        		"message": "Wifi wifiConfiguration changed successfully"
        	}, default=json_util.default
        ), mimetype="application/json")
        sys.exit(0)



    except KeyboardInterrupt:
    	print('User aborted script')
    	return Response(json.dumps({
    			"status": False,
    			"message": "Error: %s" %e
    		}, default=json_util.default), mimetype="application/json")


    	




