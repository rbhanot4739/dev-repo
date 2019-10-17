#!/bin/bash

BLACK='\033[0;30m'
RED='\033[0;31m'
DARK_GRAY='\033[1;30m'
LIGHT_RED='\033[1;31m'
GREEN='\033[1;32m'
LIGHT_GREEN='\033[0;32m'
BROWN='\033[0;33m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
LIGHT_BLUE='\033[1;34m'
PURPLE='\033[0;35m'
LIGHT_PURPLE='\033[1;35m'
CYAN='\033[0;36m'
LIGHT_CYAN='\033[1;36m'
LIGHT_GRAY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m'
OS=`lsb_release -a 2>/dev/null | awk  '$1~"Dist" {print $3}'`

if [ $OS == "ManjaroLinux" ]
then
	cd ~/
    read -sp "Enter the github password (this will be needed for downloading dotfiles): " gpass; echo
    read -sp "Enter the sudo password: " password 

	echo -e "\n${YELLOW}..................... Starting the setup process .....................${NC}\n"
	echo $password | sudo -S pacman-key --init
	echo $password | sudo -S sed -i -e '/Misc options/a Color\nILoveCandy'  /etc/pacman.conf

	echo -e "\n${YELLOW}.....................  Removing some bloatware .....................${NC}\n"
	REMOVE_PACKAGES="hplip  pidgin steam-manjaro steam-devices thunderbird ms-office-online libreoffice-still libreoffice-fresh gimp xfburn system-config-printer hexchat audacious audacious-plugins microsoft-office-online-jak xterm uget empathy lollypop brasero transmission evolution"
	for pkg in $REMOVE_PACKAGES
	do
	echo $password | sudo -S pacman --noconfirm -Rsun  $pkg
	done
	
	echo -e "\n${YELLOW}..................... Updating the system with .....................${NC}\n"
	echo $password | sudo -S pacman-mirrors -f && echo $password | sudo -S pacman --noconfirm -Syyu
	echo $password | sudo -S mhwd -a pci nonfree 0300
	

	echo -e "\n${YELLOW}..................... Installing packages .....................${NC}\n"

	INSTALL_PACKAGES=" base-devel mod_wsgi apache python2-pip python-pip neovim unzip vuze nodejs npm vagrant"

	for pkg in $INSTALL_PACKAGES;
	do
		if [ `pacman -Q | egrep ^$pkg$ | wc -l` -ge 1   ]
			then
				echo -e "${GREEN}$pkg is already installed${NC}\n"
		else
				echo -e "\n${YELLOW}..................... Installing $pkg .....................${NC}\n"
				echo $password |sudo -S pacman --noconfirm -Syu $pkg
		fi
	done
		


    echo -e "\n ${YELLOW}..................... Generating and uploading SSH Keys to GitHub .....................${NC}\n"
	if [ -d ~/.ssh ]
	then
		rm -rf ~/.ssh
	fi
	ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ''


	curl -u "rbhanot4739@gmail.com:$gpass" --data '{"title":"laptop-key","key":"'"$(cat ~/.ssh/id_rsa.pub)"'"}' https://api.github.com/user/keys

	echo -e "\n ${YELLOW}..................... Cloning the github repo ...........${NC}\n"

	> ~/.ssh/known_hosts
    ssh-keyscan github.com >> ~/.ssh/known_hosts
	git clone git@github.com:rbhanot4739/python-dotfiles.git ~/python-dotfiles
	cd ~/python-dotfiles
	git config --global user.email "rbhanot4739@gmail.com"
	git config --global user.name "Rohit Bhanot"
	cd ~/

	echo -e "\n${YELLOW}..................... Installing tmux .....................${NC}\n"
	cd /tmp
	# git clone https://github.com/tmux/tmux.git
	# cd tmux/
	# sh autogen.sh
	# ./configure && make
	wget https://github.com/tmux/tmux/releases/download/2.8/tmux-2.8.tar.gz
	tar -xzvf tmux-2.8.tar.gz && cd tmux-2.8
	 ./configure && make
	echo $password | sudo -S make install
	cd ..
	rm -rf tmux-2.8/ tmux-2.8.tar.gz
	git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm


	echo -e "\n${YELLOW}..................... Setting up Zsh ..............................${NC}\n"
	cd ~/
	wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh
	echo $password | sh install.sh > /dev/null
	cd ~/.oh-my-zsh/custom/plugins
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
	git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
	git clone https://github.com/zsh-users/zsh-completions ~/.oh-my-zsh/custom/plugins/zsh-completions
	git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search
	compaudit | xargs chmod g-w,o-w
	yes $password | chsh -s $(which zsh)
	mv .zshrc.pre-oh-my-zsh .zshrc

	cd ~/

    echo -e "\n${YELLOW}..................... Setting up Fonts..............................${NC}\n"
	if [ ! -d ~/.fonts ]
	then
		mkdir ~/.fonts
	fi
	cd ~/.fonts
	wget wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.0.0/FiraCode.zip
	unzip FiraCode.zip
	rm -f FiraCode.zip
	cd $HOME

	echo -e "\n${YELLOW}..................... Copying all the dot files from git repo ..............................${NC}\n"
	cd ~/python-dotfiles/dot-files/
	for i in .bashrc  .bashrc_home  .bashrc_work .ideavimrc .local_settings_rc .pythonrc .tmux.conf .zshrc  .zshrc_home .zshrc_work dev-tmux
	do
	cp -ar $i ~/
	done
	cp -ar ~/python-dotfiles/dot-files/nvim/ ~/.config/nvim/
	cp -ar ~/python-dotfiles/dot-files/tmux/ ~/.tmux/
	cp -ar modded-steeef.zsh-theme ~/.oh-my-zsh/custom/themes/
	cd ~/



	echo -e "\n${YELLOW}.....................  Setting up NeoVim .....................${NC}\n"
	
	nvim +'PlugInstall --sync' +qall
	nvim +'UpdateRemotePlugins' +qall

	echo $password |sudo -S python2 -m pip install neovim
	echo $password |sudo -S python3 -m pip install neovim

	echo -e "\n${YELLOW}.....................  Setting up Python .....................${NC}\n"
	echo $password |sudo -S python3 -m pip install virtualenvwrapper
	source $(which virtualenvwrapper.sh) && mkvirtualenv django-env && workon django-env && cd ~/python-dotfiles/python3/django-projects/ && pip install -r django_requirements.txt
	deactivate
	cd ~


	echo -e "\n${YELLOW}.....................  Installing Chrome from AUR .....................${NC}\n"
	cd /tmp
	git clone https://aur.archlinux.org/google-chrome.git && 	cd google-chrome/ && makepkg -s && echo $password |sudo -S pacman -U --noconfirm *xz && cd .. && rm -rf google-chrome/


	echo -e "\n${YELLOW}.....................  Installing Jetbrains Toolbox from AUR .....................${NC}\n"
	cd /tmp
	git clone https://aur.archlinux.org/jetbrains-toolbox.git &&	cd jetbrains-toolbox/ &&	makepkg -s && echo $password |sudo -S pacman -U --noconfirm *xz && cd .. && rm -rf jetbrains-toolbox/


	echo -e "\n${YELLOW}.....................  Installing VsCode from AUR .....................${NC}\n"
	cd /tmp
	git clone https://aur.archlinux.org/visual-studio-code-bin.git &&│·cd visual-studio-code-bin &&│·makepkg -s && echo $password |sudo -S pacman -U --noconfirm *xz && cd .. && rm -rf visual-studio-code-bin
	echo -e "\n${YELLOW}.....................  Cleaning up Orphans & caches .....................${NC}\n"
	echo $password |sudo -S pacman --noconfirm -Rs $(pacman -Qdtq)

	echo $password | sudo -S pacman -Scc

	# activate hover on brisk menu
	gsettings set com.solus-project.brisk-menu rollover-activate true

	echo $password | sudo -S systemctl enable redis
	echo $password | sudo -S systemctl enable httpd.service


else
	echo -e "Different OS, exitting !!"
	exit 1
fi
