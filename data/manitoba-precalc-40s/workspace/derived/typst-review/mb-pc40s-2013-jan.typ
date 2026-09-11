#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2013-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Gina correctly started to answer the following question. Complete her solution.

Question: Solve the following equation for all real values of $theta $.

Express your answer in radians correct to 3 decimal places.

$  3  sin  ^(2 ) theta - 14  sin  theta - 5 = 0   $

Gina's solution: $3  sin  ^(2 ) theta - 14  sin  theta - 5 = 0 $

$  \(3  sin  theta + 1 \)\(sin  theta - 5 \)= 0   $

== Solution

Method 1

$  mat(delim: #none,  mat(delim: #none,  3  sin  ^(2 ) theta - 14  sin  theta - 5 = 0  "" , "" ; \(3  sin  theta + 1 \)\(sin  theta - 5 \)= 0  "" , "" ; sin  theta = - frac(1 ,3 ) "" , sin  theta = 5  "" ; " no solution " "" , "" ; theta _(r )= 0.339837  "" , 1  \/ 2  " mark for " sin  theta = 5  "" ; theta = 3.481429 \,5.943  space.nobreak  348  "" , 1  " mark for no solution " "" ; "" , "" ; theta = 3.481 + 2  k  pi \, k  in  upright(I ) "" , 1  " mark for each value of " theta \) "" ; theta = 5.943 + 2  k  pi \, k  in  upright(I ) "" , bold(3 ) " marks " ) )  $

Note\(s\):

- give maximum of 2 marks for solution in degrees: $theta = 199.471 ^(degree )+ 360 ^(degree ) k \, k  in  upright(I )$

$  theta = 340.529 ^(degree )+ 360 ^(degree ) k \, k  in  upright(I )  $

#pagebreak()

= Question 2

Find and simplify the 6th term in the binomial expansion of $lr(\( 3  x ^(4 )- frac(1 ,x ^(3 ))\) )^(9 )$.

== Solution

$   t _(6 ) & =  "" _(9 ) C _(5 )lr(\( 3  x ^(4 )\) )^(4 )lr(\( - frac(1 ,x ^(3 ))\) )^(5 ) \  & = \(126 \)lr(\( 81  x ^(16 )\) )lr(\( - frac(1 ,x ^(15 ))\) ) \  & = - 10206  x    $

2 marks \(1 mark for $ "" _(9 ) C _(5 )\, frac(1 ,2 )$ mark for each consistent factor\)

1 mark for simplification \( $frac(1 ,2 )$ mark for evaluating coefficient\, $frac(1 ,2 )$ mark

for simplifying variable\)

3 marks

#pagebreak()

= Question 3

The number of times a website is visited can be modeled by the function:

$  A = 800 \(e \)^(r  t )  $

where $A = $ the total number of visitors at time $t $

$  t = " the time in days "\(t  >=  0 \)  $

$r = $ the rate of growth

After 5 days\, 40000 people have visited the site.

Determine the number of visitors expected after 9 days.

Express your answer as a whole number.

== Solution

Method 1

$   40000  & = 800  e ^(r  5 ) & & \  frac(40000 ,800 ) & = e ^(5  r ) & & 1  \/ 2  " mark for substitution " \  ln  50  & = ln  e ^(5  r ) & & 1  \/ 2  " mark for applying " op("logs") \  ln  50  & = 5  r  & & 1  " mark for " log  " theorem " \  frac(ln  50 ,5 ) & = r  & & \  r  & = 0.782404601  & &   $

$   & A = 800  e ^(\(0.782404601 \)\(9 \)) \  & A = 914610.103  \  & A = 914610    $

$  frac(1 ,2 ) " mark for substitution "  $

$frac(1 ,2 )$ mark for calculations with base $e $

3 marks

#pagebreak()

= Question 4

Solve algebraically:

$  10 ^(3  x )= 7 ^(x + 5 )  $

Express your answer correct to 3 decimal places.

== Solution

Method 1

$   10 ^(3  x ) & = 7 ^(x + 5 ) \  log  10 ^(3  x ) & = log  7 ^(x + 5 ) \  3  x \(log  10 \) & = \(x + 5 \) log  7  \  3  x  log  10  & = x  log  7 + 5  log  7  \  3  x  log  10 - x  log  7  & = 5  log  7  \  x  & = frac(5  log  7 ,3  log  10 - log  7 ) \  x  & = 1.960873  \  x  & = 1.961    $

$frac(1 ,2 )$ mark for applying logs

1 mark for power rule

$frac(1 ,2 )$ mark for collecting terms with $x $

$  frac(1 ,2 ) " mark for solving for " x   $

$frac(1 ,2 )$ mark for evaluating quotient of

logarithms

Method 2

$   10 ^(3  x ) & = 7 ^(x + 5 ) \  log  10 ^(3  x ) & = log  7 ^(x + 5 ) \  3  x \(log  10 \) & = \(x + 5 \) log  7  \  3  x  & = x  log  7 + 5  log  7  \  3  x - x  log  7  & = 5  log  7  \  x  & = frac(5  log  7 ,3 - log  7 ) \  x  & = 1.960873  \  x  & = 1.961    $

3 marks

#pagebreak()

= Question 5

A word contains two Ms\, two Es\, two Ns\, and no other repeated letters.

Suppose one of the Ns is replaced by an M.

Will this replacement result in greater or fewer permutations?

Justify your reasoning.

== Solution

Method 1

$2  upright(M s )\, 2  upright(E s )\, 2  upright(N s ):  frac(\(" total number of letters "\)! ,2 ! 2 ! 2 ! )$

$frac(\(" total number of letters "\)! ,8 )$

$3  upright(M s )\, 2  upright(E s )\, 1  upright(space.nobreak N ):  frac(\(" total number of letters "\)! ,3 ! 2 ! 1 ! )$

$frac(\(" total number of letters "\)! ,12 )$

1 mark for dividing the total number of letters by

2!2!2!

1 mark for dividing the total number of letters by

3!2!1!

2 marks

If one of the Ns is changed to an M\, there would be fewer permutations.

Method 2

If one of the Ns is changed to an M\, there would be fewer permutations because you would be dividing

the total number of letters by a larger number.

2 marks for justification

2 marks

#pagebreak()

= Question 6

There is a group of 16 boys and 12 girls. How many ways can a committee of 3 people be

formed if there must be at least 2 girls on the committee?

Express your answer as a whole number.

Note: A calculator is not required for the remaining test questions.

== Solution

Method 1

Case 1: 2 girls\, 1 boy

$   "" _(12 ) C _(2 ) dot.c  "" _(16 ) C _(1 )= 1056   $

Case 2: 3 girls

$   "" _(12 ) C _(3 )= 220   $

$  1056 + 220 = 1276   $

1 mark for case 1 \( $frac(1 ,2 )$ mark for each factor

shown in a product\)

1 mark for case 2

1 mark for addition of cases

3 marks

Method 2

Case 1: 2 boys\, 1 girl

$   "" _(16 ) C _(2 ) dot.c  "" _(12 ) C _(1 )= 1440   $

Case 2: 3 boys

$   "" _(16 ) C _(3 )= 560   $

All possibilities

$   "" _(28 ) C _(3 )= 3276   $

$3276 - 1440 - 560 = 1276 $

1 mark for case 1 \( $frac(1 ,2 )$ mark for each factor

shown in a product\)

1 mark for case 2

$frac(1 ,2 )$ mark for all possible cases

$frac(1 ,2 )$ mark for subtraction from total

3 marks

#pagebreak()

= Question 7

A student is using the formula $s = theta  r $ to find an arc length of a circle. Given a central angle

measure of $35 ^(degree )$ and a radius of 6 cm \, the student's solution is as follows:

$   & s = \(35 \)\(6 \) \  & s = 210  upright(space.nobreak c m )   $

Explain why this solution is incorrect.

Write the correct solution.

== Solution

When using the formula $s = theta  r $\, the angle must be in radians. $frac(1 ,2 )$ mark for explanation

$  35 ^(degree )lr(\( frac(pi ,180 ^(degree ))\) )= frac(35  pi ,180 ) quad  " or " quad  frac(7  pi ,36 )  $

1 mark for conversion to radians

$   therefore  s  & = theta  r  \  & = frac(7  pi ,36 )\(6 \) \  & = frac(42  pi ,36 ) upright(space.nobreak c m ) quad  " or " quad  frac(7  pi ,6 ) upright(space.nobreak c m ) quad  " or " quad  3.665  upright(space.nobreak c m )   $

$frac(1 ,2 )$ mark for simplification

2 marks

Note\(s\):

- award 1 mark for correct final answer with no work

#pagebreak()

= Question 8

Given the graph of $f \(x \)$ below\, explain how you would sketch the graph of $y = | f \(x \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/f21ede5a-1ce9-4ec7-b04c-715b9afdea72-07_637_641_1714_279.jpg", width: 30.2%)

== Solution

The negative $y $ values are reflected over the $x $-axis.

1 mark for explanation

1 mark

#pagebreak()

= Question 9

Claire correctly solves the following equation:

$  log  _(2 )\(6 - x \)+ log  _(2 )\(3 - x \)= 2   $

She finds two possible values of $x :  x = 2 $ and $x = 7 $.

Identify which one of these values is unacceptable and explain why.

== Solution

If $x $ is greater than 3 \, you have a negative argument $therefore  x = 2 $ but $x  !=  7 $.

or

The domain is restricted to values of $x < 3  therefore  x = 2 $.

1 mark for explanation

1 mark

#pagebreak()

= Question 10

Given the graph of the function $f \(x \)$ below\, state the domain of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/f21ede5a-1ce9-4ec7-b04c-715b9afdea72-08_826_858_1673_296.jpg", width: 40.4%)

== Solution

The domain is $\{ x  in  bb(R ) divides  x  <= - 1 $ or $x  >=  3 \} $.

or

The domain is $\(- oo \,- 1 \] union \[3 \, oo \)$.

1 mark for domain

1 mark

#pagebreak()

= Question 11

A school offers 4 different Science courses\, 3 different Mathematics courses\, and 2 different

English courses.

Julie must select 1 Science course\, 1 Mathematics course\, and 1 English course. She thinks this

creates 9 options for her timetable.

Show why Julie is incorrect.

== Solution

Julie should have multiplied the number of options.

or

$4  times  3  times  2 = 24 $ different options

1 mark for justification

1 mark

#pagebreak()

= Question 12

Explain how Pascal's triangle can be used to determine the coefficients in the binomial

expansion of $\(x + y \)^(n )$.

== Solution

The $\(n + 1 \)^("st ")$ row of Pascal's triangle corresponds to the coefficients

of the terms in the expansion of the binomial $\(x + y \)^(n )$.

1 mark for explanation

#pagebreak()

= Question 13

Prove the identity below for all permissible values of $x $ :

$  frac(1 + cos  2  x ,sin  2  x )= cot  x   $

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[], [],
table.hline(stroke: .5pt),
[],
);

== Solution

Method 1

$   " LHS " & = frac(1 + 2  cos  ^(2 ) x - 1 ,2  sin  x  cos  x ) & & mat(delim: #none,  1  " mark for identity " "" ; 1  \/ 2  " mark for identity " ) \  & = frac(2  cos  ^(2 ) x ,2  sin  x  cos  x ) & & \  & = frac(cos  x ,sin  x ) & & 1  " mark for simplification " \  & = cot  x  & & 1  \/ 2  " mark for identity " \  & = " RHS " & & bold(3 ) " marks "   $

Method 2

$   " LHS " & = frac(1 + 1 - 2  sin  ^(2 ) x ,2  sin  x  cos  x ) & & frac(1 ,2 ) " mark for identity " \  & = frac(2 - 2  sin  ^(2 ) x ,2  sin  x  cos  x ) & & \  & = frac(1 - sin  ^(2 ) x ,sin  x  cos  x ) & & 1  \/ 2  " mark for identity " \  & = frac(cos  ^(2 ) x ,sin  x  cos  x ) & & 1  \/ 2  " mark for identity " \  & = frac(cos  x ,sin  x ) & & 1  \/ 2  " mark for simplification " \  & = cot  x  & & 1  \/ 2  " mark for identity " \  & = " RHS " & & bold(3 ) " marks "   $

Method 3

$   " LHS " & = frac(1 + cos  ^(2 ) x - sin  ^(2 ) x ,2  sin  x  cos  x ) \  & = frac(2  cos  ^(2 ) x ,2  sin  x  cos  x ) \  & = frac(cos  x ,sin  x ) \  & = cot  x  \  & = " RHS "   $

$frac(1 ,2 )$ mark for identity

$frac(1 ,2 )$ mark for identity

$frac(1 ,2 )$ mark for identity $lr(\( 1 - sin  ^(2 ) x = cos  ^(2 ) x \) )$

1 mark for simplification

$frac(1 ,2 )$ mark for identity

3 marks

#pagebreak()

= Question 14

Your classmate\, Leo\, was absent for one of his math lessons.

Explain to Leo how to determine the cosecant ratio for an angle in standard position given that

$upright(P )\(- 3 \,- 4 \)$ is a point on the terminal arm of the angle.

== Solution

Method 1

- Locate the point \(-3\, -4\) on the coordinate plane.

- Draw a right-angle triangle by connecting the point \(-3\, -4\) to

the $x $-axis and to the origin.

- The angle created with the $x $-axis and the line connecting

the point with the origin \(the terminal arm\) is $theta $.

- Determine the length of the terminal arm by using the Pythagorean Theorem.

- Once you have the lengths of all three sides of the triangle\, find $sin  theta $.

- Invert the $sin  theta $ ratio to find $csc  theta $.

Method 2

- Determine the value of $r $ using the Pythagorean Theorem.

- Determine the value of $sin  theta lr(\( sin  theta = frac(y ,r )\) )$.

- Identify the correct quadrant.

- Invert the $sin  theta $ ratio to find $csc  theta $.

½ mark

½ mark

½ mark

½ mark

2 marks

Note\(s\):

- award a maximum of 1 mark for correct work shown without an explanation in words

#pagebreak()

= Question 15

Given the following graphs:

$  f \(x \)  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/f21ede5a-1ce9-4ec7-b04c-715b9afdea72-12_682_693_528_300.jpg", width: 32.6%)

$  g \(x \)  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/f21ede5a-1ce9-4ec7-b04c-715b9afdea72-12_682_687_528_1168.jpg", width: 32.3%)

Sketch the graph of $f \(x \)+ g \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/f21ede5a-1ce9-4ec7-b04c-715b9afdea72-12_691_693_1473_689.jpg", width: 32.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-18_892_904_1435_254.jpg", width: 42.5%)

2 marks \( $frac(1 ,2 )$ mark for each point where

the graph changes direction\)

$\[\(- 2 \,- 2 \) \;\(0 \,4 \) \;\(1 \,4 \) \;\(4 \,1 \)\]$

2 marks

Note\(s\):

- deduct a maximum of 1 mark for incorrect domain

#pagebreak()

= Question 16

If $\(2 \,3 \)$ is a point on the graph of $y = f \(x \)$\, what point must be on the graph of $y = 3  f lr(\( frac(1 ,4 ) x \) )$ ?

*A.*

$lr(\( frac(1 ,2 )\, 1 \) )$

*B.*

$lr(\( frac(1 ,2 )\, 9 \) )$

*C.*

$\(8 \,1 \)$

*D.*

$\(8 \,9 \)$

== Solution

Correct answer: D

$\(8 \,9 \)$

#pagebreak()

= Question 17

Consider the arc drawn on each circle. Which arc measure is closest to 3 radians?

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-01_197_212_1310_298.jpg", width: 10.0%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-01_130_132_1344_760.jpg", width: 6.2%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-01_229_238_1295_1196.jpg", width: 11.2%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-01_181_192_1319_1611.jpg", width: 9.0%)

