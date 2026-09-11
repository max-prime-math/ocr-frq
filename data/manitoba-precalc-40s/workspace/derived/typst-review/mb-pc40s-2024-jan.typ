#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2024-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

A pendulum that is 35 cm long swings through an angle of $50 ^(degree )$. Determine the length of the arc

through which the pendulum swings.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/2df4aaee-1088-4400-881f-a67dc08d8c2e-01_392_484_635_786.jpg", width: 22.8%)

== Solution

$   theta  & = 50 lr(\( frac(pi ,180 )\) ) quad  1  " mark for conversion " \  & = frac(5  pi ,18 )   $

or

=0.872 664...

$   s  & = theta  r  \  & = lr(\( frac(5  pi ,18 )\) )\(35 \) quad  1  " mark for substitution " \  & = frac(175  pi ,18 ) upright(space.nobreak c m ) quad  2  " marks " \  " or " & \  & = 30.543  upright(space.nobreak c m )   $

#pagebreak()

= Question 2

Solve algebraically\, where $0  <=  theta  <=  2  pi $.

$  2  cos  ^(2 ) theta = sin  ^(2 ) theta - 2  cos  theta   $

== Solution

$2  cos  ^(2 ) theta = 1 - cos  ^(2 ) theta - 2  cos  theta $

$3  cos  ^(2 ) theta + 2  cos  theta - 1 = 0 $

$\(cos  theta + 1 \)\(3  cos  theta - 1 \)= 0 $

$cos  theta = - 1  quad  cos  theta = frac(1 ,3 )$

$theta = pi $

$theta _(r )= 1.230 $ 959...

$theta = 1.231 \,5.052 $

1 mark for substitution of appropriate identity

1 mark for solving for $cos  theta $

2 marks for solving for $theta $ \( 1 mark for each branch\)

4 marks

#pagebreak()

= Question 3

Determine the number of arrangements of the letters in the word ATTENTION which begin with

the letter A.

== Solution

$  frac(8 ! ,3 ! 2 ! )= 3360   $

$  1  " mark for " 8 !   $

1 mark for division by $3 ! 2 ! lr(\( frac(1 ,2 ) )$ mark for $3 ! \; frac(1 ,2 )$ mark for 2!\)

2 marks

#pagebreak()

= Question 4

Solve for $x $\, algebraically.

$  e ^(2  x + 1 )= 5 ^(x )  $

== Solution

$   ln  lr(\( e ^(2  x + 1 )\) ) & = ln  lr(\( 5 ^(x )\) ) & & 1  \/ 2  " mark for applying logarithms " \  \(2  x + 1 \) ln  e  & = x  ln  5  & & 1  " mark for power law "\(1  \/ 2  " mark for each "\) \  2  x + 1  & = x  ln  5  & & \  2  x - x  ln  5  & = - 1  & & 1  \/ 2  " mark for collecting terms with " x  \  x \(2 - ln  5 \) & = - 1  & &   $

$   & x = frac(- 1 ,2 - ln  5 ) quad  frac(1 ,2 ) " mark for isolating " x  \  & x = - 2.560412  dots.h  \  & x = - 2.560  quad  1  \/ 2  " mark for evaluating quotient of logarithms "   $

3 marks

#pagebreak()

= Question 5

There are 10 teachers and 17 students who would like to attend a field trip.

Determine the number of ways that 3 teachers and 9 students can be selected given that Mr. Jones

and Mrs. Carol\, two of the teachers\, must be selected to attend the field trip.

Note: A calculator is not required for the remaining test questions.

== Solution

$   &  "" _(2 ) C _(2 ) dot.c  "" _(8 ) C _(1 ) dot.c  "" _(17 ) C _(9 ) \  & 194480    $

$   & 1  " mark for " "" _(8 ) C _(1 ) \  & frac(1 ,2 ) " mark for " "" _(17 ) C _(9 ) \  & frac(1 ,2 ) " mark for product of combinations " \  & bold(2 ) " marks "   $

Note:

- $2 _(2 ) C _(2 )$ does not need to be shown.

#pagebreak()

= Question 6

