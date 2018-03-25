# DailyTunes
Web app that curates a Spotify playlist based on top news headlines' sentiment. Written in Python 3.
To run this, you need a Spotify account.

## Dependencies:
 Requires pip3 packages:
  * watson-developer-cloud
  * Flask
  * Newspaper3k
  * spotipy
  * beautifulsoup4
  * requests

## To run the server:
1. cd into the DailyTunes root directory.
2. Run the command 'python3 dailytunes_main.py'.
3. You will be prompted in your browser for a Spotify username and password. Enter them.
4. At the terminal, there should be a prompt for entering the URL you were redirected to. Enter it.
5. Analysis will begin. This takes about ten minutes on the slowest computers.
6. The program will state 'Total analysis complete' and start up the server.
7. Go to http://localhost:9999 to view the fruits of your labor. Your server is now running.

You do not need to repeat steps 3-4 after you do it once. The program will remember your Spotify credentials and immediately begin analysis.
