def script(route):
    if route=="0":
        if 3 in keys:
           print("Roxy reblocks the bridge.\n")
           keys.remove(3)
    if route==5:
        if 2 not in keys:
           print("You find a Silver Ring.\n")
           keys.append(2)

print("""Generic Monster Battle Game
By Nicholas Fletcher

--------------------------
""") # Edit this to include your title and name.

# Do not go below this point if you are only scripting. The main source code is below here.

class monster(object):
    def __init__(self,name,element,hp,p_atk,p_def,s_atk,s_def,id_num,level=0,xp=0):
        self.level = int(level)
        self.name = name
        self.element = int(element)
        self.atk = [0,int(p_atk)+self.level,int(s_atk)+self.level]
        self.defe = [0,int(p_def)+self.level,int(s_def)+self.level]
        self.hp = int(hp)+(self.level*2)
        self.maxhp = int(hp)+(self.level*2)
        self.id_num = int(id_num)
        self.level = int(level)
        self.xp = int(xp)
        self.moves = []
    def __str__(self):
        return """%s -- Lvl: %i (%i/8) -- %s -- HP: %i/%i
PhA: %i -- PhD: %i -- SpA: %i -- SpD: %i""" % (self.name, self.level+1, self.xp, elements[self.element], self.hp, self.maxhp, self.atk[1], self.defe[1], self.atk[2], self.defe[2])
    def short(self):
        return """%s -- Lvl: %i (%i/8) -- %s -- HP: %i/%i""" % (self.name, self.level+1, self.xp, elements[self.element], self.hp, self.maxhp)
    def learn(self,attack):
        self.moves.append(moves[int(attack)])
    def shortmoves(self):
        smoves = ""
        for x in self.moves[:-1]:
            smoves += x.name
            smoves += ", "
        smoves += self.moves[-1].name
        return smoves
    def level_up(self):
        self.xp = self.xp + 1
        if self.xp >= 8:
            print(vocab[10] %(self.name))
            for index in range(3):
                self.atk[index] = self.atk[index] +1
                self.defe[index] = self.defe[index] +1
            self.maxhp = self.maxhp+2
            self.hp = self.maxhp
            self.level = self.level+1
            self.xp = 0
    def take_damage(self,power,element,category):
        damage=power
        damage-=self.defe[category]
        if self.element in overpower[element]:
            damage+=randint(1,3)
            print(vocab[2])
        self.hp-=damage
        if not self.is_alive():
            self.hp = 0
        return damage
    def heal(self,amount=None):
        if amount is None:
            amount = self.maxhp
        self.hp+=amount
        if self.hp > self.maxhp:
            self.hp = self.maxhp
    def is_alive(self):
        return bool(self.hp > 0)
    def capture(self,boost=0):
        roll = randint(1,self.maxhp)
        roll -= self.hp
        roll += boost
        if bool(roll>=1):
            return True
        else:
            return False

class move(object):
    def __init__(self, name, element, category, power):
        self.name = name
        self.element = int(element)
        self.category = int(category)
        self.power = int(power)
    def __str__(self):
        return "%s: Power %i %s (%s)" %(self.name, self.power, elements[self.element], categories[self.category])
    def use(self,user):
        damage=self.power
        damage+=randint(-1,1)
        damage+=user.atk[self.category]
        return damage

class location(object):
    def __init__(self, name, encounters, connections, loc_type="wild", lock=0, master=None, code=None, level=0):
        self.name = name
        self.encounters = encounters
        self.connections = connections
        self.loc_type = loc_type
        self.lock = lock
        self.master = master
        self.code = code
        self.level = level
    def __str__(self):
        return "%s: %s" %(self.name,self.loc_type)
    def rand_encounter(self):
        if self.loc_type == "wild":
            enc_id = randint(1,len(self.encounters))-1
            return self.encounters[enc_id]
        else:
            return None

class master(object):
    def __init__(self, name, team, key=0):
        self.name = name
        self.team = team
        self.key = int(key)
    def __str__(self):
        return "%s" %(self.name)
    def trash(self):
        self.team.pop(0)
        if len(self.team)==0:
            return "done"
        else:
            return "more"

