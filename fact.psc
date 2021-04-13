function fact( x : integer ) returns string
	if x = 1 then
		return 1
	else
		return x * fact(x -1)
	endif
endfunction
output fact(10)