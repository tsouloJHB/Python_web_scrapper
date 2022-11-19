# Import Module
import ftplib

# Fill Required Information
HOSTNAME = "ftpupload.net"
USERNAME = "epiz_32909284"
PASSWORD = "913uGlwgJG"

# Enter File Name with Extension
 
filename = "tvguide.json"
folder = "sportstreamer.ml/htdocs/data"

ftp_server = ""

def create_connection(HOSTNAME,USERNAME,PASSWORD):
    global ftp_server
    try:
        # Connect FTP Server
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    except:
        print("failed to connect to the server");    

    # force UTF-8 encoding
    ftp_server.encoding = "utf-8"




def upload_file(filename, folder):
    global ftp_server

    ftp_server.cwd(folder)
    try:    
        # Read file in binary mode
        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {filename}", file)
    except:
        print("failed to save the file on the server");
        return False
    # Get list of files
    ftp_server.dir()

    # Close the Connection
    ftp_server.quit()
    return True

def upload():
    create_connection(HOSTNAME,USERNAME,PASSWORD)
    if (upload_file(filename, folder)):
        return True
    return False    
        
