
" Vim language file
" Rule script language for dorfbook
" Hackish highlight mappings work on the default 'forest' color scheme

if exists("b:current_syntax")
	finish
endif

let b:current_syntax = "dorf"

syntax match dorfComment '^[^\t >#].*$'

syntax match dorfRule '^###.*$'
syntax match dorfDescription '^>.*$' contains=dorfReference
syntax match dorfReference '{[A-Za-z]\+}' contained display

syntax match dorfDefs '^\t.*$' transparent contains=dorfTagPos,dorfTagNeg,dorfArrow
syntax match dorfTagPos '+[A-Za-z!]\+' contained display
syntax match dorfTagNeg '-[A-Za-z!]\+' contained display
syntax match dorfArrow '->' contained display

highlight link dorfComment Comment
highlight link dorfTagPos Identifier
highlight link dorfTagNeg PreProc
highlight link dorfDescription Constant
highlight link dorfReference Special
highlight link dorfRule Statement
highlight link dorfArrow Statement