== Solution

Correct answer: D

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-01_181_192_1319_1611.jpg", width: 9.0%)

#pagebreak()

= Question 18

If $log  _(2 ) x = 4 $\, then $log  _(2 )\(2  x \)$ is equal to:

*A.*

5

*B.*

8

*C.*

16

*D.*

32

== Solution

Correct answer: A

5

#pagebreak()

= Question 19

Simplify the following expression:

$  cos  ^(2 ) x lr(\( 1 + cot  ^(2 ) x \) )  $

*A.*

$sin  ^(2 ) x $

*B.*

$cos  ^(2 ) x $

*C.*

$cot  ^(2 ) x $

*D.*

$sec  ^(2 ) x $

== Solution

Correct answer: C

$cot  ^(2 ) x $

#pagebreak()

= Question 20

Identify the graph of the function $y = frac(x ,x )$.

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-02_528_514_1370_382.jpg", width: 24.2%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-02_525_523_1312_1228.jpg", width: 24.6%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-02_531_510_1987_382.jpg", width: 24.0%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-02_525_519_1972_1237.jpg", width: 24.4%)

== Solution

Correct answer: C

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-02_531_510_1987_382.jpg", width: 24.0%)

#pagebreak()

= Question 21

How many terms are in the expansion of $lr(\( 3  y ^(2 )- 4  z \) )^(7 )$ ?

