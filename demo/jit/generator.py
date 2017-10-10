for i in range(1, 10):
    with open("{}.js".format(i * 100), "w") as f:
        f.write("var i;\nfor(i = 0; i < %d; ++i){panel.show(typeof '1');}" % (i * 100))
