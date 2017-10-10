panel.show('Guess how old I am?');

var i = panel.readInt();

if (i === 20) {
  panel.show('Hey! You got it.');
} else {
  panel.show('Eh... No...');
}