*A.*

2

*B.*

6

*C.*

7

*D.*

8

== Solution

Correct answer: D

8

#pagebreak()

= Question 22

Determine one possible restriction for the domain of $y = \(x + 3 \)^(2 )- 4 $ so that its inverse is a

function.

*A.*

$x  <= - 3 $

*B.*

$x  <=  0 $

*C.*

$x  <=  3 $

*D.*

$x  <=  4 $

== Solution

Correct answer: A

$x  <= - 3 $

#pagebreak()

= Question 23

Find the total possible number of arrangements for 7 adults and 3 children seated in a row if the

3 children must sit together.

*A.*

10 !

*B.*

$8 ! 3 ! $

*C.*

$7 ! 3 ! $

*D.*

7 !

== Solution

Correct answer: B

$8 ! 3 ! $

#pagebreak()

= Question 24

Identify the value of the $x $-intercept of the function $y = ln  \(x - 2 \)$.

*A.*

-1

*B.*

0

*C.*

2

*D.*

3

== Solution

Correct answer: D

3

#pagebreak()

= Question 25

Given $log  _(b ) a = 3 $\, give one example of possible values for $a $ and $b $ that make this equation true.

== Solution

Answers will vary but $b ^(3 )= a $.

Some possible solutions are: $a = 8  quad  b = 2 $

