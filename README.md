# Establishing connections between authors

**This one again is for the science community.**

The code snippet here generates a network of authors (ad co-authors) based on manuscript authorships. The code searches the NCBI Pubmed databse for manuscripts written by authors (provided as a list by the user), scrapes the list of co-authors then generates a network graph showing author connectivity. This can be used to identify author connections via an intermediary author which may not be obvious. The code can also be used to identify the shortest link between two people in the network.
Feel free to share and adapt the code for your needs.

![Example author connections](https://github.com/pranaydogra/establish_author_connections/blob/master/%5B'Pranay%20Dogra'%2C%20'%20Tim%20Sparer'%2C%20'%20Ben%20Youngblood'%2C%20'%20Donna%20L.%20Farber'%2C%20'%20Barry%20T.%20Rouse'%2C%20'%20Steven%20L.%20Reiner'%5D_connections.svg)


**CAUTION:** Please use the code responsibly and do not inundate the server with multiple scraping requests which may lead to slowing or crashing of the server.
