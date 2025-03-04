print, input = (
    (f:=(lambda *args,sep=" ",end="\n",file=__import__("sys").stdout,flush=False,interval=5:
        (None,
         w:=__import__("time").sleep,
         p:=list(__import__("string").printable)[:-6],
         o:=file.write,t:=__import__("os").get_terminal_size().columns-1,
         b:=(
             (
                 (c:=__import__("ctypes"),
                 d:=__import__("ctypes.wintypes").wintypes.DWORD(),
                 k:=c.windll.kernel32,k.GetConsoleMode(k.GetStdHandle(-10),c.byref(d)),
                 k.SetConsoleMode(k.GetStdHandle(-10),0),
                 k.GetConsoleMode(k.GetStdHandle(-11),c.byref(d)),
                 k.SetConsoleMode(k.GetStdHandle(-11),7),
                 o("\x1b[?25l\x1b[6n"),
                 file.flush(),
                 b:=(c:=lambda a:(a if a.endswith("R")else c(a+__import__("sys").stdin.read(1))))(__import__("sys").stdin.read(1)),
                 k.SetConsoleMode(k.GetStdHandle(-10),d),
                 k.SetConsoleMode(k.GetStdHandle(-11),d),
                 int(r.groups()[1]) if (r:=__import__("re").match(r"^\x1b\[(\d*);(\d*)R",b))else 1)
              if __import__("sys").platform=="win32" else\
                 (s:=__import__("sys").stdin.fileno(),
                 ta:=__import__("termios").tcgetattr(s),
                 __import__("tty").setcbreak(s,__import__("termios").TCSANOW),
                 o("\x1b[?25l\x1b[6n"),file.flush(),
                 b:=(c:=lambda a:(a if a.endswith("R")else c(a+__import__("sys").stdin.read(1))))(""),
                 __import__("termios").tcsetattr(s,__import__("termios").TCSANOW,ta),
                 int(r.groups()[1])if(r:=__import__("re").match(r"^\x1b\[(\d*);(\d*)R",b))else 1)
              )[-1]if file==__import__("sys").stdout else 0),
         m:=(str(sep).join(map(str,args))+str(end)+"\0").split("\n"),
         (m:=([" \b"*((b-1)//2)+"\0"*((b-1)%2)+m[0]]+(m[1:]if(len(m)>1)else[]))if(len(m)>0)else m,
          a:="",
          (
              [
                  [
                      [
                          [
                              ((a:=n)if n=="\x1b"else(a:=a+n)if a else()),
                                [
                                    (o(c+"\b"),
                                    file.flush(),
                                    w(interval/1000))
                                for c in p[:
                                    (p.index(n)+1 if n in p else\
                                    0 if ((n in "\0 \b") or a) else\
                                    len(p))]
                                ],
                                o(n if a=="" else ""if a=="\x1b[" or a[-1]<"@" or a[-1]>"~" else (a+" \b",a:="")[0])
                            ]
                      for n in l],
                  o("\x1b[1C\n")
                  ] for l in(a for b in([l[a:a+t]for a in range(0,len(l)+1,t)]for l in m[:-1])for a in b)
                ],
            [
                [
                    [
                        [
                            ((a:=n)if n=="\x1b"else(a:=a+n)if a else()),
                            [
                                (o(a),
                                 o(c+"\b"),
                                 file.flush(),
                                 w(interval/1000))
                                for c in p[:(p.index(n)+1 if n in p else 0 if n in"\0 \b"or a else len(p))]
                            ],
                            o(n if a==""else""if a=="\x1b["or a[-1]<"@"or a[-1]>"~"else(a+" \b",a:="")[0])
                        ]for n in l]
                ]for l in(a for b in([l[a:a+t]for a in range(0,len(l)+1,t)]for l in m[-1])for a in b)
            ])if m else(),
          file.flush()if flush else(),
          o("\x1b[?25h"))if file!=__import__("sys").stdout else o(m),
         file.close()if file!=__import__("sys").stdout else())[0]),
     f.__setattr__("__doc__","WARNING: OUTPUTTING IT INTO A FILE GIVES A RAW OUTPUT OF THIS PROGRAM INSTEAD OF WHAT YOU EXPECTED, USE AT YOUR OWN RISK\n*Made by Taokyle*\n\nPrints the values to a stream, or to sys.stdout by default.\nThis is a fancy version of printing based on the default print function, it can directly replace the print function.\nHowever, please be noted that it takes a long time to print, even if interval is set to 0 the speed is still slower than the original print function (due to the animations).\nYet you can set interval to 0, sacrifising the visibility of the animation in exchange of print speed.\nThe following are detailed (not really) description for each arguments.\n  args\n    values to be printed, every value should have __str__ method.\n  sep\n    string inserted between values, default a space.\n  end\n    string appended after the last value, default a newline.\n  file\n    a file-like object (stream), defaults to the current sys.stdout.\n  flush\n    whether to forcibly flush the stream. (but you have no choice it's gonna be flushed anyway)\n  interval\n    time between each change on console during the print, default 5ms."))[0],
    (f:=(lambda prompt="",interval=5:
        (w:=__import__("time").sleep,
         p:=[" "]+list(__import__("string").printable)[:-6],
         o:=__import__("sys").stdout.write,
         t:=__import__("os").get_terminal_size().columns-1,
         b:=(
                (c:=__import__("ctypes"),
                d:=__import__("ctypes.wintypes").wintypes.DWORD(),
                k:=c.windll.kernel32,k.GetConsoleMode(k.GetStdHandle(-10),c.byref(d)),
                k.SetConsoleMode(k.GetStdHandle(-10),0),
                k.GetConsoleMode(k.GetStdHandle(-11),c.byref(d)),
                k.SetConsoleMode(k.GetStdHandle(-11),7),
                o("\x1b[?25l\x1b[6n"),
                __import__("sys").stdout.flush(),
                b:=(
                    c:=lambda a:(a if a.endswith("R")else c(a+__import__("sys").stdin.read(1))))(__import__("sys").stdin.read(1)),
                    int(r.groups()[1])if (r:=__import__("re").match(r"^\x1b\[(\d*);(\d*)R",b))else 1
                )\
            if __import__("sys").platform=="win32"else
                (s:=__import__("sys").stdin.fileno(),
                 ta:=__import__("termios").tcgetattr(s),
                 __import__("tty").setcbreak(s,__import__("termios").TCSANOW),
                 o("\x1b[?25l\x1b[6n"),
                 __import__("sys").stdout.flush(),
                 b:=(c:=lambda a:(a if a.endswith("R")else c(a+__import__("sys").stdin.read(1))))(__import__("sys").stdin.read(1)),int(r.groups()[1])if (r:=__import__("re").match(r"^\x1b\[(\d*);(\d*)R",b))else 1))[-1],m:=(str(prompt)+"\0").split("\n"),m:=([" \b"*((b-1)//2)+"\0"*((b-1)%2)+m[0]]+(m[1:]if len(m)>1 else[]))if len(m)>0 else m,a:="",([[[[((a:=n)if n=="\x1b"else(a:=a+n)if a else()),[(o(c+"\b"),__import__("sys").stdout.flush(),w(interval/1000))for c in p[:(p.index(n)+1 if n in p else 0 if n in"\0 \b"or a else len(p))]],o(n if a==""else""if a=="\x1b["or a[-1]<"@"or a[-1]>"~"else(a+" \b",a:="")[0])]for n in l],o("\x1b[1C\n")]for l in(a for b in([l[a:a+t]for a in range(0,len(l)+1,t)]for l in m[:-1])for a in b)],[[[[((a:=n)if n=="\x1b"else(a:=a+n)if a else()),[(o(a),o(c+"\b"),__import__("sys").stdout.flush(),w(interval/1000))for c in p[:(p.index(n)+1 if n in p else 0 if n in"\0 \b"or a else len(p))]],o(n if a==""else""if a=="\x1b["or a[-1]<"@"or a[-1]>"~"else(a+" \b",a:="")[0])]for n in l]]for l in(a for b in([l[a:a+t]for a in range(0,len(l)+1,t)]for l in m[-1])for a in b)])if m else(),o("\x1b[?25h"),__import__("sys").stdout.flush(),(r:=lambda a,u,pt:(l:=__import__("sys").stdin.read(1),((u:=u[:-1],o("\b \b")if pt%(t-1)!=0 else o(f"\x1b[F\x1b[{t-2}G\b \b"),__import__("sys").stdout.flush(),pt:=pt-1)if len(u)>0 else())if l in"\x7f\x08"else(u:=u+l,o(" \n")if pt%(t-1)==0 else(),((a:=l)if l=="\x1b"else(a:=a+l)if a else()),[(o(a),o(c+"\b"),__import__("sys").stdout.flush(),w(interval/1000))for c in p[:(p.index(l)+1 if l in p else 0 if l in"\0 \b\n"or a else len(p))]],o(l if a==""else""if a=="\x1b["or a[-1]<"@"or a[-1]>"~"else(a+" \b",a:="")[0]),__import__("sys").stdout.flush(),pt:=pt+1),r(a,u,pt)if l!="\n"else u)[-1])("","",(len(m[-1])+(b if len(m)==1 else 0))%(t-1))[:-1],(k.SetConsoleMode(k.GetStdHandle(-10),d),k.SetConsoleMode(k.GetStdHandle(-11),d))if __import__("sys").platform=="win32"else __import__("termios").tcsetattr(s,__import__("termios").TCSANOW,ta))[-2]),
     f.__setattr__("__doc__","WARNING: ANSI ESCAPE CODE IS BROKEN HERE,DO NOT USE IT HERE\n*Made by Taokyle*\n\nRead a string from standard input.  The trailing newline is stripped.\nThis is a fancy version of input based on the default input function, it can directly replace the input function.\nHowever, please be noted that it takes a long time to print, even if interval is set to 0 the speed is still slower than the original print/input function (due to the animations).\nYet you can set interval to 0, sacrifising the visibility of the animation in exchange of print speed.\nThe following are detailed (not really) description for each arguments.\n  prompt\n    prompt to print out before receiving input, no trailing newline will be added\n  interval\n    time between each change on console during the print, default 5ms."))[0])
