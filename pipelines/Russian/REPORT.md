# Russian

## Verbs

1. ***Implemented***.

   There is an issue with recognising indirect objects the pipeline cannot
   retrieve information about its case (it should be *accusative* or
   *genitive*) from Malt. (This usually happens with foreign words such as
   *"Мери"*):

   *"Джон дает Мери книгу."*

   ```prolog
   джон-nn(e1,x1) & давать-vb(e2,x1,x2,u1) & мери-nn(e3,x3) & книга-nn(e4,x2)
   ```

   Malt output:

   ```
   3	Мери	мери	N	N	Npfsny	2	1-компл	_	_
   ```

   Here the word *"Мери"* has a nominative case (Npfs ***n*** y).

2. ***Implemented***.
   No issues found.

3. ***Implemented***.
   Implemented handling `instr` predicate rule and handling genitives. No
   issues found.

4. ***Implemented***.
   (pipeline) Requires option `--vbtense 1` to be specified. No issues found.

5. Recognises copulas in the following cases:

   - If `NN+NN`, no copula verb and cases of the both nouns are the same then
     produces predicate `equal`.

   - If `NN+[NN | PREP | ADJ]` and copula verb presents then removes copula
     verb and produces predicate `equal`, `compl` or makes the second
     argument same for both predicates (depending on dependency relation type
     and tree structure).

   **NOTE:** pipeline doesn't remove copula verb (and any other predicate) in
   cases when at least one another predicate is pointing on it. For
   example:

   *"Все было очень обыкновенно."*

   ```prolog
   быть-vb(e1,u1,u2,u3) & очень-rb(e2,e3) & обыкновенно-rb(e3,e1)
   ```

- a. ***Implemented***.
- b. ***Implemented***.
- c. ***Implemented***.
- d. Not implemented.

6. ***Implemented***.
   Finds passive voices constructed with the verb *был*. No issues found.

7. ***Implemented***.
   No issues found.


## Nouns

1. Not implemented.

2. ***Implemented***.
   (pipeline) Adds `of-in` predicate when noun has genetive case. Doesn't
   work when noun is foreign word (e.g. words *"Джон"*, *"Мери"* etc.) and
   parser is not able to classify case correctly.

3. ***Implemented***.

- Treats numerals. If option `--nnnumber 1` is specified then produces
  predicate `typelt` if noun has plural form. Produces predicate `card` if
  numerical information is presented, maps numericals from `ноль`/
  `нулевой` to `десять` / `десятый` into numerical form, otherwise leaves
  them as is.

  Known issues:

  Depending on the parser's output can sometimes misrecognize numericals:

  ```
  % Одна на свете , как она управится со столькими миллионами ?
  миллион-nn(e6,x5) & card(e7,x5,столькими) & typelt(e8,x5,s1)
  ```

  ```
  9	столькими	столько	M	M	Mc--i	10	количест	_	_
  10	миллионами	миллион	N	N	Ncmpin	8	предл	_	_
  ```

- Handles genitive cases to produce predicate `of-in` if such feature is
  presented in the parser's output.

4. Not implemented.
   There is no such information from the current parser.

5. ***Implemented***.
   No issues found.


## Adjectives

1. ***Implemented***.
   No issues found.


## Adverbs

1. ***Implemented***.


## Prepositions

1. ***Implemented***.
   No issues found.

2. ***Implemented***.
   No issues found.

3. Not implemented.
   There are no such constructions in the Russian language.

4. Not implemented.
   There are no such constructions in the Russian language.

5. ***Implemented***.
   No issues found.


## Pronouns

