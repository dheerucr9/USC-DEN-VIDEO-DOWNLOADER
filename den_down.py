import os
import time


# 1. get download link from the website
# 2. get until the m3u8 part and download the m3u8 file using curl
# 3. navigate to the new m3u8 part append it to the base url and download the new m3u8 file.
# 4. now the new downloaded files have all the ts files. download using them


# if __name__ == '__main__':
# download_url = raw_input('Paste the download link copied from DEN by clicking Android / iOS here: ')
download_url = 'http://denawswz.uscden.net/aws/_definst_/mp4:amazons3/gwz/CSCI585_2019312020190828-0/CSCI585_2019312020190828-0.mp4/playlist.m3u8?wowzaplaystart=0'
m3u8_url = download_url[:download_url.index('m3u8') + 4]
mp4_index = download_url.rindex('mp4')
mp4_base_url = download_url[: mp4_index + 4]
file_name = download_url[download_url[:mp4_index].rindex('/') + 1:mp4_index - 1]
timestamp = int(time.time() * 100)
# print(timestamp)
os.system('mkdir ./temp_%s/' % timestamp)
try:
    os.system('curl -s -o ./temp_%s/main_playlist.m3u8 %s'
        % (timestamp, download_url))
except:
    print('Error with the link provided')
    exit()

linked_m3u8 = ''

try:
    with open('./temp_%s/main_playlist.m3u8' % (timestamp), 'r') as m3u8_file:
        for line in m3u8_file:
            pass
        linked_m3u8 = line
except IOError as error:
    print('Error downloading the file')


if linked_m3u8 != '':
    try:
        linked_m3u8_url = mp4_base_url + linked_m3u8
    except ValueError as error:
        print('Error getting the files')
        exit()

    try:
        os.system('curl -s -o ./temp_%s/linked_playlist.m3u8 %s'
            % (timestamp, linked_m3u8_url))
    except:
        print('Error getting the files')
        exit()


    ts_files = []
    try:
        with open('./temp_%s/linked_playlist.m3u8' % (timestamp), 'r') as m3u8_file:
            for line in m3u8_file:
                if line[0] != '#':
                    ts_files.append(line.rstrip())
    except IOError as error:
        print('Error downloading the file')
        exit()

    ts_files_str = ','.join(ts_files)

    try:
        os.system('rm ./temp_%s/main_playlist.m3u8' % timestamp)
        os.system('rm ./temp_%s/linked_playlist.m3u8' % timestamp)
        os.system('curl -o ./temp_%s/part_#1 %s\{%s\}'
                  % (timestamp, mp4_base_url, ts_files_str))
        print('Files succesfully downloaded')
    except:
        print('Error with the link provided')
        exit()

    try:
        os.system('cat ./temp_%s/part* > %s.ts' % (timestamp, file_name))
        os.system('rm -rf ./temp_%s/' % timestamp)
        print("INFO: %s download completed." % file_name)
    except:
        print('Error combining files')
        exit()


    