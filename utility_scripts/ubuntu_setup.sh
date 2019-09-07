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
if [ $OS == "Ubuntu" ]
then
	cd ~/
  echo $password | sudo -S dpkg --configure -a
	read -s -p "Enter sudo password: " password
	echo
  read -sp "Enter github password: " gpass

	echo -e "\n${YELLOW}..................... Starting the setup process .....................${NC}\n"

	echo -e "\n${YELLOW}..................... Running apt-get update .....................${NC}\n"
	#echo $password | sudo -S apt update -y && apt upgrade -y > /dev/null
echo $password | sudo -S  apt-get install -y --reinstall dpkg
	#echo -e "\n${YELLOW}..................... Installing Ubuntu restricted extras .....................${NC}\n"
	#echo $password | sudo -S apt install -y ubuntu-restricted-extras # This creates problem... install it manually


 curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
	echo -e "\n${YELLOW}..................... Installing additional packages .....................${NC}\n"
	INSTALL_PACKAGES="gnome-tweaks curl git zsh bleachbit tlp python-setuptools python-wheel python-pip python3-setuptools python3-wheel python3-pip ninja-build gettext libtool libtool-bin autoconf automake libevent-dev libncurses-dev cmake g++ pkg-config unzip ctags libmysqlclient-dev ripgrep nodejs libapache2-mod-wsgi-py3 mysql-server "
for pkg in $INSTALL_PACKAGES;
do
 if [ `dpkg -l | cut -d " " -f 3 | egrep ^$pkg$ | wc -l` -ge 1   ]
			then
				echo -e "${GREEN}$pkg is already installed${NC}\n"
		else
			echo -e "\n${YELLOW}.....................  Installing $pkg.....................${NC}\n"
			echo $password |sudo -S apt install -y $pkg > /dev/null
		fi
	done


  echo -e "\n ${YELLOW}..................... Generating and SSH Keys to GitHub .....................${NC}\n"
	if [ -d ~/.ssh ]
	then
		rm -rf ~/.ssh
	fi
	ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ''


	curl -u "rbhanot4739@gmail.com:$gpass" --data '{"title":"laptop-ubuntu-key","key":"'"$(cat ~/.ssh/id_rsa.pub)"'"}' https://api.github.com/user/keys > /dev/null

	echo -e "\n ${YELLOW}..................... Cloning my github repo as over ssh remote url ...........${NC}\n"

	> ~/.ssh/known_hosts
        ssh-keyscan github.com >> ~/.ssh/known_hosts
	git clone git@github.com:rbhanot4739/python-dotfiles.git ~/python-dotfiles
	cd ~/python-dotfiles
	git config --global user.email "rbhanot4739@gmail.com"
	git config --global user.name "Rohit Bhanot"
	cd ~/



  echo -e "\n${YELLOW}..................... Installing tmux .....................${NC}\n"
  cd /tmp
  git clone https://github.com/tmux/tmux.git
  cd tmux/
  sh autogen.sh > /dev/null
  ./configure && make > /dev/null
  sudo make install > /dev/null
  cd ..
  rm -rf tmux/
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm


  echo -e "\n${YELLOW}..................... Setting up Zsh ..............................${NC}\n"
	cd ~/
  wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh
  echo $password | sh install.sh > /dev/null
  cd ~/.oh-my-zsh/custom/plugins
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting > /dev/null
  git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions > /dev/null
  git clone https://github.com/zsh-users/zsh-completions ~/.oh-my-zsh/custom/plugins/zsh-completions > /dev/null
	git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search
	compaudit | xargs chmod g-w,o-w

  cd ~/

 echo -e "\n${YELLOW}..................... Setting up NVM and NodeJS ..............................${NC}\n"
 npm config set prefix=$HOME/tools/.node_modules_global
