%{
extern int yylex(void);
#include <stdio.h>
#include <stdlib.h>

int yyerror(char *s);

#define YYDEBUG 1
%}

%token INT;
%token STR;
%token CHAR;
%token READ;
%token CONDITION;
%token NEXT;
%token WRITE;
%token WOOPA;
%token FOOPA;
%token PLUS;
%token MINUS;
%token TIMES;
%token DIV;
%token LESS;
%token LESSEQ;
%token EQ;
%token NEQ;
%token BIGGEREQ;
%token EQQ;
%token BIGGER;
%token AND;
%token OR;
%token MOD;

%token CURLYOPEN;
%token CURLYCLOSE;
%token SEMICOLON;
%token OPEN;
%token CLOSE;
%token BRACKETOPEN;
%token BRACKETCLOSE;

%token IDENTIFIER;
%token INTCONSTANT;
%token STRINGCONSTANT;

%start Program

%%
Program : START CompoundStatement END				{ printf("Program -> @ CompoundStatement @\n"); }

CompoundStatement : Statement CompoundStatement    { printf("CompoundStatement -> Statement ; CompoundStatement\n"); }
                  | Statement                      { printf("CompoundStatement -> Statement ;\n"); }
                  ;
Statement : DeclarationStatement    { printf("Statement -> DeclarationStatement\n"); }
          | AssignmentStatement     { printf("Statement -> AssignmentStatement\n"); }
          | IfStatement             { printf("Statement -> IfStatement\n"); }
          | WhileStatement          { printf("Statement -> WhileStatement\n"); }
          | ForStatement            { printf("Statement -> ForStatement\n"); }
          | PrintStatement          { printf("Statement -> PrintStatement\n"); }
          | ReadStatement           { printf("Statement -> ReadStatement\n"); }
          ;
DeclarationStatement : Type IDENTIFIER     { printf("DeclarationStatement -> Type IDENTIFIER , DeclarationStatement\n"); }
                     | Type IDENTIFIER     { printf("DeclarationStatement -> Type IDENTIFIER\n"); }
                     ;
Type : INT    { printf("Type -> integer\n"); }
     | STR    { printf("Type -> string\n"); }
     | CHAR   { printf("Type -> char\n"); }
     ;
AssignmentStatement : Type IDENTIFIER <- Expression        { printf("AssignmentStatement -> Type IDENTIFIER = Expression\n"); }
                    | Type IDENTIFIER <- STRINGCONSTANT    { printf("AssignmentStatement -> Type IDENTIFIER = STRINGCONSTANT\n"); }
                    ;
Expression : Expression PLUS Term     { printf("Expression -> Expression ++ Term\n"); }
           | Expression MINUS Term    { printf("Expression -> Expression -- Term\n"); }
           | Term                     { printf("Expression -> Term\n"); }
           ;
		   
Term : Term TIMES Factor    { printf("Term -> Term ** Factor\n"); }
     | Term DIV Factor      { printf("Term -> Term // Factor\n"); }
     | Term MOD Factor      { printf("Term -> Term %% Factor\n"); }
     | Factor               { printf("Term -> Factor\n"); }
     ;
Factor : OPEN Expression CLOSE    { printf("Factor -> << Expression >>\n"); }
       | IDENTIFIER               { printf("Factor -> IDENTIFIER\n"); }
       | INTCONSTANT              { printf("Factor -> INTCONSTANT\n"); }
       | MINUS IDENTIFIER         { printf("Factor -> - IDENTIFIER\n"); }
       ;
IfStatement : IF OPEN Condition CLOSE BRACKETOPEN CompoundStatement BRACKETCLOSE                                                                                                                         { printf("IfStatement -> if << Expression >> [ CompoundStatement ]\n"); }
            | IF OPEN Condition CLOSE BRACKETOPEN CompoundStatement BRACKETCLOSE NEXT BRACKETOPEN CompoundStatement BRACKETCLOSE                                                                         { printf("IfStatement -> if << Expression >> [ CompoundStatement ] else { CompoundStatement }\n"); }
            ;
WhileStatement : WOOPA OPEN Condition CLOSE BRACKETOPEN CompoundStatement BRACKETCLOSE    { printf("WhileStatement -> woopa << Expression >> [ CompoundStatement ]\n"); }
               ;
ForStatement : FOOPA OPEN AssignmentStatement SEMICOLON Condition SEMICOLON AssignmentStatement CLOSE BRACKETOPEN CompoundStatement BRACKETCLOSE    { printf("ForStatement -> for << AssignmentStatement | Condition | AssignmentStatement >> [ CompoundStatement ]\n"); }
             ;
PrintStatement : WRITE OPEN Expression CLOSE        { printf("PrintStatement -> write << Expression >>\n"); }
               | WRITE OPEN STRINGCONSTANT CLOSE    { printf("PrintStatement -> write << STRINGCONSTANT >>\n"); }
               ;
ReadStatement : READ OPEN IDENTIFIER CLOSE    { printf("ReadStatement -> read << IDENTIFIER >>\n"); }
              ;
Condition : Expression Relation Expression AND Condition    { printf("Condition -> Expression Relation Expression AND Condition\n"); }
          | Expression Relation Expression OR Condition     { printf("Condition -> Expression Relation Expression OR Condition\n"); }
          | Expression Relation Expression                  { printf("Condition -> Expression Relation Expression\n"); }
          ;
Relation : LESS        { printf("Relation -> <)\n"); }
         | LESSEQ      { printf("Relation -> <)=\n"); }
         | EQQ         { printf("Relation -> =\n"); }
         | NEQ         { printf("Relation -> !=\n"); }
         | BIGGEREQ    { printf("Relation -> =(>\n"); }
         | BIGGER      { printf("Relation -> (>\n"); }
	     | AND         { printf("Relation -> &\n"); }
	     | OR          { printf("Relation -> #\n"); }
         ;
%%
int yyerror(char *s) {
    printf("Error: %s", s);
}

extern FILE *yyin;

int main(int argc, char** argv) {
    if (argc > 1) 
        yyin = fopen(argv[1], "r");
    if (!yyparse()) 
        fprintf(stderr, "\tOK\n");
}