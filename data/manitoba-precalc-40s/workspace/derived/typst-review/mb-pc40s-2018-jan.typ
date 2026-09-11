#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2018-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

\(4nli

A group of 7 friends decide to go to a movie.

Determine how many ways the friends can sit in a row if two of the friends refuse to sit next to

each other.

== Solution

$7 ! - 6 ! 2 ! = 3600 $ ways

$frac(1 ,2 )$ mark for 7!

1 mark for product of 6!2!

\( $frac(1 ,2 )$ mark for 6 !\, $frac(1 ,2 )$ mark for 2 !\)

$frac(1 ,2 )$ mark for subtraction

2 marks

#pagebreak()

= Question 2

\(inli\)

Gabrielle listens to her radio at a sound level of 80 dB . She attended a music concert that had a

sound level of 115 dB . Determine how many times more intense the music concert was than

the radio.

You may use the formula:

$  beta = 10  log  lr(\( frac(I ,I _(0 ))\) )  $

where $quad  beta $ is the intensity level of sound\, measured in dB

$I $ is the intensity of sound

$I _(0 )$ is the standard minimum intensity that a person can hear

== Solution

Radio:

$   & 80 = 10  log  lr(\( frac(I ,I _(0 ))\) ) \  & 8 = log  lr(\( frac(I ,I _(0 ))\) )   $

$10 ^(8 )= frac(I ,I _(0 ))$

$  frac(1 ,2 ) " mark for exponential form "  $

Music concert:

$   & 115 = 10  log  lr(\( frac(I ,I _(0 ))\) ) \  & 11.5 = log  lr(\( frac(I ,I _(0 ))\) )   $

$10 ^(11.5 )= frac(I ,I _(0 ))$

$  1  \/ 2  " mark for exponential form "  $

$   frac(" intensity of music concert "," intensity of radio ") & = frac(10 ^(11.5 ) I _(0 ),10 ^(8 ) I _(0 )) \  & = 10 ^(3.5 ) \  & = 3162.27766  \  & = 3162.278    $

1 mark for comparison

2 marks

#pagebreak()

= Question 3

Solve\, algebraically.

$  2 \(7 \)^(x )= 3 ^(2  x - 3 )  $

== Solution

$   log  lr(\( 2 lr(\( 7 ^(x )\) )\) ) & = log  3 ^(2  x - 3 ) \  log  2 + x  log  7  & = \(2  x - 3 \) log  3  \  log  2 + x  log  7  & = 2  x  log  3 - 3  log  3  \  log  2 + 3  log  3  & = 2  x  log  3 - x  log  7  \  log  2 + 3  log  3  & = x \(2  log  3 - log  7 \) \  frac(log  2 + 3  log  3 ,2  log  3 - log  7 ) & = x  \  15.872483  & = x  \  15.872  & = x    $

$frac(1 ,2 )$ mark for applying logarithms

1 mark for product law

1 mark for power law

$frac(1 ,2 )$ mark for collecting terms with $x $

$frac(1 ,2 )$ mark for isolating $x $

$frac(1 ,2 )$ mark for evaluating quotient of logarithms

4 marks

#pagebreak()

= Question 4

Solve for $theta $\, algebraically\, over the interval $\[0 \,2  pi \]$.

$  csc  ^(2 ) theta + 2  csc  theta - 8 = 0   $

== Solution

$   \(csc  theta + 4 \)\(csc  theta - 2 \) & = 0  \  csc  theta  & = - 4  quad  csc  theta = 2  \  sin  theta  & = - frac(1 ,4 ) quad  sin  theta = frac(1 ,2 ) \  theta _(r ) & = 0.252680    $

$  mat(delim: #none,  theta = 3.394  "" , theta = frac(pi ,6 )\, frac(5  pi ,6 ) "" ; theta = 6.031  "" , )  $

1 mark for solving for $csc  theta $

1 mark for reciprocal

2 marks for solving for $theta $ \( $frac(1 ,2 )$ mark for each value\)

4 marks

$  mat(delim: #none,  theta = 3.394  "" , theta = 0.524  "" ; theta = 6.031  "" , theta = 2.618  )  $

#pagebreak()

= Question 5

You have forgotten the code to unlock your cell phone. You know the code is made up of four

numbers from 0 to 9 .

Determine the number of possible codes\, if repetition is allowed.

Note: A calculator is not required for the remaining test questions.

== Solution

$10  dot.c  10  dot.c  10  dot.c  10 = 10000 $

1 mark

#pagebreak()

= Question 6

In the binomial expansion of $lr(\( frac(7 ,x ^(3 ))- 3  x ^(7 )\) )^(n )$\, the $5 ^("th ")$ term contains $x ^(7 )$.

Determine the value of $n $.

== Solution

$   x ^(7 ) & = lr(\( frac(1 ,x ^(3 ))\) )^(n - 4 )lr(\( x ^(7 )\) )^(4 ) \  x ^(7 ) & = lr(\( x ^(- 3 )\) )^(n - 4 )lr(\( x ^(7 )\) )^(4 ) \  x ^(7 ) & = x ^(- 3  n + 12 + 28 ) \  7  & = - 3  n + 40  \  - 33  & = - 3  n  \  11  & = n    $

1 mark for $k = 4 $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $n $

2 marks

#pagebreak()

= Question 7

Given the domain of $f \(x \)$ is $\{ - 6 \,1 \,3 \,4 \} $ and the range of $f \(x \)$ is $\{ - 4 \,7 \,10 \,15 \} $\, state the

domain of $f ^(- 1 )\(x \)$.

== Solution

$  \{ - 4 \,7 \,10 \,15 \}   $

1 mark

#pagebreak()

= Question 8

Given the graph of $y = f \(x \)$\, sketch the graph of its inverse.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-08_723_772_500_696.jpg", width: 36.3%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-08_731_772_1308_696.jpg", width: 36.3%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-08_718_761_1328_254.jpg", width: 35.8%)

#pagebreak()

= Question 9

Prove the following identity for all permissible values of $theta $.

$  frac(1 + cos  theta ,1 - sin  ^(2 ) theta )= sec  theta + tan  ^(2 ) theta + 1   $

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
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   & frac(1 + cos  theta ,1 - sin  ^(2 ) theta ) \  & frac(1 + cos  theta ,cos  ^(2 ) theta ) \  & frac(1 ,cos  ^(2 ) theta )+ frac(1 ,cos  theta ) \  & sec  ^(2 ) theta + sec  theta  \  & tan  ^(2 ) theta + 1 + sec  theta    $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[$  sec  theta + tan  ^(2 ) theta + 1   $ ],
[1 mark for algebraic strategies ],
[1 mark for logical process to prove the identity ],
[1 mark for correct substitution of appropriate identities ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

Method 2

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ], [],
table.hline(stroke: .5pt),
[$frac(1 + cos  theta ,cos  ^(2 ) theta )$ ], [$   & frac(1 ,cos  theta )+ sec  ^(2 ) theta  \  & frac(1 ,cos  theta )+ frac(1 ,cos  ^(2 ) theta ) \  & frac(cos  theta + 1 ,cos  ^(2 ) theta )   $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[1 mark for algebraic strategies ],
[1 mark for logical process to prove the identity ],
[1 mark for correct substitution of appropriate identities ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 10

Thomas used graphs to solve the equation $e ^(x + 2 )= sqrt(- \(x + 1 \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-10_734_909_485_623.jpg", width: 42.8%)

He incorrectly states the solution as $\(- 2 \,1 \)$.

Describe how Thomas should have stated the solution.

== Solution

He stated his solution as a coordinate point\; his solution should have only been the value of $x $.

#pagebreak()

= Question 11

Given the graph of $y = f \(x \)$\, sketch the graph of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-11_727_773_483_691.jpg", width: 36.4%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-11_734_777_1325_689.jpg", width: 36.6%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-12_720_761_1336_249.jpg", width: 35.8%)

1 mark for restricting domain

$frac(1 ,2 )$ mark for shape between both pairs of

invariant points

$frac(1 ,2 )$ mark for shape above both pairs of

invariant points

2 marks

#pagebreak()

= Question 12

When a polynomial\, $P \(x \)$\, is divided by \( $x - 2 $ \) the resulting equation is

$frac(P \(x \),x - 2 )= x ^(2 )- x + 1 + frac(3 ,x - 2 )$.

a\) Explain why $x - 2 $ is not a factor of $P \(x \)$.

b\) Determine the equation for the polynomial function $P \(x \)$.

$P \(x \)= $

== Solution

a\) There is a remainder when $P \(x \)$ is divided by $x - 2 $.

1 mark

b\) $P \(x \)= \(x - 2 \)lr(\( x ^(2 )- x + 1 \) )+ 3 $

1 mark

or

$  P \(x \)= x ^(3 )- 3  x ^(2 )+ 3  x + 1   $

#pagebreak()

= Question 13

Determine the equation for $g \(x \)$ in terms of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-13_798_839_468_234.jpg", width: 39.5%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/ea112177-c09c-466e-9f1b-01beecd98dd9-13_798_830_468_1102.jpg", width: 39.1%)

$g \(x \)= $

$\_ \_ \_ \_ $

== Solution

$  g \(x \)= - f \(x - 1 \)+ 3   $

1 mark for vertical reflection

1 mark for horizontal translation

1 mark for vertical translation

3 marks

#pagebreak()

= Question 14

Explain why the binomial expansion of $\(2  x + y \)^(9 )$ does not have a middle term.

== Solution

The expansion contains $n + 1 $ terms. Since $n $ equals 9\, there are 10 terms\, which would not allow

for a middle term.

1 mark

#pagebreak()

= Question 15

Using the laws of logarithms\, completely expand the expression $log  lr(\( frac(5  sqrt(a ),b ^(3 ))\) )$.

== Solution

$log  5 + frac(1 ,2 ) log  a - 3  log  b $

1 mark for product law

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

1 mark for quotient law

3 marks

#pagebreak()

= Question 16

Identify $10 ^(degree )$ in radians.

*A.*

$frac(1800 ,pi )$

*B.*

$frac(pi ,1800 )$

*C.*

$frac(18 ,pi )$

*D.*

$frac(pi ,18 )$

== Solution

Correct answer: D

$frac(pi ,18 )$

#pagebreak()

= Question 17

The polynomial function\, $P \(x \)= a \(x - 1 \)^(2 )\(x + 4 \)^(2 )$\, has a $y $-intercept of -8 .

Identify the value of $a $.

*A.*

-2

*B.*

$- frac(1 ,2 )$

*C.*

$frac(1 ,2 )$

*D.*

2

== Solution

Correct answer: B

$- frac(1 ,2 )$

#pagebreak()

= Question 18

Identify the value of $log  _(4 )lr(\( frac(1 ,16 )\) )$.

*A.*

-2

*B.*

$- frac(1 ,2 )$

*C.*

$frac(1 ,2 )$

*D.*

2

== Solution

Correct answer: A

-2

#pagebreak()

= Question 19

Given the angle $frac(25  pi ,7 )$\, identify the coterminal angle on the interval $\[- 2  pi \, 0 \]$.

*A.*

$frac(18  pi ,7 )$

*B.*

$frac(11  pi ,7 )$

*C.*

$- frac(3  pi ,7 )$

*D.*

$- frac(10  pi ,7 )$

== Solution

Correct answer: C

$- frac(3  pi ,7 )$

#pagebreak()

= Question 20

Identify which expression cannot be evaluated.

*A.*

$ "" _(7 ) P _(0 )$

*B.*

$ "" _(7 ) P _(6 )$

*C.*

$ "" _(7 ) P _(7 )$

*D.*

$ "" _(7 ) P _(8 )$

== Solution

Correct answer: D

$ "" _(7 ) P _(8 )$

#pagebreak()

= Question 21

Identify the graph of $f \(x \)= frac(- 3  x ,2  x + 4 )$.

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-03_753_802_586_219.jpg", width: 37.7%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-03_753_777_586_1108.jpg", width: 36.6%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-03_751_759_1396_234.jpg", width: 35.7%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-03_766_772_1392_1108.jpg", width: 36.3%)

== Solution

Correct answer: B

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-03_753_777_586_1108.jpg", width: 36.6%)

#pagebreak()

= Question 22

Given a point $\(- 2 \,0 \)$ on the graph of $y = f \(x \)$\, identify the coordinates of the corresponding

point on the graph of $y = 4  f lr(\( frac(1 ,2 ) x \) )$.

*A.*

$\(- 8 \,0 \)$

*B.*

$\(- 4 \,0 \)$

*C.*

$\(- 2 \,0 \)$

*D.*

$\(- 1 \,0 \)$

== Solution

Correct answer: B

$\(- 4 \,0 \)$

#pagebreak()

= Question 23

Identify the non-permissible value of $theta $ for the expression $frac(cos  theta ,1 + sin  theta )$.

*A.*

$frac(pi ,2 )$

*B.*

$pi $

*C.*

$frac(3  pi ,2 )$

*D.*

$2  pi $

== Solution

Correct answer: C

$frac(3  pi ,2 )$

#pagebreak()

= Question 24

Identify the function with an asymptote at $x = - 3 $.

*A.*

$y = log  \(x + 3 \)$

*B.*

$y = log  x + 3 $

*C.*

$y = log  \(x - 3 \)$

*D.*

$y = log  x - 3 $

== Solution

Correct answer: A

$y = log  \(x + 3 \)$

#pagebreak()

= Question 25

Evaluate the following expression.

$  tan  lr(\( frac(2  pi ,3 )\) ) csc  lr(\( frac(- 2  pi ,3 )\) )+ cos  \(3  pi \)  $

== Solution

$   \(- sqrt(3 )\)lr(\( - frac(2 ,sqrt(3 ))\) )+ \(- 1 \) \  2 - 1  \  1    $

$   & 1  " mark for " tan  lr(\( frac(2  pi ,3 )\) )\(1  \/ 2  " mark for quadrant, " 1  \/ 2  " mark for value "\) \  & 1  " mark for " csc  lr(\( - frac(2  pi ,3 )\) )\(1  \/ 2  " mark for quadrant, " 1  \/ 2  " mark for value "\) \  & 1  " mark for " cos  \(3  pi \)   $

3 marks

#pagebreak()

= Question 26

State the range of the graph below.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-06_894_899_449_625.jpg", width: 42.3%)

Range:

$\_ \_ \_ \_ $

== Solution

$\_ \_ \_ \_ $

$\{ y  in  bb(R )\, y  !=  0 $ and $y  !=  1 \} $

1 mark \( $frac(1 ,2 )$ mark for $y  !=  0 \, frac(1 ,2 )$ mark for $y  !=  1 $ \)

1 mark

#pagebreak()

= Question 27

Sketch the graph of the function $f \(x \)= frac(2  x ^(2 )- 5  x ,x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-07_843_846_552_661.jpg", width: 39.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-23_754_746_602_254.jpg", width: 35.1%)

1 mark for point of discontinuity \(hole\) at \(0\, -5\)

$lr(\( frac(1 ,2 ) )$ mark for $x = 0 \, frac(1 ,2 )$ mark for $lr( y = - 5 \) )$

1 mark for shape of a linear function

2 marks

#pagebreak()

= Question 28

State a possible value of $n $ if the polynomial function $P \(x \)= \(x - 1 \)^(2 )\(x + 2 \)^(n )$ has a range of $\[0 \, oo \)$.

== Solution

$n = 2 $

1 mark

Note\(s\):

- Accept any even positive value of $n $\, including zero.

#pagebreak()

= Question 29

Sketch the graph of $y = lr(\( frac(1 ,2 )\) )^(x - 1 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-09_882_889_552_635.jpg", width: 41.8%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-25_793_894_599_204.jpg", width: 42.1%)

1 mark for decreasing exponential function

1 mark for horizontal translation

2 marks

#pagebreak()

= Question 30

Solve.

$  log  _(x ) 27 = 3   $

== Solution

$   x ^(3 ) & = 27  \  x  & = 3    $

$  1  " mark for exponential form "  $

1 mark

#pagebreak()

= Question 31

Sketch at least two periods of the graph $y = tan  x $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-10_897_1406_1484_333.jpg", width: 66.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-27_898_1222_580_251.jpg", width: 57.5%)

