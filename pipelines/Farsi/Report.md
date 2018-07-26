# Farsi

## Verbs

DONE

1. Link arguments: subject - second arg, direct object - third arg,
   indirect object - fourth arg

2. Argument control: first arguments of both verbs are the same

```
% John tried to go.
john-nn(e1,x1) & try-vb(e2,x1,e3,u1) & go-vb(e3,x1,u2,u3)
```

3. Other args


4. Add tense information if available from the parser: present, past, future


## Nouns

1. Noun compounds: if there are noun compounds in the language you are
   working with, use the predicate "nn" to express it.

```
% book store
book-nn(e1,x1) & store-nn(e2,x2) & nn(e1,x1,x2)
```

2. Genitive: always use the predicate "of-in" for expressing genitives

```
% John's book
john-nn(e1,x1) & book-nn(e2,x2) & of-in(e3,x2,x1)
```

3. Add number information if available from the parser (if plural)

```
% books
book-nn(e1,x1) & typelt(e2,x1,s)
```

4. If there is other information available from the parser (e.g. type of
   the named entity), please add it.

```
% John went to London.
john-nn(e1,x1) & per(e2,x1) & go-vb(e3,x1,u1,u2) & to-in(e4,e3,x2) & london-nn(e5,x2) & loc(e6,x2)
```


## Adjectives

DONE

Adjectives share the second argument with the noun they are modifying


## Adverbs

Second args of adverbs are verbs they are modifying

```
% John runs fast.
run-vb(e1,x1,u1,u2) & fast-rb(e2,e1)
```


## Prepositions

1. Verb+noun

```
% John goes to school.
go-vb(e1,x1,u1,u2) & to-in(e2,e1,x2) & school-nn(e3,x2)
```

2. Noun+noun

```
% book for Mary
book-nn(e1,x1) & for-in(e2,x1,x2) & mary-nn(e2,x2)
```

3. Second arg is a prep

```
% John goes out of the store.
go-vb(e1,x1,u1,u2) & out-in(e2,e1,u3) & of-in(e3,e2,x2) & store-nn(e4,x2)
```

4. Verb+verb

```
% Thank you for not smoking.
thank-vb(e1,u1,x1,u2) & person(e1,x1) & for-in(e3,e1,e4) & not(e4,e5) & smoke-vb(e5,u3,u4,u5)
```


## Pronouns

- NOT AVAILABLE: "he" -> male(e1,x1)
- NOT AVAILABLE: "she"->female(e1,x1)

```
"it"->neuter(e1,x1)
"I"->person(e1,x1)
"we"->person(e1,x1) & typelt(e2,x1,s)
"you"->person(e1,x1)
"they"->thing(e1,x1) & typelt(e2,x1,s)
```

## Numerals

Use card/3 predicate to express numerals (third argument is a number)

```
% John has two books.
have-vb(e1,x1,x2,u1) & book-nn(e2,x2) & card(e3,x2,2)
```

## Connectors

1. and, or

```
% John sits and reads.
john-nn(e1,x1) & sit-vb(e2,x1,u1,u2) & read-vb(e3,x1,u1,u2)
```

```
% John sits or runs.
john-nn(e1,x1) & sit-vb(e2,x1,u1,u2) & run-vb(e3,x1,u1,u2) & or(e4,e2,e3)
```

DONE:
```
% John reads a book and a newspaper
john-nn(e1,x1) & read-vb(e2,x1,x3,u2) & book-nn(e3,x2) & read-vb(e4,x1,x4,u2) & newspaper-nn(e5,x4)
```

```
% John reads a book or a newspaper
john-nn(e1,x1) & read-vb(e2,x1,x3,u2) & book-nn(e3,x2) & read-vb(e4,x1,x4,u2) & newspaper-nn(e5,x4) & or(e6,e2,e4)
```

2. if

```
% If John has time then he reads.
read-vb(e1,x1,u1,u2) & have-vb(e2,x1,u3,u4) & imp(e3,e1,e2)
```

3. because, while, when,...

```
% John reads , because he has time .
read-vb(e1,x1,u1,u2) & have-vb(e2,x1,u3,u4) & because(e3,e1,e2)
```

4. not

Represent all negation using the predicate not/2

```
% John does not read
read-vb(e1,x1,u1,u2) & not(e2,e1)
```

```
% not John
not(e1,x1) & john-nn(e2,x1)
```

