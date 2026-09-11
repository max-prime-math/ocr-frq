#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2025-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Youyi wants to buy a new cell phone from a company that offers 33 different types of cell

phones. Each cell phone is available in 5 different colours. Determine the total number of

available options.

== Solution

$underline(33 ) bullet  underline(5 )= 165 $ options

1 mark

#pagebreak()

= Question 2

Determine the central angle subtended by an arc length of 30 cm on a circle with a diameter of

20.6 cm . Express your answer in degrees.

== Solution

$   s  & = theta  r  \  30  & = theta \(10.3 \) \  theta  & = 2.912621  dots.h  \  theta  & = \(2.912621 \)lr(\( frac(180 ^(degree ),pi )\) ) \  theta  & = 166.880911  dots.h  "" ^(degree ) \  theta  & = 166.881 ^(degree )   $

1 mark for substitution

1 mark for conversion

2 marks

#pagebreak()

= Question 3

A choir has 14 sopranos. Karin and Ellen are two of them. Determine the number of possible

ensembles of 3 sopranos that could be formed if either Karin or Ellen\, or both\, must be

included.

== Solution

Method 1

Case 1: $ "" _(1 ) C _(1 ) dot.c  "" _(12 ) C _(2 )= 66  quad  1 $ mark for Case 1 and Case 2

Case 2: $ "" _(1 ) C _(1 ) dot.c  "" _(12 ) C _(2 )= 66 $

Case $3 :  "" _(2 ) C _(2 ) dot.c  "" _(12 ) C _(1 )= 12  quad  1 $ mark for Case 3

$  66 + 66 + 12 = 144  quad  1  " mark for addition of cases "  $

3 marks

Method 2

$   "" _(14 ) C _(3 )-  "" _(12 ) C _(3 )= 144   $

1 mark for $ "" _(14 ) C _(3 )$

1 mark for $ "" _(12 ) C _(3 )$

1 mark for subtraction of cases

3 marks

#pagebreak()

= Question 4

Loïc invests $dollar  5000 $ at an annual interest rate of $6.75  % $ compounded semi-annually. The value of

his investment grows according to the following formula:

$  A = P lr(\( 1 + frac(r ,n )\) )^(n  t )  $

where $A $ is the value of the investment after $t $ years

$P $ is the amount of the initial deposit

$r $ is the annual interest rate \(as a decimal\)

$n $ is the number of compounding periods per year

$t $ is the time in years

Determine\, algebraically\, the length of time it will take Loïc's investment to grow to $dollar  9500 $.

== Solution

$   9500  & = 5000 lr(\( 1 + frac(0.0675 ,2 )\) )^(2  t ) & & 1  \/ 2  " mark for substitution " \  1.9  & = \(1.03375 \)^(2  t ) & & \  log  1.9  & = log  \(1.03375 \) & & 1  " mark for applying logarithms " \  log  1.9  & = 2  t  log  1.03375  & & 1  " mark for power law (or appropriate logarithm laws) " \  t  & = frac(log  1.9 ,2  log  1.03375 ) & & \  t  & = 9.668522  dots.h  & & 1  \/ 2  " mark for evaluating a quotient of logarithms " \  t  & = 9.669  " years " & & 3  " marks " \  therefore  t  & & &   $

Note:

Accept $t = 9.669 $ years as a final answer \(or consistent value of $t $ \).

#pagebreak()

= Question 5

Solve\, algebraically\, over the interval $\[0 \,2  pi \]$.

$  csc  ^(2 ) theta - csc  theta - 6 = 0   $

== Solution

Method 1

$  \(csc  theta - 3 \)\(csc  theta + 2 \)= 0   $

