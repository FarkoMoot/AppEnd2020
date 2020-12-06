try:
    # -*- coding: latin-1 -*-
    # Importa as bibliotecas necessarias
    from time import sleep
    from datetime import datetime
    import paho.mqtt.client as mqtt
    import pymongo
    import os

    # CONFIGURÇÕES MONGODB
    def init_mongo():
        global db, hw, app
        while True:
            try:
                # Conecta ao server do MongoDB
                cliente = pymongo.MongoClient(
                    'mongodb://admin:b00tk1ll22031998@10.0.0.172:27888/?authSource=admin')
                break
            except:
                print('Erro 01: Erro ao conectar ao servidor mongo')
                init_mongo()

        # Seleciona o banco
        db = cliente.peixe
        # Seleciona a colection HW
        hw = db.hw
        # Seleciona a colection APP
        app = db.app

    # INICIA O MQTT
    client = mqtt.Client()
    client.connect("10.0.0.172", 1883, 60)
    client.loop_start()

    # Função de receber e
    def init_var(x=0):
        # Chama a função d_ini
        d_ini(x)
        # Atribui valores as variaveis de controle
        while x < numesp:
            motor.append(0)
            controlali.append(0)
            hdesl.append(0)
            if horai[x] > horaf[x]:
                tempototalali.append((horaf[x]-horai[x]) + 86400)
            else:
                tempototalali.append(horaf[x]-horai[x])
            intervaloali.append((tempototalali[x]/numali[x]))
            margemerro.append(horai[x]+10)
            x += 1

    # Obtem as variaveis do server MongoDB

    def d_ini(x=0):
        while x < numesp:
            placa = "tk%s" % (x)
            dado = hw.find_one({"_id": placa})
            horai.append(dado["horai"]*60)
            horaf.append(dado["horaf"]*60)
            numali.append(dado["numali"])
            tempoali.append(dado["tempoali"]*60)
            horareset.append(dado["horai"]*60)
            is_on.append(dado["is_on"])
            x += 1

    # Manda comando para todas as ESP8266 começarem desligadas por padrão

    def desl(x=0):
        while x < numesp:
            placa = "tk%s" % (x)
            client.publish(placa+"/onoff", "D")
            x += 1

    # Funções para dar update nos dados ou adicionar esp ano

    def update_db(numesp):
        # Recebe variavel de controle do server
        ctrl = hw.find_one({"_id": "ctrl"})
        control = ctrl["control"]
        tara = ctrl["tara"]

        # Obtem numesp para verificar se teve adicão de novas placas na rede
        e = hw.find_one({"_id": "numesp"})
        nesp = e["numesp"]

        # Atualiza os dados
        if(control == 1 and nesp == numesp and tara == 0):
            d_update()
            hw.update_one({'_id': 'ctrl'}, {'$set': {'control': 0}})

        # Se for adicionado mais uma esp
        elif(control == 1 and nesp > numesp and tara == 0):
            add = nesp-numesp
            numesp = numesp+add
            init_var(nesp-add)
            d_update()
            hw.update_one({'_id': 'ctrl'}, {'$set': {'control': 0}})
        # Confere a tara
        elif(control == 1 and tara != 0):
            tk_tara = tara[0:4]
            tara_s_n = tara[5:]
            if(tara_s_n == 1):
                client.publish(tk_tara+"/onoff", "L")
                sleep(60.0)
                client.publish(tk_tara+"/onoff", "D")

    def d_update(x=0):
        while x < numesp:
            placa = "tk%s" % (x)
            dado = hw.find_one({"_id": placa})
            horai[x] = (dado["horai"]*60)
            horaf[x] = (dado["horaf"]*60)
            numali[x] = (dado["numali"])
            tempoali[x] = (dado["tempoali"]*60)
            horareset[x] = (dado["horai"]*60)
            is_on[x] = (dado["is_on"])
            motor[x] = 0
            controlali[x] = 0
            hdesl[x] = 0
            if horai[x] > horaf[x]:
                tempototalali[x] = (horaf[x]-horai[x]) + 86400
            else:
                tempototalali[x] = horaf[x]-horai[x]
            intervaloali[x] = (tempototalali[x]/numali[x])
            margemerro[x] = horai[x]+10
            x += 1

    # MQTT SUBSCRIBE
    # Atualiza Temp e Comida a cada 30 segundos

    def switching(m):
        # Se segundos for igual a 0
        if (m == 0):
            # Subscribe no topico temp
            client.subscribe(esp+"/temp")
            # Se tiver mensagem chama a função on_message_temp
            client.on_message = on_message_temp

        else:
            # Se não Unsubscribe no topico temp
            client.unsubscribe(esp+"/temp")

        # Se segundos for igual a 30
        if (m == 30):
            # Subscribe no topico comid
            client.subscribe(esp+"/comid")
            # Se tiver mensagem chama a função on_message_comid
            client.on_message = on_message_comid
        else:
            # Se não Unsubscribe no topico comid
            client.unsubscribe(esp+"/comid")

    # Função para decodificar a mensagem

    def on_message_temp(client, userdata, msg):
        t_esp = msg.topic[0:3]
        # Salva a mensagem do topico na variavel dados_temp
        dados_temp = msg.payload.decode()
        # Faz o update do dado de temperatura no server
        app.update_one({'_id': t_esp}, {
                       '$set': {'temp': float(dados_temp[0:5])}})

    def on_message_comid(client, userdata, msg):
        t_esp = msg.topic[0:3]
        # Salva a mensagem do topico na variavel dados_comid
        dados_comid = msg.payload.decode()
        # Faz o update do dado de comida no server
        app.update_one({'_id': t_esp}, {
                       '$set': {'comid': float(dados_comid[0:5])}})

    # Inicia o Mongo
    init_mongo()

    # Confere se o usuario digitou corretamente o servidor mongo e se conectar ao server obtem a variavel de quantas ESP8266 tem no sistema
    #while True:
        #try:
            #n = hw.find_one({"_id": "numesp"})
            #break
        #except:
            #print('Erro 02: erro ao conectar ao servidor mongo')
            #init_mongo()

    # Obtem a variavel de quantas ESP8266 tem no sistema
    n = hw.find_one({"_id": "numesp"})
    numesp = n["numesp"]

    # Variaveis de controle das ESP's
    horai = []
    horareset = []
    horaf = []
    numali = []
    tempoali = []
    tempototalali = []
    intervaloali = []
    margemerro = []
    motor = []
    controlali = []
    hdesl = []
    is_on = []
    i = 0

    # Chama a função init_var()
    init_var()

    # Chama a função desl()
    desl()

    file = open('teste.txt', 'w')

    # Void Loop :)
    while True:
        # Obtem o horario atual antes da execução do codigo
        t = datetime.now()

        # Salva em S1 os segundos e microsegundos para calcular tempo de maquina
        s1 = float(f'{t.second}.{t.microsecond}')

        # Chama update_db
        update_db(numesp)

        # Converte as horario atual para segundos
        hora = (((t.hour*60)+t.minute)*60)+t.second

        # Salva em S1 os segundos e microsegundos para calcular tempo de maquina
        s1 = float(f'{hora}.{t.microsecond}')

        # Printa variavel de hora para conferencia
        print(f'{t.hour}:{t.minute}:{t.second}')

        # Laço para processar os dados e atuar todas as placas
        while i < numesp:
            esp = "tk%s" % (i)
            if(is_on[i] == 1):
                #  Obtem os dados da ESP8266 Temperatura e Comida
                switching(t.second)
                # Logica de Ligar o Motor
                if hora >= horai[i] and hora <= margemerro[i] and motor[i] == 0:
                    motor[i] = 1
                    # Manda comando para a ESP8266 ligar o motor
                    client.publish(esp+"/onoff", "L")
                    hdesl[i] = horai[i] + tempoali[i]
                    controlali[i] = controlali[i]+1
                    file.write(
                        f'A {esp} ligou as {t.hour}:{t.minute}:{t.second} e controlali = {controlali[i]} \n')
                if hora >= hdesl[i] and motor[i] == 1:
                    motor[i] = 0
                    # Manda comando para a ESP8266 desligar o motor
                    client.publish(esp+"/onoff", "D")
                    horai[i] = horai[i] + intervaloali[i]
                    margemerro[i] = horai[i]+10
                    file.write(
                        f'A {esp} desligou as {t.hour}:{t.minute}:{t.second} \n')
                if numali[i] == controlali[i]:
                    horai[i] = horareset[i]
                    controlali[i] = 0
                    file.write(f'Resetou as {t.hour}:{t.minute}:{t.second} \n')
                i += 1
            else:
                i += 1
                print(f'Ignorou o {esp} \n')
        i = 0

        # Obtem o horario atual depois da execução do codigo
        t2 = datetime.now()

        # Converte as horario atual para segundos
        hora2 = (((t2.hour*60)+t2.minute)*60)+t2.second

        # Salva em S1 os segundos e microsegundos para calcular tempo de maquina
        s2 = float(f'{hora2}.{t2.microsecond}')

        # GAMBIARRA
        # Calcula o tempo de maquina
        if s2 > s1:
            s3 = s2-s1
        else:
            s3 = s1-s2
            file.write(
                f'Caiu na exceção as {t.hour}:{t.minute}:{t.second} \n'),
        # Delay de 1 segundo menos o tempo maquina
        if s3 > 1:
            sleep(0.00000001)
        else:
            sleep(1.0-s3)


except KeyboardInterrupt:
    file.write("Até mais :)")
    file.close()
    print("Até mais :)")