1 mark for increasing trigonometric function

1 mark for asymptotic behaviour approaching $x = frac(pi ,2 )+ k  pi \, k  in  bb(Z )$

2 marks

#pagebreak()

= Question 32

Given the graph of $f \(x \)$\, determine the domain of $frac(1 ,f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-11_852_854_517_653.jpg", width: 40.2%)

Domain:

$\_ \_ \_ \_ $

== Solution

Domain: $\{ x  in  bb(R )\, x  !=  plus.minus  2 \} $

1 mark \( $frac(1 ,2 )$ mark for $x  !=  2 \, frac(1 ,2 )$ mark for $x  != - 2 $ \)

1 mark

#pagebreak()

= Question 33

Determine the values of $upright(A )\, upright(B )$\, and D of the sinusoidal function in the form $y = upright(A ) sin  \(upright(B ) x \)+ upright(D )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-12_794_918_500_644.jpg", width: 43.2%)

A =

$\_ \_ \_ \_ $

$upright(B )= $

$\_ \_ \_ \_ $

D =

$\_ \_ \_ \_ $

== Solution

$  A = 2   $

$\_ \_ \_ \_ $

$  upright(B )= frac(1 ,5 )  $

1 mark for B

$  upright(D )= 1   $

1 mark for D

□

#pagebreak()

= Question 34

Determine if the point $lr(\( - frac(sqrt(7 ),5 )\, frac(2 ,5 )\) )$ is on the unit circle.

Justify your answer.

== Solution

$   x ^(2 )+ y ^(2 ) & = 1  \  " Left-hand side " & = lr(\( - frac(sqrt(7 ),5 )\) )^(2 )+ lr(\( frac(2 ,5 )\) )^(2 ) \  & = frac(7 ,25 )+ frac(4 ,25 ) \  & = frac(11 ,25 ) \  frac(11 ,25 ) & !=  1  \  & therefore  " not on the unit circle "   $

1 mark for justification

1 mark

#pagebreak()

= Question 35

Solve\, algebraically.

$  frac( "" _(n ) C _(5 ), "" _(n ) C _(4 ))= 6   $

== Solution

$  frac(frac(n ! ,\(n - 5 \)! 5 ! ),frac(n ! ,\(n - 4 \)! 4 ! ))= 6   $

$  frac(n ! \(n - 4 \)\(n - 5 \)! 4 ! ,n ! \(n - 5 \)! 5  dot.c  4 ! )= 6   $

$   & frac(n - 4 ,5 )= 6  \  & n - 4 = 30  \  & n = 34    $

$frac(1 ,2 )$ mark for substitution into equation

1 mark for factorial expansion

\( $frac(1 ,2 )$ mark for numerical factors\; $frac(1 ,2 )$ mark for factors with variables\)

1 mark for simplification of factorials

\( $frac(1 ,2 )$ mark for numerical factors\; $frac(1 ,2 )$ mark for factors with variables\)

$frac(1 ,2 )$ mark for solving for $n $

3 marks

#pagebreak()

= Question 36

Given $sin  alpha = frac(4 ,5 )$\, where $alpha $ is in quadrant II\, determine the exact value of $sin  2  alpha $.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-32_578_602_608_331.jpg", width: 28.3%)

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  x ^(2 )+ 16  & = 25  \  x ^(2 ) & = 9  \  x  & =  plus.minus  3  \  x  & = - 3    $

$  cos  alpha = - frac(3 ,5 )  $

$   & 1  \/ 2  " mark for value of " x  \  & 1  \/ 2  " mark for " cos  alpha    $

$   sin  2  alpha  & = 2  sin  alpha  cos  alpha  \  & = 2 lr(\( frac(4 ,5 )\) )lr(\( - frac(3 ,5 )\) ) \  & = - frac(24 ,25 )   $

1 mark for substitution into correct identity

2 marks

- Accept any of the following values for $x :  x =  plus.minus  3  \; x = - 3 $\; or $x = 3 $.

#pagebreak()

= Question 37

Given the functions $f \(x \)= x + 1 $ and $g \(x \)= sqrt(x )$\,

a\) determine the equation of $g \(f \(x \)\)$.

