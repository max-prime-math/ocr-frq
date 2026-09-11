#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2016-jun

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

A wheel has a diameter of 20 cm and rotates through a central angle of $252 ^(degree )$.

Determine how far the wheel rolled.

== Solution

$   theta  & = lr(\( 252 ^(degree )\) )lr(\( frac(pi ,180 ^(degree ))\) ) \  & = frac(7  pi ,5 )   $

$  1  " mark for conversion "  $

$   s  & = theta  r  \  & = lr(\( frac(7  pi ,5 )\) )lr(\( frac(20 ,2 )\) ) \  & = 14  pi  upright(space.nobreak c m )   $

$  1  " mark for substitution "  $

$  2  " marks "  $

or

$  = 43.982  upright(space.nobreak c m )  $

#pagebreak()

= Question 2

Solve the following equation over the interval $\[0 \,2  pi \]$ :

$  3  sin  ^(2 ) theta - 10  sin  theta - 8 = 0   $

== Solution

$\(3  sin  theta + 2 \)\(sin  theta - 4 \)= 0 $

$sin  theta = - frac(2 ,3 ) quad  sin  theta = 4 $

$theta _(r )= 0.729728  quad $ No solution

$theta = 3.871 $

$theta = 5.553 $

1 mark for solving for $sin  theta $ \( $frac(1 ,2 )$ mark for each branch\)

2 marks for solving for $theta $ \( 1 mark for indicating no

solution\, $frac(1 ,2 )$ mark for each value\)

3 marks

#pagebreak()

= Question 3

Determine and simplify the fourth term in the expansion of $lr(\( 2  x ^(4 )- 3  y \) )^(8 )$.

== Solution

$   t _(4 ) & =  "" _(8 ) C _(3 )lr(\( 2  x ^(4 )\) )^(5 )\(- 3  y \)^(3 ) \  & = 56 lr(\( 32  x ^(20 )\) )lr(\( - 27  y ^(3 )\) ) \  & = - 48384  x ^(20 ) y ^(3 )   $

1 mark for simplification \( $frac(1 ,2 )$ mark for coefficient\, $frac(1 ,2 )$ mark for exponents\)

3 marks

#pagebreak()

= Question 4

Sheeva's bank is lending her $dollar  50000 $ at an annual interest rate of $6  % $\, compounded monthly\, to

purchase a car.

Given that the last payment will be a partial payment\, determine how many full monthly

payments of $dollar  800 $ Sheeva will have to make.

The formula below may be used.

$   & P  V = frac(R lr(\[ 1 - \(1 + i \)^(- n )\] ),i ) \  & " where " quad   P  V  & = " the present value of the amount borrowed " \  R  & = " the amount of each periodic payment " \  i  & = frac(" annual interest rate (as a decimal) "," the number of compounding periods per year ") \  n  & = " the number of equal periodic payments "    $

