#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2015-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Convert $- frac(13  pi ,5 )$ to degrees.

== Solution

$   & - frac(13  pi ,5 ) times  frac(180 ^(degree ),pi ) \  & - 468 ^(degree )   $

#pagebreak()

= Question 2

圈

a\) 1 mark

b\) 1 mark

c\) 1 mark

a\) From a group of 9 people\, in how many ways can you select a committee of 4 members?

b\) From a group of 9 people\, in how many ways can you select a president\, a vice president\, a

secretary\, and a treasurer?

c\) Explain why the answers in a\) and b\) are different.

== Solution

a\) $ "" _(9 ) C _(4 )= 126 $ ways

1 mark for $ "" _(9 ) C _(4 )$

1 mark

b\) $ "" _(9 ) P _(4 )= 3024 $ ways

1 mark for $ "" _(9 ) P _(4 )$

1 mark

c\) Part a\) is a combination because the order does not matter\; part b\) is a permutation because

committee members have specific roles.

1 mark

#pagebreak()

= Question 3

A population of 500 bacteria will triple in 20 hours.

Using the formula given below\,

$A = P  e ^(r  t )$

$A = $ population after $t $ hours

$P = $ initial population

$r = $ rate of growth

$t = $ time in hours

a\) Determine the rate of growth\, $r $.

b\) Determine how many hours it will take for the initial population to double with the same rate

of growth.

== Solution

a\)

$   1500  & = 500  e ^(r \(20 \)) \  3  & = e ^(20  r ) \  ln  3  & = ln  e ^(20  r ) \  ln  3  & = 20  r  dot.c  ln  e  \  r  & = frac(ln  3 ,20 ) \  r  & = 0.054930614    $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for applying logarithms

$frac(1 ,2 )$ mark for power rule

$frac(1 ,2 )$ mark for evaluating quotient of logarithms

2 marks

b\)

$   1000  & = 500  e ^(0.054930614  t ) \  2  & = e ^(0.054930614  t ) \  ln  2  & = ln  e ^(0.054930614  t ) \  ln  2  & = 0.054930614  t  dot.c  ln  e  \  t  & = frac(ln  2 ,0.054930614 ) \  t  & = 12.619  " hours "   $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for applying logarithms

$frac(1 ,2 )$ mark for power rule

$frac(1 ,2 )$ mark for evaluating quotient of logarithms

#pagebreak()

= Question 4

DDID

Talla incorrectly solved the following trigonometric equation:

Solve: $2  sec  x - 5 = 0  \; 0 ^(degree ) <=  x  <=  360 ^(degree )$.

Talla's work:

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/f9e98f8f-f220-4959-adbb-a3fc0dda0c09-04_180_408_592_592.jpg", width: 19.2%)

No solution\, sec $x $ cannot be greater than 1 .

a\) Explain her error.

b\) Determine the correct solution.

== Solution

a\) Talla incorrectly stated that $sec  x $ cannot be greater than 1 .

The value of $cos  x $ cannot be greater than 1 .

b\) $sec  x = frac(5 ,2 )$

$   cos  x  & = frac(2 ,5 ) \  x _(r ) & = 66.421821  \  x  & = 66.422 ^(degree ) \  x  & = 293.578 ^(degree )   $

#pagebreak()

= Question 5

Simplify the 6th term in the expansion of:

$  lr(\( 2  x - frac(3 ,x ^(2 ))\) )^(10 )  $

== Solution

$   t _(6 ) & =  "" _(10 ) C _(5 )\(2  x \)^(5 )lr(\( - frac(3 ,x ^(2 ))\) )^(5 ) \  & = 252 lr(\( 32  x ^(5 )\) )lr(\( - frac(243 ,x ^(10 ))\) ) \  & = - 1959552  x ^(- 5 )   $

2 marks \(1 mark for $ "" _(10 ) C _(5 )\, frac(1 ,2 )$ mark for each consistent factor\)

1 mark for simplification \( $frac(1 ,2 )$ mark for coefficient\, $frac(1 ,2 )$ mark for exponent\)

3 marks

#pagebreak()

= Question 6

Determine the arc length subtended by a central angle if the diameter is 19 cm and the central