$  mat(delim: #none,  csc  theta = 3  "" , csc  theta = - 2  "" ; sin  theta = frac(1 ,3 ) "" , sin  theta = - frac(1 ,2 ) "" ; theta _(r )= 0.339836  dots.h  "" , )  $

1 mark for solving for $csc  theta $

1 mark for reciprocal

2 marks for solving for $theta $ \( $frac(1 ,2 )$ mark for each value\)

4 marks

Method 2

$   & frac(1 ,sin  ^(2 ) theta )- frac(1 ,sin  theta )- 6 = 0  \  & 1 - sin  theta - 6  sin  ^(2 ) theta = 0  \  & 6  sin  ^(2 ) theta + sin  theta - 1 = 0  \  & \(3  sin  theta - 1 \)\(2  sin  theta + 1 \)= 0  \  & sin  theta = frac(1 ,3 ) quad  sin  theta = frac(- 1 ,2 ) \  & theta _(r )= 0.339836  dots.h  \  & theta = 0.340  \; 2.802  quad  theta = frac(7  pi ,6 )\, frac(11  pi ,6 )   $

1 mark for reciprocal

1 mark for solving for $sin  theta $

2 marks for solving for $theta $ \( $frac(1 ,2 )$ mark for each value\)

4 marks

#pagebreak()

= Question 6

Determine how many 4 -digit numbers can be made using the digits $0 \,1 \,2 \,3 \,4 $\, and 5 \, if the

third digit must be 3 \, and repetition is not allowed.

== Solution

#table(stroke: none,
columns: 6,
align: (left, left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5), table.vline(stroke: .5pt, x: 6),
table.hline(stroke: .5pt),
[4 ], [• ], [• ], [1 ], [• ], [3 ],
table.hline(stroke: .5pt),
[not 0 or 3 ], [], [], [3 ], [], [],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for restriction of first digit

$frac(1 ,2 )$ mark for restriction of third digit

1 mark for fundamental counting principle

2 marks

#pagebreak()

= Question 7

Describe the transformations required to obtain the graph of the function $y = - 4  f lr(\( frac(1 ,3 ) x \) )$ from

the graph of $y = f \(x \)$.

== Solution

- Reflection over the $x $-axis

- Vertical stretch by a factor of 4

- Horizontal stretch by a factor of 3

1 mark for vertical reflection

1 mark for vertical stretch

1 mark for horizontal stretch

3 marks

#pagebreak()

= Question 8

Given the graph of $y = f \(x \)$\, sketch the graph of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-08_828_826_554_543.jpg", width: 38.9%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-08_835_826_1428_543.jpg", width: 38.9%)

The graph of $f \(x \)$

has already been

drawn for your

reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-08_825_816_584_245.jpg", width: 38.4%)

1 mark for restricting domain

$frac(1 ,2 )$ mark for shape between invariant points\,

$  \{ 0  <=  y  <=  1 \}   $

$frac(1 ,2 )$ mark for shape above invariant points\,

$  \{ 1  <=  y  <=  2 \}   $

2 marks

#pagebreak()

= Question 9

Describe how to determine if $\(x - a \)$ is a factor of the polynomial function\, $p \(x \)$.

== Solution

$\(x - a \)$ is a factor of $p \(x \)$\, if and only if $p \(a \)= 0 $.

1 mark

#pagebreak()

= Question 10

Express $frac(1 ,2 ) log  x - 2  log  y + log  z $ as a single logarithm.

== Solution

$log  lr(\( frac(sqrt(x ) bullet  z ,y ^(2 ))\) )$

1 mark for product law

1 mark for quotient law

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

3 marks

#pagebreak()

= Question 11

Given the graph of $g \(x \)$\, sketch the graph of $f \(x \)= frac(1 ,g \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-11_907_1352_522_378.jpg", width: 63.6%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-11_974_1442_1465_378.jpg", width: 67.9%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-11_911_1833_1538_168.jpg", width: 86.3%)

#pagebreak()

= Question 12

Given the identity $frac(1 - tan  ^(2 ) theta ,sec  ^(2 ) theta )= cos  2  theta $\,

a\) state a non-permissible value of $theta $.

b\) prove the identity for all permissible values of $theta $.

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

a\) Any value where $theta = frac(pi ,2 )+ k  pi \, k  in  bb(Z )$ or $theta = 90 ^(degree )+ 180 ^(degree ) k \, k  in  bb(Z )$\, is acceptable.

b\)