Express your answer as a whole number.

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[#table(stroke: none,
columns: 1,
align: (left, ),

[$50000 = frac(800 lr(\[ 1 - lr(\( 1 + frac(0.06 ,12 )\) )^(- n )\] ),frac(0.06 ,12 ))$ $   250  & = 800 lr(\[ 1 - \(1 + 0.005 \)^(- n )\] ) \  0.3125  & = 1 - 1.005 ^(- n ) \  - 0.6875  & = - 1.005 ^(- n ) \  0.6875  & = 1.005 ^(- n ) \  upright(space.nobreak g ) 0.6875  & = - n  log  1.005  \  frac(0.6875 ,upright(o g ) 1.005 ) & = n    $ ],
[$75.12588088 = n $ ],
[∴ 75 full monthly payments are needed ],
); ], [#table(stroke: none,
columns: 1,
align: (left, ),

[$frac(1 ,2 )$ mark for substitution ],
[$frac(1 ,2 )$ mark for simplification ],
[$frac(1 ,2 )$ mark for applying logarithms 1 mark for power law ],
[$frac(1 ,2 )$ mark for solving for $n $ ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 5

\(3007

An employee asked 10 people in an ice cream shop to wait in line.

Determine the number of different arrangements possible if two of the people\, Jamie and John\,

refused to stand next to each other in the line.

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[10!-9!2! ], [$frac(1 ,2 )$ mark for 10! 1 mark for product of 9 ! 2 ! \( $frac(1 ,2 )$ mark for 9 !\, $frac(1 ,2 )$ mark for 2 !\) $frac(1 ,2 )$ mark for subtraction ],
table.hline(stroke: .5pt),
[2903040 ], [2 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 6

The point $\(- 2 \,4 \)$ is on the graph of $f \(x \)$.

State the coordinates of the corresponding point when $f \(x \)$ is reflected over the $y $-axis.

== Solution

$\(2 \,4 \)$

1 mark

#pagebreak()

= Question 7

Given the graphs of $f \(x \)$ and $g \(x \)$\, sketch the graph of $\(f + g \)\(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-07_592_622_534_343.jpg", width: 29.3%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-07_590_613_534_1102.jpg", width: 28.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-07_596_622_1299_717.jpg", width: 29.3%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-07_597_617_1336_316.jpg", width: 29.0%)

1 mark for operation of addition

1 mark for restricted domain

2 marks

#pagebreak()

= Question 8

Using the laws of logarithms\, fully expand the expression:

$  log  _(2 )lr(\( frac(w ^(3 ) x ,y - 1 )\) )  $

== Solution

$3  log  _(2 ) w + log  _(2 ) x - log  _(2 )\(y - 1 \)$

1 mark for power law

1 mark for product law

1 mark for quotient law

3 marks

#pagebreak()

= Question 9

Solve the following equation algebraically for $theta $\, where $0  <=  theta  <=  2  pi $ :

$  2  cos  2  theta = 1   $

== Solution

Method 1

$   2 lr(\( 2  cos  ^(2 ) theta - 1 \) ) & = 1  \  4  cos  ^(2 ) theta - 2  & = 1  \  cos  ^(2 ) theta  & = frac(3 ,4 ) \  cos  theta  & =  plus.minus  frac(sqrt(3 ),2 ) \  cos  theta  & = - frac(sqrt(3 ),2 ) \  frac(1  pi ,6 ) quad  theta  & = frac(5  pi ,6 )\, frac(7  pi ,6 )   $

1 mark for substitution of an appropriate identity

1 mark for solving for $cos  theta $ \( $frac(1 ,2 )$ mark for each value\)

2 marks \( $frac(1 ,2 )$ mark for each value of $theta $ \)

4 marks

Method 2

$   2 lr(\( 1 - 2  sin  ^(2 ) theta \) ) & = 1  & & 1  " mark for substitution of an appropriate identity " \  2 - 4  sin  ^(2 ) theta  & = 1  & & \  - 4  sin  ^(2 ) theta  & = - 1  & & \  sin  ^(2 ) theta  & = frac(1 ,4 ) & & \  sin  theta  & =  plus.minus  frac(1 ,2 ) & & \  sin  theta  & = - frac(1 ,2 ) & & 1  " mark for solving for " sin  theta lr(\( frac(1 ,2 ) " mark for each value "\) ) \  theta  & = frac(7  pi ,6 )\, frac(11  pi ,6 ) & & 2  " marks "lr(\( frac(1 ,2 ) " mark for each value of " theta \) )   $

Note\(s\):

- Deduct a maximum of 1 mark if student omits second branch when taking the square root.

#pagebreak()

= Question 10

Given the graph of $y = f \(x \)$\, sketch the graph of $y = 2 | f \(x - 1 \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-10_693_699_472_309.jpg", width: 32.9%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-10_704_708_1314_309.jpg", width: 33.3%)

The graph of

$f \(x \)$ has

already been

drawn for your

reference.

No marks will

be awarded for

the graph of

$f \(x \)$.

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-10_690_700_1422_232.jpg", width: 32.9%)

1 mark for vertical stretch

1 mark for horizontal translation

1 mark for absolute value

3 marks

#pagebreak()

= Question 11

Prove the identity for all permissible values of $theta $ :

$  cos  theta + tan  theta  sin  theta = frac(tan  theta  sin  theta ,1 - cos  ^(2 ) theta )  $

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
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
[$   & cos  theta + tan  theta  sin  theta  \  & cos  theta + frac(sin  theta ,cos  theta ) sin  theta  \  & cos  theta + frac(sin  ^(2 ) theta ,cos  theta ) \  & frac(cos  ^(2 ) theta + sin  ^(2 ) theta ,cos  theta ) \  & frac(1 ,cos  theta )   $ ], [$   & frac(tan  theta  sin  theta ,1 - cos  ^(2 ) theta ) \  & frac(frac(sin  theta ,cos  theta ) dot.c  sin  theta ,sin  ^(2 ) theta ) \  & frac(sin  ^(2 ) theta ,cos  theta ) dot.c  frac(1 ,sin  ^(2 ) theta ) \  & frac(1 ,cos  theta )   $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 12

Raoul has 8 shirts\, 5 pairs of pants\, and 3 hats. He adds the options together and determines that

he has 16 different outfits to wear.

Raoul made an error in calculating the number of different outfits. Describe how to determine the

correct number of outfits.

== Solution

Raoul should have multiplied the number of clothing items to determine the total number of outfits.

#pagebreak()

= Question 13

Given $f \(x \)= 2  x - 1 $ and $g \(x \)= x ^(2 )+ 1 $ :

a\) Determine $f \(x \) dot.c  g \(x \)$.

b\) Determine $g \(g \(x \)\)$.

== Solution

a\)

$   f \(x \) dot.c  g \(x \) & = \(2  x - 1 \)lr(\( x ^(2 )+ 1 \) ) \  & = 2  x ^(3 )+ 2  x - x ^(2 )- 1  \  & = 2  x ^(3 )- x ^(2 )+ 2  x - 1    $

1 mark for product

1 mark

b\)

$   g \(g \(x \)\) & = lr(\( x ^(2 )+ 1 \) )^(2 )+ 1  \  & = x ^(4 )+ 2  x ^(2 )+ 1 + 1  \  & = x ^(4 )+ 2  x ^(2 )+ 2    $

1 mark for composition

1 mark

#pagebreak()

= Question 14

Given the graph of $y = f \(x \)$\, sketch the graph of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-14_817_863_468_302.jpg", width: 40.6%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/5a195c7d-e898-4531-ae64-e47834c0e2db-14_818_880_1445_300.jpg", width: 41.4%)