angle is 1.6 radians.

== Solution

$   & s = theta  r  \  & s = \(1.6 \)\(9.5 \) \  & s = 15.2  upright(space.nobreak c m )   $

#pagebreak()

= Question 7

Solve the following equation algebraically for $x $\, where $0  <=  x  <=  2  pi $.

$  2  cos  ^(2 ) x = - 3  sin  x   $

== Solution

$  2 lr(\( 1 - sin  ^(2 ) x \) )= - 3  sin  x   $

$  2 - 2  sin  ^(2 ) x = - 3  sin  x   $

$  0 = 2  sin  ^(2 ) x - 3  sin  x - 2   $

$  0 = \(2  sin  x + 1 \)\(sin  x - 2 \)  $

$  sin  x = - frac(1 ,2 )  $

No Solution

$  1  " mark for identity "  $

$  1  " mark for solving for " sin  x   $

1 mark for indicating no solution

1 mark for solving for $x $ \( $frac(1 ,2 )$ mark for

each value\)

4 marks

#pagebreak()

= Question 8

In how many different ways can you arrange the letters in the word VOLLEYBALL?

State your answer as a factorial.

== Solution

$  frac(10 ! ,4 ! )  $

1 mark

Note\(s\):

- award full marks for 151200

#pagebreak()

= Question 9

Is $\(x - 2 \)$ a factor of the polynomial $p \(x \)= - x ^(4 )- 3  x ^(3 )+ 11  x ^(2 )+ 3  x - 10 $ ?

Justify your response.

== Solution

Method 1

$   p \(2 \) & = - \(2 \)^(4 )- 3 \(2 \)^(3 )+ 11 \(2 \)^(2 )+ 3 \(2 \)- 10  \  & = - 16 - 24 + 44 + 6 - 10  \  & = 0    $

The remainder is zero\, so $\(x - 2 \)$ is a factor.

$frac(1 ,2 )$ mark for $p \(2 \)$

1 mark for the remainder theorem

$frac(1 ,2 )$ mark for justification

2 marks

Method 2

#table(stroke: none,
columns: 6,
align: (left, left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5), table.vline(stroke: .5pt, x: 6),
table.hline(stroke: .5pt),
[2 ], [-1 ], [-3 ], [11 ], [3 ], [-10 ],
table.hline(stroke: .5pt),
[], [↓ ], [-2 ], [-10 ], [2 ], [10 ],
table.hline(stroke: .5pt),
[], [-1 ], [-5 ], [1 ], [5 ], [L0 ],
table.hline(stroke: .5pt),
[],
);

The remainder is zero\, so $\(x - 2 \)$ is a factor.

$frac(1 ,2 )$ mark for $x = 2 $

1 mark for synthetic division

\(or for any equivalent strategy\)

$frac(1 ,2 )$ mark for justification

2 marks

Method 3

I entered $y = - x ^(4 )- 3  x ^(3 )+ 11  x ^(2 )+ 3  x - 10 $ into my calculator

and located the zeroes.

$x = 2 $ was a zero\, which means $\(x - 2 \)$ is a factor.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-09_397_578_2166_309.jpg", width: 27.2%)

1 mark for graphing calculator method

1 mark for relating the zeroes to the

factors

2 marks

#pagebreak()

= Question 10

Determine the period of the sinusoidal function $y = frac(1 ,2 ) sin  lr(\( frac(1 ,3 ) x \) )$.

State your answer in radians.

== Solution

$   & p = frac(2  pi ,| upright(space.nobreak b )| ) \  & p = frac(2  pi ,lr(|  frac(1 ,3 )|  )) \  & p = 6  pi  quad  " or " quad  p = 18.850    $

$frac(1 ,2 )$ mark for correct value of $b $

$frac(1 ,2 )$ mark for period consistent with b

1 mark

#pagebreak()

= Question 11

The domain of $f \(x \)$ is $x  <=  2 $. The domain of $g \(x \)$ is $x  >= - 7 $.

State the domain of $f \(x \)+ g \(x \)$.

Justify your answer.

== Solution

Both $f \(x \)$ and $g \(x \)$ have restricted domains\, so both domains need to be considered.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-11_251_896_916_188.jpg", width: 42.2%)