$  g \(f \(x \)\)=   $

$\_ \_ \_ \_ $

b\) sketch the graph of $g \(f \(x \)\)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-16_798_805_1014_646.jpg", width: 37.9%)

== Solution

a\) $g \(f \(x \)\)= sqrt(x + 1 )$

b\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-33_791_795_993_254.jpg", width: 37.4%)

1 mark

1 mark for domain of $g \(f \(x \)\)$

1 mark for shape consistent with $g \(f \(x \)\)$

2 marks

#pagebreak()

= Question 38

Steve is asked to determine an equation with a larger period than the period of the graph of

$y = cos  \(2  x \)$.

Justify why Steve's answer of $y = cos  \(6  x \)$ is incorrect.

== Solution

Steve's equation needs to have a value of $| b | $ less than 2. 1 mark

or

Steve's graph would have a period of $frac(2  pi ,6 )= frac(pi ,3 )$\, which is smaller than $frac(2  pi ,2 )= pi $\, the period of the

given graph.

#pagebreak()

= Question 39

Given the graphs of $f \(x \)$ and $g \(x \)$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-18_699_727_466_315.jpg", width: 34.2%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-18_701_736_464_1140.jpg", width: 34.6%)

a\) determine the value of $\(f  dot.c  g \)\(- 1 \)$.

