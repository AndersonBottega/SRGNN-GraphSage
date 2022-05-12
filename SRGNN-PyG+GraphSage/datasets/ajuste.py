import time
import csv

dataset = "30music"
#dataset = "retailrocket"
#dataset = "playlists-aotm"

if (dataset == "30music-200ks.csv"):
    data = "30music/raw/30music-200ks.csv"
    with open("30music.csv", 'w') as files:
        files.write('session_id;user_id;item_id;timeframe;eventdate' + '\n')
        with open(data, "r") as f:
            #user_id;session_id;item_id;timeframe;ArtistId
            reader = csv.reader(f, delimiter=';')   
            for linha in reader:
                #print("asctime(localtime(secs)): %s" % time.asctime(time.localtime(int(linha[3]))))
                #print(linha)
                #print(linha[0])
                files.write(linha[1] + ';' + linha[0] + ';' + linha[2] + ';' + '0' + ';' + linha[3] + '\n')
    print("Done!")

elif dataset == "retailrocket":
    data = "events.csv"
    with open("retailrocket.csv", 'w') as files:
        files.write('session_id;user_id;item_id;timeframe;eventdate' + '\n')
        with open(data, "r") as f:
            #user_id;session_id;item_id;timeframe;ArtistId
            reader = csv.reader(f, delimiter=',')   
            next(reader)
            for linha in reader:
                #print("asctime(localtime(secs)): %s" % time.asctime(time.localtime(int(linha[3]))))
                #print(linha)
                #print(linha[0])
                if (linha[2] == 'view'):
                    files.write(linha[1] + ';' + linha[1] + ';' + linha[3] + ';' + '0' + ';' + linha[0] + '\n')
    print("Done!")   

elif dataset == 'playlists-aotm':
    data = "playlists-aotm.csv"
    with open("aotm.csv", 'w') as files:
        files.write('session_id;user_id;item_id;timeframe;eventdate' + '\n')
        with open(data, "r") as f:
            #user_id;session_id;item_id;timeframe;ArtistId
            reader = csv.reader(f, delimiter='	')   
            next(reader)
            for linha in reader:
                #print("asctime(localtime(secs)): %s" % time.asctime(time.localtime(int(linha[3]))))
                #print(linha)
                #print(linha[0])
                files.write(linha[1] + ';' + linha[0] + ';' + linha[2] + ';' + '0' + ';' + linha[3] + '\n')
    print("Done!")     