# File reading and processing starts here.
print("Loading terms...")
vocab = []
with open("Vocab.txt") as f:
    for line in f:
        vocab.append(line)
messages = []
with open("Messages.txt") as f:
    for line in f:
        messages.append(line)

print("Loading keys...")
keylist = []
with open("Keys.txt") as f:
  for num, line in enumerate(f):
    line = line.rstrip()
    linelist = line.split()
    keylist.append([linelist[0],linelist[1].replace("_"," "),linelist[2]])

print("Loading elements...")
elements = ["Null"]
overpower = [["Null"]]
with open("Elements.txt") as f:
    for line in f:
        line = line.rstrip()
        linelist = line.split()
        elements.append(linelist[1])
        overpower.append([])
        for i in linelist[2:]:
            overpower[-1].append(int(i))

moves = []
categories = ["Null","Physical","Special"]

print("Loading moves...")
with open("Moves.txt") as f:
    for line in f:
        line = line.rstrip()
        linelist = line.split()
        moves.append(move(linelist[1].replace("_"," "), linelist[2], linelist[3], linelist[4]))

print("Loading monsters...")
monsters = []
with open("Monsters.txt") as f:
  for num, line in enumerate(f):
    line = line.rstrip()
    linelist = line.split()
    monsters.append(monster(linelist[1], linelist[2], linelist[3], linelist[4], linelist[5], linelist[6], linelist[7], num))
    for i in linelist[8:]:
        monsters[-1].learn(i)

def instance(base_id,level=0,xp=0):
    base = monsters[base_id]
    new = monster(base.name, base.element, base.maxhp, base.atk[1], base.defe[1], base.atk[2], base.defe[2], base.id_num,level,xp)
    new.moves = base.moves
    return new

print("Loading masters...")
masters = []
with open("Masters.txt") as f:
  for line in f:
    line = line.rstrip()
    linelist = line.split()
    master_name = linelist[1].replace("_"," ")
    master_key = linelist[2]
    master_level = linelist[3]
    team_list = []
    for i in linelist[5:]:
        team_list.append(instance(int(i),master_level))
    masters.append(master(master_name,team_list,master_key))

print("Loading locations...")
locations = []
with open("Locations.txt") as f:
  for line in f:
    line = line.rstrip()
    linelist = line.split()
    place_name = linelist[1].replace("_"," ")
    wild_level = int(linelist[2])
    encounter_list = []
    connection_list = []
    flip_line = 0
    lockkey = 0
    wildmaster = None
    code = int(linelist[0])
    for i in linelist[3:]:
        if i == "|":
            flip_line = flip_line + 1
        elif flip_line == 0:
            encounter_list.append(int(i))
        elif flip_line == 1:
            if i[0] == "T":
                connection_list.append(i)
            else:
                connection_list.append(int(i))
        elif flip_line == 2:
            lockkey=int(i)
            flip_line = 3
        elif flip_line == 3:
            wildmaster=masters[int(i)]
            flip_line = 999
    if encounter_list==[]:
        xyz="road"
    else:
        xyz="wild"
    locations.append(location(place_name,encounter_list,connection_list,xyz,lockkey,wildmaster,code,wild_level))

print("Loading towns...")
towns = []
with open("Towns.txt") as f:
  for line in f:
    line = line.rstrip()
    linelist = line.split()
    code = linelist[0][1:]
    town_name = linelist[1].replace("_"," ")
    connection_list = []
    local_master = None
    flip_line = False
    for i in linelist[2:]:
        if flip_line == True:
            local_master=masters[int(i)]
        elif i == "|":
            flip_line = True
        elif i[0] == "T":
            connection_list.append(i)
        else:
            connection_list.append(int(i))
    towns.append(location(town_name,[],connection_list,"town",0,local_master,code,0))

print("\n--------------------------\n")

def read_save(file_name):
    savelines = []
    with open(file_name) as f:
        for line in f:
            line = line.rstrip()
            linelist = line.split()
            linelist.pop(0)
            savelines.append(linelist)
    return savelines