Given the graph of $f \(x \)$\, sketch the graph of $y = - f \(2  x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/2df4aaee-1088-4400-881f-a67dc08d8c2e-06_891_905_487_595.jpg", width: 42.6%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/2df4aaee-1088-4400-881f-a67dc08d8c2e-06_899_909_1445_595.jpg", width: 42.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-06_855_859_584_254.jpg", width: 40.4%)

1 mark for vertical reflection

1 mark for horizontal compression

2 marks

#pagebreak()

= Question 7

There are 5 roads between Anneville and Berrybourg\, and 2 roads between Berrybourg and

Carriton.

Determine how many ways Blake can travel from Anneville to Carriton and back to Anneville\,

given the following conditions:

- he must travel through Berrybourg in both directions

- he cannot use the same road twice

== Solution

$frac(5 ,A  ->  B ) bullet  frac(2 ,B  ->  C ) bullet  frac(1 ,C  ->  B ) bullet  frac(4 ,B  ->  A )$

40 ways

$frac(1 ,2 )$ mark for correct number of routes between towns

$frac(1 ,2 )$ mark for product

1 mark

#pagebreak()

= Question 8

Determine which term contains $x ^(0 )$ in the binomial expansion of $lr(\( x ^(2 )+ frac(1 ,x )\) )^(6 )$.

== Solution

Method 1

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$x ^(0 )= lr(\( x ^(2 )\) )^(6 - k )lr(\( frac(1 ,x )\) )^(k )$ ], [$frac(1 ,2 )$ mark for substitution ],
table.hline(stroke: .5pt),
[$x ^(0 )= x ^(12 - 2  k ) x ^(- k )$ ], [],
table.hline(stroke: .5pt),
[$x ^(0 )= x ^(12 - 3  k )$ ], [],
table.hline(stroke: .5pt),
[$3  k = 12 $ ], [],
table.hline(stroke: .5pt),
[$k = 4 $ ], [$frac(1 ,2 )$ mark for solving for $k $ ],
table.hline(stroke: .5pt),
[∴ the fifth term ], [1 mark for the fifth term \(or a term consistent with the value of $k $ \) ],
table.hline(stroke: .5pt),
[], [2 marks ],
table.hline(stroke: .5pt),
[],
);

Method 2

$   & lr(\( x ^(2 )\) )^(6 )\,lr(\( x ^(2 )\) )^(5 )lr(\( frac(1 ,x )\) )\,lr(\( x ^(2 )\) )^(4 )lr(\( frac(1 ,x )\) )^(2 ) " 1 mark for determining the pattern " \  & x ^(12 )\, x ^(9 )\, x ^(6 ) dots.h    $

∴ the fifth term 1 mark for the fifth term \(or a term consistent with the pattern\)

2 marks

#pagebreak()

= Question 9

Given $f \(x \)= x ^(3 )+ 1 $\, determine the equation of $f ^(- 1 )\(x \)$.

== Solution

Let $y = f \(x \)$

$  y = x ^(3 )+ 1   $

To determine the inverse of $f \(x \)$\, switch $x $ and $y $.

$   & x = y ^(3 )+ 1  \  & x - 1 = y ^(3 ) \  & root(3 ,x - 1 )= y  \  & f ^(- 1 )\(x \)= root(3 ,x - 1 )   $

1 mark for switching $x $ and $y $

$frac(1 ,2 )$ mark for isolating $y $

$frac(1 ,2 )$ mark for writing equation in terms of $f ^(- 1 )\(x \)$

2 marks

#pagebreak()

= Question 10

Guillermo was asked to determine the number of ways to select a president\, a vice president\, and

a treasurer from a group of 11 people.

His solution: $ "" _(11 ) C _(3 )$.

Explain why he should have used a permutation instead of a combination.

== Solution

He should have used a permutation because the people are being selected for specific positions.

1 mark

#pagebreak()

= Question 11

Prove the following identity for all permissible values of $x $.