The graph of

$f \(x \)$ has

already been

drawn for your

reference.

No marks will

be awarded for

the graph of

$f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-14_801_872_1467_185.jpg", width: 41.0%)

1 mark for restricting the domain

$frac(1 ,2 )$ mark for shape between invariant points

$frac(1 ,2 )$ mark for shape to the left of invariant points

2 marks

#pagebreak()

= Question 15

Given the polynomial function $P \(x \)= x ^(4 )- 5  x ^(2 )- 2  x + 6 $\, if $P \(1 \)= 0 $\, identify which statement

is true.

*A.*

The $y $-intercept is 1 .

*B.*

$P \(x \)$ has a factor of $\(x + 1 \)$.

*C.*

The graph has a zero at 1 .

*D.*

The graph has a zero at -1 .

== Solution

Correct answer: C

The graph has a zero at 1 .

#pagebreak()

= Question 16

There are 6 different books that are being distributed evenly amongst three people.

Identify which expression represents the number of possible combinations.

*A.*

$ "" _(6 ) C _(2 ) dot.c  "" _(6 ) C _(2 ) dot.c  "" _(6 ) C _(2 )$

*B.*

$ "" _(6 ) C _(2 ) dot.c  "" _(4 ) C _(2 ) dot.c  "" _(2 ) C _(2 )$

*C.*

$ "" _(2 ) C _(2 ) dot.c  "" _(2 ) C _(2 ) dot.c  "" _(2 ) C _(2 )$

*D.*

$3  dot.c  "" _(6 ) C _(2 )$

== Solution

Correct answer: B

$ "" _(6 ) C _(2 ) dot.c  "" _(4 ) C _(2 ) dot.c  "" _(2 ) C _(2 )$

#pagebreak()

= Question 17

Identify the graph that corresponds to the function $f \(x \)= - sqrt(\(x - 2 \))$.

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-02_430_470_537_317.jpg", width: 22.1%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-02_424_465_537_1061.jpg", width: 21.9%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-02_424_467_1061_320.jpg", width: 22.0%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-02_424_471_1052_1074.jpg", width: 22.2%)

== Solution

Correct answer: D

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-02_424_471_1052_1074.jpg", width: 22.2%)

#pagebreak()

= Question 18

Solve:

$  7 ^(log  _(7 ) 2 )= x   $

*A.*

$x = 1 $

*B.*

$x = 2 $

*C.*

$x = 7 $

*D.*

$x = 49 $

== Solution

Correct answer: B

$x = 2 $

#pagebreak()

= Question 19

