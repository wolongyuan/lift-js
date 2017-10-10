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

