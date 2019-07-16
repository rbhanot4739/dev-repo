" Python specific settings.
setlocal tabstop=4
setlocal shiftwidth=4
setlocal expandtab
setlocal autoindent
setlocal wrap
setlocal textwidth=79
setlocal formatoptions=tj
setlocal linebreak
let python_highlight_all=1

" Use the below highlight group when displaying bad whitespace is desired.
highlight BadWhitespace ctermbg=red guibg=red

" Display tabs at the beginning of a line in Python mode as bad.
au BufRead,BufNewFile *.py,*.pyw match BadWhitespace /^\t\+/
" Make trailing whitespace be flagged as bad.
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/

ca todo vimgrep TODO %<CR>:cw<CR>
" Run existing python file in terminal using
nnoremap <buffer> <localleader>q :20sp <CR> :term python % <CR>
nnoremap <buffer> <localleader>i :ImportName<CR>

" All these mappings work only for python code:
" Go to definition
let g:jedi#goto_command = "<localleader>d"
" " Find ocurrences
let g:jedi#usages_command = "<localleader>u"
" " Find assignments
" let g:jedi#goto_assignments_command = '<localleader>a'
" " Rename command
let g:jedi#rename_command = "<localleader>r"
" " Open Documentation
let g:jedi#documentation_command = "K"
let g:jedi#use_splits_not_buffers = "right"

" " Disable warnings about trailing whitespace for Python files.
" let b:ale_warn_about_trailing_whitespace = 0