The solution is the intersection of the two domains.

$  \{ x  divides  x  in  bb(R )\,- 7  <=  x  <=  2 \}  quad  " or " quad \[- 7 \,2 \]  $

1 mark for justification

1 mark for domain

2 marks

#pagebreak()

= Question 12

Prove the identity below for all permissible values of $theta $.

$  frac(1 ,1 + cos  theta )= csc  ^(2 ) theta - frac(cot  theta ,sin  theta )  $

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

Method 1

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ], [],
table.hline(stroke: .5pt),
[$frac(1 ,1 + cos  theta )$ ], [$   & csc  ^(2 ) theta - frac(cot  theta ,sin  theta ) \  & frac(1 ,sin  ^(2 ) theta )- frac(frac(cos  theta ,sin  theta ),sin  theta ) \  & frac(1 ,sin  ^(2 ) theta )- frac(cos  theta ,sin  theta ) dot.c  frac(1 ,sin  theta ) \  & frac(1 ,sin  ^(2 ) theta )- frac(cos  theta ,sin  ^(2 ) theta ) \  & frac(1 - cos  theta ,sin  ^(2 ) theta ) \  & frac(1 - cos  theta ,1 - cos  ^(2 ) theta ) \  & frac(1 - cos  theta ,\(1 - cos  theta \)\(1 + cos  theta \)) \  & frac(1 ,1 + cos  theta )   $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[1 mark for correct substitution of identities ],
[1 mark for algebraic strategies ],
[1 mark for logical process to prove an identity ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

Method 2

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   & frac(1 ,1 + cos  theta )\(1 - cos  theta \) \  & frac(1 - cos  theta ,1 - cos  ^(2 ) theta ) \  & frac(1 - cos  theta ,sin  ^(2 ) theta ) \  & frac(1 ,sin  ^(2 ) theta )- frac(cos  theta ,sin  ^(2 ) theta ) \  & csc  ^(2 ) theta - frac(cos  theta ,sin  theta ) dot.c  frac(1 ,sin  theta ) \  & csc  ^(2 ) theta - frac(cot  theta ,sin  theta )   $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[$  csc  ^(2 ) theta - frac(cot  theta ,sin  theta )  $ ],
[1 mark for algebraic strategies ],
[1 mark for correct substitution of identities ],
[1 mark for logical process to prove an identity ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 13

Explain how the end behaviours of the graphs of polynomial functions with an even degree and

with an odd degree are different.

== Solution

When the degree is odd\, the end behaviour is in opposite directions.

When the degree is even\, the end behaviour is in the same direction.

#pagebreak()

= Question 14

Given the graphs of $f \(x \)$ and $g \(x \)$\, sketch the graph of $g \(x \)- f \(x \)$.

$f \(x \)$

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/f9e98f8f-f220-4959-adbb-a3fc0dda0c09-14_671_665_526_279.jpg", width: 31.3%)

$g \(x \)$

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/f9e98f8f-f220-4959-adbb-a3fc0dda0c09-14_667_667_526_1102.jpg", width: 31.4%)

$  g \(x \)- f \(x \)  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/f9e98f8f-f220-4959-adbb-a3fc0dda0c09-14_673_665_1366_708.jpg", width: 31.3%)

== Solution

#table(stroke: none,
columns: 4,
align: (left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4),
table.hline(stroke: .5pt),
[$x $ ], [$g \(x \)$ ], [$f \(x \)$ ], [$\(g - f \)\(x \)$ ],
table.hline(stroke: .5pt),
[-4 ], [4 ], [-1 ], [5 ],
table.hline(stroke: .5pt),
[-2 ], [6 ], [2 ], [4 ],
table.hline(stroke: .5pt),
[0 ], [4 ], [5 ], [-1 ],
table.hline(stroke: .5pt),
[2 ], [4 ], [8 ], [-4 ],
table.hline(stroke: .5pt),
[],
);

1 mark for subtraction of $g \(x \)- f \(x \)$

1 mark for restricting domain on graph

2 marks

$g \(x \)- f \(x \)$

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-15_633_663_1362_1041.jpg", width: 31.2%)

#pagebreak()

= Question 15

Given $f \(x \)= - 3  x + 7 $\, evaluate $f ^(- 1 )\(- 2 \)$.

== Solution

Let $y = f \(x \)$

$  f \(x \)= - 3  x + 7   $

$  y = - 3  x + 7   $

$  x = - 3  y + 7   $

$  1  " mark for switching " x  " and " y   $

$  x - 7 = - 3  y   $

$  y = frac(x - 7 ,- 3 )  $

$  f ^(- 1 )\(x \)= frac(x - 7 ,- 3 )  $

$  1  \/ 2  " mark for " f ^(- 1 )\(x \)  $

$  f ^(- 1 )\(- 2 \)= frac(- 2 - 7 ,- 3 )  $

$  f ^(- 1 )\(- 2 \)= 3   $

$  1  \/ 2  " mark for " f ^(- 1 )\(- 2 \)  $

2 marks

#pagebreak()

= Question 16

How many terms are there in the expansion of $lr(\( x ^(12 )+ 3 \) )^(10 )$ ?

*A.*

9

*B.*

10

*C.*

11

*D.*

12

== Solution

Correct answer: C

11

#pagebreak()

= Question 17

A co-terminal angle for $theta = frac(11  pi ,3 )$ in the domain $- 2  pi  <=  theta  <=  0 $ would be:

*A.*

$- frac(5  pi ,3 )$

*B.*

$- frac(pi ,3 )$

*C.*

$frac(pi ,3 )$

*D.*

$frac(5  pi ,3 )$

== Solution

Correct answer: B

$- frac(pi ,3 )$

#pagebreak()

= Question 18

The $x $-intercept of the graph of $y = 3 ^(x )- 1 $ is:

*A.*

-1

*B.*

0

*C.*

1

*D.*

2

== Solution

Correct answer: B

0

#pagebreak()

= Question 19

If $ "" _(n ) C _(5 )=  "" _(n ) C _(3 )$\, the value of $n $ must be:

*A.*

3

*B.*

5

*C.*

8

*D.*

15

== Solution

Correct answer: C

8

#pagebreak()

= Question 20

What is the domain of the function $f \(x \)= sqrt(- \(x + 1 \))$ ?

*A.*

$\{ x  divides  x  in  bb(R )\, x  != - 1 \} $

*B.*

$\{ x  divides  x  in  bb(R )\, x  >= - 1 \} $

*C.*

$\{ x  divides  x  in  bb(R )\, x  <= - 1 \} $

*D.*

$\{ x  divides  x  in  bb(R )\} $

== Solution

Correct answer: C

$\{ x  divides  x  in  bb(R )\, x  <= - 1 \} $

#pagebreak()

= Question 21

1 mark

Identify a non-permissible value of $x $ for the expression $frac(1 ,cos  2  x )$.

*A.*

0

*B.*

$frac(pi ,4 )$

*C.*

$frac(pi ,2 )$

*D.*

$pi $

== Solution

Correct answer: B

$frac(pi ,4 )$

#pagebreak()

= Question 22

The expression $2  log  x - frac(1 ,3 ) log  y $ as a single logarithm is:

*A.*

$quad  log  frac(x ^(2 ),root(3 ,y ))$

*B.*

$quad  log  frac(2  x ,3  y )$

*C.*

$- log  x ^(2 ) root(3 ,y )$

*D.*

$quad  log  lr(\( x ^(2 )- root(3 ,y )\) )$

== Solution

Correct answer: A

$quad  log  frac(x ^(2 ),root(3 ,y ))$

#pagebreak()

= Question 23

1 mark

The point $upright(P )\(theta \)$ lies on the unit circle. What are the coordinates of the point if $theta = 300 ^(degree )$ ?

*A.*

$lr(\( frac(1 ,2 )\, frac(sqrt(3 ),2 )\) )$

*B.*

$lr(\( - frac(1 ,2 )\, frac(sqrt(3 ),2 )\) )$

*C.*

$lr(\( frac(sqrt(3 ),2 )\,- frac(1 ,2 )\) )$

*D.*

$lr(\( frac(1 ,2 )\,- frac(sqrt(3 ),2 )\) )$

== Solution

Correct answer: D

$lr(\( frac(1 ,2 )\,- frac(sqrt(3 ),2 )\) )$

#pagebreak()

= Question 24

What is the degree of the polynomial function represented by the graph below?

*A.*

2

*B.*

3

*C.*

4

*D.*

5

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-04_831_703_429_1142.jpg", width: 33.1%)

== Solution

Correct answer: C

4

#pagebreak()

= Question 25

When the point $\(- 4 \,- 3 \)$ is reflected in the line $y = x $\, the coordinates of the new point are:

*A.*

\(-3\, -4\)

*B.*

$\(3 \,4 \)$

*C.*

$\(4 \,- 3 \)$

*D.*

$\(- 4 \,3 \)$

== Solution

Correct answer: A

\(-3\, -4\)

#pagebreak()

= Question 26

a\) Sketch the graph of $y = lr(\( frac(1 ,4 )\) )^(x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-05_894_1056_509_468.jpg", width: 49.7%)

b\) Sketch the graph of $y = 2 lr(\( frac(1 ,4 )\) )^(x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-05_888_1054_1583_468.jpg", width: 49.6%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-21_889_941_752_148.jpg", width: 44.3%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-21_889_935_1714_150.jpg", width: 44.0%)

$frac(1 ,2 )$ mark for decreasing exponential

function

$frac(1 ,2 )$ mark for $y $-intercept $\(0 \,1 \)$

$frac(1 ,2 )$ mark for consistent point of an

exponential function

$frac(1 ,2 )$ mark for horizontal asymptote at

$y = 0 $

2 marks

1 mark for a vertical stretch by a factor

of 2 of the graph consistent with a\)

1 mark

#pagebreak()

= Question 27

Determine all of the zeroes of the function $p \(x \)= x ^(3 )- 5  x ^(2 )- 2  x + 24 $\, given one of the factors

of $p \(x \)$ is $\(x - 3 \)$.

== Solution

$  0 = x ^(3 )- 5  x ^(2 )- 2  x + 24   $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[3 ], [1 ], [-5 ], [-2 ], [24 ],
table.hline(stroke: .5pt),
[], [↓ ], [3 ], [-6 ], [-24 ],
table.hline(stroke: .5pt),
[], [1 ], [-2 ], [-8 ], [0 ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for $x = 3 $

1 mark for synthetic division \(or for any equivalent strategy\)

$   x ^(2 )- 2  x - 8 = 0  \  \(x - 4 \)\(x + 2 \)= 0    $

zeroes: 3\, 4\, - 2

$frac(1 ,2 )$ mark for consistent zeroes

2 marks

#pagebreak()

= Question 28

Given the graph of $f \(x \)$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-07_765_807_464_257.jpg", width: 38.0%)

sketch the graph of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-07_766_807_1602_562.jpg", width: 38.0%)

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

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-23_771_814_1534_180.jpg", width: 38.3%)

1 mark for restricting domain

$frac(1 ,2 )$ mark for shape between invariant

points

$frac(1 ,2 )$ mark for shape to the right of the

invariant points

2 marks

#pagebreak()

= Question 29

Sketch the graph of at least one period of the function $y = - 2  sin  \(4  x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-08_888_1056_554_515.jpg", width: 49.7%)

== Solution

1 mark for amplitude
1 mark for period
1 mark for reflection in the x-axis
3 marks
2
π
−
1
1
−
2
2
−
y
x
4
π
−
4
π
2
π

#pagebreak()

= Question 30

Evaluate:

$  frac(1 ,2 ) log  _(3 ) 144 - log  _(3 ) 4 + 2  log  _(3 ) 3   $

== Solution

$log  _(3 )\(144 \)^(frac(1 ,2 ))- log  _(3 ) 4 + log  _(3 )\(3 \)^(2 )$

1 mark for power rule

$log  _(3 ) 12 - log  _(3 ) 4 + log  _(3 ) 9 $

$log  _(3 )lr(\( frac(12  dot.c  9 ,4 )\) )$

$log  _(3 ) 27 $

3

$frac(1 ,2 )$ mark for product rule

$frac(1 ,2 )$ mark for quotient rule

1 mark for evaluating a logarithm

3 marks

#pagebreak()

= Question 31

Match each function with its correct description.

a\) The graph of this function has a vertical asymptote at $x = - 1 $.

b\) The graph of this function has a point of discontinuity \(hole\) at $x = 3 $.

c\) The graph of this function has a horizontal asymptote at $y = 4 $.

