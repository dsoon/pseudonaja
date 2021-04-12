declare ttt : array [1 : 9] of CHAR
declare choice : integer
declare count : integer
declare player1 : boolean
declare finished : boolean

// Procedure to set-up the game
 procedure setup
	for i <- 1 to len(ttt)
		ttt[i] <- '_'
	next
	finished <- false
	player1 <- true
	count <- 0

	// Print out instructions
	output "TIC-TAC-TOE"
	output "==========="
	output "This is a 2 player game. Each player takes a turn to pick"
	output "a location on a 3 x 3 board. The first player, player1 is" 
	output "assigned a 'X', and player 2 a 'O'."
	output ""
	output "Board locations are as follows:"
	for i <- 1 to 9 step 3
		output i, i+1, i+2
	next
	output ""
	output "Current board"
	call print
endprocedure

// Procedure to print out the board 
procedure print
	for i <- 1 to len(ttt) step 3
		output ttt[i], ttt[i+1], ttt[i+2]
	next
endprocedure

// Function to check if there is a winner
function checkwin(player1_turn: boolean) returns boolean
	declare symbol : char
	declare win : boolean

	win <- false
	
	if player1 then
		symbol <- 'X'		
	else
		symbol <- 'O'
	endif

	if (ttt[1] = symbol and ttt[2] = symbol and ttt[3] = symbol) or
           (ttt[4] = symbol and ttt[5] = symbol and ttt[6] = symbol) or
           (ttt[7] = symbol and ttt[8] = symbol and ttt[9] = symbol) or
           (ttt[1] = symbol and ttt[4] = symbol and ttt[7] = symbol) or
           (ttt[2] = symbol and ttt[6] = symbol and ttt[8] = symbol) or
           (ttt[3] = symbol and ttt[6] = symbol and ttt[9] = symbol) or
           (ttt[1] = symbol and ttt[5] = symbol and ttt[9] = symbol) or
           (ttt[3] = symbol and ttt[5] = symbol and ttt[7] = symbol) then
		win <- True
	endif

	return win

endfunction

// Function to check if a location is empty
function isempty(location: integer) returns boolean
	declare empty: boolean
	if ttt[location] = '_' then 
		empty <- True
	endif
endfunction

// Function to get a valid location
function getposition(prompt : string) returns integer
	output prompt, ">"
	input choice
	while choice > 9 or choice < 1 or isempty(choice) = False do
		output "Invalid choice", choice, "value should be 1 to 9 and location should be empty"
		output prompt, ">"
		input choice
	endwhile
	return choice
endfunction

procedure play
	while count <> 9 and finished = false do
		if player1 then
			ttt[ getposition("player1" )] <- 'X'
		else
			ttt[ getposition("player2" )] <- 'O'
		endif
	
		count  <- count + 1
		if player1 then
			if checkwin(player1) then
				output "**** Player1 wins ****"
				finished <- True
			endif
			player1 <- False
		else
			if checkwin(player1) then
				output "**** Player2 wins ****"
				finished <- True
			endif
			player1 <- True
		endif
		call print
	endwhile

endprocedure


// Main code starts here ....

call setup
call play
