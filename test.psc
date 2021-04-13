function simple(arg : integer) returns boolean
	declare val : boolean
	val <- False
	if mod(arg, 2) = 0 then
		val <- True
	endif
	return val
endfunction

output simple(5)