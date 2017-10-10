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
