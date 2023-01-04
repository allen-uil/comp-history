import os

gold, silver, bronze, other = "\U0001f947", "\U0001f948", "\U0001f949", "\U0001f3c5"
comp_conv = {
"AC":"Accounting",
"CL":"Calculator",
"CA":"Computer Apps",
"CS":"Computer Sci",
"CE":"Current Events",
"GM":"General Math",
"WR":"Journalism",
"LC":"Literary Crit",
"NS":"Number Sense",
"SC":"Science",
"SS":"Social Studies",
"SP":"Spelling"
}

def rep(s): # ok so apparently I only need this bcz the other medal is stupid
	s = s.replace("GOLD", gold)
	s = s.replace("SILVER", silver)
	s = s.replace("BRONZE", bronze)
	s = s.replace("OTHER", other)
	return s

names = set()

info = list(map(str.strip, open("info.js", "r").readlines()))
team_idx = info.index("var tres = [")
start_idx = info.index("var res = [")
for i in range(start_idx+1, len(info)-1):
	s = info[i][13:-3]
	if s[-1] == ',':
		s = s[:-1]
	s = s.split(" | ")
	for x in s:
		colon_idx = x.find(":")
		x = x[:colon_idx]
		names.add(x)

template = open("template.html", "r").readlines()

os.chdir("profiles")
for s in names:
	file_name = '-'.join(map(str, s.lower().split(" ")))
	f = open(file_name + ".html", "wb")
	tester = open("test.html", "wb")
	txt = ''.join(map(str, template))
	txt = txt.replace("(Name)", s)

	# ok so some steps
	# - figure out what teams they were on
	# - while you're at it, extract individual results
	# - using those teams, find team results
	go, si, br, ot = 0, 0, 0, 0
	comp, res = [], []
	for i in range(start_idx+1, len(info)-1):
		if s in info[i]:
			# the person is here!
			comp.append(info[i][2:9]) # the competition
			SI = info[i].find(s)
			FI = info[i].find("|", SI)
			if FI == -1:
				FI = info[i].find("\"", SI)

			ev_res = info[i][SI + len(s) + 2: FI].strip()
			res.append(ev_res)

			go += ev_res.count("1st")
			si += ev_res.count("2nd")
			br += ev_res.count("3rd")
			ot += ev_res.count("4th") + ev_res.count("5th") + ev_res.count("6th")

	for cidx in range(len(comp)):
		c = comp[cidx]
		# ok now find the team results :clown:
		for i in range(team_idx+1, start_idx-2):
			if c in info[i]:
				ev_te_res = info[i][13:info[i].find("]")-1]
				ev_te_res = ', '.join(map(str, ev_te_res.split(" | ")))
				# just to double check...
				if len(ev_te_res) != 0:
					if ev_te_res[-2] == ',':
						ev_te_res = ev_te_res[:-2]
					if ev_te_res[-1] == ',':
						ev_te_res = ev_te_res[:-1]
					if ev_te_res[0] == ',':
						ev_te_res = ev_te_res[2:]
					res[cidx] += ", " + ev_te_res


				go += ev_te_res.count("1st")
				si += ev_te_res.count("2nd")
				br += ev_te_res.count("3rd")

		if len(res[cidx]) != 0:
			if res[cidx][-2] == ',':
				res[cidx] = res[cidx][:-2]
			if res[cidx][-1] == ',':
				res[cidx] = res[cidx][:-1]
			if res[cidx][0] == ',':
				res[cidx] = res[cidx][2:]

	txt_res = "<h2>"
	txt_res += (gold * go) + (silver * si) + (bronze * br) + (other * ot)
	txt_res += "</h2>\n<br>"
	txt_res += "<ul>\n\t"
	for i in range(len(comp)):
		txt_res += "<li>" + comp[i][:5] + comp_conv[comp[i][5:]]
		if len(res[i]) >= 3: # idk some random value
			txt_res += ": " + res[i] + "</li>\n"
	txt_res += "</ul>"
	
	txt = txt.replace("some crazy stuff", txt_res)

	f.write(rep(txt).encode())