d\) The domain of this function is $x  in  bb(R )$.

Place the appropriate letter in this column.

$f \(x \)= frac(4 ,x ^(2 )+ 1 )$

$g \(x \)= frac(4  x ,x + 3 )$

$h \(x \)= frac(4 \(x - 3 \)\(x + 2 \),\(x - 3 \))$

$k \(x \)= frac(4 \(x - 3 \),\(x + 3 \)\(x + 1 \))$

== Solution

$   & f \(x \)= frac(4 ,x ^(2 )+ 1 ) \  & g \(x \)= frac(4  x ,x + 3 ) \  & h \(x \)= frac(4 \(x - 3 \)\(x + 2 \),\(x - 3 \)) \  & k \(x \)= frac(4 \(x - 3 \),\(x + 3 \)\(x + 1 \))   $

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$frac(1 ,2 )$ mark for each correct answer

2 marks

#pagebreak()

= Question 32

The point $\(- 3 \,4 \)$ is on the graph of $y = frac(1 ,2 ) f \(3  x \)$.

State the coordinates of the corresponding point on the graph of $y = f \(x \)$.

== Solution

\(-9\, 8\)

$frac(1 ,2 )$ mark for each coordinate

1 mark

#pagebreak()

= Question 33

Sketch the graph of $y = - 2 \(x - 1 \)\(x - 3 \)\(x + 1 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-12_887_1056_605_515.jpg", width: 49.7%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-28_1048_1087_576_168.jpg", width: 51.2%)