1 mark

or

$  a = 27  quad  b = 3   $

or

$  a = 64  quad  b = 4   $

#pagebreak()

= Question 26

The range of the graph of $y = f \(x \)$ is $\[- 3 \,2 \]$.

Explain why there is no effect on the range of the graph that is a result of the transformation

$y = f \(- x \)$.

== Solution

$y = f \(- x \)$ is a reflection over the $y $-axis.

The domain is affected\, but the range remains the same.

1 mark for explanation

#pagebreak()

= Question 27

Sketch the graph of $y = \(x + 1 \)\(x - 2 \)^(2 )\(x + 5 \)$.

Identify the $x $-intercepts and $y $-intercept.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-05_1123_1217_575_455.jpg", width: 57.3%)

$x $-intercepts:

$\_ \_ \_ \_ $

$y $-intercept:

$\_ \_ \_ \_ $

== Solution

$x $-intercepts: $- 5 \,- 1 $\, and 2

$y $-intercept: 20

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-23_986_1038_859_215.jpg", width: 48.8%)

1 mark for $x $-intercepts

1 mark for $y $-intercept

1 mark for multiplicity of a zero at $x = 2 $

3 marks

Note\(s\):

- if no graph is shown\, give $frac(1 ,2 )$ mark for $x $-intercepts $\(- 5 \,- 1 $\, and 2$\)$ and $frac(1 ,2 )$ mark for

