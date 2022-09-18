#!/bin/bash

# Install utilities
yum install git -y
amazon-linux-extras install firefox -y


# Install FFMPEG 4
mkdir -v -p /usr/local/bin/ffmpeg
cd /usr/local/bin/ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz
tar -v -xf ffmpeg-release-i686-static.tar.xz --strip-components=1
rm -v -f ffmpeg-release-i686-static.tar.xz
ln -snf /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
ln -snf /usr/local/bin/ffmpeg/ffpropbe /usr/bin/ffpropbe

# Install Docker
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
chkconfig docker on
systemctl start docker

# Install Docker Compose
wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
chmod -v +x /usr/local/bin/docker-compose
/usr/local/bin/docker-compose --version