1 mark for $x $-intercepts

1 mark for $y $-intercept

1 mark for end behaviour

3 marks

#pagebreak()

= Question 34

a\) Verify that the equation $frac(1 - sin  ^(2 ) x ,cos  x )= frac(sin  2  x ,2  sin  x )$ is true for $x = frac(pi ,3 )$.

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

b\) Explain why verifying the equation for $x = frac(pi ,3 )$ is insufficient to conclude that the equation is

an identity.

== Solution

a\)

$  mat(delim: #none,  frac(1 - sin  ^(2 )lr(\( frac(pi ,3 )\) ),cos  frac(pi ,3 )) "" , frac(sin  2 lr(\( frac(pi ,3 )\) ),2  sin  frac(pi ,3 )) "" , "" ; frac(1 - lr(\( frac(sqrt(3 ),2 )\) )^(2 ),frac(1 ,2 )) "" , frac(frac(sqrt(3 ),2 ),2 lr(\( frac(sqrt(3 ),2 )\) )) "" , 1  " mark for exact values "lr(\( frac(1 ,2 ) " mark for " sin  frac(pi ,3 )\, 1  \/ 2  " mark for " cos  frac(pi ,3 )\) ) "" ; frac(1 - frac(3 ,4 ),frac(1 ,2 )) "" , frac(sqrt(3 ),sqrt(3 )) "" , 1  " mark for simplification "lr(\( frac(1 ,2 ) " mark for LHS, " 1  \/ 2  " mark for RHS "\) ) "" ; frac(frac(1 ,4 ),frac(1 ,2 )) "" , 2  " marks " "" ; frac(1 ,2 ) "" , "" , "" ; "" , "" , )  $

b\) Proving that it is true for one value does not mean that it is true for all values.