Identify the equation that has a general solution of $lr( mat(delim: #none, theta = frac(pi ,6 )+ 2  pi  k  "" ; theta = frac(5  pi ,6 )+ 2  pi  k )\} )$ where $k  in  bb(Z )$.

*A.*

$sin  theta = frac(1 ,2 )$

*B.*

$cos  theta = frac(1 ,2 )$

*C.*

$sin  theta = frac(sqrt(3 ),2 )$

*D.*

$cos  theta = frac(sqrt(3 ),2 )$

== Solution

Correct answer: A

$sin  theta = frac(1 ,2 )$

#pagebreak()

= Question 20

Identify the function that has a domain of $x  <= - 2 $ and a range of $y  >=  3 $.

*A.*

$y = sqrt(x + 2 )+ 3 $

*B.*

$y = sqrt(- \(x + 2 \))+ 3 $

*C.*

$y = - sqrt(x - 2 )- 3 $

*D.*

$y = - sqrt(- \(x - 2 \))- 3 $

== Solution

Correct answer: B

$y = sqrt(- \(x + 2 \))+ 3 $

#pagebreak()

= Question 21

Given $f \(x \)= 3  x + 2 $\, identify $f ^(- 1 )\(x \)$.

*A.*

$f ^(- 1 )\(x \)= - 3  x - 2 $

*B.*

$f ^(- 1 )\(x \)= 2  x + 3 $

*C.*

$f ^(- 1 )\(x \)= frac(x ,3 )- 2 $

*D.*

$f ^(- 1 )\(x \)= frac(x - 2 ,3 )$

== Solution

Correct answer: D

$f ^(- 1 )\(x \)= frac(x - 2 ,3 )$

#pagebreak()

= Question 22

Identify a possible value for the angle $theta $ sketched in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-04_396_405_1626_279.jpg", width: 19.1%)

*A.*

2

*B.*

3

*C.*

4

*D.*

5

== Solution

Correct answer: C

4

#pagebreak()

= Question 23

Solve the following equation:

$  log  _(3 )\(x + 3 \)+ log  _(3 )\(x - 5 \)= 2   $

== Solution

$   log  _(3 )\[\(x + 3 \)\(x - 5 \)\] & = 2  \  \(x + 3 \)\(x - 5 \) & = 3 ^(2 ) \  x ^(2 )- 2  x - 15  & = 9  \  x ^(2 )- 2  x - 24  & = 0  \  \(x - 6 \)\(x + 4 \) & = 0    $

$  x = 6  quad  x > < 4   $

1 mark for product law

1 mark for exponential form

$frac(1 ,2 )$ mark for solving for $x $

$frac(1 ,2 )$ mark for rejecting extraneous root

3 marks

#pagebreak()

= Question 24

State a coterminal angle for $theta = frac(9  pi ,4 )$.

== Solution

$  frac(9  pi ,4 )+ frac(8  pi ,4 )= frac(17  pi ,4 )  $

1 mark

$  405 ^(degree )- 360 ^(degree )= 45 ^(degree )  $

Note\(s\):

- Other answers are possible.

#pagebreak()

= Question 25

Sketch the graph of the function $f \(x \)= frac(2  x + 2 ,x ^(2 )- 1 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-07_924_981_595_483.jpg", width: 46.2%)

== Solution

$   f \(x \) & = frac(2 \(x + 1 \),\(x - 1 \)\(x + 1 \)) \  & = frac(2 ,x - 1 )   $

∴ there is a point of discontinuity \(hole\) at $\(- 1 \,- 1 \)$

vertical asymptote at $x = 1 $

horizontal asymptote at $y = 0 $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-21_808_997_1242_146.jpg", width: 46.9%)

1 mark for asymptotic behaviour at $x = 1 $

1 mark for asymptotic behaviour at $y = 0 $

1 mark for point of discontinuity \(hole\) at

$\(- 1 \,- 1 \)lr(\( frac(1 ,2 ) )$ mark for $x = - 1 \, frac(1 ,2 )$ mark for

$y = - 1 $ \)

$frac(1 ,2 )$ mark for graph left of $x = 1 $

$frac(1 ,2 )$ mark for graph right of $x = 1 $

4 marks

#pagebreak()

= Question 26

Justify why the binomial expansion of $lr(\( x + x ^(3 )\) )^(7 )$ does not have a term containing $x ^(10 )$.

== Solution

Method 1

$\(x \)^(7 )\,\(x \)^(6 )lr(\( x ^(3 )\) )^(1 )\,\(x \)^(5 )lr(\( x ^(3 )\) )^(2 )\, dots.h $

$x ^(7 )\, x ^(9 )\, x ^(11 )\, dots.h $

The exponents increase by 2 .

Therefore $x ^(10 )$ is not in the pattern.

1 mark for determining the pattern

1 mark for justification

2 marks

Method 2

$x ^(7 - r )lr(\( x ^(3 )\) )^(r )= x ^(10 )$

$  x ^(7 + 2  r )= x ^(10 )  $

$  7 + 2  r = 10   $

$  2  r = 3   $

$  r = frac(3 ,2 )  $

The binomial expansion does not contain $x ^(10 )$

because the value of $r $ must be a whole number.

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $r $

1 mark for justification

2 marks

#pagebreak()

= Question 27

Sketch the graph of $y = - sin  lr(\( frac(pi ,2 )\(x - 1 \)\) )+ 3 $ over the domain $\[0 \,6 \]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-09_924_1477_653_249.jpg", width: 69.5%)

== Solution

period $= frac(2  pi ,frac(pi ,2 ))= 4 $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-23_498_900_902_191.jpg", width: 42.4%)

1 mark for vertical reflection

1 mark for horizontal translation

1 mark for period

1 mark for vertical translation

4 marks

Note\(s\):

- Deduct $frac(1 ,2 )$ mark if the domain \[0\, 6\] is not completely sketched.

#pagebreak()

= Question 28

When $P \(x \)= 3  x ^(4 )- k  x ^(3 )+ 5  x - 14 $ is divided by $\(x + 2 \)$\, the remainder is -8 .

Determine the value of $k $.

== Solution

Method 1

$   x  & = - 2  \  - 8  & = 3 \(- 2 \)^(4 )- k \(- 2 \)^(3 )+ 5 \(- 2 \)- 14  \  - 8  & = 48 + 8  k - 10 - 14  \  - 8  & = 24 + 8  k  \  - 32  & = 8  k  \  k  & = - 4    $

$frac(1 ,2 )$ mark for $x = - 2 $

1 mark for remainder theorem

$frac(1 ,2 )$ mark for solving for $k $

2 marks

Method 2

#table(stroke: none,
columns: 6,
align: (left, left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5), table.vline(stroke: .5pt, x: 6),
table.hline(stroke: .5pt),
[-2 ], [3 ], [-k ], [0 ], [5 ], [-14 ],
table.hline(stroke: .5pt),
[], [↓ ], [-6 ], [$2  k + 12 $ ], [$- 4  k - 24 $ ], [$8  k + 38 $ ],
table.hline(stroke: .5pt),
[], [3 ], [$- k - 6 $ ], [$2  k + 12 $ ], [$- 4  k - 19 $ ], [$8  k + 24 $ ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for $x = - 2 $

1 mark for synthetic division

\(or any other equivalent

strategy\)

$frac(1 ,2 )$ mark for solving for $k $

2 marks

#pagebreak()

= Question 29

a\) 3 marks

b\) 1 mark

Given that $cos  alpha = frac(7 ,12 )$ where $alpha $ is in quadrant IV\, and $sin  beta = frac(3 ,5 )$ where $beta $ is in quadrant I\,

determine the exact value of:

a\) $quad  sin  \(alpha - beta \)$

b\) $csc  \(alpha - beta \)$

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-25_359_374_887_262.jpg", width: 17.6%)

