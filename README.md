# RogueEditor

**RogueEditor** is a simple Pokerogue.net save editor written in Python.

![cmd](https://i.imgur.com/EpHux7x.png)
![dex](https://i.imgur.com/UeS96O9.png)

## Before You Read More

This program was passed down to me by
Onyxdev, the original maintainer. You may
have heard of them.
Here's proof of Onyx's permission to use this program: https://imgur.com/a/08ucctc

## Requirements

- Python 3.10.x
- Requests library

## Running the program without Python

- Download rogueEditor.zip from the "Compiled" folder
- Unzip/extract it into your desired location (It's recommended to create a new folder)
- Run the program with "rogueEditor.exe"

## Running the program in the browser
Want to run the program in the browser without downloading anything?
- Register an account at https://replit.com
- Navigate to https://replit.com/@legacy1999/RogueEditor
- Click fork and run
- This requires no setup or programming skills.

## Warning

Some antivirus software may give false positives when running this program.
Feel free to decompile it and look at its content.
- Compiled with PyInstaller 

## Usage
(Refresh your pokerogue.net page after any modifications!)

Hatch all eggs
- This will make all your eggs hatch after you defeat 1 Pokemon.

Dump trainer data to JSON file
- This will download your trainer data and generate a file called trainer.json (This file contains data such as stats, gacha tickets, etc) -> Edit the file with notepad or notepad ++

Dump save data (slot 1-5) to JSON file
- This will download your session data from one of your saves (slot 1-5) (This file contains data such as money, wave, your pokemons level and stats, etc) -> Edit the file with notepad or notepad ++

Update trainer data from the dumped JSON file
- This will reupload the trainer.json file to pokerouge.net's servers

Update save data (slot 1-5) from the dumped JSON file
- This will reupload the slot(number).json file to pokerouge.net's servers

Unlock/modify a starter Pokémon (name/id)
- This allows you to unlock and/or modify a Pokemon by its name or id (IVs, Candies, Shiny tiers, etc)

Modify the number of egg gacha tickets you have
- This allows you to set the amount of egg gacha tickets you have of every tier

Unlock all starters
- This will unlock every single Pokemon in the Pokedex with Perfect IVs, All natures, abilities, genders and optional shiny tiers.

Display all Pokémon with their names and id
- This simply shows you all the available Pokemon in the game with their names and id (Useful when you want to modify specific Pokemon)

Unlock all game modes
- Unlocks: classic, endless, spliced endless

Unlock all achievements
- Unlocks every achievement

Unlock all vouchers
- Unlocks every voucher
  
## Q & A

Will I get banned for using this?
- Unlikely, but use common sense.
  
Why did nothing happen after my modifications?
- Refresh pokerogue.net in your browser.

Why does the program say that my login information is incorrect when it isn't?
- You may be temporarily flagged by Cloudflare. (Changing connection/ip will fix this)
- Pokerogue may be down or lagging (This causes the program to timeout)

Can I bypass the Cloudflare issues by running the program via the replit.com fork?
- Yes.

How can I use this on the local version of Pokerogue?
- You can modify the API endpoints in the source to point towards localhost:8000.

## Discord

Would you like to contact me?
- Add me on Discord: **fire6945**


<!-- Metadata: keywords -->
<meta name="description" content="RogueEditor is a simple Pokerogue.net save editor written in Python.">
<meta name="keywords" content="pokerogue, pokerogue save editor, pokerogue hacks, pokerogue hack, pokerogue cheats, pokerogue cheat, pokerogue trainer, pokerogue cheat table, rogueEditor, free, gacha, ticket, tickets, egg, eggs, shiny, save, edit, pokemon, unlimited, hack, hacks, cheat, cheats, trainer, table, pokedex, dex, wave, money, level, levels, iv, ivs, stat, stats, item, items, api, mod, mods, tool, tools">