1. ***Implemented***.
   Maps pronuouns *"он"*, *"она"*, *"оно"*, *"я"*, *"мы"*, *"ты"*, *"вы"*,
   *"они"*, *"это"*, *"эти"* into according predicates such as `male`,
   `female`, `person` etc., then handles them as nouns. Treats any other
   pronoun, such as *"который"*, *"там"*, *"тут"*, etc. Or does not treats
   them if any other predicate shares at least one argument with them, for
   example:

   ```
   % Я его оставил под открытым небом на палубе , возле скамейки , на которой рассчитывал сидеть во время плавания , присматривая за сохранностью багажа .

   person(e1,x1) & male(e2,x2) & оставить-vb(e3,x1,x2,u1) &
   под-in(e4,e3,x3) & открытый-adj(e5,x3) &
   небо-nn(e6,x3) & на-in(e7,e3,x4) &
   палуба-nn(e8,x4) & возле-in(e9,e3,x5) &
   скамейка-nn(e10,x5) & на-in(e11,e13,x6) &
   который-pr(e12,x6) & рассчитывать-vb(e13,x1,e14,u2) &
   сидеть-vb(e14,x1,e18,u3) & во-in(e15,e14,x7) &
   время-nn(e16,x7) & плавание-nn(e17,x8) &
   присматривать-vb(e18,x1,u4,u5) & за-in(e19,e18,x9) &
   сохранность-nn(e20,x9) & багаж-nn(e21,x10) &
   of-in(e22,x7,x8) & of-in(e23,x9,x10)
   ```

   It's impossible to determine that the word *"которой"* is pointing to
   *"скамейка"* due to incorrect parser's output, so the pronoun has not
   been treated.

2. Does not handle reflexives. There is no such information from the
   current parser.

3. Not implemented.


## Numerals

1. **Implemented** in NOUNS#2 rule (for the case when numerals have digital
   representation).


## Connectors

1. **Implemented**.
2. **Implemented**.
3. Not implemented.
4. **Implemented**.

## Negation

1. **Implemented**.


## Subordinate Clauses

1. **Implemented**
   Finding relative clauses and WH-nominals for persons, non-animate
   objects, locations, reasons, times and manner.

2. Not implemented handling constructions such as: because, while, when,
   as, after, since.


## Questions

1. Implemented handling constructions such as: что (what/thing), кто
   (whom/person), когда (when/time), зачем (why/reason), как (how/manner),
   where (где/loc).


## Foreign Words

The pipeline usually mispredicts the POS tag of non-Russian words, which
may cause different mistakes in the output:

1.

```prolog
% ... телеканал Russia Today выложил впечатляющее ...
телеканал-nn(e2,x2) & today-nn(e3,x3) & выложить-vb(e4,x3,u1,x4) & впечатляющий-adj(e5,x5) …
```

Here the word "Russia" was treated because the POS tag was mispredicted:


```
1	Давеча	давеча	R	R	R	0	ROOT	_	_
2	телеканал	телеканал	N	N	Ncmsnn	0	ROOT	_	_
3	Russia	russia	-	-	-	2	аппоз	_	_
4	Today	today	N	N	Ncmsnn	5	предик	_	_
5	выложил	выложить	V	V	Vmis-sma-p	2	релят	_	_
6	впечатляющее	впечатляющий	A	A	Afpnsaf	7	опред	_	_
...
```

2.

```prolog
% ... рассказал анонимный сотрудник ГИБДД из Ставрополья в ролике на YouTube .
анонимный-adj(e7,x4) & сотрудник-nn(e8,x4) & гибдд-nn(e9,x5) & из-in(e10,x4,x6) & ставрополье-nn(e11,x6) & в-in(e12,x6,x7) & ролик-nn(e13,x7) & на-in(e14,e6,x8) & card(e15,u4,youtube) & of-in(e17,x4,x5)
```

Again, the POS tag for the "Youtube" is incorrect:

```
...
12	из	из	S	S	Sp-g	10	атриб	_	_
13	Ставрополья	ставрополье	N	N	Ncnsgn	12	предл	_	_
14	в	в	S	S	Sp-l	13	атриб	_	_
15	ролике	ролик	N	N	Ncmsln	14	предл	_	_
16	на	на	S	S	Sp-l	8	обст	_	_
17	YouTube	youtube	M	M	Mc	16	предл	_	_
18	.	.	S	S	SENT	17	PUNC	_	_
...
```
