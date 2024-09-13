import time
import requests, json, random, os
import random
import string
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

'''
Description:

A simple pokerogue.net
profile and game save editor.

Original Author: Onyxdev
Current Maintainer: fire6945

'''

class pokeRogue:

    def __init__(self, user, password, log_error = True):
        
        #Login api url
        self.login_url = "https://api.pokerogue.net/account/login"
        
        #Get trainer data api url
        self.trainer_data_url = "https://api.pokerogue.net/savedata/system/get"
        
        #Update trainer data api url
        self.update_trainer_data_url = "https://api.pokerogue.net/savedata/updateall"
        
        #Get gamesave data api url (slot required) -> int 0-4
        self.gamesave_slot_url = "https://api.pokerogue.net/savedata/session/get?slot="
        
        #Update gamesave data api url (slot required) -> int 0-4
        self.update_gamesave_slot_url = "https://api.pokerogue.net/savedata/updateall"
        
        #Login headers
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Brave\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Origin": "https://pokerogue.net"
            }
        
        #Login payload
        self.data = {
            "username": user,
            "password": password
            }   

        #Initiate authentication token    
        with requests.session() as s:
            
            try:
             self.auth = s.post(self.login_url, headers = self.headers, data = self.data).json()["token"]
             
            except Exception as e:
                
                if log_error:
                 print(f"Error on __init__ self.auth -> {e}")

        #Session headers with authentication token
        self.auth_headers = {
         "authorization": self.auth,
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
         "sec-ch-ua": "\"Brave\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
         "sec-ch-ua-mobile": "?0",
         "sec-ch-ua-platform": "\"Windows\"",
         "Origin": "https://pokerogue.net"
        }
        
        self.clientSessionId = self.random_string(32)

        #Pokedex IDs by Pokemon name -> data['bulbasaur'] >> 1
        with open("./data/pokemon.json") as f:
            self.pokemon_id_by_name = json.loads(f.read())

            
        #Contains extra data for some functions
        with open("./data/data.json") as f:
            self.extra_data = json.loads(f.read())

    def random_string(self, length: int, seeded: bool = False, seed: int = None) -> str:
        characters = string.ascii_letters + string.digits
        result = []

        if seeded and seed is not None:
            random.seed(seed)
        
        for _ in range(length):
            random_index = random.randint(0, len(characters) - 1)
            result.append(characters[random_index])

        return ''.join(result)

    #Get trainer data -> json
    def get_trainer_data(self):
        
        try:
            
            with requests.session() as s:
                urlWithSession = self.add_session_query_param(self.trainer_data_url)
                data = s.get(urlWithSession, headers = self.auth_headers).json()
                return data
        
        except Exception as e:
            print(f"Error on get_trainer_data() -> {e}")

    #Get saved game data (slot required -> int 1-5) -> json
    def get_gamesave_data(self, slot=1):

        try:
            
            with requests.session() as s:
                urlWithSession = self.add_session_query_param(f"{self.gamesave_slot_url}{slot-1}")
                data = s.get(urlWithSession, headers = self.auth_headers).json()
                return data

        except Exception as e:
            print(f"Error on get_gamesave_data() -> {e}")
    
    def add_session_query_param(self, url):
        if self.clientSessionId is None:
            self.clientSessionId = self.random_string(32)

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['clientSessionId'] = [self.clientSessionId]

        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=new_query_string))

        return new_url

    #Update trainer data from json payload -> None
    def update_trainer_data(self, payload):

        try:

            with requests.session() as s:
                slot0Data = self.get_gamesave_data(1)
                data = {
                    "session": slot0Data,
                    "system": payload,
                    "clientSessionId": self.clientSessionId,
                    "sessionSlotId": 0
                }
                data = s.post(self.update_trainer_data_url, headers = self.auth_headers, json = data)
                return data

        except Exception as e:
            print(f"Error on update_trainer_data() -> {e}")

    #Update game data from json payload (slot required -> int 1-5) -> None
    def update_gamesave_data(self, payload):

        try:            
            with requests.session() as s:
                data = s.post(self.update_gamesave_slot_url, headers = self.auth_headers, json = payload)
                return data

        except Exception as e:
           print(f"Error on update_gamesave_data() -> {e}")
           
    #Dump trainer data to json file -> None
    def dump_trainer_data(self):

        try:

            with open("trainer.json", "w") as f:
                f.write(json.dumps(self.get_trainer_data(), indent=2))
                print("Your trainer data has been dumped! -> trainer.json")

        except Exception as e:
            print(f"Error on dump_trainer_data() -> {e}")

    #Dump gamesave data to json file (slot required -> int 1-5) -> None
    def dump_gamesave_data(self, slot = None):

        try:

            if not slot:
                slot = int(input("Slot(1-5): "))
                if slot > 5: return print(f"This slot does not exist!")
                if slot < 1: return print(f"This slot does not exist!")

            with open(f"slot {slot}.json", "w") as f:
                f.write(json.dumps(self.get_gamesave_data(slot), indent=2))
                print(f"The saved game on slot {slot} has been dumped! -> slot {slot}.json")

        except Exception as e:
            print(f"Error on dump_trainer_data() -> {e}")


    #Update trainer data from json dump file as payload -> None
    def update_trainer_data_from_file(self):

        try:

            if "trainer.json" not in os.listdir():
                return print("trainer.json file was not found!")

            with open("trainer.json", "r") as f:
                data = json.loads(f.read())
                self.get_trainer_data()
                self.update_trainer_data(data)
                print("Your trainer data has been updated!")

        except Exception as e:
            print(f"Error on update_trainer_data_from_file() -> {e}")

    #Update gamesave data from json dump file as payload -> None
    def update_gamesave_data_from_file(self, slot = None):

        try:

            if not slot:
                slot = int(input("Slot(1-5): "))
                if slot > 5: return print(f"This slot does not exist!")
                if slot < 1: return print(f"This slot does not exist!")
                if f"slot {slot}.json" not in os.listdir(): return print(f"slot {slot}.json was not found!")

            with open(f"slot {slot}.json", "r") as f:
                data = json.loads(f.read())
                system = self.get_trainer_data()
                payload = {
                    "session": data,
                    "system": system,
                    "clientSessionId": self.clientSessionId,
                    "sessionSlotId": (slot-1)
                }
                self.update_gamesave_data(payload)
                print(f"Your save data has been updated in slot: {slot}!")
                
        except Exception as e:
            pass

    #Display all available Pokemon -> None
    def pokedex(self):
        dex = []
        
        for pkm in self.pokemon_id_by_name['dex']:
            dex.append(f"{self.pokemon_id_by_name['dex'][pkm]}: {pkm}")
            
        print("\n".join(dex))
            
    #Unlock all starters with perfect ivs and all shiny variants -> None
    def unlock_all_starters(self):

        try:
        
            total_caught = 0
            total_seen = 0
            data = self.get_trainer_data()

            isShiny = int(input("Do you want the Pokemon to be shiny? (1: Yes, 2: No)(number): "))
            if isShiny == 1:
                
               isShiny = 143
               
               shiny_types = {
                   "Default": 16,
                   "Rare": 32,
                   "Ultra rare": 64
                   }
               
               for shiny in shiny_types:
                   flag = int(input(f"Do you want them to unlock [{shiny}] tier shiny? (1: Yes, 2: No)(number): "))
                   if flag == 1:
                       isShiny += shiny_types[shiny]
                       
            else: isShiny = 253
            
            for entry in list(data["dexData"]):
                
                caught = random.randint(150, 250)
                seen = random.randint(150, 350)
                total_caught += caught
                total_seen += seen
                
                data["dexData"][entry] = {
                              "seenAttr": 479,
                              "caughtAttr": isShiny,
                              "natureAttr": 67108862,
                              "seenCount": seen,
                              "caughtCount": caught,
                              "hatchedCount": 0,
                              "ivs": [
                                31,
                                31,
                                31,
                                31,
                                31,
                                31
                              ]
                            }
                
                data["starterData"][entry] = {
                            "moveset": None,
                            "eggMoves": 15,
                            "candyCount": caught + 20,
                            "abilityAttr": 7,
                            "passiveAttr": 0,
                            "valueReduction": 0
                            }
                
                data["gameStats"]["battles"] = total_caught + random.randint(1, total_caught)
                data["gameStats"]["pokemonCaught"] = total_caught
                data["gameStats"]["pokemonSeen"] = total_seen
                data["gameStats"]["shinyPokemonCaught"] = len(list(data["dexData"])) * 2
                    
            self.update_trainer_data(data)
            print("All starter Pokemon has been updated!")

        except Exception as e:
            print(f"Error on unlock_all_starters() -> {e}")
            
    #Modify/add a pokemon to starters -> None
    def starter_edit(self, dexId = None): # self.pokemon_id_by_name

        try:
            
            data = self.get_trainer_data()
            
            if not dexId:
                dexId = input("Which Pokemon?(Pokemon name / Pokedex ID): " )

                #Using Pokedex ID
                if dexId.isnumeric():
                    
                   if dexId not in data["starterData"]:
                       return print(f"There's no Pokemon with the ID: {dexId}")
                    
                #Using Pokemon name
                else:
                    
                    if dexId.lower() in self.pokemon_id_by_name["dex"]:
                        dexId = self.pokemon_id_by_name["dex"][dexId]
                        
                    else:
                       return print(f"There's no Pokemon with the Name: {dexId}")
                        
            isShiny = int(input("Do you want the Pokemon to be shiny? (1: Yes, 2: No)(number): "))
            if isShiny == 1:
                
               isShiny = 143
               
               shiny_types = {
                   "Default": 16,
                   "Rare": 32,
                   "Ultra rare": 64
                   }
               
               for shiny in shiny_types:
                   flag = int(input(f"Do you want it to unlock [{shiny}] tier shiny? (1: Yes, 2: No)(number): "))
                   if flag == 1:
                       isShiny += shiny_types[shiny]
                       
            else: isShiny = 253
            seenAttr = 479
            caughtAttr = isShiny
            natureAttr = 67108862
            caught = int(input("How many of this Pokemon have you caught? (at least one) (+1 candy per)(number): "))
            hatched = int(input("How many of this pokemon have you hatched? (at least one) (+2 candy per hatch)(number): "))
            seenCount = int(input("How many of this Pokemon have you seen? (Needs to be more or equal to caught)(number): "))
            spatk_iv = int(input("What's the [special attack IV] of the Pokemon?(number): "))
            def_iv = int(input("What's the [defense IV] of the Pokemon?(number): "))
            atk_iv = int(input("What's the [attack IV] of the Pokemon?(number): "))
            hp_iv = int(input("What's the [health IV] of the Pokemon?(number): "))
            spd_iv = int(input("What's the [speed IV] of the Pokemon?(number): "))
            spdef_iv = int(input("What's the [special defense IV] of the Pokemon?(number): "))
            ivs = [spatk_iv, def_iv, atk_iv, hp_iv, spd_iv, spdef_iv]

            data["dexData"][dexId] = {
              "seenAttr": seenAttr,
              "caughtAttr": caughtAttr,
              "natureAttr": natureAttr,
              "seenCount": seenCount,
              "caughtCount": caught,
              "hatchedCount": hatched,
              "ivs": ivs
                }

            data["starterData"][dexId] = {
              "moveset": None,
              "eggMoves": 15,
              "candyCount": caught + (hatched * 2),
              "abilityAttr": 7,
              "passiveAttr": 0,
              "valueReduction": 0
                }

            self.get_trainer_data()
            self.update_trainer_data(data)
            print(f"The Pokemon with the dex entry of {dexId} has been updated!")

        except Exception as e:
            print(f"Error on starter_edit() -> {e}")

    #Modify the amount of egg gacha tickets you have -> None
    def egg_gacha(self):
        
        try:
            
            data = self.get_trainer_data()
            
            voucherCounts = {
                "0": int(input("How many [Common] tickets do you want to have?(number): ")),
                "1": int(input("How many [Rare] tickets do you want to have?(number): ")),
                "2": int(input("How many [Epic] tickets do you want to have?(number): ")),
                "3": int(input("How many [Legendary tickets do you want to have?(number):")) 
                }
            
            data["voucherCounts"] = voucherCounts
            self.update_trainer_data(data)
            print("Your gacha tickets has been updated!")
                
            
        except Exception as e:
            print(f"Error on egg_gacha() -> {e}")
   
    #Makes all your eggs hatch after the next wave -> None
    def hatch_all_eggs(self):
        
        try:
            
            data, eggs = self.get_trainer_data(), []
            
            if not data["eggs"]:
                return print("You have no eggs to hatch!")
            
            for egg in data["eggs"]:
                egg["hatchWaves"] = 0
                eggs.append(egg)
                
            data["eggs"] = eggs
            self.get_trainer_data()
            self.update_trainer_data(data)
            print("Done! -> Your eggs will hatch after the next wave!")
            
        except Exception as e:
            print(f"Error when hatching eggs: {e}")

    #Unlock all gamemodes -> None
    def unlock_all_gamemodes(self):
        try:

            data = self.get_trainer_data()

            if not data["unlocks"]:
                return print("Unable to find data entry: unlocks")

            for i in list(data["unlocks"]):
                data["unlocks"][i] = True

            self.update_trainer_data(data)
            print("All gamemodes have been unlocked!")
        
        except Exception as e:
            print(f"Error on unlock_all_gamemodes() -> {e}")       

    #Unlock all achievements -> None
    def unlock_all_achievements(self):
        
        try:
            
            data = self.get_trainer_data()

            #For randomized timestamps
            current_time_ms = int(time.time() * 1000) # to milliseconds
            min_time_ms = current_time_ms - 3600 * 1000  # 1 hour margain

            #Writes achievement data with randomized timestamps
            achievements = self.extra_data["achievements"]
            data["achvUnlocks"] = {
                achievement: random.randint(min_time_ms, current_time_ms)
                for achievement in achievements
            }

            self.update_trainer_data(data)
            print("All achievements have been unlocked!")

        except Exception as e:
            print(f"Error on unlock_all_achievements -> {e}")

    #Unlock all vouchers -> None
    def unlock_all_vouchers(self):
        try:

            data = self.get_trainer_data()

            #For randomized timestamps
            current_time_ms = int(time.time() * 1000) # to milliseconds
            min_time_ms = current_time_ms - 3600 * 1000 # 1 hour margain
            

            #Writes voucher data with randomized timestamps 
            vouchers = self.extra_data["vouchers"]
            data["voucherUnlocks"] = {voucher: min_time_ms + random.randint(0, current_time_ms - min_time_ms) for voucher in vouchers}
            
            self.update_trainer_data(data)
            print("All vouchers have been unlocked!")

        except Exception as e:
            print(f"Error on unlock_all_vouchers -> {e}")   

