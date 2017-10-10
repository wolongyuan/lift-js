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