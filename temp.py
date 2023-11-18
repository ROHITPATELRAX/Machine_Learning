import sys
import cv2
import time
import json
import requests
import m3u8
import shutil
import os
import socket
from time import sleep



# cv2.VideoCapture("http://localhost:9999/warcarfttrailer13.ts")

dataPackets=list()

def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]


def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)

    for chunk in r.iter_content(chunk_size=188):
        if chunk:
            dataPackets.append(chunk)

    # with open(f"ts_files/{local_filename}", 'wb') as f:
    #     for chunk in r.iter_content(chunk_size=1024):
    #         if chunk:
    #             f.write(chunk)
    #
    # return local_filename


def file_writer(fileName):
    with open(fileName, "wb") as f:
        for i in dataPackets:
            f.write(i)


m3u8_url =str(sys.argv[1])
#str("http://192.168.0.51/content/verimatrix-hls/DRM_Client_Integration_Test_HLS/hls_content_ah_clear_rev1/list_1280x720_5000.m3u8")
r = requests.get(m3u8_url)
m3u8_master = m3u8.loads(r.text)


m3u8_file = m3u8_url.split('/')[-1]
url = strip_end(m3u8_url, m3u8_file)
url_copy = url

# if not os.path.exists('ts_files'):
#     print('ts_file folder is not found, creating the folder.')
#     os.makedirs('ts_files')

tsFileUrl=list()

print(m3u8_master.simple_attributes)
# print(m3u8_master.files.)
for seg in m3u8_master.data['segments']:
    # print(url)
    url += seg['uri']
    print(url)
    # temp=dict()
    # temp['url']=url
    # tsFileUrl.append(temp)
    print(f'downloading {seg["uri"]}')
    download_file(url)
    url = url_copy

file_writer("mainfile.ts")




# import PIL.Image as pillowImage
# import base64
# import io

# b=base64.b64encode(dataPackets[0])

# b=base64.b64decode(b)
# img=pillowImage.open(io.BytesIO(b))
# img.show()

# print("Streaming on 9096")

# import socket

# def main():
#     host = "127.0.0.1"
#     port = 4455
#     addr = (host, port)

#     """ Creating the UDP socket """
#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#     i=0

#     while True:
#         # data = input("Enter a word: ")

#         # if data == "!EXIT":
#         #     data = data.encode("utf-8")
#         #     client.sendto(data, addr)

#             # print("Disconneted from the server.")
#             # break

#         if (len(dataPackets)<i):
#             break

#         data = dataPackets[i]
#         client.sendto(data, addr)
#         time.sleep(10)
#         i+=1

#         # data, addr = client.recvfrom(1024)
#         # data = data.decode("utf-8")
#         # print(f"Server: {data}")


# main()






# tsFileUrl=json.dumps(tsFileUrl,indent=3)

# with open('ts_File_url.json','w') as f:
#     f.write(tsFileUrl)

# import glob
# # cwd = os.getcwd()
# cwd="/home/rohitpatel/storefile"
#
# list_of_files = sorted( filter( os.path.isfile,
#                         glob.glob(cwd+"/tmp" + '*') ) )
#
# # os.chdir("/home/rohitpatel/storefile/tmp")
#
#
# TS_DIR = 'tmp'
# with open('merged.ts', 'wb') as merged:
#     for ts_file in os.listdir(f'{cwd}/{TS_DIR}'):
#         with open(f'{cwd}/{TS_DIR}/{ts_file}', 'rb') as mergefile:
#             shutil.copyfileobj(mergefile, merged)


import time, vlc  
   
# defining the method to play video  
def vlc_video(src):  
       
    # creating an instance of vlc  
    vlc_obj = vlc.Instance()  
       
    # creating a media player  
    vlcplayer = vlc_obj.media_player_new()  
       
    # creating a media  
    vlcmedia = vlc_obj.media_new(src)  
       
    # setting media to the player  
    vlcplayer.set_media(vlcmedia)  
       
    # playing the video  
    vlcplayer.play()  
       
    # waiting time  
    time.sleep(0.5)  
       
    # getting the duration of the video  
    video_duration = vlcplayer.get_length()  
       
    # printing the duration of the video  
    print("Duration : " + str(video_duration))  
       
# calling the video method  
vlc_video("mainfile.ts") 