$   5 ^(2 )- 3 ^(2 ) & = x ^(2 ) \  16  & = x ^(2 ) \  plus.minus  4  & = x    $

$   & 1  \/ 2  " mark for value of " x  \  & 1  \/ 2  " mark for value of " y    $

$   & = lr(\( frac(- sqrt(95 ),12 )\) )lr(\( frac(4 ,5 )\) )- lr(\( frac(7 ,12 )\) )lr(\( frac(3 ,5 )\) ) \  & = frac(- 4  sqrt(95 ),60 )- frac(21 ,60 ) \  & = frac(- 4  sqrt(95 )- 21 ,60 )   $

3 marks

b\) $quad  csc  \(alpha - beta \)= frac(60 ,- 4  sqrt(95 )- 21 )$

1 mark

Note\(s\):

- accept any of the following values for $x :  x =  plus.minus  4 $\, or $x = 4 $

- accept any of the following values for $y :  y =  plus.minus  sqrt(95 )\, y = sqrt(95 )$\, or $y = - sqrt(95 )$

#pagebreak()

= Question 30

Describe the difference between the graph of $f \(x \)= frac(7 \(x + 2 \),x + 2 )$ and the graph of

$g \(x \)= frac(7 \(x - 2 \),x + 2 )$ at $x = - 2 $.