b\) determine the value of $g \(f \(0 \)\)$.

== Solution

a\)

$   \(f  dot.c  g \)\(- 1 \) & = \(- 1 \)\(4 \) \  & = - 4    $

b\) $f \(0 \)= 1 $

$g \(f \(0 \)\)= 2 $

1 mark for value of $\(f  dot.c  g \)\(- 1 \)$

1 mark

$frac(1 ,2 )$ mark for $f \(0 \)$

$frac(1 ,2 )$ mark for $g \(f \(0 \)\)$ consistent with $f \(0 \)$ value

#pagebreak()

= Question 40

Sketch the graph of $P \(x \)= - \(x - 1 \)^(3 )\(x - 3 \)\(x + 1 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-19_894_929_608_590.jpg", width: 43.7%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/d195e22b-d1e2-4412-b9a3-37e28601558f-36_793_823_567_303.jpg", width: 38.7%)

1 mark for $x $-intercepts

$frac(1 ,2 )$ mark for $y $-intercept

1 mark for multiplicity \(degree 3 at $x = 1 $ \)

$frac(1 ,2 )$ mark for end behaviour

3 marks

#pagebreak()

= Question 41

The point $\(- sqrt(3 )\, 1 \)$ is on the terminal arm of an angle $theta $\, in standard position.

