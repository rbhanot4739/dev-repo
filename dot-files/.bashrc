# Common config

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

function cd() { builtin cd $@ ; ls; }

# aliases

alias .='cd '
alias ..='cd ..'
alias ...='cd ../..'
alias md='mkdir'

alias ssh='ssh -x '
alias c='clear'
alias h='history'
alias r='source ~/.bashrc'
alias cp='cp -arv'
alias xx='exit'
alias zz='vim ~/.bashrc'

alias ls='ls -F --color --hide="*.pyc"'
alias lsa='ls -a'
alias ll='ls -ltrh --color '
alias lla='ll -a '
alias grep='grep -E --color=auto '
alias df='df -hPT'
alias cp='cp -arv'
alias py='python '
alias dmux='bash ~/dev-tmux'

umask 0002
HOSTNAME=`hostname`


#if [ -f /etc/bashrc ]; then
#	source /etc/bashrc
#fi
#

if grep -q 'home' <<< "$HOSTNAME"
then
	source ~/.home.bashrc
fi

if grep -q 'tower-research.com' <<< "$HOSTNAME"
then
	source ~/.bashrc_work
fi

export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
export TERM=xterm-256color
export PATH
#export PYTHONSTARTUP=~/.pythonrc

[ -f ~/.fzf.bash ] && source ~/.fzf.bash
