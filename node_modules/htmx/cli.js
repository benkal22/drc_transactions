var
fs= require('fs'),
readFile= fs.readFileSync,
writeFile= fs.writeFileSync,
statPath= fs.statSync,

JSON= /^\s*\{[^]*\}\s*$/gi
// relaxed Javascript Object, for use with eval([js]).pop()


module.exports= function (HTMX){
  function unpickle (__json){ return eval ('[' + __json + ']')[0] }

  var
  test= process.argv.slice(2).join(' '),
  getParam= function (name){
            return new RegExp(name + '\\s+([^]*?)\\s*(-|$)', 'gi') },
  dir= getParam('[-]?-b\\w*').exec(test),
  ctx= getParam('[-]?-c\\w*').exec(test),
  tpl= getParam('[-]?-t\\w*').exec(test),
  dat= getParam('[-]?-r\\w*').exec(test)
  
  // TODO: yuck, replace this shit
  var
  delim= /[-]?-d\w*\s+([^]*?)\s([^]*?)\s*(-|$)/gi.exec(test)
  if (delim) delim= [delim[1], delim[2]]

  var
  render= HTMX(delim)

  if (dir) {
    dir= dir[1]
    var isdir
    try {
      isdir= statPath(dir).isDirectory
    } catch (_) { }
    if (!isdir)
      throw new Error("--build isn't a directory, can't read")
  }

  if (dat){
    dat= dat[1]
    if (!dir)
      throw new Error("--build directory required")
    // TODO: for each file in `dat` recursively, `render()` that fucker, with it's `ctx`
    process.stderr.write( 'TODO: not implemented, PRs welcome')

  } else {
		tpl && (tpl= tpl[1])

    if (ctx){
      ctx= ctx[1], 
      process.stderr.write('Running ' + (tpl || 'STDIN') + ' with ' + ctx + "\n")

      if (ctx && ctx.match( JSON)){
        ctx= unpickle( ctx)
      } else {
        try {
          ctx= unpickle( readFile( ctx).toString())
        } catch (_){
          throw new Error("--context not a Javascript object, can't read as filename")
        }
      }
    }
    if (tpl){
      try {
        var out= render( readFile( tpl).toString(), ctx)
      } catch (TemplateException){
        if ('ENOENT' == TemplateException.code)
          throw new Error("--template can't be read as filename")
        else {
          process.stderr.write( "Can't render template")
          throw TemplateException
        }
      }
      if (!dir)
        process.stdout.write( out)
      else
        writeFile( dir + '/' + tpl.split('/').pop(), out)

    } else {
      tpl= []
      process.stdin.on('readable', function (){
        tpl.push( process.stdin.read())
      })
      process.stdin.on('end', function (){
        if (tpl)
          process.stdout.write( render( tpl.join(''), ctx))
      })
    }
  }
}