#pagebreak()

= Question 35

Evaluate:

$  frac( "" _(7 ) P _(2 ), "" _(7 ) P _(5 ))  $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[7! ], [],
table.hline(stroke: .5pt),
[\(7-2\)! ], [$frac(1 ,2 )$ mark for substitution ],
table.hline(stroke: .5pt),
[\(7-5\)! ], [],
table.hline(stroke: .5pt),
[], [],
table.hline(stroke: .5pt),
[7! ], [],
table.hline(stroke: .5pt),
[$frac(2 ! ,5 ! )$ ], [$frac(1 ,2 )$ mark for simplification ],
table.hline(stroke: .5pt),
[$frac(2  times  1 ,5  times  4  times  3  times  2  times  1 )$ ], [1 mark for expanding factorials ],
table.hline(stroke: .5pt),
[$frac(1 ,60 )$ ], [2 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 36

Use the graph of $y = f \(x \)$ to sketch the graph of $y = f \(3  x \)+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-15_936_1073_472_464.jpg", width: 50.5%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-15_929_1069_1583_302.jpg", width: 50.3%)

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

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-31_935_1063_1577_174.jpg", width: 50.0%)

1 mark for horizontal compression

1 mark for vertical translation

2 marks

#pagebreak()

= Question 37

Solve the following equation:

