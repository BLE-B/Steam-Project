# Steam-Project
This project thus far delivers a primer in using the Steam Web API and web scraping in order to build a database based on Steam as a social network.

It follows a simple structure which incorporates building a network database of Steam users based on their "friend" relationship ('json_save_official.py') and using this network to scrape the users' bios ('scrape_official.py', more to come, such as profile comments). The resulting data may then be used in a machine learning environment with natural language processing for means such as sentiment analyses. A base model is provided ('sentiment_analysis.py').

Required packages are: steam_api and nltk. Furthermore, a key is required in order to use the Steam API (for more information, see https://partner.steamgames.com/doc/webapi_overview/auth).

As each Steam user is free to share their data (such as their bio) with everyone, this project can be considered in line with current data protection legislature. However, I strongly recommend handling this code with care, as misuse may be on the horizon with some further tweaks.