Method 1

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   1 - frac(sin  ^(2 ) theta ,cos  ^(2 ) theta ) \    frac(1 ,cos  ^(2 ) theta ) \  frac(cos  ^(2 ) theta - sin  ^(2 ) theta ,cos  ^(2 ) theta ) \    frac(1 ,cos  ^(2 ) theta ) \  frac(cos  2  theta ,cos  ^(2 ) theta ) \  frac(1 ,cos  ^(2 ) theta ) \  cos  2  theta    $ ], [$cos  2  theta $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 13

Determine an equation of the radical function represented by the graph of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-13_1020_1013_534_560.jpg", width: 47.7%)

$f \(x \)= $

$\_ \_ \_ \_ $

== Solution

$  f \(x \)= 3  sqrt(x - 2 )  $

1 mark for vertical stretch

1 mark for horizontal translation

2 marks

#pagebreak()

= Question 14

Given the graphs of $f \(x \)$ and $g \(x \)$\, sketch the graph of $g \(f \(x \)\)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-14_729_744_515_294.jpg", width: 35.0%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-14_733_729_511_1104.jpg", width: 34.3%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-14_729_733_1310_696.jpg", width: 34.5%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-14_728_726_1351_700.jpg", width: 34.2%)

1 mark for $g \(f \(x \)\)$

1 mark for restricted domain

2 marks

#pagebreak()

= Question 15

Sketch a graph of $p \(x \)$ that satisfies all of the following conditions:

- $p \(x \)$ is a polynomial function of degree 3

- $p \(x \)$ has a zero at -5 with a multiplicity of 2

- $p \(x \)$ has a zero at 1

- $p \(x \)$ has a leading coefficient of -2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-15_1039_1279_863_421.jpg", width: 60.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-15_947_1003_941_243.jpg", width: 47.2%)

$frac(1 ,2 )$ mark for $x $-intercepts

1 mark for multiplicity of 2 at $x = - 5 $

$frac(1 ,2 )$ mark for $y $-intercept

$frac(1 ,2 )$ mark for end behaviour

$frac(1 ,2 )$ mark for shape of cubic function

3 marks

#pagebreak()

= Question 16

