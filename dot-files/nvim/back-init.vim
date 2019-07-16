" Settings ---------------------------------------------- {{{
if has("nvim")
	set guicursor=
	let $VTE_VERSION="100"
	set inccommand=nosplit
else
	set nocompatible
	set ruler
	set showcmd
	set incsearch               " search as characters are entered
	set hlsearch                " highlight matches
	set wildmenu               " visual autocomplete for command menu
	set autoread
	set autoindent
	set laststatus=2
	set encoding=utf-8
	set backspace=indent,eol,start
	set display=lastline
endif
set hidden
set list
set listchars=tab:│·,trail:·,extends:→
" set mouse=a
set visualbell    " stop that ANNOYING beeping
set textwidth=0
set wrap
" set linebreak
set cursorline              " highlight current line
set showmatch               " highlight matching [{()}]
set wildmode=list:longest,full
set wildignore+=*.bmp,*.gif,*.ico,*.jpg,*.png,*.ico
set wildignore+=*/tmp/*,*.so,*.swp,*.zip
set wildignore+=*.pdf,*.psd
set lazyredraw              " redraw only when we need to.
"set colorcolumn=80
"highlight ColorColumn ctermbg=80
set relativenumber number
"Improve Search and Replace
" set gdefault" Never have to type /g at the end of search / replace again
set ignorecase              " ignore case when searching
set smartcase" make search case Sensitive if it contains an Uppercase letter otherwise search is case insensitive
" Code Folding
set foldenable              " enable folding
set foldmethod=indent
set foldnestmax=5
set foldlevelstart=99
" Disable backup and swap files - they trigger too many events
" for file system watchers
set nobackup
set nowritebackup
set noswapfile
set clipboard=unnamed " copy to system clipboard
set splitbelow
set splitright
" Spaces / Tabs
set tabstop=2
set softtabstop=2
set shiftwidth=2
set undofile
set undodir="$HOME/.VIM_UNDO_FILES"
" see help 'complete' for details
set complete=.,w,b,u,t
set shortmess+=c
" set fillchars+=vert:\|  " remove chars from seperators

" Put your python path below
let g:python_host_prog  = 'python'
let g:python3_host_prog = 'python3'
"}}}

"Plugins ----------------------------------------------- {{{
" Plugins will be downloaded under the specified directory.
call plug#begin('~/.config/nvim/plugged') "------------------------------ {{{
" Declare the list of plugins.
Plug 'ncm2/ncm2'
Plug 'roxma/nvim-yarp'
Plug 'ncm2/ncm2-jedi'
Plug 'ncm2/ncm2-tern',  {'do': 'npm install'}
Plug 'ncm2/ncm2-cssomni'
Plug 'ncm2/ncm2-ultisnips'
Plug 'ncm2/ncm2-path'
Plug 'ncm2/ncm2-html-subscope'
Plug 'ncm2/ncm2-syntax' | Plug 'Shougo/neco-syntax'
Plug 'davidhalter/jedi-vim' , {'on_ft': 'python'}
Plug 'w0rp/ale'
Plug 'Glench/Vim-Jinja2-Syntax'
Plug 'ap/vim-css-color'
Plug 'mgedmin/python-imports.vim'
Plug 'mattn/emmet-vim'
Plug 'tomtom/tcomment_vim'
Plug 'editorconfig/editorconfig-vim'
Plug 'honza/vim-snippets'
Plug 'SirVer/ultisnips'
Plug 'tpope/vim-surround'
Plug 'Raimondi/delimitMate'
Plug 'Valloric/MatchTagAlways', {'on_ft': 'html'}
" Plug 'tpope/vim-repeat'
" Plug 'sheerun/vim-polyglot'

" Navigation
Plug 'majutsushi/tagbar'
Plug 'ludovicchabant/vim-gutentags'
Plug 'scrooloose/nerdtree'
Plug 'machakann/vim-highlightedyank'
Plug 'junegunn/fzf', { 'do': './install --all' }
Plug 'junegunn/fzf.vim'
Plug 'christoomey/vim-tmux-navigator'

" UI
" Plug 'itchyny/lightline.vim'
Plug 'edkolev/tmuxline.vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
Plug 'ajh17/Spacegray.vim'
Plug 'jpo/vim-railscasts-theme'
Plug 'romainl/Apprentice'
Plug 'ryanoasis/vim-devicons'

" Plug 'altercation/vim-colors-solarized'
call plug#end()
" }}}

" Autocompletion----------------------------------------------- {{{

" NCM2 ---------------------------------------------------------{{{
" enable ncm2 for all buffers
autocmd BufEnter * call ncm2#enable_for_buffer()

" IMPORTANT: :help Ncm2PopupOpen for more information
set completeopt=noinsert,menuone,noselect
" make it fast
let ncm2#popup_delay = 5
let ncm2#complete_length = [[1, 1]]
" Use new fuzzy based matches
let g:ncm2#matcher = 'substrfuzzy'
" }}}

" Jedi ------------------------------------------------------{{{
" let g:jedi#auto_initialization = 1
" let g:jedi#completions_enabled = 0
" let g:jedi#auto_vim_configuration = 0
" let g:jedi#smart_auto_mappings = 0
" let g:jedi#popup_on_dot = 0
" let g:jedi#completions_command = ""
" let g:jedi#show_call_signatures = "0"
" let g:jedi#show_call_signatures_delay = 0
" let g:jedi#use_tabs_not_buffers = 0
" " let g:jedi#show_call_signatures_modes = 'i'  " ni = also in normal mode
" let g:jedi#enable_speed_debugging=0
"}}}

" Ultisnip----------------------------------------------- {{{
" Press enter key to trigger snippet expansion
imap <expr> <CR> ncm2_ultisnips#expand_or("\<CR>", 'n')
" inoremap <silent> <expr> <CR> ((pumvisible() && empty(v:completed_item)) ?  "\<c-y>\<cr>" : (!empty(v:completed_item) ? ncm2_ultisnips#expand_or("", 'n') : "\<CR>" ))

" smap <c-u> <Plug>(ultisnips_expand)
let g:UltiSnipsExpandTrigger		= "<Plug>(ultisnips_expand)"
let g:UltiSnipsJumpForwardTrigger="<a-j>"
let g:UltiSnipsJumpBackwardTrigger="<a-k>"
let g:UltiSnipsRemoveSelectModeMappings = 0
" }}}
" }}}

" ALE settings ----------------------------------------------- {{{
" Do not lint or fix minified files.
let g:ale_pattern_options = {
			\ '\.min\.js$': {'ale_linters': [], 'ale_fixers': []},
			\ '\.min\.css$': {'ale_linters': [], 'ale_fixers': []},
			\}
let g:ale_linters = {
			\ 'python': ['flake8'],
			\	'javascript': ['eslint']
			\}

let g:ale_fixers = {
			\ '*': ['remove_trailing_lines', 'trim_whitespace'],
			\ 'python' : ['isort', 'autopep8'],
			\ 'javascript': ['eslint', 'prettier'],
			\ 'css' : ['stylelint', 'prettier'],
			\ }
" Echo msg format
let g:ale_echo_msg_error_str = 'E'
let g:ale_echo_msg_warning_str = 'W'
let g:ale_echo_msg_format = '[%linter%] %s [%severity%]'
" Set this variable to 1 to fix files when you save them.
let g:ale_fix_on_save = 1
let g:ale_sign_error = '>>'
let g:ale_sign_warning = '--'
" " let g:ale_sign_error = '✘'
" " let g:ale_sign_warning = '⚠'
highlight ALEErrorSign ctermbg=NONE ctermfg=red
highlight ALEWarningSign ctermbg=NONE ctermfg=yellow
let g:airline#extensions#tabline#buffer_idx_mode = 1
let g:airline#extensions#tabline#buffer_idx_format = {
			\ '0': '0 ',
			\ '1': '1 ',
			\ '2': '2 ',
			\ '3': '3 ',
			\ '4': '4 ',
			\ '5': '5 ',
			\ '6': '6 ',
			\ '7': '7 ',
			\ '8': '8 ',
			\ '9': '9 ',
\}

" }}}

" Disable netrw
let loaded_netrwPlugin = 1

" fzf settings ----------------------------------------------- {{{
" [Tags] Command to generate tags file
let g:fzf_tags_command = 'ctags -R'
let g:fzf_action = {
			\ 'ctrl-t': 'tab split',
			\ 'ctrl-x': 'split',
			\ 'ctrl-v': 'vsplit' }
" Default fzf layout
" - down / up / left / right
let g:fzf_layout = { 'down': '~40%' }
" You can set up fzf window using a Vim command (Neovim or latest Vim 8 required)
let g:fzf_layout = { 'window': 'enew' }
let g:fzf_layout = { 'window': '-tabnew' }
let g:fzf_layout = { 'window': '10split enew' }
" Customize fzf colors to match your color scheme
let g:fzf_colors =
			\ { 'fg':      ['fg', 'Normal'],
			\ 'bg':      ['bg', 'Normal'],
			\ 'hl':      ['fg', 'Comment'],
			\ 'fg+':     ['fg', 'CursorLine', 'CursorColumn', 'Normal'],
			\ 'bg+':     ['bg', 'CursorLine', 'CursorColumn'],
			\ 'hl+':     ['fg', 'Statement'],
			\ 'info':    ['fg', 'PreProc'],
			\ 'border':  ['fg', 'Ignore'],
			\ 'prompt':  ['fg', 'Conditional'],
			\ 'pointer': ['fg', 'Exception'],
			\ 'marker':  ['fg', 'Keyword'],
			\ 'spinner': ['fg', 'Label'],
			\ 'header':  ['fg', 'Comment'] }
" }}}

" Tmuxline ----------------------------------------------- {{{
let g:tmuxline_preset = {
			\'a'    : '#S',
			\'b'    : '#{?pane_synchronized,PANES-ARE-SYNCED,}',
			\'win'  : '#I #W',
			\'cwin' : '#I #W',
			\'x'    : '%a',
			\'y'    : '%R',
			\'z'    : '#(date +%F)'}
" }}}

" Airline ----------------------------------------------- {{{
let g:airline_powerline_fonts = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#show_tabs = 1
let g:airline#extensions#tabline#show_buffers = 0
let g:airline#extensions#tabline#show_splits = 0
let g:airline#extensions#tabline#show_tab_type = 0
" Show just the filename
let g:airline#extensions#tabline#fnamemod = ':t'
" let g:airline#extensions#tabline#formatter = 'unique_tail'
" }}}

" NerdTree ----------------------------------------------- {{{
let g:NERDTreeLimitedSyntax = 1
let g:NERDTreeFileExtensionHighlightFullName = 1
let g:NERDTreeExactMatchHighlightFullName = 1
let g:NERDTreePatternMatchHighlightFullName = 1
let g:NERDTreeHighlightFolders = 1 " enables folder icon highlighting using exact match
let g:NERDTreeHighlightFoldersFullName = 1 " highlights the folder name
let NERDTreeDirArrowExpandable = "▸"
let NERDTreeDirArrowCollapsible = "▾"
" let g:NERDTreeDirArrowExpandable = '├'
" let g:NERDTreeDirArrowCollapsible = '└'
let NERDTreeShowHidden=0
let g:NERDTreeWinSize=30
let NERDTreeMinimalUI=1
let NERDTreeHijackNetrw=0
let NERDTreeQuitOnOpen = 1
" }}}

" Vim-Devicons --------------------------------------------------------------{{{
let g:DevIconsEnableNERDTreeRedraw = 0
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols = {}
" let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['js'] = ''
let g:WebDevIconsUnicodeDecorateFolderNodes = 1
" let g:WebDevIconsNerdTreeAfterGlyphPadding = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['css'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['html'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['json'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['md'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['sql'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['py'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['zip'] = ''
let g:WebDevIconsUnicodeDecorateFileNodesExtensionSymbols['txt'] = ''
if exists("g:loaded_webdevicons")
	call webdevicons#refresh()
endif
	" }}}


" Tagbar settings --------------------------------------------- {{{
let g:tagbar_autoshowtag=1
let g:tagbar_width=25
let g:tagbar_autofocus=1
" let g:tagbar_left = 1
" let g:tagbar_vertical = 30
" }}}

" }}}

"Color schemes ----------------------------------------------- {{{
" if !exists('g:syntax_on')
" 	syntax enable
" endif
let $NVIM_TUI_ENABLE_TRUE_COLOR=1
" let g:lightline = {'colorscheme':'solarized'}
set background=dark
colo railscasts
let g:airline_theme='bubblegum'
hi CursorLineNR guifg=#ffffff
" }}}

"AutoCommands ----------------------------------------------- {{{
source ~/.config/nvim/autocommands.vim
" }}}

"Mappings ----------------------------------------------- {{{
source ~/.config/nvim/mappings.vim
" }}}
