// 
// rtti
//
var a;

a = "test";
panel.show(typeof a);

a = 1;
panel.show(typeof a);

//
// overloading
// 
panel.show(3 + 3);
panel.show("te" + "st");
panel.show(6 * 6);
panel.show(3 * "test");
panel.show("test" * 2);

//
// recursion
// 
function fib(n) {
  if (n < 2) {
    return n;
  } else {
    return fib(n-1) + fib(n-2);
  }
};

var i;
for (i = 0; i < 9; ++i) {
    panel.show(fib(i));
};

//
// closure
// 
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

//
// functional
// 
function add(a, b) {
    return a + b;
};

function mul(a, b) {
    return a * b;
};

function calc(a, b, op) {
    return op(a, b);
};

panel.show(calc(4, 5, add));
panel.show(calc(4, 5, mul));

//
// prototype inheritance
// 
function Person() {};

Person.prototype.dance = function() {
    return 'dance';
};

var Tom = new Person();

panel.show(Tom.dance());

function Ninja() {};

Ninja.prototype = new Person();
Ninja.prototype.swing = function() {
    return 'swing';
};

var Bob = new Ninja();

panel.show(Bob.dance());
panel.show(Bob.swing());
