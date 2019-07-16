" System mappings ----------------------------{{{
let mapleader = "\<Space>"
let maplocalleader = ','
" Install/Uninstall Plugins
nnoremap <leader>pi :source $MYVIMRC<CR>:PlugInstall<CR>
nnoremap <leader>pc :source $MYVIMRC<CR>:PlugClean!<CR>
nnoremap <leader>pu :source $MYVIMRC<CR>:PlugUpdate<CR>
" noremap leader r to reload vimrc
noremap <leader>r :source $MYVIMRC<cr>
noremap <leader>ev :e $MYVIMRC<CR>
noremap <left> <Nop>
noremap <right> <Nop>
noremap <up> <Nop>
noremap <down> <Nop>
" toggle folds with '-'
nnoremap - za
" nnoremap _ zA

" Buffers and Tabs -------------
noremap  <a-w> :bd<CR>
nnoremap <c-s-left> :bp<CR>
nnoremap <c-s-right> :bn<CR>
" Tab Handling
nnoremap <leader>t <ESC>:tabnew
nnoremap <s-right> <ESC>:tabnext<CR>
nnoremap <s-left> <ESC>:tabprevious<CR>
nnoremap <leader>w <ESC>:tabclose<CR>
" create splits easily
noremap <a--> :sp<CR>
noremap <a-\> :vsp<CR>
" move b/w splits easily using ctrl+h,j,k,l
noremap <c-j> <c-w>j
noremap <c-k> <c-w>k
noremap <c-l> <c-w>l
noremap <c-h> <c-w>h
nnoremap <silent> <c-a-up> :resize +3<cr>
nnoremap <silent> <c-a-down> :resize -3<cr>
nnoremap <silent> <c-a-right> :vertical resize +3<cr>
nnoremap <silent> <c-a-left> :vertical resize -3<cr>
nnoremap <leader>- :wincmd \|<cr>:wincmd _<cr>
nnoremap <leader>= :wincmd =<cr>
" Navigate properly when lines are wrapped
nnoremap j gj
nnoremap k gk
noremap L g_
noremap H _
nnoremap Y y$
inoremap <c-CR> <ESC>o
" For seamless jumping b/w tags
" c-] takes you the tag under the cursor, so c-[ to come back
nnoremap <special> <c-[>  <c-t>
" inoremap <c-d> <ESC>yypA
noremap gv :vertical wincmd f<CR>
nnoremap <leader>o o<ESC>xk
nnoremap <leader>O O<ESC>xj
nmap <silent> <Esc> :nohl<CR>
"--- Copy/Paste to system register
noremap <leader>y "*yy
noremap <leader>p "*p
inoremap <C-h> <Left>
inoremap <C-j> <Down>
inoremap <C-k> <Up>
inoremap <C-l> <Right>
" Disable arrow keys
inoremap <left> <Nop>
inoremap <right> <Nop>
inoremap <up> <Nop>
inoremap <down> <Nop>
vnoremap <left> <Nop>
vnoremap <right> <Nop>
vnoremap <up> <Nop>
vnoremap <down> <Nop>
" complete with tab
" inoremap <expr> <CR> (pumvisible() ? "\<c-y>\<cr>" : "\<CR>")
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
" Indent everything
	nnoremap <leader>i ggvG=
" Keep a block highlighted while shifting
vnoremap < <gv
vnoremap > >gv
vnoremap = =gv
" deletes into blackhole register
nnoremap <leader>d "_dd
vnoremap <leader>d "_d
cmap W w
cmap Q q
cabbr ht Helptags
cabbr h: History:
" Toggle Paste Mode
set pastetoggle=<F2>
if has("nvim")
" NeoVim specific mappings
" tnoremap <Esc> <C-\><C-n>   "tnoremap stands for terminal mode mappings in neovim"
" tnoremap <c-h> <C-\><C-N><C-w>h
" tnoremap <c-j> <C-\><C-N><C-w>j
" tnoremap <c-k> <C-\><C-N><C-w>k
" tnoremap <c-j> <C-\><C-N><C-w>j
endif

" Generate ctags for python
" map <F8> :!ctags -R -f ./tags `python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"`<CR>

" run macro on visual selection with @
xnoremap @ :<C-u>call ExecuteMacroOverVisualRange()<CR>
function! ExecuteMacroOverVisualRange()
echo "@".getcmdline()
execute ":'<,'>normal @".nr2char(getchar())
endfunction
cabbr mf global/require/normal " run macro on whole file

" global replace the word under cursor
nnoremap gr *:%s//<C-r><C-w>/g<left><left>
" Better movement with { }
nnoremap } }w
nnoremap <expr><silent> { (col('.')==1 && len(getline(line('.')-1))==0? '2{j' : '{j')
" }}}

" Plugin Mappings ------------------------------------{{{
nnoremap ,, :ALEFix<CR>

" NERDTree mappings ----------------------------------{{{
nnoremap <F3> :NERDTreeToggle<CR>
inoremap <F3> :NERDTreeToggle<CR>
let g:NERDTreeMapActivateNode = '<tab>'
" let g:NERDTreeMapOpenInTab = '<c-t>'
" let g:NERDTreeMapOpenInTabSilent = '<c-s-t>'
" let g:NERDTreeMapOpenVSplit = '<c-v>'
" let g:NERDTreeMapOpenSplit = '<c-x>'
let g:NERDTreeMapOpenInTab = '<a-t>'
let g:NERDTreeMapOpenSplit = '<a-->'
let g:NERDTreeMapOpenVSplit = '<a-\>'

" }}}

" Tagbar mappings ----------------------------------{{{
nnoremap <F7> :TagbarToggle<CR>
let g:tagbar_map_togglefold = "<tab>"
" }}}

" FZF mappings ----------------------------------{{{
nnoremap <leader>ff :Files<CR>
nnoremap <leader>fh :History<CR>
nnoremap <leader>fg :Rg<CR>
nnoremap <c-p> :Tags<CR>
let g:fzf_action = {
  \ 'ctrl-t': 'tab split',
  \ 'ctrl-s': 'split',
  \ 'ctrl-v': 'vsplit' }
" let g:fzf_action = {
"   \ 'a-t': 'tab split',
"   \ 'a--': 'split',
"   \ 'a-\': 'vsplit' }
" }}}

" }}}
