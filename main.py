import requests, time, json, os

f1 = open("messages.json", "r")
data = json.loads(f1.read())
f1.close()

guild_id = ""
author_id = ""

#1916
for i in range(1916):
    if i < 11:
        continue;

    print(i)
    resp = requests.get("https://discord.com/api/v9/guilds/"+guild_id+"/messages/search?author_id="+author_id+"&offset="+str(i*25), headers={"Authorization": os.getenv('token')})
    resp = resp.json()

    if 'messages' not in resp.keys():
        print(resp)

    messages_list = [item[0] for item in resp['messages']]

    messages_list = [*data['messages'], *messages_list]

    #remove duplicates
    #use enumerate to get position, and check to see if the position is the first index of the element found in list
    data['messages'] = [item for pos, item in enumerate(messages_list) if messages_list.index(item) == pos]

    f2 = open("messages.json", "w")
    f2.write(json.dumps(data, indent=4))
    f2.close()
    print('saved now '+str(len(data['messages']))+" items long")

    #try not to get ratelimited
    time.sleep(1.5);
