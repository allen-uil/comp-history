function query() {
	let y = $("#year").val();
	let e = $("#event").val();
	let comp = event.find(x => x[0] == e)[1];
	document.getElementById('toggle').innerHTML = 
		"<h2>" + y + " " + comp + "</h2>\n";

	if (e != "WR" && e != "CA") { // no compapps team results
		let team_res = tres.find(x => x[0] == (y + " " + e))[1].split(" | ");
		team_res.forEach(
			function box(s) {
				if (s.length == 0) return;
				var txt = "<div class=\"box"
				if (s.includes("1st")) txt += " gold";
				if (s.includes("2nd")) txt += " silver";
				if (s.includes("3rd")) txt += " bronze";
				txt += "\">" + s + "</div>\n";
				
				document.getElementById('toggle').innerHTML += 
					txt;
			}
		)
	}
	document.getElementById('toggle').innerHTML += "<br\n";
	
	let ind_res = res.find(x => x[0] == (y + " " + e))[1].split(" | ");
	document.getElementById('toggle').innerHTML += 
		"<h4>Team Members:</h4>\n<ul>\n"
	ind_res.forEach(
		function mem(s) {
			let txt = "<li>";
			let idx = s.indexOf(":");
			let name = s.substring(0, idx);
			console.log(name);
			let link = name.toLowerCase().split(" ").join("-") + ".html";
			txt += "<b><u><a href=\"profiles/" + link + "\">" + name + "</a></u></b>";

			if (s.length - idx > 2) {
				txt += ": " + s.substring(idx+1);
			}
			document.getElementById('toggle').innerHTML +=
				txt + "</li>\n";
		}
	);
	document.getElementById('toggle').innerHTML += 
		"</ul>\n<br>";


}