$  log  _(4 )\(x + 2 \)+ log  _(4 ) 3 = log  _(4 ) x   $

== Solution

Method 1

$   log  _(4 )\(x + 2 \)+ log  _(4 ) 3  & = log  _(4 ) x  \  log  _(4 )\[\(x + 2 \) 3 \] & = log  _(4 ) x  \  3 \(x + 2 \) & = x  \  3  x + 6  & = x  \  x  & = - 3    $

No solution

Method 2

$   log  _(4 )\(x + 2 \)+ log  _(4 ) 3  & = log  _(4 ) x  \  log  _(4 )\(x + 2 \)+ log  _(4 ) 3 - log  _(4 ) x  & = 0  \  log  _(4 )lr(\[ frac(3 \(x + 2 \),x )\] ) & = 0  \  4 ^(0 ) & = frac(3  x + 6 ,x ) \  x  & = - 3  \  x  & > - 3    $

1 mark for product rule

1 mark for equating arguments

$frac(1 ,2 )$ mark for solving for $x $

$frac(1 ,2 )$ mark for rejecting extraneous root

3 marks

1 mark for logarithmic rules \( $frac(1 ,2 )$ mark for

product rule\; $frac(1 ,2 )$ mark for quotient rule\)

1 mark for exponential form

$frac(1 ,2 )$ mark for solving for $x $

$frac(1 ,2 )$ mark for rejecting extraneous root

3 marks

#pagebreak()

= Question 38

Determine the coordinates of the point of discontinuity \(hole\) for the graph of the function

$y = frac(\(2 - x \)\(x - 3 \),\(x - 2 \))$.

== Solution

$   & x  !=  2  \  & y = - \(x - 3 \) \  & y = - \(2 - 3 \) \  & y = 1  \  & quad \(2 \,1 \)   $

1 mark for point of discontinuity \(hole\) at $\(2 \,1 \)$

\( $frac(1 ,2 )$ mark for $x = 2 \, frac(1 ,2 )$ mark for consistent $y $-coordinate\)

1 mark

#pagebreak()

= Question 39

Evaluate and simplify $sec  lr(\( frac(5  pi ,6 )\) ) dot.c  tan  lr(\( - frac(pi ,6 )\) )$.

== Solution

$lr(\( - frac(2 ,sqrt(3 ))\) ) dot.c lr(\( - frac(1 ,sqrt(3 ))\) )$

$frac(2 ,3 )$

1 mark for $sec  lr(\( frac(5  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for value\, $frac(1 ,2 )$ mark for quadrant $\)$

1 mark for $tan  lr(\( - frac(pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for value\, $frac(1 ,2 )$ mark for quadrant $\)$

2 marks

#pagebreak()

= Question 40

Sketch the graph of the following function:

$  y = - 2  sqrt(x - 3 )  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-19_839_876_586_575.jpg", width: 41.2%)

== Solution

Method 1

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-35_829_862_705_243.jpg", width: 40.6%)

1 mark for shape \(graph of a radical

function\)

1 mark for vertical reflection

1 mark for horizontal shift

1 mark for vertical stretch

4 marks

Method 2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-35_795_1091_1684_185.jpg", width: 51.3%)

1 mark for invariant points where

$y = 0 $ and $y = 1 lr(\( frac(1 ,2 ) upright(m a r k ) )$ for each

point\)

1 mark for domain of $\[3 \, oo \)$

$frac(1 ,2 )$ mark for shape between invariant

points

$frac(1 ,2 )$ mark for shape to the right of the

invariant points

1 mark for applying transformations

\(vertical stretch\, vertical reflection\)

4 marks

#pagebreak()

= Question 41

Sketch the graph of $f \(x \)= frac(2  x + 3 ,x + 2 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/5e50bc3b-d61f-4b32-9c8b-85ed881dd029-20_888_1052_627_558.jpg", width: 49.5%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-36_825_793_627_288.jpg", width: 37.3%)

1 mark for vertical asymptote

1 mark for horizontal asymptote

$frac(1 ,2 )$ mark for graph left of the vertical asymptote

$frac(1 ,2 )$ mark for graph right of the vertical asymptote

3 marks

#pagebreak()

= Question 42

a\) 2 marks

b\) 1 mark

138 139

a\) Given the functions $f \(x \)= sqrt(4 + x )$ and $g \(x \)= | 3  x - 6 | $\, evaluate $f \(g \(- 5 \)\)$.

b\) Is it possible to evaluate $g \(f \(- 5 \)\)$ ?