import os.path
if os.path.isfile("Save.txt"):
    while True:
        print("[L]oad your save or [C]reate a new file?")
        save_cmd = input("> ")
        if save_cmd == "l" or save_cmd == "L":
            savelines = read_save("Save.txt")
            print("Loading save...")
            break
        elif save_cmd == "c" or save_cmd == "C":
            savelines = read_save("Start.txt")
            print("Creating new file...")
            break
        else:
            print("Not sure what you mean.\n")
else:
    savelines = read_save("Start.txt")
    print("Creating new file...")

startpoint = int(savelines[0][0])
startparty = []
for (n,l,x) in zip(savelines[1],savelines[2],savelines[3]):
    char = instance(int(n),int(l),int(x))
    startparty.append(char)
startstorage = []
for (n,l,x) in zip(savelines[4],savelines[5],savelines[6]):
    char = instance(int(n),int(l),int(x))
    startstorage.append(char)
startkeys = []
for n in savelines[7]:
    startkeys.append(int(n))

# The gameplay functions start here.
def fight(attacker, target, attack):
    print("%s uses %s!" %(attacker.name,attack.name))
    damage = attack.use(attacker)
    damage = target.take_damage(damage,attack.element,attack.category)
    print("%s takes %i damage!" %(target.name,damage))
    if target.hp == 0:
        message = (vocab[1] %(target.name))
        print(message)
    print("")

def pickmove(user):
    for n, m in enumerate(user.moves):
        print(str(n+1)+": ",end="")
        print(m)
    while True:
        x = input("> ")
        if x.isdigit():
            if int(x) <= len(user.moves):
                return user.moves[int(x)-1]
            else:
                print("%s doesn't know that many moves."%(user.name))
        else:
            print("That doesn't make sense.")

def pick_location(current_loc,party):
    script(current_loc.code)
    town_track = print_locs(current_loc)
    while True:
        x = input("> ")
        if x.isdigit():
            x = int(x)
            if x <= len(current_loc.connections):
                if town_track[x-1] == True:
                    x = int(current_loc.connections[x-1][1:])
                    if towns[x].code == current_loc.code:
                        global player_storage
                        town_loop(party,player_storage,current_loc)
                        return current_loc,"closed"
                    else:
                        return towns[x],"closed"
                else:
                    test=locations[current_loc.connections[x-1]]
                    if test.lock != 0:
                        if test.lock in keys:
                            return test,"open"
                        else:
                            if keylist[test.lock][2] == "1":
                                print("You can't go there. You need the %s!"%(keylist[test.lock][1]))
                            else: 
                                print("You can't go there. You need to defeat %s!"%(keylist[test.lock][1]))
                    else:
                        return test,"open"
            else:
                print("That doesn't make sense.")
        elif x == "S" or x == "s":
            party = switch(party,False)
            return current_loc,"closed"
        elif x == "I" or x == "i":
            show_keys()
            return current_loc,"closed"
        elif (x == "C" or x == "c") and current_loc.master != None and current_loc.loc_type != "town":
            master_loop(party,current_loc.master)
            return current_loc,"closed"
        else:
            print("That doesn't make sense.")

def print_locs(current_loc):
    town_track = []
    global locations
    for n, loc in enumerate(current_loc.connections):
        if isinstance(loc,str):
            town_id = int(loc[1:])
            print(str(n+1)+": %s."%(towns[town_id].name))
            town_track.append(True)
        else:
            print(str(n+1)+": %s."%(locations[loc].name),end="")
            if locations[loc].lock != 0:
                if keylist[locations[loc].lock][2] == "1":
                    print(" (Need %s.)"%(keylist[locations[loc].lock][1]))
                else:
                    test=locations[loc]
                    global keys
                    if keylist[test.lock][2] == "0" and test.lock not in keys:
                        print(" (Need to defeat %s.)"%(keylist[locations[loc].lock][1]))
                    else:
                        print("")
            else:
                print("")
            town_track.append(False)
    print("S: Switch.")
    print("I: Check Inventory.")
    if current_loc.master != None and current_loc.loc_type != "town":
        print("C: Challenge %s." %(current_loc.master.name))
    return town_track