$y $-intercept \(20\)

- relative maximum and minimum are not required

#pagebreak()

= Question 28

The graph of the function $y = sin  x $ has been transformed to create a new graph.

The range of this new graph is $\[- 4 \,4 \]$ and the zeros are $x = k  frac(pi ,2 )$\, where $k $ is an integer.

Write the equation that corresponds to this new graph.

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Amplitude = 4 ], [1 mark for correct amplitude ],
table.hline(stroke: .5pt),
[$   & " Period "= pi  \  & therefore  b = frac(2  pi ,pi )= 2  \  & y = 4  sin  \(2  x \) \  & " or " \  & y = - 4  sin  \(2  x \)   $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[$frac(1 ,2 )$ mark for correct period ],
[$frac(1 ,2 )$ mark for consistent value of $b $ ],
[2 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

Note\(s\):

- deduct $frac(1 ,2 )$ mark for a translation that results in an incorrect range and\/or zeros

#pagebreak()

= Question 29

Given the functions $f \(x \)= x ^(2 )- 1 $ and $g \(x \)= x + 1 $\, state the domain of $frac(g \(x \),f \(x \))$.

== Solution

Domain: $x  in  bb(R )$ where $x  !=  1 $ and $x  != - 1  quad  1 $ mark \( $frac(1 ,2 )$ mark for $x  !=  1 \, frac(1 ,2 )$ mark for $x  != - 1 $ \)

1 mark

#pagebreak()

= Question 30

a\) Sketch the graph of $y = 3 ^(x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-07_884_899_541_655.jpg", width: 42.3%)

b\) Explain how the graph of $y = 3 ^(x )$ can be used to sketch the graph of $y = log  _(3 ) x $.

== Solution

a\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-25_793_812_711_215.jpg", width: 38.2%)

$frac(1 ,2 )$ mark for increasing exponential function

$frac(1 ,2 )$ mark for $y $-intercept at $\(0 \,1 \)$

$frac(1 ,2 )$ mark for consistent point on exponential

function

$frac(1 ,2 )$ mark for asymptotic behaviour

2 marks

b\)

To graph $y = log  _(3 ) x $\, you can reflect the graph of $y = 3 ^(x )$ over the line $y = x $.

or

You can switch the $x $ and $y $ coordinates of $y = 3 ^(x )$ to get the graph of $y = log  _(3 ) x $.

1 mark for explanation

1 mark

Note\(s\):

- in \(b\)\, give $frac(1 ,2 )$ mark for having only stated they are inverse functions of each other

#pagebreak()

= Question 31

A box in the shape of a rectangular prism has side lengths $x \, x + 2 $ and $x + 10 $.

Write a function\, $V \(x \)$\, to express the volume of the box in terms of $x $.

Find all possible values of $x $\, given that the volume of the box is $96  upright(space.nobreak c m )^(3 )$.

State the dimensions of the box.

== Solution

$  mat(delim: #none,  V \(x \) "" , = \(x \)\(x + 2 \)\(x + 10 \) "" , "" ; 96  "" , = \(x \)\(x + 2 \)\(x + 10 \) "" , "" ; 96  "" , = x ^(3 )+ 12  x ^(2 )+ 20  x  "" , "" ; 0  "" , = x ^(3 )+ 12  x ^(2 )+ 20  x - 96  "" , 1  \/ 2  " mark for expressing volume in terms of " x  "" ; "" , "" , )  $

when $x = 2 $ :

$   0  & = \(2 \)^(3 )+ 12 \(2 \)^(2 )+ 20 \(2 \)- 96  \  0  & = 8 + 48 + 40 - 96  \  0  & = 0  \  & therefore  x = 2  " is a possible value. "   $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [1 ], [12 ], [20 ], [-96 ],
table.hline(stroke: .5pt),
[], [], [2 ], [28 ], [96 ],
table.hline(stroke: .5pt),
[], [1 ], [14 ], [48 ], [0 ],
table.hline(stroke: .5pt),
[],
);

$   \(x - 2 \)lr(\( x ^(2 )+ 14  x + 48 \) ) & = 0  \  \(x - 2 \)\(x + 8 \)\(x + 6 \) & = 0    $

$   & x = - 8 \,- 6 \,2  \  & x  != - 8  " and " x  != - 6  " because dimensions " \  & quad  " cannot be negative values. "   $

