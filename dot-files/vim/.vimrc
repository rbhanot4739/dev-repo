call plug#begin('~/.vim/plugged')

" Declare the list of plugins.

Plug 'davidhalter/jedi-vim'
Plug 'scrooloose/nerdcommenter'
Plug 'machakann/vim-highlightedyank'
Plug 'itchyny/lightline.vim'
Plug 'morhetz/gruvbox'
" List ends here. Plugins become visible to Vim after this call.
call plug#end()


colo gruvbox
set autoindent
set hidden
set background=dark
set encoding=utf-8
set t_Co=256
set laststatus=2

" UI Layout
"set mouse=a
set visualbell    " stop that ANNOYING beeping
set textwidth=100
set wrap
set linebreak
set nolist
set ruler
set showcmd                 " show command in bottom bar
set cursorline              " highlight current line
set showmatch               " highlight matching [{()}]
set wildmenu               " visual autocomplete for command menu
set wildmode=list:longest,full
set lazyredraw              " redraw only when we need to.
set relativenumber number

"Improve Search and Replace
set gdefault								" Never have to type /g at the end of search / replace again
set ignorecase              " ignore case when searching
set smartcase								" make search case Sensitive if it contains an Uppercase letter otherwise search is case insensitive
set incsearch               " search as characters are entered
set hlsearch                " highlight matches


" Disable backup and swap files - they trigger too many events
" for file system watchers
set nobackup
set nowritebackup
set noswapfile
set clipboard=unnamed " copy to system clipboard
set splitbelow
set splitright