Justify your answer.

== Solution

a\)

$   g \(- 5 \) & = | 3 \(- 5 \)- 6 |  \  g \(- 5 \) & = 21  \  f \(21 \) & = sqrt(4 + 21 ) \  & = sqrt(25 ) \  & = 5    $

1 mark for consistent value of $f \(g \(- 5 \)\)$

2 marks

b\) No\, because $f \(x \)$ is undefined when $x = - 5 $

1 mark for justification

or

$   & f \(- 5 \)= sqrt(4 + \(- 5 \)) \  & f \(- 5 \)= sqrt(- 1 )   $

1 mark

$f \(- 5 \)$ is undefined because you cannot evaluate the square root of a negative number.

#pagebreak()

= Question 43

Identify which of these values is greater. Justify your answer.

$  log  _(5 ) 80  " or " log  _(3 ) 30   $

== Solution

$   & 5 ^(2 )= 25  \  & 5 ^(3 )= 125   log  _(5 ) 80  " is less than " 3   $

$   & 3 ^(3 )= 27  \  & 3 ^(4 )= 81   quad  log  _(3 ) 30  " is more than " 3   $

$  therefore  log  _(3 ) 30  " is greater "  $

$  1  " mark for justification "  $

$  1  " mark "  $

#pagebreak()

= Question 44

Given $cos  alpha = frac(3 ,5 )$\, where $alpha $ is in quadrant IV\, and $cos  beta = - frac(2 ,3 )$\, where $beta $ is in quadrant II\,

determine the exact value of $sin  \(alpha - beta \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2015-jan/assets/fbd17110-3bea-49b5-a7b2-fb6a1395e016-39_468_544_718_234.jpg", width: 25.6%)

$  sin  alpha = - frac(4 ,5 )  $

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  4 + y ^(2 ) & = 9  \  y ^(2 ) & = 5  \  y  & =  plus.minus  sqrt(5 ) \  y  & = sqrt(5 )   $

$  sin  beta = frac(sqrt(5 ),3 )  $

$  frac(1 ,2 ) " mark for value of " y   $

$  frac(1 ,2 ) " mark for value of " y   $

$   sin  \(alpha - beta \) & = sin  alpha  cos  beta - cos  alpha  sin  beta  \  & = lr(\( - frac(4 ,5 )\) )lr(\( - frac(2 ,3 )\) )- lr(\( frac(3 ,5 )\) )lr(\( frac(sqrt(5 ),3 )\) ) \  & = frac(8 - 3  sqrt(5 ),15 )   $

$frac(1 ,2 )$ mark for $sin  alpha $

$frac(1 ,2 )$ mark for $sin  beta $

1 mark for substitution into

correct identity

3 marks

#pagebreak()

= Question 45

Determine the number of possible sandwiches from the following menu.

*MENU*

Select one item from each column:

#table(columns: 4, stroke: none,
  [*Bread*], [*Sauce*], [*Meat*], [*Vegetable*],
  [White], [Mayo], [Turkey], [Tomato],
  [Rye], [Mustard], [Ham], [Onion],
  [Brown], [], [Roast Beef], [Lettuce],
  [], [], [Chicken], [],
)

== Solution

$3  times  2  times  4  times  3 $

72 sandwiches