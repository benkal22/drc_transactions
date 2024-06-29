#!/usr/bin/env node
// build a --template, or a whole project --root directory
// default context filename is `index.js` for dirs, unless --context
// specify a --build directory to output there, instead of STDOUT

var
preprocess= require('./preprocess'),
// here you can pre-process the response before final output

DELIM= ["::", "::"], // or use ["<\\?js", "\\?>"] to get `1<?js2?>3`  → `123` 
// describe your document context in JSON, then use <?js ?> for the template
// i.e. root/index.json {a:1, b:"hi"} , index.html <!doctype html> ::b+a::  → "hi1"

JSON= /^\s*\{[^]*\}\s*$/gi
// relaxed Javascript Object, for use with eval([js]).pop()


function HTMX (delim){
  function unpickle (__ctx, __js){ with (__ctx){ return eval (__js) }}

  var
  EMPTY_STR= '',
  NOT_DELIM= ANY= "([^]*?)"

  return (function (delim, pre){
    return function renderTemplateWithContext (t, c){
      var
      r= t.split( new RegExp(delim.join( NOT_DELIM), 'ig')),
      n= 0, s,
      c= c || {}

      do {
        s= 3 *n + 1
        if (r[s] && r[s].match( JSON)){

          r[s]= unpickle( c, '[' + r[s] + ']')[0]
          r[s]= pre.call( c, r[s])
          r[s]= r[s].return
        } else {
          r[s]= unpickle( c, r[s])
        }
        n += 1
      } while (void 0 !== r[3 *n])
      return r.join(EMPTY_STR)
    }
  })(delim || DELIM, preprocess)
}


if (require.main === module){
  if (2 >= process.argv.length)
    throw new Error("use --root with --build, or --template with --context")
  require('./cli')(HTMX)
  
} else
  module.exports= HTMX

