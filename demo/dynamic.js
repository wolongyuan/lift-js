var obj = {};
var i = 0;

while (i < 3) {
  var str = panel.readStr();
  obj[str] = str;

  panel.show(obj);
  ++i;
}
