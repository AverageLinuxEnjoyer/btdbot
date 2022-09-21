# Bloons Tower Defense 6 Bot
The bot is mainly made to farm event totems/easter eggs/halloween pumpkins/candies etc.

## How to use?
  Run the main.py file and then switch to the BTD6 window. Move the mouse cursor to one of the screen corners to stop the bot.

## What does it do?
  - Searches through the maps and plays on medium difficulty the one with the event icon attached
  - Chooses and follows one of the strategies defined in /strategies based on the map selected
  - Closes possible tooltips, pop-ups or level up notifications that may appear
  - Uses [scanmem](https://github.com/scanmem/scanmem) to locate the memory address of the money count, so they can be accessed instantly at any time (making screenshots and using an ocr here would've been a massive bottleneck)
  - Once the map is finished, opens the chest if there is one and collects the rewards if there are any

## Notes
  - the bot only works on linux, an alternative to memscan could be used for it to work on Windows as well.