$  therefore  x = 2  " is the only solution. "  $

$frac(1 ,2 )$ mark for rejecting extraneous roots

$frac(1 ,2 )$ mark for stating the dimensions of the box

5 marks

#pagebreak()

= Question 32

Given the graph of $f \(x \)$ below\, sketch the graph of $y = - f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-09_542_579_571_262.jpg", width: 27.2%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-09_542_579_569_947.jpg", width: 27.2%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will

be awarded for

the graph of

$f \(x \)$.

== Solution

Reflect the graph of $f(x)$ across the $x$-axis. Every point $(x, y)$ becomes $(x, -y)$.

The reflected vertices are $(-2, -1)$, $(-1, -1)$, and $(2, 1)$. Join them in that order with straight line segments and include the endpoints.

#pagebreak()

= Question 33

Determine the coordinates of a point $\(x \, y \)$ on the unit circle if you are given $theta = 30 ^(degree )$ where

$theta $ is in standard position.

== Solution

$  upright(P )\(theta \)= \(cos  theta \, sin  theta \)  $

If $theta = 30 ^(degree )$\, then the coordinates of $upright(P )\(theta \)$ would be $lr(\( cos  30 ^(degree )\, sin  30 ^(degree )\) )$.

or

1 mark for answer stated

as coordinate point

1 mark

$  upright(P )lr(\( 30 ^(degree )\) )= lr(\( frac(sqrt(3 ),2 )\, frac(1 ,2 )\) )  $

#pagebreak()

= Question 34

Given the following sinusoidal equation:

$  upright(P )\(t \)= 3000  sin  lr(\[ frac(pi ,10 )\(t - 2010 \)\] )+ 10000   $

Determine the maximum value of $upright(P )\(t \)$ and a value of $t $ at which this maximum occurs.

Maximum value of $upright(P )\(t \)$ :

$\_ \_ \_ \_ $

Value of $t $ :

$\_ \_ \_ \_ $

== Solution

Method 1

$   " Maximum value " & = 10000 + 3000  \  & = 13000  quad  1  " mark for maximum value "   $

$   13000  & = 3000  sin  lr(\[ frac(pi ,10 )\(t - 2010 \)\] )+ 10000  \  3000  & = 3000  sin  lr(\[ frac(pi ,10 )\(t - 2010 \)\] ) \  1  & = sin  lr(\[ frac(pi ,10 )\(t - 2010 \)\] ) \  frac(pi ,2 ) & = frac(pi ,10 )\(t - 2010 \) \  5  & = t - 2010  \  t  & = 2015    $

3 marks

Note\(s\):

- the period of the function is 20 ∴ other acceptable answers are: $t = 2015  plus.minus  20 $

Method 2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-29_788_1184_638_172.jpg", width: 55.7%)

1 mark for period

$   upright(P )\(t \) & = 13000  \  t  & = 2015    $

∴ the maximum value is 13000 when $t = 2015 $.

1 mark for maximum value

1 mark for solving for $t $

3 marks

#pagebreak()

= Question 35

Sketch the graph of $y = sqrt(2  x - 2 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-11_957_1013_524_554.jpg", width: 47.7%)

== Solution

Method 1

$   y  & = sqrt(2  x - 2 ) \  & = sqrt(2 \(x - 1 \))   $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-30_904_1021_935_176.jpg", width: 48.0%)

1 mark for domain: $\[1 \, oo \)$

1 mark for shape \(graph of a radical

function\)

1 mark for horizontal compression

3 marks

#pagebreak()

= Question 36

Given $f \(x \)= 2  x - 6 $\, write the equation of $f ^(- 1 )\(x \)$.

== Solution

Switch the $x $ and $y $ values.

$  x = 2  y - 6  quad  1  " mark for switching " x  " and " y  " values "  $

$   & x + 6 = 2  y  \  & frac(x + 6 ,2 )= y  \  & therefore  f ^(- 1 )\(x \)= frac(x + 6 ,2 ) quad  frac(1 ,2 ) " mark for solving for " y  \  & frac(1 ,2 ) " mark for writing equation of " f ^(- 1 )\(x \)   $

2 marks

#pagebreak()

= Question 37

Frank tried to expand a logarithmic expression using the laws of logarithms. He made one error.

Frank's solution: $log  _(a ) frac(\(x + 2 \),z  w )= log  _(a ) x + log  _(a ) 2 - log  _(a ) z - log  _(a ) w $

Write the correct solution.

== Solution

Correct solution: $log  _(a ) frac(\(x + 2 \),z  w )= log  _(a )\(x + 2 \)- log  _(a ) z - log  _(a ) w  quad  1 $ mark for correct solution

1 mark

#pagebreak()

= Question 38

Determine all non-permissible values of $theta $ over the interval $\[0 \,2  pi \]$.

$  frac(sin  theta ,1 + cos  theta )+ csc  theta + cot  theta   $

Explain your reasoning.

== Solution

To determine non-permissible values\, the denominator

needs to equal zero.

The denominators of this expression are \" $1 + cos  theta $ \"

and \" $sin  theta $ \" $lr(\(  )$ since $csc  theta = frac(1 ,sin  theta )$ and $lr( cot  theta = frac(cos  theta ,sin  theta )\) )$.

$   therefore  1 + cos  theta  & = 0  & sin  theta  & = 0  \  cos  theta  & = - 1  & theta  & = 0 \, pi \, 2  pi  \  theta  & = pi  & &   $

∴ the non-permissible values of $theta $ over $\[0 \,2  pi \]$

are $0 \, pi $\, and $2  pi $.

1 mark for explanation

1 mark \( $frac(1 ,2 )$ mark for identifying each

restriction\)

1 mark for all non-permissible values of $theta $

\( $frac(1 ,2 )$ mark for each equation\)

3 marks

#pagebreak()

= Question 39

Given the following graphs:

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-14_667_721_476_283.jpg", width: 33.9%)

a\) 1 mark

