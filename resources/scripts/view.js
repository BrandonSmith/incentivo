function addClassName(body_node, browser, ignoreCase) {
    if (body_node.className) {
        var body_classes = body_node.className.split(" ");
        if (ignoreCase) {
            var iBrowser = browser.toUpperCase();
            for (var i = 0; i < body_classes.length; i++) {
                if (body_classes[i].toUpperCase() == iBrowser) {
                    body_classes.splice(i, 1);
                    i--;
                }
            }
        }
        body_classes[body_classes.length] = browser;
        body_node.className = body_classes.join(" ");
    } else {
        body_node.className = browser;
    }
}

function getElementsByClassName(node, tag, class) {
    var elements = (tag == "*" && node.all) ? node.all : node.getElementsByTagName(tag);
    var filteredElements = new Array;
    class = class.replace(/\-/g, "\\-");
    var regex = new RegExp("(^|\\s)" + class + "(\\s|$)");
    var element;
    for (var i = 0; i < elements.length; i++) {
        element = elements[i];
        if (regex.test(element.className)) {
            filteredElements.push(element);
        }
    }
    return filteredElements;
}

function initialize() {
    var _1 = document.getElementById("main_body");
    if (_1) {
        removeClassName(_1, "no_guidelines");
        var _2 = getElementsByClassName(document, "*", "guidelines");
        if (_1.offsetWidth <= 450 || (_2 == "")) {
            addClassName(_1, "no_guidelines", true);
        }
    }
    elements = getElementsByClassName(document, "*", "element");
    for (i = 0; i < elements.length; i++) {
        if (elements[i].type == "checkbox" ||
            elements[i].type == "radio" || elements[i].type == "file") {
            elements[i].onclick = function () {safari_reset();addClassName(this.parentNode.parentNode, "highlighted", true);};
            elements[i].onfocus = function () {safari_reset();addClassName(this.parentNode.parentNode, "highlighted", true);};
            el_array.splice(el_array.length, 0, elements[i]);
        } else {
            elements[i].onfocus = function () {safari_reset();addClassName(this.parentNode.parentNode, "highlighted", true);};
            elements[i].onblur = function () {removeClassName(this.parentNode.parentNode, "highlighted");};
        }
    }
    var _3 = navigator.userAgent.toLowerCase();
    var body_nodes = document.getElementsByTagName("body");
    if (_3.indexOf("safari") + 1) {
        addClassName(_4[0], "safari", true);
    }
    if (_3.indexOf("firefox") + 1) {
        addClassName(body_nodes[0], "firefox", true);
    }
}