$  frac(csc  ^(2 ) x  sec  x ,tan  x + cot  x )= csc  x   $

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

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   frac(lr(\( frac(1 ,sin  ^(2 ) x )\) )lr(\( frac(1 ,cos  x )\) ),frac(sin  x ,cos  x )+ frac(cos  x ,sin  x )) \  frac(1 ,frac(sin  ^(2 ) x  cos  x ,sin  ^(2 ) x + cos  ^(2 ) x )) \  frac(1 ,sin  ^(2 ) x  cos  x ) dot.c  frac(sin  x  cos  x ,1 ) \  frac(1 ,sin  x ) \  csc  x    $ ], [$csc  x $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 12

Determine the value of $x $\, algebraically.

$  5  log  _(a ) 2 - frac(1 ,4 ) log  _(a ) 16 = log  _(a ) x   $

== Solution

$   log  _(a ) 2 ^(5 )- log  _(a ) 16 ^(frac(1 ,4 )) & = log  _(a ) x  & & 1  " mark for power law "lr(\( frac(1 ,2 ) " mark for each "\) ) \  log  _(a )lr(\( frac(32 ,2 )\) ) & = log  _(a ) x  & & 1  " mark for quotient law " \  log  _(a ) 16  & = log  _(a ) x  & & \  x  & = 16  & & 1  " mark for equating arguments "   $

3 marks

#pagebreak()

= Question 13

Tamara must determine the factors of $x ^(4 )- 13  x + 2  x ^(3 )- 14  x ^(2 )+ 24 $.

Explain why the coefficients Tamara used to set up her synthetic division are not written correctly.

$  1  mat(delim: #none,  1  "" , - 13  "" , 2  "" , - 14  "" , 24  )  $

== Solution

Tamara did not arrange the coefficients of the terms in order of descending degree.

#pagebreak()

= Question 14

Determine the equation of the graph of $g \(x \)$ in terms of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/2df4aaee-1088-4400-881f-a67dc08d8c2e-14_828_837_560_627.jpg", width: 39.4%)

$  g \(x \)=   $

== Solution

$  g \(x \)= f \(- \(x + 2 \)\)- 5   $

or

$  g \(x \)= - f \(x + 10 \)+ 1   $

1 mark for horizontal reflection

1 mark for horizontal translation

1 mark for vertical translation

1 mark for vertical reflection

1 mark for horizontal translation

1 mark for vertical translation

3 marks

#pagebreak()

= Question 15

Expand\, using the laws of logarithms.

$  log  _(2 )lr(\[ frac(\(x - 1 \)\(x - 2 \),x )\] )  $

== Solution

$log  _(2 )\(x - 1 \)+ log  _(2 )\(x - 2 \)- log  _(2 ) x $

1 mark for product law

1 mark for quotient law

2 marks

#pagebreak()

= Question 16

Identify the range of the function $g \(x \)= frac(1 ,2 ) f \(x + 1 \)$\, given that the range of the function $y = f \(x \)$

is $\[- 6 \,4 \]$.

*A.*

$\[- 12 \,8 \]$

*B.*

$\[- 7 \,3 \]$

*C.*

$\[- 5 \,5 \]$

*D.*

$\[- 3 \,2 \]$

== Solution

Correct answer: D

$\[- 3 \,2 \]$

#pagebreak()

= Question 17

Identify the value of $a $\, given that there are 11 terms in the expansion of $lr(\( 3  x ^(4 )- y \) )^(2  a )$.

*A.*

5

*B.*

6

*C.*

10

*D.*

11

== Solution

Correct answer: A

5

#pagebreak()

= Question 18

Identify the angle that best represents $theta = - frac(6  pi ,5 )$.

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-02_544_532_524_326.jpg", width: 25.0%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-02_540_541_524_1228.jpg", width: 25.5%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-02_544_546_1250_322.jpg", width: 25.7%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-02_546_545_1248_1224.jpg", width: 25.6%)

== Solution

Correct answer: C

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-02_544_546_1250_322.jpg", width: 25.7%)

#pagebreak()

= Question 19

Identify a possible value for $n $\, given the graph of $y = - frac(1 ,2 )\(x + 2 \)^(2 )\(x - 1 \)^(n )$.

*A.*

1

*B.*

2

*C.*

3

*D.*

4

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-03_542_519_451_777.jpg", width: 24.4%)

== Solution

Correct answer: C

3

#pagebreak()

= Question 20

Identify the statement that is false\, given $g \(x \)= frac(8  x ^(2 ),x ^(2 )- 16 )$.

*A.*

the graph of $g \(x \)$ has one $x $-intercept.

*B.*

the graph of $g \(x \)$ has a point of discontinuity \(hole\) at $x = 0 $.

*C.*

the graph of $g \(x \)$ has two vertical asymptotes.

*D.*

the graph of $g \(x \)$ has a horizontal asymptote at $y = 8 $.

== Solution

Correct answer: B

the graph of $g \(x \)$ has a point of discontinuity \(hole\) at $x = 0 $.

#pagebreak()

= Question 21

1 mark

Identify the equivalent form of $log  _(a )lr(\( frac(1 ,x ^(2 ))\) )$.

*A.*

$- 2  log  _(a ) x $

*B.*

$1 - 2  log  _(a ) x $

*C.*

$2  log  _(a ) x $

*D.*

$- 2  log  _(a )lr(\( frac(1 ,x )\) )$

== Solution

Correct answer: A

$- 2  log  _(a ) x $

#pagebreak()

= Question 22

Identify which one of the following expressions is equivalent to $ "" _(13 ) C _(6 )$.

*A.*

$ "" _(13 ) P _(6 )$

*B.*

$ "" _(13 ) C _(7 )$

*C.*

$ "" _(12 ) P _(7 )$

*D.*

$ "" _(12 ) C _(6 )$

== Solution

Correct answer: B

$ "" _(13 ) C _(7 )$

#pagebreak()

= Question 23

Identify the equation of $h \(x \)= f \(x \)- g \(x \)$\, given $f \(x \)= x + 5 $ and $g \(x \)= 4  x + 1 $.

*A.*

$h \(x \)= - 3  x + 6 $

*B.*

$h \(x \)= - 3  x + 4 $

*C.*

$h \(x \)= 3  x + 6 $

*D.*

$h \(x \)= 3  x - 4 $

== Solution

Correct answer: B

$h \(x \)= - 3  x + 4 $

#pagebreak()

= Question 24

Determine the equation of the radical function represented by the graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-05_798_805_436_648.jpg", width: 37.9%)

$  y =   $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$y = frac(1 ,2 ) sqrt(x + 4 )- 2 $ ], [1 mark for vertical compression 1 mark for horizontal translation 1 mark for vertical translation ],
table.hline(stroke: .5pt),
[or ], [3 marks ],
table.hline(stroke: .5pt),
[$y = sqrt(frac(1 ,4 )\(x + 4 \))- 2 $ ], [1 mark for horizontal stretch 1 mark for horizontal translation 1 mark for vertical translation ],
table.hline(stroke: .5pt),
[], [3 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 25

Determine the exact value of $x $.

$  sec  lr(\( frac(2  pi ,3 )\) )lr(\( sin  lr(\( - frac(5  pi ,3 )\) )\) )\(x \)= 3   $

== Solution

$\(- 2 \)lr(\( frac(sqrt(3 ),2 )\) )\(x \)= 3 $

$  - sqrt(3 )\(x \)= 3   $

$  x = - frac(3 ,sqrt(3 ))  $

1 mark for $sec  lr(\( frac(2  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for value\; $frac(1 ,2 )$ mark for quadrant $\)$

1 mark for $sin  lr(\( - frac(5  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for value\; $frac(1 ,2 )$ mark for quadrant $\)$

2 marks

$  x = - sqrt(3 )  $

#pagebreak()

= Question 26

Sketch the graph of $y = 2 ^(- x )- 3 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-07_796_802_586_683.jpg", width: 37.7%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-22_801_950_522_243.jpg", width: 44.7%)

#pagebreak()

= Question 27

Given the graph of $y = g \(x \)$\, sketch the graph of $y = frac(1 ,g \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-08_876_867_489_605.jpg", width: 40.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-08_884_869_1551_605.jpg", width: 40.9%)

The graph of

$g \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $g \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-23_892_950_1581_206.jpg", width: 44.7%)

1 mark for asymptotic behaviour approaching

$x = - 2 lr(\( frac(1 ,2 ) )$ mark for each side $\)$

$frac(1 ,2 )$ mark for asymptotic behaviour approaching

$y = 0 $

$frac(1 ,2 )$ mark for graph left of $x = - 2 $

$frac(1 ,2 )$ mark for graph right of $x = - 2 $

$frac(1 ,2 )$ mark for restricting domain

3 marks

#pagebreak()

= Question 28

Determine the exact value of $tan  lr(\( frac(pi ,12 )\) )$.

== Solution

$  mat(delim: #none,  tan  lr(\( frac(pi ,12 )\) ) "" , = tan  lr(\( frac(4  pi ,12 )- frac(3  pi ,12 )\) ) "" , "" ; tan  lr(\( frac(pi ,3 )- frac(pi ,4 )\) ) "" , = frac(tan  frac(pi ,3 )- tan  frac(pi ,4 ),1 + tan  frac(pi ,3 ) tan  frac(pi ,4 )) "" , "" ; "" , = frac(sqrt(3 )- 1 ,1 + sqrt(3 )) "" , 1  " mark for substitution into correct identity " "" ; "" , " or " "" , 1  " mark for exact values "lr(\( frac(1 ,2 ) " mark for each value "\) ) "" ; "" , = 2 - sqrt(3 ) "" , "" ; "" , " or " "" ; "" , = frac(3 - sqrt(3 ),3 + sqrt(3 )) )  $

- Other combinations are possible.

#pagebreak()

= Question 29

Explain why the graph of $g \(x \)= frac(3 ,x ^(2 )+ 4 )$ does not have a vertical asymptote.

== Solution

The graph of a rational function has a vertical asymptote when the denominator is equal to zero.

The denominator of $g \(x \)$ will never be equal to zero.

1 mark

#pagebreak()

= Question 30

Solve\, algebraically.

$  log  _(3 ) x + log  _(3 )\(x + 8 \)= 2   $

== Solution

Method 1

$   log  _(3 )\[x \(x + 8 \)\] & = 2  \  x ^(2 )+ 8  x  & = 3 ^(2 ) \  x ^(2 )+ 8  x - 9  & = 0  \  \(x + 9 \)\(x - 1 \) & = 0  \  x + 4  quad  x  & = 1    $

1 mark for product law

1 mark for exponential form

$frac(1 ,2 )$ mark for the permissible value of $x $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

3 marks

Method 2

$   log  _(3 ) x + log  _(3 )\(x + 8 \) & = log  _(3 ) 3 ^(2 ) \  log  _(3 )\[x \(x + 8 \)\] & = log  _(3 ) 9  \  x ^(2 )+ 8  x  & = 9  \  x ^(2 )+ 8  x - 9  & = 0  \  \(x + 9 \)\(x - 1 \) & = 0  \  x  >= - 9  quad  x  & = 1    $

1 mark for logarithmic form

1 mark for product law

$frac(1 ,2 )$ mark for the permissible value of $x $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

3 marks

#pagebreak()

= Question 31

Sketch at least one period of the graph of the function $y = sin  lr(\( 3 lr(\( x + 30 ^(degree )\) )\) )- 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-12_942_1631_504_249.jpg", width: 76.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-27_922_920_587_318.jpg", width: 43.3%)

1 mark for shape of a sinusoidal function with correct amplitude

1 mark for period

1 mark for horizontal translation

1 mark for vertical translation

4 marks

#pagebreak()

= Question 32

Explain why the domain of the function\, $f \(x \)= log  \(x - 3 \)$\, is $x > 3 $.

== Solution

The argument of a logarithm cannot be negative or zero.

1 mark

#pagebreak()

= Question 33

Sketch the graph of $p \(x \)= - \(x - 3 \)\(x + 1 \)^(2 )\(x - 5 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-14_991_1621_543_251.jpg", width: 76.3%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-29_997_1042_593_243.jpg", width: 49.0%)

1 mark for $x $-intercepts

1 mark for multiplicity of 2 at $x = - 1 $

$frac(1 ,2 )$ mark for end behaviour

$frac(1 ,2 )$ mark for $y $-intercept

3 marks

#pagebreak()

= Question 34

Given that $sin  theta = - frac(2 ,3 )$ and $tan  theta > 0 $\, determine the exact value of $sin  2  theta $.

== Solution

$   & x ^(2 )= r ^(2 )- y ^(2 ) \  & x ^(2 )= 9 - 4  \  & x ^(2 )= 5    $

$   x  & =  plus.minus  sqrt(5 ) \  x  & = - sqrt(5 ) \  cos  theta  & = - frac(sqrt(5 ),3 ) \  sin  2  theta  & = 2  sin  theta  cos  theta  \  & = 2 lr(\( - frac(2 ,3 )\) )lr(\( - frac(sqrt(5 ),3 )\) ) \  & = frac(4  sqrt(5 ),9 )   $

$frac(1 ,2 )$ mark for value of $x $

$frac(1 ,2 )$ mark for value of $cos  theta $

2 marks

Note:

- Accept any of the following values for $x :  x =  plus.minus  sqrt(5 )\, x = - sqrt(5 )$\, or $x = sqrt(5 )$.

#pagebreak()

= Question 35

Justify whether $frac(5  pi ,8 )$ and $- frac(11  pi ,4 )$ are coterminal angles.

== Solution

Method 1

$   & frac(5  pi ,8 )- lr(\( - frac(11  pi ,4 )\) ) \  & frac(5  pi ,8 )+ frac(11  pi ,4 ) \  & frac(5  pi ,8 )+ frac(22  pi ,8 ) \  & frac(27  pi ,8 )   $

Since $frac(27  pi ,8 )$ is not a multiple of $2  pi $ they are not coterminal angles.

1 mark

Method 2

Coterminal angles of $frac(5  pi ,8 )$ :

$   & frac(5  pi ,8 )- frac(16  pi ,8 )= - frac(11  pi ,8 ) \  & - frac(11  pi ,8 )- frac(16  pi ,8 )= - frac(27  pi ,8 )   $

Coterminal angles of $- frac(11  pi ,4 )$ :

$  - frac(11  pi ,4 )lr(\( frac(2 ,2 )\) )= - frac(22  pi ,8 )  $

∴ Angles are not coterminal since $- frac(27  pi ,8 ) != - frac(22  pi ,8 )$.

1 mark

#pagebreak()

= Question 36

Sketch the graph of $f \(x \)= frac(- 2  x \(x + 1 \)\(x - 3 \),2  x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-17_809_806_539_640.jpg", width: 37.9%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-32_864_855_610_245.jpg", width: 40.2%)

1 mark for point of discontinuity \(hole\) at $x = 0 $

$frac(1 ,2 )$ mark for shape of a parabola with correct

$x $-intercepts

$frac(1 ,2 )$ mark for end behaviour

2 marks

Note:

- Deduct $frac(1 ,2 )$ mark for procedural error \(incorrect $y $-value for point of discontinuity \(hole\)\).

#pagebreak()

= Question 37

Given $frac(sin  theta + cos  theta  csc  theta ,sin  theta )$\, determine the non-permissible values of $theta $\, where $theta  in  bb(R )$.

== Solution

Method 1

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$sin  theta = 0 $ ], [$frac(1 ,2 )$ mark for $sin  theta = 0 $ ],
table.hline(stroke: .5pt),
[$theta = 0 \, pi \, 2  pi $ ], [$frac(1 ,2 )$ mark for any non-permissible value of $theta $ ],
table.hline(stroke: .5pt),
[$theta = pi  k \, k  in  bb(Z )$ ], [1 mark for all non-permissible values of $theta $ ],
table.hline(stroke: .5pt),
[],
);

2 marks

Method 2

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$sin  theta = 0 $ ], [$frac(1 ,2 )$ mark for $sin  theta = 0 $ ],
table.hline(stroke: .5pt),
[$theta = 0 \, pi \, 2  pi $ ], [$frac(1 ,2 )$ mark for any non-permissible value of $theta $ ],
table.hline(stroke: .5pt),
[$lr( mat(delim: #none, theta = 2  pi  k \, k  in  bb(Z ) "" ; theta = pi + 2  pi  k \, k  in  bb(Z ))\} )$ ], [1 mark for all non-permissible values of $theta $ ],
table.hline(stroke: .5pt),
[], [2 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 38

Write an equation of a rational function that has a horizontal asymptote at $y = 0 $ and a vertical

asymptote at $x = 6 $.

== Solution

$f \(x \)= frac(1 ,x - 6 ) quad  1 $ mark for horizontal asymptote

1 mark for vertical asymptote

2 marks

Note:

- Other answers are possible.

#pagebreak()

= Question 39

Given the functions $f \(x \)= sqrt(x - 1 )$ and $g \(x \)= x ^(2 )$\,

a\) state the equation of $g \(f \(x \)\)$.

$  g \(f \(x \)\)=   $

$\_ \_ \_ \_ $

b\) sketch the graph of $g \(f \(x \)\)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-20_890_897_1437_597.jpg", width: 42.2%)

== Solution

a\) $g \(f \(x \)\)= x - 1 \, x  >=  1 $

1 mark

b\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-35_853_864_1098_258.jpg", width: 40.7%)

1 mark for shape of graph consistent with a\)

1 mark for restricted domain

2 marks

Notes:

- Deduct a maximum of 1 mark for the concept error of not restricting the domain.

- Deduct $frac(1 ,2 )$ mark for procedural error \(not stating domain\) if graph shows correct domain.

#pagebreak()

= Question 40

Suzanne was asked to determine the value of $tan  theta $\, given that $sec  theta = - frac(8 ,3 )$ and $theta $ terminates in

quadrant II.

Her solution:

$   \(- 3 \)^(2 )+ y ^(2 ) & = \(8 \)^(2 ) \  y ^(2 ) & = 55  \  y  & = sqrt(55 ) \  tan  theta  & = frac(sqrt(55 ),3 )   $

Describe her error.

== Solution

Suzanne did not consider that the value of $tan  theta $ is negative in quadrant II.

#pagebreak()

= Question 41

Given the graph of $y = f \(x \)$\, sketch the graph of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-22_850_852_470_620.jpg", width: 40.1%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-22_861_856_1445_618.jpg", width: 40.3%)