b\) 1 mark

c\) 1 mark

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-14_661_716_485_1119.jpg", width: 33.7%)

a\) Determine the value of $\[f  dot.c  g \]\(0 \)$.

b\) Determine the value of $g \(f \(4 \)\)$.

c\) Determine a value for $k $ where $f \(k \)= 1 $.

== Solution

a\)

$   & f \(0 \)= - 1  \  & g \(0 \)= 2    $

$   \[f  dot.c  g \]\(0 \)  & = \(- 1 \)\(2 \) \  & = - 2    $

1 mark for the value of $\[f  dot.c  g \]\(0 \)$

1 mark

b\)

$   f \(4 \) & = - 1  \  g \(- 1 \) & = 3    $

$frac(1 ,2 )$ mark for $f \(4 \)$

$frac(1 ,2 )$ mark for $g \(f \(4 \)\)$ consistent with $f \(4 \)$ value

1 mark

c\) $k = 2 $ or $k = - 3 $

1 mark for a value for $k $

1 mark

#pagebreak()

= Question 40

Given that $h \(x \)= 2  x ^(2 )+ 5  x - 3 $ and that $h \(x \)= f \(x \) dot.c  g \(x \)$\, determine $f \(x \)$ and $g \(x \)$.

== Solution

$   & f \(x \)= 2  x - 1  \  & g \(x \)= x + 3    $

1 mark for two correct factors of $h \(x \)$

1 mark

Other answers are possible.

#pagebreak()

= Question 41

The graph of $y = 2  cos  theta + 1 $ below can be used to solve the equation $cos  theta = - frac(1 ,2 )$ over the

interval $\[- 2  pi \, 2  pi \]$. Indicate on the graph where to find the solutions to the equation $cos  theta = - frac(1 ,2 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-15_878_1101_1572_590.jpg", width: 51.8%)

== Solution

The solution to the equation $cos  theta = - frac(1 ,2 )$ is found where the graph of $y = 2  cos  theta + 1 $ crosses the $x $-axis.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-35_877_1717_1504_249.jpg", width: 80.8%)

Note\(s\):

- give $frac(1 ,2 )$ mark for indicating 1\, 2\, or 3 of the solutions

#pagebreak()

= Question 42

The function $f \(x \)$ is transformed.

A new function\, $y = frac(1 ,f \(x \))$\, is created that does not have any vertical asymptotes.

What can you conclude about the original function $f \(x \)$ ?

== Solution

If $f \(x \)$ does not have any $x $-intercepts\, then the transformation would not have any vertical asymptotes.

or

$f \(x \)$ cannot equal zero.

1 mark for conclusion

1 mark

$   " or " \  f  !=  0    $

Note\(s\):

- award $frac(1 ,2 )$ mark for a correct example without a given conclusion

#pagebreak()

= Question 43

Draw the angle $- frac(7  pi ,8 )$ in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-16_858_854_1602_612.jpg", width: 40.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-36_653_713_1942_226.jpg", width: 33.6%)

1 mark for angle drawn in Quadrant III

1 mark

#pagebreak()

= Question 44

Determine the exact value of:

$  4  cos  lr(\( frac(11  pi ,12 )\) )  $

== Solution

Method 1

$   4  cos  lr(\( frac(11  pi ,12 )\) ) & = 4  cos  lr(\( frac(pi ,4 )+ frac(2  pi ,3 )\) ) \  & = 4 lr(\[ cos  frac(pi ,4 ) cos  frac(2  pi ,3 )- sin  frac(pi ,4 ) sin  frac(2  pi ,3 )\] ) \  & = 4 lr(\[ lr(\( frac(sqrt(2 ),2 )\) )lr(\( - frac(1 ,2 )\) )- lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(sqrt(3 ),2 )\) )\] ) \  & = 4 lr(\[ frac(- sqrt(2 )- sqrt(6 ),4 )\] ) \  & = - sqrt(2 )- sqrt(6 )   $

