import requests
import time
import termcolor

options = []

channel = input("Loja alvo: ").lower()

token = input(" 'JWT Token': ").strip()

print("")

channel_id = requests.get("https://api.streamelements.com/kappa/v2/channels/"+channel, headers={"Accept":"application/json", "Authorization":"Bearer "+token}).json()["_id"]

itemapi = requests.get("https://api.streamelements.com/kappa/v2/store/"+channel_id+"/items", headers={"accept":"application/json"}).json()

for itenn in itemapi:
    options.append({"name":itenn["name"], "cooldown":itenn["cooldown"]["user"], "id":itenn["_id"], "cost":itenn["cost"]})
print(termcolor.colored("=", "red")*100)

for indexdisp in options:
    print("[{}] {}".format(termcolor.colored(options.index(indexdisp), "magenta"), termcolor.colored(indexdisp["name"], "cyan")))
print(termcolor.colored("=", "red")*100)

print("")

choice = options[int(input("Escolha o número relativo ao item: "))]

print("")
print(termcolor.colored("=", "red")*100)
print("Nome: {}\nCooldown: {}\nID: {}\nPreço: {}".format(choice["name"], choice['cooldown'], choice["id"], choice["cost"]))
print(termcolor.colored("=", "red")*100)
print("")

quant = int(input("Quantidade: "))
msg = input("Caso seja uma mensagem: ").strip()
print("")

for a in range(quant):
    data = '{"input":[],"message":"try"}'.replace("try", msg)
    rsp = requests.post("https://api.streamelements.com/kappa/v2/store/"+channel_id+"/redemptions/"+choice["id"], headers={"Authorization":"Bearer "+token, "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0", "Accept":"application/json, text/plain, */*", "Accept-Language":"en-US,en;q=0.5", "Accept-Encoding":"gzip, deflate", "Referer":"https://streamelements.com/", "Content-Type":"application/json;charset=utf-8", "Origin":"https://streamelements.com"}, data=data)
    if rsp.status_code == 200:
        print(termcolor.colored("Você resgatou o item com êxito!", "green") + " [{}]".format(choice["name"]))

    else:
        print(termcolor.colored("Erro ao comprar o item selecionado!", "red" + " [SERVER RESPONSE: {}]".format(rsp.text)))
    if quant > 1 and a < quant-1:
        print(termcolor.colored("Item em cooldown... [{} sec]".format(choice['cooldown']), "yellow"))
        time.sleep(choice['cooldown'])