The graph of

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/589d58a9-6779-468e-aa7e-cb58697728e6-22_98_93_1658_1770.jpg", width: 5.0%)

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jan/assets/c66b384c-1697-41b1-8524-28dfc43e9cef-37_855_862_546_260.jpg", width: 40.6%)

1 mark for restricting domain

$frac(1 ,2 )$ mark for shape between invariant points

$frac(1 ,2 )$ mark for shape to the right of invariant points

2 marks

#pagebreak()

= Question 42

The point $P \(theta \)= \(0 \,- 1 \)$ lies on the unit circle. State the angle $theta $\, over the interval $\[2  pi \, 4  pi \]$.

== Solution

$  theta = frac(7  pi ,2 )  $

1 mark

#pagebreak()

= Question 43

Describe how the transformations of $f \(x \)$ on the graphs of $g \(x \)= f \(3  x - 6 \)$ and

$h \(x \)= f \(3 \(x - 6 \)\)$ are different.

== Solution

The graph of $g \(x \)$ is a horizontal translation of $f \(x \)$ two units to the right and the graph of

$h \(x \)$ is a horizontal translation of $f \(x \)$ six units to the right.

1 mark

#pagebreak()

= Question 44

a\) Solve.

$  sqrt(2  x + 5 )- 3 = 0   $

