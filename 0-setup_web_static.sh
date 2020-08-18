#!/usr/bin/env bash
# sets up web servers for deployment of web_static

# Install Nginx if it not already installed

if ! command -v nginx &> /dev/null
then
    apt-get -y update
    apt-get -y install nginx
fi


# Create test folder and its parent folders
DIR='/data/web_static/releases/test/'
if [ ! -d $DIR ]
then
    mkdir -p $DIR;
fi

# Create BRAND NEW symbolic link to test folder.
# Remove old symbolic link if it exists
LINK_NAME='/data/web_static/current'

if [ -f $LINK_NAME ]
then
    rm $LINK_NAME;
fi

ln --symbolic $DIR $LINK_NAME

# Create a placeholder HTML file in test folder
FAKE_HTML_TEXT="\
<html>\n\
<head>\n\
\t<title>jicruz.tech</title>\n\
</head>\n\
<body>\n\
\t<h1>Welcome!</h1>\n\
\t<p>This site is under construction, dad.</p>\n\
</body>\n\
</html>"
FILE="index.html"
FILE_PATH="$DIR$FILE"

echo -e "$FAKE_HTML_TEXT" > $FILE_PATH

# Create shared folder under web_static
DIR='/data/web_static/shared'
if [ ! -d $DIR ]
then
    mkdir -p $DIR;
fi

# Give ownership of /data/ folder to ubuntu user AND group
chown -hR ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current/
# to /hbnb_static
STR="\tlocation = /hbnb_static {\n\
\t\talias /data/web_static/current/;\n\
\t}\n\
}\n"
sed -i "s@^}@$STR@" /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
