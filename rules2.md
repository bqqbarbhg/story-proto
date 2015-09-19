
### Dwarves are afraid of spiders
> {dwarf} gets a fright from {spider}

	dwarf +dwarf +alive -scared
	spider +spider +alive
	->
	spider +scare! dwarf
	dwarf +scared

### Scared dwarves drop stuff
> {dwarf} drops {item} in fear

	dwarf +dwarf +alive
	dwarf +hold item
	something +scare! dwarf
	->
	item +drop!

### Dropped glasses can break
> {glass} shatters as it falls

	glass +glass +drop!
	->
	glass +break!

### Dwarves get mad when something they own breaks
> {dwarf} is mad that his {item} broke

	dwarf +dwarf +alive
	dwarf +own item
	item +break!
	->
	dwarf +mad

