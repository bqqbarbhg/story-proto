from collections import namedtuple, defaultdict
import itertools
import random

Tag = namedtuple("Tag", ("bind", "tags", "notags"))
Rel = namedtuple("Rel", ("src", "dst", "tags"))
Cond = namedtuple("Cond", ("tags", "rels"))
Rule = namedtuple("Rule", ("desc", "texts", "pre", "post"))

def parse_rules(lines):
	rules = []

	started = False
	desc = None
	texts = None
	defs = (Cond([], []), Cond([], []))
	defin = 0
	
	for line in lines:
		if line.startswith('###'):
			if started:
				rules.append(Rule(desc, texts, defs[0], defs[1]))

			started = True
			defin = 0
			defs = (Cond([], []), Cond([], []))
			texts = []

			desc = line[3:].strip()
		elif line.startswith('>'):
			texts.append(line[1:].strip())
		else:
			tokens = line.split()
			if tokens == ['->']:
				defin = 1
			
			binds = []
			tags = []
			notags = []

			for token in tokens:
				if token.startswith('+'):
					tags.append(token[1:])
				elif token.startswith('-'):
					notags.append(token[1:])
				else:
					binds.append(token)

			if len(binds) == 1:
				defs[defin].tags.append(Tag(binds[0], tags, notags))
			elif len(binds) == 2:
				defs[defin].rels.append(Rel(binds[0], binds[1], tags))

	rules.append(Rule(desc, texts, defs[0], defs[1]))
	return rules

with open('rules2.md', 'r') as fl:
	rules = parse_rules(fl)

def cond_lines(cond):
	lines = []
	for tag in cond.tags:
		lines.append('\t%s %s %s' % (tag.bind,
			' '.join('+%s' % t for t in tag.tags),
			' '.join('-%s' % t for t in tag.notags)))
	for rel in cond.rels:
		lines.append('\t%s %s %s' % (rel.src,
			' '.join('+%s' % t for t in rel.tags),
			rel.dst))
	return lines

def rule_string(rule):
	lines = []
	lines.append('### ' + rule.desc)
	lines.append('> ' + rule.text)
	lines += cond_lines(rule.pre)
	lines.append('\t->')
	lines += cond_lines(rule.pre)
	return '\n'.join(lines)

class Entity(object):
	def __init__(self, name, tags):
		self.name = name
		self.tags = tags
		self.oldtags = set()
	def __repr__(self):
		return '!%s [%s]!' % (self.name, ', '.join(self.tags))

class RelInfo(object):
	def __init__(self):
		self.new = True

entities = [
	Entity("Urist", { "dwarf", "alive" }),
	Entity("Spider", { "spider", "alive" }),
	Entity("Beer", { "glass" }),
]

relations = defaultdict(lambda: defaultdict(RelInfo))

relations["hold"][(entities[0], entities[2])].new = True
relations["own"][(entities[0], entities[2])].new = True

def match_tags(entity, cond):
	return all(tag in entity.tags for tag in cond.tags)	and not any(tag in entity.tags for tag in cond.notags)

def match_rule(rule, entities, relations):
	tagbinds = set()
	tagpos = defaultdict(set)
	tagneg = defaultdict(set)
	for tag in rule.pre.tags:
		tagbinds.add(tag.bind)
		for entity in entities:
			if match_tags(entity, tag):
				tagpos[tag.bind].add(entity)
			else:
				tagneg[tag.bind].add(entity)

	relbinds = set()
	relpos = defaultdict(set)
	for rel in rule.pre.rels:
		relbinds |= { rel.src, rel.dst }
		ents = (set(relations[r].keys()) for r in rel.tags)
		matching = set.intersection(*ents)
		relpos[rel.src] |= { m[0] for m in matching }
		relpos[rel.dst] |= { m[1] for m in matching }
		
	candidates = { }
	binds = tagbinds | relbinds
	for bind in binds:
		istag = bind in tagbinds
		isrel = bind in relbinds

		if istag and isrel:
			candidates[bind] = (tagpos[bind] - tagneg[bind]) & relpos[bind]
		elif istag:
			candidates[bind] = tagpos[bind] - tagneg[bind]
		elif isrel:
			candidates[bind] = relpos[bind]

	if not all(candidates.values()):
		return None

	return candidates

def check_rule(rule, binds, relations):
	for tag in rule.pre.tags:
		if not match_tags(binds[tag.bind], tag):
			return False
	for rel in rule.pre.rels:
		for tag in rel.tags:
			if (binds[rel.src], binds[rel.dst]) not in relations[tag]:
				return False
	return True

def apply_rule(rule, binds, entities, relations):
	for tag in rule.post.tags:
		binds[tag.bind].tags |= set(tag.tags)
		binds[tag.bind].tags -= set(tag.notags)
	for rel in rule.post.rels:
		for tag in rel.tags:
			relations[tag][(binds[rel.src], binds[rel.dst])].new = True

def select_candidates(candidates):
	options = itertools.product(*candidates.values())
	return [{ bind: opt for bind, opt in zip(candidates.keys(), opts) } for opts in options]

RuleBind = namedtuple("RuleBind", ("rule", "binds"))

def match_rules(rules, entities, relations):
	rule_list = []

	for rule in rules:
		candidates = match_rule(rule, entities, relations)
		if candidates:
			if all(candidates.values()) and False:
				print "Rule '%s' applicable for" % rule.desc
				print '\n'.join('\t%s: %s' % (bind, ', '.join(e.name for e in entities)) for (bind, entities) in candidates.items())

			options = select_candidates(candidates)
			if options:
				rule_list += (RuleBind(rule, opt) for opt in options)

	random.shuffle(rule_list)

	for rule, binds in rule_list:
		if not check_rule(rule, binds, relations):
			continue

		names = { bind: ent.name for bind, ent in binds.items() }
		text = random.choice(rule.texts)
		print text.format(**names)
		apply_rule(rule, binds, entities, relations)

for l in range(20):
	for entity in entities:
		entity.tags -= entity.oldtags
		entity.oldtags = { action for action in entity.tags if action.endswith('!') }
	for tag, rels in relations.items():
		if tag.endswith('!'):
			removelist = []
			for rel, info in rels.items():
				if not info.new:
					removelist.append(rel)
				else:
					info.new = False
			for rem in removelist:
				del rels[rem]

	match_rules(rules, entities, relations)

