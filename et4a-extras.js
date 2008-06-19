// Requires prototype & effects.js from Scriptaculous

// array manipulation

IBM.ET4A.setBehaviorHandler("filter", function(node, data, params) {
	var fn = eval("function(data) { return " + params[0] + "}");
	console.log(data.findAll(fn).toSource());
	return data.findAll(fn);	
});

IBM.ET4A.setBehaviorHandler("sort", function(node, data, params) {
	var fn = eval("function(a, b) { return " + params[0] + "}");
	return data.sort(fn);
});

IBM.ET4A.setBehaviorHandler("sortBy", function(node, data, params) {
	var by = params[0];
	var type = params[1] || 'lexically';
	var fn;
	if (type == 'lexically') {
		if (by.match(/^-/)) {
			by = by.substring(1);
			fn = function(a, b) {
				return a[by] == b[by] ? 0 : " " + a[by] > " " + b[by] ? -1 : 1; 
			}
		} else {
			fn = function(a, b) {
				return a[by] == b[by] ? 0 : " " + a[by] > " " + b[by] ? 1 : -1; 
			}
		}
	} else if (type == 'numerically') {
		var fn;
		if (by.match(/^-/)) {
			by = by.substring(1);
			fn = function(a, b) {
				return b[by] - a[by]; 
			}
		} else {
			fn = function(a, b) {
				return a[by] - b[by]; 
			}
		}
	} else {
		throw 'unknown sort type: ' + type;
	}
	return data.sort(fn);
});

// pager
var pager = document.createElement("span");
pager.innerHTML = 
	"<span class='pager'>" +
		"Showing <span bind='showing'></span> of <span bind='total'></span>&nbsp;" +
		"<span bind='back' behavior='hide-if-null'><a href='javascript:void(0)'>&laquo;</a></span>&nbsp;" +
		"<span bind='forward' behavior='hide-if-null'><a href='javascript:void(0)'>&raquo;</a></span>" +
	"</span>";
IBM.ET4A.setBehaviorHandler("pager", function(node, data, params, rebind) {
	var page = params[0] || 10;
	if (page && data instanceof Array && data.length > page) {
		if (!rebind) {
			var pgr = IBM.ET4A.include(pager);
			node.parentNode.appendChild(pgr);
			node._pager_t = new IBM.ET4A.Template(pgr);
		}
		node._pager_t.bind({ 
			showing: page,
			total: data.length
			})
		data = data.slice(0, page);
	}

	return data;
});


// handle "contracted" class

var contractor =  document.createElement("span");
contractor.innerHTML = 
	"<span class='contractor'>" +
		"<a style='font-family:monospace' href='javascript:void(0)'>[+]</a>" +
	"</span>";

IBM.ET4A.setBehaviorHandler("contracted", function(node, data, params, rebind) {
	if (rebind)
		return data;
	var ctr = IBM.ET4A.include(contractor);
	ctr._contracted = true;
	node.style.display = "none";
	node.parentNode.replaceChild(ctr, node);
	var a = ctr.getElementsByTagName("a")[0];
	a.onclick = function(event) {
		if (ctr._contracted) {
			new Effect.Appear(node, {duration: 0.4});
			a.innerHTML = "[-]";
		} else {
			new Effect.Fade(node, {duration: 0.4});
			a.innerHTML = "[+]";
		}
		ctr._contracted = !ctr._contracted;
	};
	ctr.appendChild(node);
	return data;
});

// handle "maxlen" attribute
IBM.ET4A.addTemplateListener({
	handleObject: function(node, data) {

		var maxlen = node.getAttribute("maxlen");
		if (maxlen && typeof data == "string" && data.length > maxlen) {
			data = textEllipsis(data, maxlen);
		}
		return data;
	}
});

var ellipsis = document.createElement("span");
ellipsis.innerHTML = 
	"<span class='snip'></span>" +
        "&nbsp;<span class='ellipsis' bindAttributes='onmouseout:hide, onmouseover:show' >...</span>&nbsp;" +
        "<span class='rest' style='display:none'></span>";


function textEllipsis(txt, max) {
	var snip = txt.substring(0, max); // TODO find space
	var rest = txt.substring(max);
	return function(node, data) {
		node.appendChild(IBM.ET4A.include(ellipsis));
		return { 
			snip: snip, 
			rest: rest,
			show: function(node, data, event) {
				var r = node.parentNode.getElementsByTagName("span")[2];
				if (!r._appearing || r._appearing.state != 'running') {
					if (r._fading) r._fading.cancel();
					r._appearing = new Effect.Appear(r, {duration: 0.4});
				}
			},
			hide: function(node, data, event) {
				var r = node.parentNode.getElementsByTagName("span")[2];
				if (!r._fading || r._fading.state != 'running') {
					if (r._showing) r._showing.cancel();
					r._fading = new Effect.Fade(r, {duration: 0.4});
				}
			}
		 }
	}
}

// handle date formatting
var defaultDateFormat = "%D";
var defaultDateFormatToday = "%D %T";
var dateRe = /^(\d\d\d\d)-(\d\d)-(\d\d).(\d\d):(\d\d):(\d\d)\S*/;
IBM.ET4A.addTemplateListener({
	handleObject: function(node, data) {
		var i = node.tagName == "A" ? 1 : 0; // That's too bad

		if (typeof data == "string") {
			m = dateRe.exec(data);
			if (m) {
				var today = new Date();
				var d = new Date(m[1], m[2] - 1, m[3], m[4], m[5], m[6]);
				if (node.getAttribute("dateFormat")){
					fmt = node.getAttribute("dateFormat");
					data = dojo.date.format(d,fmt);
					node.title = m[0];
				}
			}
		}
		return data;
	}
});