npm install npm --global
#  nvm install node
#  nvm use --delete-prefix v11.9.0
#	curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
#	source ~/.bashrc
#	nvm install node
#	cd ~/python-dotfiles/python3/web/
#	npm -y init
#	npm install -D eslint
#	npm install -D prettier eslint-plugin-prettier eslint-config-prettier
#	npm -D install stylelint --save-dev
#	npm -D install stylelint-config-recommended --save-dev


  echo -e "\n${YELLOW}..................... Setting up Fonts..............................${NC}\n"
	if [ ! -d ~/.fonts ]
	then
		mkdir ~/.fonts
	fi
	cd ~/.fonts
	wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.0.0/InconsolataLGC.zip
	unzip FiraCode.zip
	rm -f FiraCode.zip
	cd $HOME

	echo -e "\n${YELLOW}..................... Copying all the dot files from git repo ..............................${NC}\n"
	cd ~/python-dotfiles/dot-files/
	for i in .bashrc  .bashrc_home  .bashrc_work .ideavimrc .local_settings_rc .pythonrc .tmux.conf .zshrc  .zshrc_home .zshrc_work dev-tmux
	do
	cp -ar $i ~/.
	done
	cp -ar ~/python-dotfiles/dot-files/nvim/ ~/.config/nvim/
	cp -ar ~/python-dotfiles/dot-files/tmux/ ~/.tmux/
	cd ~/
  source ~/.zshrc

  echo -e "\n${YELLOW}.....................  Installing Conda .....................${NC}\n"
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
	bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/tools/miniconda3
	echo -e "\n${YELLOW}.....................  Setting up virtual environments .....................${NC}\n"
	$HOME/tools/miniconda3/bin/conda create --name py37 --clone base
	cd


  echo -e "\n${YELLOW}.....................  Installing NeoVim .....................${NC}\n"
	python -m pip install neovim
	python3 -m pip install neovim
  cd /tmp
  git clone https://github.com/neovim/neovim.git > /dev/null
  cd neovim/
  if [ ! -d $HOME/tools ]
  then
	mkdir $HOME/tools
  fi
  make CMAKE_EXTRA_FLAGS="-DCMAKE_INSTALL_PREFIX=$HOME/tools/nvim"
  sudo make install  > /dev/null
  cd ../
  rm -rf neovim/
  cd ~/tools/nvim/bin/
  ./nvim +'PlugInstall --sync' +qa  > /dev/null
  ./nvim +'UpdateRemotePlugins' +qa  > /dev/null

  echo -e "\n${YELLOW}.....................  Installing Pycharm Professional .....................${NC}\n"
  echo $password | sudo -S snap install pycharm-professional --classic


  echo -e "\n${YELLOW}.....................  Installing Google Chrome .....................${NC}\n"
	wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
	echo $password | sudo -S sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
	echo $password | sudo -S apt-get update > /dev/null
	echo $password | sudo -S apt-get install google-chrome-stable

  echo -e "\n${YELLOW}.....................  Removing some bloatware .....................${NC}\n"

  REMOVE_PACKAGES="hplip hplip-data gimp gimp-data gimp-help-common gimp-help-en libgimp2.0 simple-scan pix pix-data pix-dbg
  printer-driver-brlaser printer-driver-c2esp printer-driver-foo2zjs printer-driver-foo2zjs-common printer-driver-gutenprint printer-driver-hpcups printer-driver-m2300w printer-driver-min12xxw printer-driver-pnm2ppa printer-driver-ptouch printer-driver-pxljr printer-driver-sag-gdi printer-driver-splix bluez-cups foomatic-db-compressed-ppds libgutenprint2 ippusbxd openprinting-ppds libreoffice*
  hyphen-ru mythes-de mythes-de-ch mythes-en-us mythes-fr mythes-it mythes-pt-pt mythes-ru uno-libs3 ure thunderbird* transmission-* nano vim.tiny aisleriot gnome-mahjongg gnome-mines gnome-sudoku libgme0:amd64 libgnome-games-support-1-3:amd64 libgnome-games-support-common deja-dup luez-cups foomatic-db-compressed-ppds ippusbxd libgutenprint-common libgutenprint9 openprinting-ppds printer* "
  for pkg in $REMOVE_PACKAGES
do
echo $password | sudo -S apt remove --purge -y $pkg
done

echo -e "\n${YELLOW}.....................  Cleaning up some temp files .....................${NC}\n"
echo $password | sudo -S apt autoclean -y
echo $password | sudo -S apt-get clean -y
echo $password | sudo -S apt-get autoremove -y --purge
echo $password | sudo -S apt-get autoremove --purge

else
	echo -e "Different OS, exitting !!"
	exit 1
fi
