import requests, time, json, os

f1 = open("messages.json", "r")
data = json.loads(f1.read())
f1.close()

#change these
guild_id = ""
author_id = ""
#times should be ceil( user messages count / 25 )
times = 1916

#1916 is an arbitrary number. discord actually stops us at 200 pages, I think
for i in range(1916):

    print(i)
    resp = requests.get("https://discord.com/api/v9/guilds/"+guild_id+"/messages/search?author_id="+author_id+"&offset="+str(i*25), headers={"Authorization": os.getenv('token')})
    resp = resp.json()

    #handle ratelimits. although... its better to just stop for a minute or two, and the ratelimit will be reset, because sending request right after message isnt very good
    if 'messages' not in resp.keys():
        duration = math.ceil(resp['retry_after'])+1
        print("Ratelimited, sleeping for "+str(duration)+" seconds")
        time.sleep(duration)
        resp = requests.get("https://discord.com/api/v9/guilds/"+guild_id+"/messages/search?author_id="+author_id+"&offset="+str(i*25), headers={"Authorization": os.getenv('token')})
        resp = resp.json()

    messages_list = [item[0] for item in resp['messages']]

    messages_list = [*data['messages'], *messages_list]

    before = len(messages_list)
    #remove duplicates
    #use enumerate to get position, and check to see if the position is the first index of the element found in list
    messages_list = [item for pos, item in enumerate(messages_list) if messages_list.index(item) == pos]
    after = len(messages_list)
    if after != before:
        print(str(before-after)+" items removed for duplicate")
    data['messages'] = messages_list

    f2 = open("messages.json", "w")
    f2.write(json.dumps(data, indent=4))
    f2.close()
    print('saved now '+str(len(data['messages']))+" items long")

    #try not to get ratelimited
    time.sleep(1.5);
