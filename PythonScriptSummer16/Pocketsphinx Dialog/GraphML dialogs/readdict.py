dialog = dict()
d = open("dialog.txt", "r"); 
turns = d.readlines()
global human 
for turn in turns:
	if 'HUMAN: ' in str(turn): 
		human = turn[7:].rstrip()
		
		inside_paren = human[human.find("(")+1:human.find(")")]
		#print 'Inside: %s' %inside_paren
		outside_paren = human[human.find(")")+2:]
		#print 'Outside: %s' %outside_paren
		single_turn = human
		pos = 0
		for char in inside_paren:
			#print char
			if char is "|":
				#print inside_paren[pos:inside_paren.index(char)]
				single_turn = inside_paren[pos:inside_paren.index(char)].join(outside_paren)
				print single_turn
				pos = inside_paren.index(char)+1
					
		dialog[single_turn] = []
	elif 'ROBOT: ' in str(turn):
		turn = turn[7:].rstrip()
		dialog[single_turn].append(turn)
	

print dialog
