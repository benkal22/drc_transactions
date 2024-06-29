HTMX - static document generator, with Javascript preprocessing
====

Use Javascript where you would ordinarily use PHP or some templating language.

### STATUS: [v0.0.2](https://gist.github.com/godDLL/f31224df756fff2623290e331b40b1fe/2154551fb333e861ab258ccb42e6d30fd2733a04) _so **alpha** it hurts_
This has just been hacked together, so expect a bumpy ride.


Overview
---

    $ echo "1::b::3" | htmx --context "{b:'2'}"
    → 123

Default script delimiters are the same for left and right side. Double
colon `::` was chosen for it's scarse use in websites source-code.

You can set it up with `['<\\?', '\\?>']` delimiters for PHP-like short tags.

If your Javascript returns an object structure instead of a text response, (say
some vDOM) you can use the `preprocess()` function to layout the final output.


Download
---

    npm install -g htmx

Node.js Quickstart
-------

    var
    fs= require('fs'),
    htmx= require('htmx')()

    fs.writeFileSync(
      'test.html',                                // → "123"
      htmx(
        fs.readFileSync('test.htmx').toString(),  // → "1::b::3"
        fs.readFileSync('test.js').toString()     // → "{b:2}"
    ))


Shell Quickstart
-----

    $ cat index.html
    → "1::b::3"
    $ cat index.js
    → {b:'2'}
    $ htmx --context index.js  --template index.html
    → 123
    // -c can be a JSON string
    // if -t is missing, STDIN is used instead
    $ htmx --root .  --build ../build  // see TODO.md
    // builds current dir, using index.js for context, if exists

F. A. Q. (advanced usage)
-------

All shell options can be shortened, as long as they are distinguishable.  
So the `--root` option can become `-r` and the `--context` option can become `-c`

Use the `--delimiter` option like so: `htmx -d \\\{\\\{ \\\}\\\}`. Yes, I know.  
RegExp escape, shell escape, no quotes, weird space in the middle. PRs welcome.

The `preprocess()` function lives in the `preprocess.js` module, which
you will have to hack on. PRs welcome.


Rationale
---

PHP is way too clunky still. Things like Jinja's filter pipes in Javascript naturally become chains, the script return value naturally becomes the response, I mean, I didn't do much to make all this work, not at all.

Javascript is a fine templating language, when used like this.