Sketch the graph of $f \(x \)= frac(x ^(2 )+ x ,x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/d48d4585-9f6b-42e8-8029-339c3c881816-16_1037_1025_629_550.jpg", width: 48.2%)

== Solution

$   & f \(x \)= frac(cancel(x )\(x + 1 \),cancel(x )) \  & f \(x \)= x + 1 \, x  !=  0    $

∴ there is a point of discontinuity \(hole\) at $\(0 \,1 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-16_1023_1014_967_245.jpg", width: 47.7%)

1 mark for point of discontinuity

\(hole\) at $x = 0 $

1 mark for shape of $y = x + 1 $

2 marks

#pagebreak()

= Question 17

Identify the function that has a different range than $f \(x \)= x ^(2 )$.

*A.*

$y = 4  f \(x \)$

*B.*

$y = f \(x \)+ 4 $

*C.*

$y = f \(x + 4 \)$

*D.*

$y = f \(- x \)$

== Solution

Correct answer: B

$y = f \(x \)+ 4 $

#pagebreak()

= Question 18

Identify the exact value of $sin  lr(\( - frac(7  pi ,3 )\) )$.

*A.*

$- frac(sqrt(3 ),2 )$

*B.*

$- frac(1 ,2 )$

*C.*

$frac(1 ,2 )$

*D.*

$frac(sqrt(3 ),2 )$

== Solution

Correct answer: A

$- frac(sqrt(3 ),2 )$

#pagebreak()

= Question 19

Identify the value of $a $ in the equation\, $log  _(a ) 3 = frac(1 ,4 )$.

*A.*

$frac(1 ,64 )$

*B.*

$3 ^(frac(1 ,4 ))$

*C.*

12

*D.*

81

== Solution

Correct answer: D

81

#pagebreak()

= Question 20

Identify a value of $x $ where the graphs of $y = cos  x $ and $y = sin  x $ intersect.

*A.*

$- frac(3  pi ,4 )$

*B.*

$- frac(pi ,4 )$

*C.*

0

*D.*

$frac(3  pi ,4 )$

== Solution

Correct answer: A

$- frac(3  pi ,4 )$

#pagebreak()

= Question 21

1 mark

Identify the number of negative terms in the binomial expansion of $\(2  x - y \)^(6 )$.

*A.*

0

*B.*

3

*C.*

4

*D.*

6

== Solution

Correct answer: B

3

#pagebreak()

= Question 22

1 mark

Identify the general solution of the equation\, $sin  x = 1 $.

*A.*

$x = k  pi \, k  in  bb(Z )$

*B.*

$x = 2  k  pi \, k  in  bb(Z )$

*C.*

$x = frac(pi ,2 )+ k  pi \, k  in  bb(Z )$

*D.*

$quad  x = frac(pi ,2 )+ 2  k  pi \, k  in  bb(Z )$

== Solution

Correct answer: D

$quad  x = frac(pi ,2 )+ 2  k  pi \, k  in  bb(Z )$

#pagebreak()

= Question 23

Identify a possible degree of the polynomial function represented below.

*A.*

2

*B.*

3

*C.*

4

*D.*

5

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/e97237d6-bd89-41df-a227-5137b7812dd3-03_431_480_433_1005.jpg", width: 22.6%)

== Solution

Correct answer: C

4

#pagebreak()

= Question 24

Identify the expression that is equivalent to $cos  x  cot  x $.

*A.*

$frac(1 - sin  x ,sin  x )$

*B.*

$frac(sin  ^(2 ) x - 1 ,sin  x )$

*C.*

$sin  x $

*D.*

$frac(1 - sin  ^(2 ) x ,sin  x )$

== Solution

Correct answer: D

$frac(1 - sin  ^(2 ) x ,sin  x )$

#pagebreak()

= Question 25

Given that the point $\(- 7 \,- 5 \)$ is on the graph of $y = g \(x \)$\, identify the corresponding point on the

graph of $y = | g \(x \)| $.

*A.*

$\(7 \,5 \)$

*B.*

$\(- 7 \,5 \)$

*C.*

$\(7 \,- 5 \)$

*D.*

\(-5\, -7\)

== Solution

Correct answer: B

$\(- 7 \,5 \)$

#pagebreak()

= Question 26

Given that $x = 1 $ is one of the zeros of $p \(x \)= x ^(3 )+ x ^(2 )- 10  x + 8 $\, express $p \(x \)$ in completely

factored form.

$p \(x \)= $

== Solution

$p \(x \)= x ^(3 )+ x ^(2 )- 10  x + 8 $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[1 ], [1 ], [1 ], [-10 ], [8 ],
table.hline(stroke: .5pt),
[], [↓ ], [1 ], [2 ], [-8 ],
table.hline(stroke: .5pt),
[], [1 ], [2 ], [-8 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or any equivalent strategy\)

$   & p \(x \)= \(x - 1 \)lr(\( x ^(2 )+ 2  x - 8 \) ) \  & p \(x \)= \(x - 1 \)\(x + 4 \)\(x - 2 \)   $

1 mark for consistent factors

2 marks

#pagebreak()

= Question 27

Determine the exact value of $frac(csc  ^(2 ) theta - 1 ,1 - cos  ^(2 ) theta )$ if $theta = frac(5  pi ,6 )$.

== Solution

Method 1

$   & frac(csc  ^(2 )lr(\( frac(5  pi ,6 )\) )- 1 ,1 - cos  ^(2 )lr(\( frac(5  pi ,6 )\) )) \  & frac(\(2 \)^(2 )- 1 ,1 - lr(\( frac(- sqrt(3 ),2 )\) )^(2 )) \  & frac(4 - 1 ,1 - frac(3 ,4 )) \  & frac(3 ,frac(1 ,4 )) \  & 12    $

1 mark for $csc  lr(\( frac(5  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

1 mark for $cos  lr(\( frac(5  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

2 marks

Method 2

$   & frac(cot  ^(2 ) theta ,sin  ^(2 ) theta ) \  & frac(cot  ^(2 )lr(\( frac(5  pi ,6 )\) ),sin  ^(2 )lr(\( frac(5  pi ,6 )\) )) \  & frac(\(- sqrt(3 )\)^(2 ),lr(\( frac(1 ,2 )\) )^(2 )) \  & frac(3 ,frac(1 ,4 )) \  & 12    $

1 mark for $cot  lr(\( frac(5  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

1 mark for $sin  lr(\( frac(5  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

2 marks

#pagebreak()

= Question 28

Solve\, graphically.

$  - 2  x + 5 = sqrt(x - 1 )  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/e97237d6-bd89-41df-a227-5137b7812dd3-06_1028_1032_625_543.jpg", width: 48.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-22_913_1036_651_245.jpg", width: 48.8%)

$  therefore  x = 2   $

1 mark for shape of a radical function

1 mark for horizontal translation

1 mark for $x $-value consistent with intersection point of the two graphs

3 marks

#pagebreak()

= Question 29

If $log  _(a ) 2 = p $ and $log  _(a ) 5 = q $\, express $log  _(a ) 40 $ in terms of $p $ and $q $.

== Solution

$   log  _(a ) 40  & = log  _(a )lr(\( 2 ^(3 ) dot.c  5 \) ) \  & = 3  log  _(a ) 2 + log  _(a ) 5  \  & = 3  p + q    $

1 mark for power law

1 mark for product law

2 marks

#pagebreak()

= Question 30

Describe how to sketch the graph of $y = f ^(- 1 )\(x \)$\, given the graph of a linear function\, $y = f \(x \)$.

== Solution

The graph of $y = f ^(- 1 )\(x \)$ is obtained by reflecting the graph of $y = f \(x \)$ over the line $y = x $.

or

To sketch the inverse\, $y = f ^(- 1 )\(x \)$\, transform all points on the graph of $y = f \(x \)$ from

$\(x \, y \)$ to $\(y \, x \)$.

1 mark

#pagebreak()

= Question 31

Given that $sin  alpha = - frac(4 ,5 )$ where $alpha $ is in quadrant III\, and $cos  beta = frac(12 ,13 )$ where $beta $ is in quadrant IV\,

determine the exact value of $cos  \(alpha - beta \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-25_374_365_685_249.jpg", width: 17.2%)

$   x ^(2 )+ 4 ^(2 ) & = 5 ^(2 ) \  x ^(2 ) & = 9  \  x  & =  plus.minus  3    $

$   12 ^(2 )+ y ^(2 ) & = 13 ^(2 ) \  y ^(2 ) & = 25  \  y  & =  plus.minus  5    $

$frac(1 ,2 )$ mark for value of $x $

$frac(1 ,2 )$ mark for value of $y $

$   cos  \(alpha - beta \) & = cos  alpha  cos  beta + sin  alpha  sin  beta  \  & = lr(\( - frac(3 ,5 )\) )lr(\( frac(12 ,13 )\) )+ lr(\( - frac(4 ,5 )\) )lr(\( - frac(5 ,13 )\) ) \  & = frac(- 36 + 20 ,65 ) \  & = - frac(16 ,65 )   $

$frac(1 ,2 )$ mark for consistent value of $cos  alpha $

$frac(1 ,2 )$ mark for consistent value of $sin  beta $

1 mark for substitution into correct identity

3 marks

Note:

Accept any of the following values for $x :  x =  plus.minus  3  \; x = - 3 $\; or $x = 3 $.

Accept any of the following values for $y :  y =  plus.minus  5  \; y = - 5 $\; or $y = 5 $.

#pagebreak()

= Question 32

Sketch the graph of $f \(x \)= frac(2  x - 4 ,x + 1 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/e97237d6-bd89-41df-a227-5137b7812dd3-10_994_989_586_569.jpg", width: 46.5%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-26_967_980_606_241.jpg", width: 46.1%)

1 mark for asymptotic behaviour approaching $x = - 1 $

1 mark for asymptotic behaviour approaching $y = 2 $

1 mark for shape of rational function

\( $frac(1 ,2 )$ mark for graph left of $x = - 1 \, frac(1 ,2 )$ mark for graph right of $x = - 1 $ \)

3 marks

#pagebreak()

= Question 33

Due to the tidal variations\, the depth of the water in a bay is represented by the function\,

$  d \(t \)= - 2  cos  lr(\[ frac(pi ,6 )\(t + 4 \)\] )+ 16   $

where $d $ is the depth of the water\, in metres and

$t $ is the time\, in hours.

a\) Determine the depth of the water when $t = 2 $.

b\) State the minimum depth of the water.

c\) Determine the length of time between two consecutive low tides \(minimum depths\).

== Solution

a\)

$   d \(2 \) & = - 2  cos  lr(\[ frac(pi ,6 )\(2 + 4 \)\] )+ 16  \  & = - 2  cos  pi + 16  \  & = - 2 \(- 1 \)+ 16  \  & = 18  " metres "   $

1 mark for exact value

1 mark

b\) 14 metres

1 mark

c\)

$   " period " & = frac(2  pi ,frac(pi ,6 )) \  & = 12  " hours "   $

1 mark for period

1 mark

#pagebreak()

= Question 34

Evaluate.

$  sin  ^(2 )lr(\( frac(5  pi ,4 )\) ) sec  lr(\( frac(13  pi ,3 )\) )- cot  lr(\( frac(7  pi ,4 )\) )  $

== Solution

$lr(\( - frac(sqrt(2 ),2 )\) )^(2 )lr(\( frac(2 ,1 )\) )- \(- 1 \) quad  1 $ mark for $sin  lr(\( frac(5  pi ,4 )\) )lr(\( frac(1 ,2 ) )$ mark for value\; $frac(1 ,2 )$ mark for quadrant\)

$1 + 1 $ 2 $quad  1 $ mark for $sec  lr(\( frac(13  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for value\; $frac(1 ,2 )$ mark for quadrant $\)$

1 mark for $cot  lr(\( frac(7  pi ,4 )\) )lr(\( frac(1 ,2 ) )$ mark for value\; $frac(1 ,2 )$ mark for quadrant\)

3 marks

#pagebreak()

= Question 35

a\) State the non-permissible value\(s\) of the function\, $f \(x \)= frac(x - 3 ,x ^(2 )- 9 )$.

b\) Describe what each non-permissible value represents on the graph of $f \(x \)= frac(x - 3 ,x ^(2 )- 9 )$.

== Solution

1 mark for non-permissible values \( $frac(1 ,2 )$ mark for each\)

1 mark

b\) At $x = 3 $\, there is a point of discontinuity \(hole\) on the graph of $f \(x \)$. At $x = - 3 $\, there is a

vertical asymptote on the graph of $f \(x \)$.

$frac(1 ,2 )$ mark for point of discontinuity \(hole\) at $x = 3 $

$frac(1 ,2 )$ mark for vertical asymptote at $x = - 3 $

1 mark

#pagebreak()

= Question 36

Determine which of the given values is greater. Justify your answer.

$  log  _(3 ) 38  " or " log  _(4 ) 50   $

== Solution

$   & 3 ^(3 )= 27  \  & 3 ^(4 )= 81  quad  log  _(3 ) 38 > 3  \  & 4 ^(2 )= 16  \  & 4 ^(3 )= 64  quad  log  _(4 ) 50 < 3  \  & therefore  log  _(3 ) 38  " is greater "   $

1 mark for justification

1 mark

#pagebreak()

= Question 37

Determine if the point $lr(\( frac(3 ,4 )\, frac(sqrt(5 ),4 )\) )$ is on the unit circle. Justify your answer.

== Solution

$   x ^(2 )+ y ^(2 ) & = 1  \  " LHS " & = lr(\( frac(3 ,4 )\) )^(2 )+ lr(\( frac(sqrt(5 ),4 )\) )^(2 ) \  & = frac(9 ,16 )+ frac(5 ,16 ) \  & = frac(14 ,16 )   $

$  frac(14 ,16 ) !=  1   $

∴ The point is not on the unit circle.

1 mark for justification

1 mark

#pagebreak()

= Question 38

Determine which term contains $x ^(5 )$ in the binomial expansion of $lr(\( 2  x + frac(3 ,x )\) )^(11 )$.

== Solution

Method 1

$x ^(11 )\,lr(\( x ^(10 )\) )lr(\( frac(1 ,x )\) )\,lr(\( x ^(9 )\) )lr(\( frac(1 ,x ^(2 ))\) )\, dots.h $

$x ^(11 )\, x ^(9 )\, x ^(7 )\, dots.h $

∴ The fourth term contains $x ^(5 )$.

1 mark for determining a pattern

1 mark for fourth term

\(or a term consistent with the pattern\)

2 marks

Method 2

$\(x \)^(11 - k )lr(\( x ^(- 1 )\) )^(k )= x ^(5 )$

$x ^(11 - 2  k )= x ^(5 )$

$11 - 2  k = 5 $

$6 = 2  k $

$k = 3 $

∴ The fourth term contains $x ^(5 )$.

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $k $

1 mark for fourth term

\(or a term consistent with the value of $k $ \)

2 marks

#pagebreak()

= Question 39

Sketch the graph of $y = 2 lr(\( 3 ^(x )\) )+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/e97237d6-bd89-41df-a227-5137b7812dd3-17_939_931_537_595.jpg", width: 43.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-33_932_956_576_243.jpg", width: 45.0%)

1 mark for shape of an increasing exponential function

1 mark for vertical stretch

1 mark for vertical translation

3 marks

#pagebreak()

= Question 40

Solve\, algebraically.

$  log  \(2  x + 1 \)= log  \(x - 2 \)+ 1   $

== Solution

Method 1

$   log  \(2  x + 1 \) & - log  \(x - 2 \)= 1  \  log  lr(\( frac(2  x + 1 ,x - 2 )\) ) & = 1  \  10 ^(1 ) & = frac(2  x + 1 ,x - 2 ) \  10  x - 20  & = 2  x + 1  \  8  x  & = 21  \  x  & = frac(21 ,8 )   $

1 mark for quotient law

1 mark for exponential form

2 marks

Method 2

$   log  \(2  x + 1 \) & = log  \(x - 2 \)+ log  10  \  log  \(2  x + 1 \) & = log  \(10 \(x - 2 \)\) \  2  x + 1  & = 10 \(x - 2 \) \  2  x + 1  & = 10  x - 20  \  21  & = 8  x  \  x  & = frac(21 ,8 )   $

$frac(1 ,2 )$ mark for logarithmic form

1 mark for product law

$frac(1 ,2 )$ mark for equating arguments

2 marks

#pagebreak()

= Question 41

Given the functions\, $f \(x \)= x + 2 $ and $g \(x \)= x - 2 $\,

a\) state the equation of $h \(x \)= f \(x \) bullet  g \(x \)$.

b\) sketch the graph of $h \(x \)= f \(x \) dot.c  g \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/e97237d6-bd89-41df-a227-5137b7812dd3-19_906_901_1228_610.jpg", width: 42.4%)

== Solution

a\) $h \(x \)= \(x + 2 \)\(x - 2 \)$

or

$  h \(x \)= x ^(2 )- 4   $

b\)



#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/ebd6325a-af89-422d-b2be-1478c91e6960-35_896_898_1222_245.jpg", width: 42.3%)

1 mark

1 mark for graph consistent with a\)

1 mark

#pagebreak()

= Question 42

Given $p \(x \)= - 2  x ^(3 )+ 3  x + 1 $\, determine the remainder when $p \(x \)$ is divided by $\(x - 2 \)$.

== Solution

Method 1

$   & p \(2 \)= - 2 \(2 \)^(3 )+ 3 \(2 \)+ 1  \  & p \(2 \)= - 2 \(8 \)+ 6 + 1  \  & p \(2 \)= - 9    $

1 mark for remainder theorem

1 mark

Method 2

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [-2 ], [0 ], [3 ], [1 ],
table.hline(stroke: .5pt),
[], [↓ ], [-4 ], [-8 ], [-10 ],
table.hline(stroke: .5pt),
[], [-2 ], [-4 ], [-5 ], [-9 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or any equivalent strategy\)

1 mark

∴ The remainder is . -9

#pagebreak()

= Question 43

Determine the equation of the sinusoidal function in the form $y = A  cos  \(B  x \)+ D $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2025-jan/assets/e97237d6-bd89-41df-a227-5137b7812dd3-21_981_1221_534_451.jpg", width: 57.5%)

$y = $

$\_ \_ \_ \_ $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$y = 6  cos  lr(\( frac(pi ,15 ) x \) )+ 4 $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[1 mark for the value of $A $
- \[1\] mark for the value of $B $ \( $frac(1 ,2 )$ mark for period\; $frac(1 ,2 )$ mark for consistent value of $B $ \)
- \[1\] mark for the value of $D $  ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 44

Determine the total number of arrangements of the letters in the word TORONTO.

State your answer as a whole number.

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[2!3! ], [$frac(1 ,2 )$ mark for 7! ],
table.hline(stroke: .5pt),
[], [],
table.hline(stroke: .5pt),
[$7  dot.c  6  dot.c  5  dot.c  4  dot.c  3 ! $ ], [$frac(1 ,2 )$ mark for factorial expansion ],
table.hline(stroke: .5pt),
[2! 3! ], [],
table.hline(stroke: .5pt),
[$7  dot.c  6  dot.c  5  dot.c  4 $ ], [],
table.hline(stroke: .5pt),
[2 ], [],
table.hline(stroke: .5pt),
[$7  dot.c  6  dot.c  5  dot.c  2 $ ], [],
table.hline(stroke: .5pt),
[420 ], [$frac(1 ,2 )$ mark for consistent number of arrangements ],
table.hline(stroke: .5pt),
[], [2 marks ],
table.hline(stroke: .5pt),
[],
);