# !/bin/bash

mkdir -p ~/.config/fish/
cp .devcontainer/config.fish ~/.config/fish/
sed -i "s|zoxideDatabasePath|$PWD|g" ~/.config/fish/config.fish

sudo pacman -Syu --noconfirm

git config --global --add safe.directory $PWD

yay -Sua --noconfirm

pip install -r requirements.txt --break-system-packages