def foeturn(user,target):
    if user.is_alive():
        fight(user,target,user.moves[randint(1,len(user.moves))-1])

def switch(party,battle=True):
    while True:
        for n, p in enumerate(party):
            print(str(n+1)+": ",end="")
            print(p.short())
        x = input("> ")
        if x.isdigit():
            x=int(x)
            if x > len(party):
                print("Your team isn't that big.")
            elif not party[x-1].is_alive():
                print(vocab[8]%(party[x-1].name)+"\n")
            elif x == 1:
                print(vocab[9]%(party[x-1].name)+"\n")
                if not battle:
                    return party
            elif x <= 0:
                print("That doesn't make sense.")
            else:
                if battle:
                    print(vocab[0]%(party[x-1].name)+"\n")
                else:
                    print(vocab[7]%(party[x-1].name))
                party[0],party[x-1] = party[x-1],party[0]
                return party
        else:
            print("That doesn't make sense.")

import copy
def master_loop(party,npc):
    print("\n--------------------------\n\n")
    npc_ins = copy.deepcopy(npc)
    print(vocab[11]%(npc_ins.name))
    masterstate = "more"
    while masterstate != "done":
        print(npc_ins.name + " sends out " + npc_ins.team[0].name+"!\n")
        status = battle(player_party,npc_ins.team[0],False)
        if status=="fail":
            print("\n" + npc_ins.name + " has defeated you.\nThey fully heal your team.")
            for p in party:
                p.heal()
            return "XXX"
        else:
            masterstate = npc_ins.trash()
            print("--------------------------\n")
    print("You have defeated " + npc_ins.name + "!")
    if npc_ins.key != 0:
        global keys
        if npc_ins.key not in keys and keylist[npc_ins.key][2] == "1":
            print("They give you the " + keylist[npc_ins.key][1] + "!")
        keys.append(npc_ins.key)

def town_loop(party,bank,city):
    print("\n--------------------------\n")
    while True:
        print(city.name+":\n")
        print(messages[int(city.code)]+"\n")
        for p in party:
            print(p.short())
        global towns
        if city.master != None:
                    cmd = input("\n[H]eal, [O]pen Storage, [C]hallenge " + city.master.name + "\n[R]ecord your Save, [S]witch Team Members or [L]eave?\n>")
        else:
            cmd = input("\n[H]eal, [O]pen Storage, [R]ecord \nyour Save, [S]witch Team Members or [L]eave?\n>")
        if cmd == "H" or cmd == "h":
            for p in party:
                p.heal()
            print("Your team is healed.")
        elif cmd == "O" or cmd == "o":
            storage(party,bank)
        elif cmd == "L" or cmd == "l":
            break
        elif cmd == "S" or cmd == "s":
            party = switch(party)
        elif cmd == "R" or cmd == "r":
            writesave(party,bank,city.code)
        elif (cmd == "C" or cmd == "c") and city.master != None:
            master_loop(party,city.master)
        else:
            print("Not sure what you want.\n")
        print("\n--------------------------\n")

def writesave(party,bank,code):
    with open("Save.txt","w") as f:
        f.write("x "+str(code)+"\n")
        f.write("x ")
        for i in party:
            f.write(str(i.id_num)+" ")
        f.write("\nx ")
        for i in party:
            f.write(str(i.level)+" ")
        f.write("\nx ")
        for i in party:
            f.write(str(i.xp)+" ")
        f.write("\nx ")
        for i in bank:
            f.write(str(i.id_num)+" ")
        f.write("\nx ")
        for i in bank:
            f.write(str(i.level)+" ")
        f.write("\nx ")
        for i in bank:
            f.write(str(i.xp)+" ")
        f.write("\nx ")
        global keys
        for i in keys:
            f.write(str(i)+" ")
    print("Save recorded.\n")

def show_keys():
    print("\nYou have the following items:\n")
    global keys
    for i in keys:
        if keylist[i][2] == "1":
            print(keylist[i][1])
    