== Solution

The graph of $f \(x \)= frac(7 \(x + 2 \),x + 2 )$ has a point of discontinuity and the graph of $g \(x \)= frac(7 \(x - 2 \),x + 2 )$ has an

asymptote.

1 mark

#pagebreak()

= Question 31

Sketch the graph of $f \(x \)= 3 ^(x )+ 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-13_1107_1103_623_436.jpg", width: 51.9%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-27_846_889_587_189.jpg", width: 41.8%)

1 mark for increasing exponential function

1 mark for asymptotic behaviour at $y = 2 $

2 marks

#pagebreak()

= Question 32

Solve algebraically:

$   "" _(n ) C _(3 )= n - 2   $

== Solution

#table(stroke: none,
columns: 1,
align: (left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1),
table.hline(stroke: .5pt),
[$frac(n ! ,\(n - 3 \)! 3 ! )= n - 2 $ ],
table.hline(stroke: .5pt),
[$frac(n \(n - 1 \)\(n - 2 \)\(n - 3 \)! ,\(n - 3 \)! 3 ! )= n - 2 $ ],
table.hline(stroke: .5pt),
[$n \(n - 1 \)= 6 $ ],
table.hline(stroke: .5pt),
[$n ^(2 )- n - 6 = 0 $ ],
table.hline(stroke: .5pt),
[$\(n - 3 \)\(n + 2 \)= 0 $ ],
table.hline(stroke: .5pt),
[$n = 3 $ ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for substitution

1 mark for factorial expansion

$frac(1 ,2 )$ mark for simplification of factorials

$frac(1 ,2 )$ mark for rejecting extraneous root

$frac(1 ,2 )$ mark for the value of $n $

3 marks

#pagebreak()

= Question 33

Describe the error that was made when solving the following equation:

$   & sin  ^(2 ) theta + sin  theta - 2 = 1  \  & sin  ^(2 ) theta + sin  theta = 3  \  & sin  theta \(sin  theta + 1 \)= 3  \  & sin  theta = 3  quad  sin  theta + 1 = 3  \  & mat(delim: #none,  " sin " theta = 2  "" ; " \u2234 No solution " quad  therefore  " No solution " )   $

== Solution

The student did not apply the zero product principle before factoring.

#pagebreak()

= Question 34

Sketch the graph of the polynomial function with the following characteristics.

- a $y $-intercept of -9

- zeroes at -1 and 3

- the zero at -1 has a multiplicity of 1 and the zero at 3 has a multiplicity of 2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-16_1445_1406_713_309.jpg", width: 66.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-30_874_920_773_153.jpg", width: 43.3%)

1 mark for $x $-intercepts

$frac(1 ,2 )$ mark for $y $-intercept

1 mark for multiplicity \( $frac(1 ,2 )$ mark for multiplicity

at $x = 3 \, frac(1 ,2 )$ mark for multiplicity at $x = - 1 $ \)

$frac(1 ,2 )$ mark for shape of a cubic function

3 marks

#pagebreak()

= Question 35

Given $cot  theta = - frac(1 ,3 )$\, where $theta $ is in quadrant II\, determine the exact value of $sin  theta $.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-31_541_587_612_221.jpg", width: 27.6%)

$   cot  theta  & = frac(x ,y ) \  r ^(2 ) & = x ^(2 )+ y ^(2 ) \  r ^(2 ) & = \(- 1 \)^(2 )+ \(3 \)^(2 ) \  r ^(2 ) & = 10  \  r  & =  plus.minus  sqrt(10 ) \  sin  theta  & = frac(3 ,sqrt(10 ))   $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $r $

1 mark for $sin  theta $ \( $frac(1 ,2 )$ mark for the quadrant\, $frac(1 ,2 )$ mark for the value\)

2 marks

Note\(s\):

- accept any of the following values for $r :  r =  plus.minus  sqrt(10 )\, r = sqrt(10 )$

#pagebreak()

= Question 36

Given the function $f \(x \)$\, sketch the graph of the reciprocal\, $frac(1 ,f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-18_919_946_517_571.jpg", width: 44.5%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-18_914_935_1555_367.jpg", width: 44.0%)

The graph of

$f \(x \)$ has

already been

drawn for your

reference.

No marks will

be awarded for

the graph of

$f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-32_902_928_1555_176.jpg", width: 43.7%)

1 mark for asymptotic behaviour at $x = 1 $

$frac(1 ,2 )$ mark for graph left of vertical asymptote at

$x = 1 $

$frac(1 ,2 )$ mark for graph right of vertical asymptote

at $x = 1 $

2 marks

#pagebreak()

= Question 37

The volume of a planter\, in the shape of a rectangular prism\, can be modelled

by the polynomial function $V \(x \)= x ^(3 )+ 3  x ^(2 )- 34  x + 48 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-19_141_179_369_1624.jpg", width: 8.4%)

Determine the factors of the function\, $V \(x \)$\, which represent possible dimensions of this planter.

$V \(x \)= $

$\_ \_ \_ \_ $

== Solution

$  2 ^(3 )+ 3 \(2 \)^(2 )- 34 \(2 \)+ 48 = 0   $

$therefore  x - 2 $ is a factor

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [1 ], [3 ], [-34 ], [48 ],
table.hline(stroke: .5pt),
[], [↓ ], [2 ], [10 ], [-48 ],
table.hline(stroke: .5pt),
[], [1 ], [5 ], [-24 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for identifying one possible value of $x $

1 mark for synthetic division \(or any other equivalent strategy\)

$   & V \(x \)= \(x - 2 \)lr(\( x ^(2 )+ 5  x - 24 \) ) \  & V \(x \)= \(x - 2 \)\(x + 8 \)\(x - 3 \)   $

1 mark for identifying all factors

3 marks

#pagebreak()

= Question 38

Describe how to determine the range of the inverse of the following graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-20_617_646_507_328.jpg", width: 30.4%)

== Solution

The domain of the graph becomes the range of the inverse.

#pagebreak()

= Question 39

Sketch the graph of the function $y = sqrt(2  x )+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-21_768_796_526_590.jpg", width: 37.5%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/d40a5513-7bb4-48ff-98e6-c9f731122cdf-35_587_645_576_196.jpg", width: 30.4%)

1 mark for shape of a radical function

1 mark for vertical translation

1 mark for horizontal compression

3 marks

#pagebreak()

= Question 40

Given the following characteristics of a sinusoidal function:

- an amplitude of 2

- a vertical translation down 3 units

- a period of $frac(pi ,4 )$

a\) Determine an equation of this sinusoidal function in the form $y = a  sin  b \(x - c \)+ d $.

