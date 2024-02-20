FROM archlinux:base-devel-20240101.0.204074

# Creating a user that is almost root but not quite and switching to it
RUN useradd -m -G wheel defoNotRoot && passwd -d defoNotRoot
RUN echo 'defoNotRoot ALL=(ALL) NOPASSWD: ALL' >>/etc/sudoers
USER defoNotRoot

# Installing other development tools
RUN sudo pacman -Syu --noconfirm
RUN sudo pacman -S git --noconfirm
RUN sudo pacman -S fish --noconfirm

# Installing yay
RUN mkdir -p /tmp/yay-build
RUN git clone https://aur.archlinux.org/yay.git /tmp/yay-build/yay
RUN cd /tmp/yay-build/yay && makepkg -si --noconfirm
RUN rm -rf /tmp/yay-build
RUN yay -Sua --noconfirm

RUN sudo pacman -S --noconfirm neovim

RUN sudo pacman -S --noconfirm fastfetch

RUN sudo pacman -S --noconfirm eza

RUN sudo pacman -S --noconfirm zoxide
RUN sudo pacman -S --noconfirm fzf

RUN sudo pacman -S --noconfirm bat

RUN sudo pacman -S --noconfirm ripgrep

RUN sudo pacman -S --noconfirm python python-pip
