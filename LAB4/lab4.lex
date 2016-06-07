%namespace lab4
%option noparser, caseInsensitive


alpha [a-zA-Z]
digits [0-9]+
error [^a-zA-Z0-9\+\-\*\/=,\ \r\n]
operators [\+\-\*\/]
%%

begin |
end |
var              Console.WriteLine("keyword:     " + yytext + " ("+ yyline + ":" + yycol +")");
{alpha}+         Console.WriteLine("identifier:  " + yytext + " ("+ yyline + ":" + yycol +")");
=                Console.WriteLine("assignment:  " + yytext + " ("+ yyline + ":" + yycol +")");
{operators}      Console.WriteLine("operator:    " + yytext + " ("+ yyline + ":" + yycol +")");
{digits}         Console.WriteLine("constant:    " + yytext + " ("+ yyline + ":" + yycol +")");
{error}+         Console.WriteLine("error:       " + yytext + " ("+ yyline + ":" + yycol +")");

%%

    public static void Main(string[] argp) {
        DateTime start = DateTime.Now;
        int count = 0;
        if (argp.Length == 0)  
            Console.WriteLine("Usage: WordCount filename(s), (wildcards ok)");
        DirectoryInfo dirInfo = new DirectoryInfo(".");
        for (int i = 0; i < argp.Length; i++) {
            string name = argp[i];
            FileInfo[] fInfo = dirInfo.GetFiles(name);
            foreach (FileInfo info in fInfo)
            {
	        try {
		    int tok;
 		    FileStream file = new FileStream(info.Name, FileMode.Open); 
		    Scanner scnr = new Scanner(file);
		    Console.WriteLine("File: " + info.Name);
		    do {
  		        tok = scnr.yylex();
		    } while (tok > (int)Tokens.EOF);
		    count++;
		} catch (IOException) {
		    Console.WriteLine("File " + name + " not found");
		}
            }
        }
        TimeSpan span = DateTime.Now - start;
        Console.WriteLine("Elapsed time: {0,4:D} msec", (int)span.TotalMilliseconds);
    }