b\) Determine the range of this function.

Range:

== Solution

a\)

$   & b = frac(2  pi ,frac(pi ,4 )) \  & b = 8  \  & y = 2  sin  \(8  x \)- 3    $

1 mark for the value of $b $

$frac(1 ,2 )$ mark for amplitude

$frac(1 ,2 )$ mark for vertical translation

2 marks

b\) Range: $\{ y  divides  y  in  bb(R )\,- 5  <=  y  <= - 1 \} $

or

Range:

$  \[- 5 \,- 1 \]  $

#pagebreak()

= Question 41

Suah was given the graph of $f \(x \)$ and asked to graph $y = sqrt(f \(x \))$.

Her solution is given on the graph below.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jun/assets/f7f6f5b8-fb73-4d72-a6ed-6798c349679a-23_751_716_586_262.jpg", width: 33.7%)

Describe the error Suah made when sketching the graph of $y = sqrt(f \(x \))$.

== Solution

Suah's graph did not cross the invariant point at $y = 1 $.

#pagebreak()

= Question 42

Solve:

$  9 ^(2  x + 1 )= 27 ^(x )  $

== Solution

$3 ^(2 \(2  x + 1 \))= 3 ^(3  x )$

$  3 ^(4  x + 2 )= 3 ^(3  x )  $

$  4  x + 2 = 3  x   $

$  x = - 2   $

1 mark for changing to a common base

1 mark for exponent law \( $frac(1 ,2 )$ mark for each side\)

$frac(1 ,2 )$ mark for equating exponents

$frac(1 ,2 )$ mark for solving for $x $

3 marks