def storage(party,bank):
    while True:
        print("\n--------------------------\n\nYou open your storage.\n")
        cmd = input("[D]eposit, [W]ithdraw or [L]eave?\n>")
        if cmd == "D" or cmd == "d":
            deposit(party,bank)
        elif cmd == "W" or cmd == "w":
            withdraw(party,bank)
        elif cmd == "L" or cmd == "l":
            break
        else:
            print("Not sure what you want.\n")

def deposit(party,bank):
    while True:
        if len(party) == 1:
            print("You've only got %s left."%(party[0].name))
            break
        print("\n0: Exit")
        for n, p in enumerate(party):
            print(str(n+1)+": ",end="")
            print(p.short())
            print(p.shortmoves())
        x = input("> ")
        if x.isdigit():
            x=int(x)
            if x > len(party):
                print("Your team isn't that big.")
            elif x == 0:
                break
            else:
                print("%s is now in storage."%(party[x-1].name))
                bank.append(party.pop(x-1))
        else:
            print("That doesn't make sense.")

def withdraw(party,bank):
    while True:
        if len(party) >= 6:
            print("Your team is full.")
            break
        if len(bank) == 0:
            print("Your storage is empty.")
            break
        print("\n0: Exit")
        for n, p in enumerate(bank):
            print(str(n+1)+": ",end="")
            print(p.short())
        x = input("> ")
        if x.isdigit():
            x=int(x)
            if x > len(party):
                print("Your team isn't that big.")
            elif x == 0:
                break
            else:
                print("%s is now in your party."%(bank[x-1].name))
                party.append(bank.pop(x-1))
        else:
            print("That doesn't make sense.")

def battle(party,foe,speak=True):
    foe.hp=foe.maxhp
    if speak == True:
        print(vocab[3]%(foe.name))
    while True:
        active=party[0]
        print(active)
        print("")
        print(foe.short())
        if speak == True:
            cmd = input("\n[F]ight, [S]witch, [C]apture or [R]un?\n>")
        else:
            cmd = input("\n[F]ight or [S]witch?\n>")
        if cmd == "F" or cmd == "f":
            attack = pickmove(active)
            print("")
            fight(active,foe,attack)
            foeturn(foe,active)
        elif cmd == "S" or cmd == "s":
            party = switch(party)
            active=party[0]
            foeturn(foe,active)
        elif speak == True:
            if cmd == "C" or cmd == "c":
                success = foe.capture()
                if success == True:
                    print(vocab[4]%(foe.name))
                    if len(party) >= 6:
                        print(vocab[6] %(foe.name))
                        global player_storage
                        player_storage.append(foe)
                    else:
                        party.append(foe)
                    return "capture"
                else:
                    print(vocab[5])
                    foeturn(foe,active)
            elif cmd == "R" or cmd == "r":
                print("You attempt to flee the battle.")
                if randint(1,3) == 1:
                    print("You can't get away!\n")
                    foeturn(foe,active)
                else:
                    print("You escape the battle.")
                    return "run"
            else:
                print("Not sure what you want.\n")
        else:
                print("Not sure what you want.\n")
        if not foe.is_alive():
            if foe.level >= active.level - 1:
                active.level_up()
            return "win"
        elif not active.is_alive():
            for h in party:
                if h.is_alive():
                    break
            else:
                print("Your team has fallen.")
                return "fail"
            print("You must switch.")
            party = switch(party)
        print("\n--------------------------\n")


# The actual gameplay loop starts here.
from random import randint
player_party = startparty
player_storage = startstorage
keys = startkeys
status = "win"
location = towns[startpoint]
forceenter=True
while status != "fail":
    if forceenter == False:
        print("You are in %s." %(location.name))
        print("Where will you go next?")
        print("\n--------------------------\n")
        location,status = pick_location(location,player_party)
    if location.loc_type == "wild":
        if randint(0,2) != 0 and status == "open":
            wild = instance(location.rand_encounter(),location.level)
            status = battle(player_party,wild)
        else:
            status = "open"
    elif location.loc_type == "town":
        if forceenter == True:
            forceenter = False
            town_loop(player_party,player_storage,location)
    print("\n--------------------------\n")
print("Game Over.")