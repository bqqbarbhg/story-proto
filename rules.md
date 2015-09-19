### Chop wood to gather
> {dwarf} chops down {tree} for gathering

	dwarf +dwarf +alive +gather -busy
	tree +tree +standing -busy
	->
	tree +busy
	dwarf +busy
	dwarf +chop! tree

### Chopped down trees fall
> {tree} falls down

	tree +tree +standing
	something +chop! tree
	->
	tree +fall! -standing

### Falling trees crush dwarves
> {tree} crushes {dwarf}

	tree +tree +fall!
	dwarf +dwarf +standing
	->
	dwarf +busy -standing
	tree +crush! dwarf

### Getting crushed hurts
> {object} breaks {dwarf} with its weight

	dwarf +alive
	object +crush! dwarf
	->
	dwarf +hurt!

### Hurting may kill
> {dwarf} dies from the pain

	dwarf +hurt!
	->
	dwarf +die! -alive