if __name__ ==  '__main__':

    with open("./data/data.json") as f:
         data = json.loads(f.read())

    print(data["startup_message"])
    
    while True:
        
        try:
            
            print("\n<Pokerogue account>")
            username, password = input("Username: "), input("Password: ")
            rogueEditor = pokeRogue(username, password, log_error = False)
            break
        
        except:
            print("Incorrect login information/server down... try again!")

    print(f"Successfully logged in as: {username.capitalize()}")
               
    func = {
        "1": rogueEditor.hatch_all_eggs,
        "2": rogueEditor.egg_gacha,
        "3": rogueEditor.starter_edit,
        "4": rogueEditor.unlock_all_starters,
        "5": rogueEditor.pokedex,
        "6": rogueEditor.unlock_all_gamemodes,
        "7": rogueEditor.unlock_all_achievements,
        "8": rogueEditor.unlock_all_vouchers,
        "9": rogueEditor.dump_trainer_data,
        "10": rogueEditor.dump_gamesave_data,
        "11": rogueEditor.update_trainer_data_from_file,
        "12": rogueEditor.update_gamesave_data_from_file
        }
    
    cmd = ["<------------------------- COMMANDS ------------------------>",
           "1: Hatch all eggs",
           "2: Modify the number of egg gacha tickets you have",
           "3: Unlock/modify a starter Pokémon [name/id]",
           "4: Unlock all starter Pokémon",
           "5: Display all Pokémon with their names and id",
           "6: Unlock all game modes",
           "7: Unlock all achievements",
           "8: Unlock all vouchers",
           "9: Dump trainer data to JSON file",
           "10: Dump save data (slot 1-5) to JSON file",
           "11: Update trainer data from the dumped JSON file",
           "12: Update save data (slot 1-5) from the dumped JSON file",
           "---------------------------------------------------------------"
           ]
    
    while True:
        
        print("\n".join(cmd))
        command = input("Command: ")
        
        if command in func:
           func[command]()
            
        else:
           print("Command not found!")
