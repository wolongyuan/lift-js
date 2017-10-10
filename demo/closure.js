function Number() {
  num = 0;
  this.set = function (n) {
    num = n;
  };
  this.get = function () {
    return num;
  };
};

n = new Number();
panel.show(n.get());
n.set(5);
panel.show(n.get());