a\) Determine $tan  theta $.

b\) Determine a possible value of $theta $\, in radians.

== Solution

a\) $tan  theta = - frac(1 ,sqrt(3 ))$

b\) $theta = frac(5  pi ,6 )$

#pagebreak()

= Question 42

Describe the transformation used to obtain the graph of $y = log  _(5 ) x $ given the graph of $y = 5 ^(x )$.

== Solution

The graph of $y = log  _(5 ) x $ is obtained by reflecting the graph of $y = 5 ^(x )$ over the line $y = x $.

or

1 mark

The graph of $y = log  _(5 ) x $ is the inverse of $y = 5 ^(x )$.

#pagebreak()

= Question 43

Solve $sin  theta = - frac(sqrt(3 ),2 )$\, where $theta  in  bb(R )$.

== Solution

$theta = frac(4  pi ,3 )\, frac(5  pi ,3 ) quad  1 $ mark for values of $theta lr(\( frac(1 ,2 ) )$ mark for each value\)

$theta =  cases(frac(4  pi ,3 )+ 2  k  pi \, k  in  bb(Z ) , frac(5  pi ,3 )+ 2  k  pi \, k  in  bb(Z ) & 1  " mark for general solution ")$

or

$   & theta = 240 ^(degree )\, 300 ^(degree ) \  & theta = lr(\{ mat(delim: #none,  240 ^(degree )+ 360 ^(degree ) k \, k  in  bb(Z ) "" ; 300 ^(degree )+ 360 ^(degree ) k \, k  in  bb(Z ) )\} )   $

#pagebreak()

= Question 44

Given that the point $\(a \, b \)$ is on the graph of $f \(x \)$\, describe how you would determine the

corresponding point on the graph of $y = sqrt(f \(x \))$.

== Solution

The value of $a $ stays the same\, square root the value of $b $.

1 mark

#pagebreak()

= Question 45

Evaluate.

$  cos  lr(\( frac(pi ,20 )\) ) cos  lr(\( frac(pi ,5 )\) )- sin  lr(\( frac(pi ,20 )\) ) sin  lr(\( frac(pi ,5 )\) )  $

== Solution

$cos  lr(\( frac(pi ,20 )+ frac(pi ,5 )\) )$

$cos  lr(\( frac(pi ,20 )+ frac(4  pi ,20 )\) )$

$cos  lr(\( frac(5  pi ,20 )\) )$

cos $lr(\( frac(pi ,4 )\) )$

$frac(sqrt(2 ),2 )$

$frac(1 ,2 )$ mark for substitution of an appropriate identity

$frac(1 ,2 )$ mark for exact value

1 mark

#pagebreak()

= Question 46

Describe the transformations used to obtain the graph of the function $y = f \(- x + 6 \)- 8 $ from

the graph of $y = f \(x \)$.

== Solution

Reflect the graph of $y = f \(x \)$ over the $y $-axis and then translate 6 units right and 8 units down.

1 mark for horizontal reflection

1 mark for horizontal translation

1 mark for vertical translation

3 marks

Note\(s\):

- Deduct 1 mark if correct transformations are given in the wrong order.

#pagebreak()

= Question 47

State the equations of all the asymptotes of the function\, $y = frac(1 ,3  x + 1 )$.

== Solution

$y = 0 $

$  x = - frac(1 ,3 )  $

1 mark for horizontal asymptote

1 mark for vertical asymptote

2 marks

#pagebreak()

= Question 48

Determine the zeros of the polynomial function $P \(x \)= 2  x ^(3 )+ 5  x ^(2 )- 4  x - 3 $.

== Solution

$P \(1 \)= 2 \(1 \)^(3 )+ 5 \(1 \)^(2 )- 4 \(1 \)- 3  quad  1 $ mark for identifying one possible value of $x $

$P \(1 \)= 0 $

$\(x - 1 \)$ is a factor

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[1 ], [2 ], [5 ], [-4 ], [-3 ],
table.hline(stroke: .5pt),
[], [↓ ], [2 ], [7 ], [3 ],
table.hline(stroke: .5pt),
[], [2 ], [7 ], [3 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or for any equivalent strategy\)

$   P \(x \) & = \(x - 1 \)lr(\( 2  x ^(2 )+ 7  x + 3 \) ) \  0  & = \(x - 1 \)\(2  x + 1 \)\(x + 3 \) \  x  & = 1  quad  x = - frac(1 ,2 ) quad  x = - 3    $

$frac(1 ,2 )$ mark for consistent factors

$frac(1 ,2 )$ mark for all zeros

3 marks

#pagebreak()

= Question 49

Determine the equation of the radical function represented by the graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jan/assets/4501c3d0-94eb-4e91-b980-a66de8649abd-25_798_803_519_678.jpg", width: 37.8%)

$  y =   $

== Solution

$  y = underline(2  sqrt(x )+ 3 ) quad   & 1  " mark for vertical stretch " \  & 1  " mark for vertical translation "   $

$  y =  " or " \  sqrt(4  x )+ 3  \      $

1 mark for horizontal stretch

1 mark for vertical translation

2 marks