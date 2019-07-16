" Triger `autoread` when files changes on disk
" https://unix.stackexchange.com/questions/149209/refresh-changed-content-of-file-opened-in-vim/383044#383044
" https://vi.stackexchange.com/questions/13692/prevent-focusgained-autocmd-running-in-command-line-editing-mode
augroup ReloadVim
	autocmd!
	autocmd FocusGained,BufEnter,CursorHold,CursorHoldI * if mode() != 'c' | checktime | endif
	" Notification after file change
	" https://vi.stackexchange.com/questions/13091/autocmd-event-for-autoread
	autocmd FileChangedShellPost *
	\ echohl WarningMsg | echo "File changed on disk. Buffer reloaded." | echohl None
augroup END

" jumps to the last known position in a file just after opening it, if the '" mark is set:
autocmd BufReadPost *
\ if line("'\"") > 1 && line("'\"") <= line("$") && &ft !~# 'commit'
\ |   exe "normal! g`\""
\ | endif

" " Indent folding with manual folds
" augroup ManualFolds
" 	autocmd!
" 	au BufReadPre * setlocal foldmethod=indent
" 	au BufWinEnter * if &fdm == 'indent' | setlocal foldmethod=manual | endif
" augroup END

" Save and load folds
" augroup AutoSaveFolds
" 	autocmd!
" 	autocmd BufWinLeave *.* mkview
" 	autocmd BufWinEnter *.* silent! loadview
" augroup END

augroup NerdTree
	autocmd!
	" autocmd StdinReadPre * let s:std_in=1
	" autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
	autocmd BufEnter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif" Close Vim if the only window left open is NERDTree
augroup END

" center buffer around cursor when opening files
autocmd BufEnter * normal zz

" Turn off auto-commenting
au FileType * setlocal formatoptions+=t
au FileType * setlocal formatoptions-=c
au FileType * setlocal formatoptions-=r
au FileType * setlocal formatoptions-=o

autocmd FileType vim setlocal foldmethod=marker
autocmd FileType vim setlocal foldlevel=4
autocmd FileType python,html setlocal foldmethod=indent
autocmd FileType css,scss,json setlocal foldmethod=marker
autocmd FileType javascript setlocal foldmethod=syntax
autocmd FileType python,javascript,html,css,scss setlocal foldlevel=99
autocmd FileType css,scss,json setlocal foldmarker={,}

augroup OmniCompletionSetup
	autocmd!
	autocmd FileType python     set omnifunc=jedi#completions
	autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
	" autocmd FileType html       set omnifunc=htmlcomplete#CompleteTags
	autocmd FileType css        set omnifunc=csscomplete#CompleteCSS
augroup END