b\) Describe how the solution in a\) relates to the graph of $y = sqrt(2  x + 5 )- 3 $.

== Solution

a\)

$   \(sqrt(2  x + 5 )\)^(2 ) & = 3 ^(2 ) \  2  x + 5  & = 9  \  2  x  & = 4  \  x  & = 2    $

1 mark

b\) The solution is the $x $-intercept of the graph.

1 mark

#pagebreak()

= Question 45

Determine all of the zeros of the function $p \(x \)= x ^(3 )- 2  x ^(2 )- 9  x + 18 $.

== Solution

$   p \(2 \) & = 2 ^(3 )- 2 \(2 \)^(2 )- 9 \(2 \)+ 18  quad  1  " mark for identifying one possible zero of " p \(x \) \  & = 0  \  & therefore \(x - 2 \) " is a factor of " p \(x \)   $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [1 ], [-2 ], [-9 ], [18 ],
table.hline(stroke: .5pt),
[], [], [2 ], [0 ], [-18 ],
table.hline(stroke: .5pt),
[], [1 ], [0 ], [-9 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or equivalent strategy\)

$  mat(delim: #none,  \(x - 2 \)lr(\( x ^(2 )- 9 \) )= 0  "" , 1  \/ 2  " mark for consistent factors " "" ; \(x - 2 \)\(x - 3 \)\(x + 3 \)= 0  "" , "" ; x = 2 \, x = 3 \, x = - 3  "" , 1  \/ 2  " mark for consistent zeros " )  $

3 marks

#pagebreak()

= Question 46

Given that the point $lr(\( frac(sqrt(23 ),6 )\, y \) )$ is on the unit circle\, determine the exact value\(s\) of $y $.

== Solution

$lr(\( frac(sqrt(23 ),6 )\) )^(2 )+ y ^(2 )= 1  quad  frac(1 ,2 )$ mark for substitution

$frac(23 ,36 )+ y ^(2 )= 1 $

$y ^(2 )= frac(36 ,36 )- frac(23 ,36 )$

$y =  plus.minus  frac(sqrt(13 ),6 ) quad  1  \/ 2 $ mark for exact values of $y $

1 mark

#pagebreak()

= Question 47

State one zero of the function $y = tan  x $.

== Solution

Any solution where $x = pi  k \, k  in  bb(Z )$\, is acceptable.