1 mark for combination

2 marks \( $frac(1 ,2 )$ mark for each exact value\)

3 marks

Method 2

$frac(11  pi ,12 )$ has a reference angle of $frac(pi ,12 )$.

$   cos  lr(\( frac(pi ,12 )\) ) & = cos  lr(\( frac(pi ,4 )- frac(pi ,6 )\) ) \  & = cos  frac(pi ,4 ) cos  frac(pi ,6 )+ sin  frac(pi ,4 ) sin  frac(pi ,6 ) \  & = lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(sqrt(3 ),2 )\) )+ lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(1 ,2 )\) ) \  & = frac(sqrt(6 )+ sqrt(2 ),4 )   $

$frac(1 ,2 )$ mark for correct reference angle

$frac(1 ,2 )$ mark for substitution into correct identity

1 mark for exact values

Since $frac(11  pi ,12 )$ is in Quadrant II\, cosine is negative.

$   therefore  4  cos  lr(\( frac(11  pi ,12 )\) ) & = 4 lr(\( frac(- sqrt(6 )- sqrt(2 ),4 )\) ) \  & = - sqrt(6 )- sqrt(2 )   $

1 mark for the concept that $cos  lr(\( frac(11  pi ,12 )\) )$ is < 0

3 marks

Note\(s\):

- $frac(- 2 - 2  sqrt(3 ),sqrt(2 ))$ is an acceptable way to write the solution

- in Method 1\, another possible combination is $lr(\( frac(pi ,6 )+ frac(3  pi ,4 )\) )$

- deduct $frac(1 ,2 )$ mark if answer is not expressed as a single fraction

- in Method 2\, the reference angle need not be explicitly stated in order to obtain full marks

#pagebreak()

= Question 45

Sketch the graph of $f \(x \)= frac(x - 4 ,x ^(2 )- 3  x - 4 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/0f470e23-ee06-4b33-94db-5331c1fecb3e-18_957_1015_567_620.jpg", width: 47.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2013-jan/assets/827de64f-75db-4074-8492-505e06135358-39_823_788_711_217.jpg", width: 37.1%)

1 mark for vertical asymptote at $x = - 1 $

$frac(1 ,2 )$ mark for graph left of vertical asymptote

$frac(1 ,2 )$ mark for graph right of vertical asymptote

1 mark for point of discontinuity at $x = 4 $

3 marks

#pagebreak()

= Question 46

Estimate the value of $log  _(5 ) 35 $.

Justify your answer.

== Solution

$  5 ^(2 )= 25   $

$  5 ^(3 )= 125   $

The value of $log  _(5 ) 35 $ is more than 2 but less than 2.5.

$frac(1 ,2 )$ mark for justification

$frac(1 ,2 )$ mark for estimated answer

1 mark

#pagebreak()

= Question 47

If $p \(x \)= x ^(5 )- 12  x + 1 $\, determine the remainder when $p \(x \)$ is divided by $\(x + 2 \)$.

== Solution

Method 1

$   p \(x \) & = x ^(5 )- 12  x + 1  \  p \(- 2 \) & = \(- 2 \)^(5 )- 12 \(- 2 \)+ 1  \  & = - 32 + 24 + 1  \  & = - 7    $

Method 2

$   & -  2  | overline( 1  ) quad  0  quad  0  quad  0  quad  -  12  quad  1  \  & -  2  | overline( 1  ) quad  0  quad  0  quad  0  quad  -  12  quad  1  \  & arrow.b - 2  quad  4  quad - 8  quad  16 - 8  \  &   1 - 2  quad  4  quad - 8  quad  4 - 7    $

1 mark for correct

set-up of synthetic

division

1 mark

The remainder is -7.

#pagebreak()

= Question 48

Describe the effects on the graph of $y = f \(x \)$ when asked for the graph of $y = f \(x - 3 \)+ 5 $.

== Solution

Shift right 3 and up 5

or

$\(x + 3 \, y + 5 \)$

$frac(1 ,2 )$ mark for horizontal translation

$frac(1 ,2 )$ mark for vertical translation

1 mark

#pagebreak()

= Question 49

Find the exact value of the following expression:

$  sin  lr(\( frac(11  pi ,3 )\) ) dot.c  sec  lr(\( frac(4  pi ,3 )\) ) dot.c  tan  lr(\( - frac(5  pi ,6 )\) )  $

== Solution

$= lr(\( - frac(sqrt(3 ),2 )\) )\(- 2 \)lr(\( frac(1 ,sqrt(3 ))\) )$

$= 1 $

1 mark for $sin  lr(\( frac(11  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\, $frac(1 ,2 )$ mark for value\)

1 mark for $sec  lr(\( frac(4  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\, $frac(1 ,2 )$ mark for value\)

1 mark for $tan  lr(\( - frac(5  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\, $frac(1 ,2 )$ mark for value\)

3 marks