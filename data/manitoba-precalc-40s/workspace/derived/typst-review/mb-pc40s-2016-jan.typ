#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2016-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

mili

A pizza with a diameter of 15 inches is cut into equal slices\, each with a central angle of $36 ^(degree )$.

Determine the length of the crust on the outer edge of one slice of pizza.

== Solution

$  mat(delim: #none,  frac(36 ^(degree ),180 ^(degree )) "" , = frac(theta ,pi ) "" , "" ; theta  "" , = frac(pi ,5 ) "" , 1  " mark for conversion " "" ; s  "" , = theta  r  "" , "" ; s  "" , = lr(\( frac(pi ,5 )\) )lr(\( frac(15 ,2 )\) ) "" , 1  " mark for substitution " "" ; s  "" , = frac(3  pi ,2 ) " inches " "" , 2  " marks " "" ; " or " "" , "" , "" ; s  "" , = 4.712  " inches " )  $

#pagebreak()

= Question 2

m

There are 9 girls and 7 boys in a math class from which a committee of 5 is to be chosen.

a\) How many different committees of 5 can be formed if one of the boys\, William\, must be on

the committee?

b\) How many different committees of 5 can be formed if there must be 2 girls and 3 boys on the

committee?

== Solution

a\) $ "" _(1 ) C _(1 ) dot.c  "" _(15 ) C _(4 )= 1365 $

b\) $ "" _(9 ) C _(2 ) dot.c  "" _(7 ) C _(3 )= 1260 $

$frac(1 ,2 )$ mark for $ "" _(9 ) C _(2 )$

$frac(1 ,2 )$ mark for $ "" _(7 ) C _(3 )$

1 mark for the product of combinations

2 marks

Note\(s\):

- $ "" _(1 ) C _(1 )$ does not need to be shown

#pagebreak()

= Question 3

Solve the following equation over the interval $\[0 \,2  pi \]$ :

$  sin  ^(2 ) theta + 6  sin  theta - 2 = 0   $

== Solution

$sin  theta = frac(- 6  plus.minus  sqrt(\(6 \)^(2 )- 4 \(1 \)\(- 2 \)),2 \(1 \))$

$sin  theta = frac(- 6  plus.minus  sqrt(36 + 8 ),2 )$

$sin  theta = frac(- 6  plus.minus  sqrt(44 ),2 )$

$sin  theta = 0.316 $ 624...

$sin  theta = - 6.316624  dots.h $

$theta _(r )= 0.322169 $

$theta = 0.322 $

no solution

$  theta = 2.819   $

1 mark for solving for $sin  theta $

2 marks for solving for $theta $ \( $frac(1 ,2 )$ mark for each

value\, 1 mark for indicating no solution\)

3 marks

#pagebreak()

= Question 4

Solve:

$  6 \(5 \)^(3  x + 2 )= 9 ^(2 - x )  $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$log  lr(\[ 6 \(5 \)^(3  x + 2 )\] )= log  9 ^(2 - x )$ ], [$frac(1 ,2 )$ mark for applying logarithms ],
table.hline(stroke: .5pt),
[$log  6 + log  5 ^(3  x + 2 )= log  9 ^(2 - x )$ ], [1 mark for product law ],
table.hline(stroke: .5pt),
[$log  6 + \(3  x + 2 \) log  5 = \(2 - x \) log  9 $ ], [1 mark for power law ],
table.hline(stroke: .5pt),
[$log  6 + 3  x  log  5 + 2  log  5 = 2  log  9 - x  log  9 $ ], [],
table.hline(stroke: .5pt),
[$x \(3  log  5 + log  9 \)= 2  log  9 - 2  log  5 - log  6 $ ], [$frac(1 ,2 )$ mark for collecting terms with $x $ ],
table.hline(stroke: .5pt),
[], [],
table.hline(stroke: .5pt),
[$x = frac(2  log  9 - 2  log  5 - log  6 ,3  log  5 + log  9 )$ ], [$frac(1 ,2 )$ mark for solving for $x $ ],
table.hline(stroke: .5pt),
[$x = - 0.087707 $ ], [$frac(1 ,2 )$ mark for evaluating quotient of logarithms ],
table.hline(stroke: .5pt),
[$= - 0.088 $ ], [4 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 5

Solve $\(2  sin  theta - 1 \)\(sin  theta + 1 \)= 0 $ where $theta  in  bb(R )$.

== Solution

$   2  sin  theta - 1  & = 0  \  sin  theta  & = frac(1 ,2 ) \  theta _(r ) & = frac(pi ,6 ) \  theta  & = frac(pi ,6 )+ 2  k  pi \, k  in  bb(Z ) \  theta  & = frac(5  pi ,6 )+ 2  k  pi \, k  in  bb(Z )   $

$  sin  theta + 1 = 0   $

$  theta _(r )= frac(3  pi ,2 )  $

1 mark for solving for $sin  theta $

2 marks for solving for $theta $ \( 1 mark

for each branch\)

1 mark for general solution

$   theta _(r ) & = 30 ^(degree ) \  theta  & = 30 ^(degree )+ 360 ^(degree ) k \, k  in  bb(Z ) \  theta  & = 150 ^(degree )+ 360 ^(degree ) k \, k  in  bb(Z )   $

$   theta _(r ) & = 270 ^(degree ) \  theta  & = 270 ^(degree )+ 360 ^(degree ) k \, quad  k  in  bb(Z )   $

4 marks

#pagebreak()

= Question 6

The roots of the polynomial equation $3 \(x - 2 \)\(x + 1 \)^(2 )= 0 $ are $x = 2 $ and $x = - 1 $.

Explain what these roots represent on the graph of $p \(x \)= 3 \(x - 2 \)\(x + 1 \)^(2 )$.

== Solution

They are the $x $-intercepts of the graph of $p \(x \)$.

#pagebreak()

= Question 7

Determine an equation for $g \(x \)$ as a transformation of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/7c0ba9f2-ef05-4567-9bb3-c01bb6b60d51-07_583_766_485_356.jpg", width: 36.0%)

$g \(x \)= $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$g \(x \)= underline(2  f \(x + 6 \))$ ], [1 mark for vertical stretch 1 mark for horizontal translation ],
table.hline(stroke: .5pt),
[], [2 marks ],
table.hline(stroke: .5pt),
[or ], [],
table.hline(stroke: .5pt),
[$g \(x \)= 2  f \(- x \)$ ], [1 mark for vertical stretch 1 mark for horizontal reflection ],
table.hline(stroke: .5pt),
[], [2 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 8

A student must determine the factors of $5  x ^(4 )- 2  x ^(3 )+ 4  x - 1 $. He used 5\, $- 2 \,4 $\, and -1

as the coefficients of the polynomial when using synthetic division.

Explain the student's error.

== Solution

The student did not write the coefficient of 0 for the $x ^(2 )$ term.

#pagebreak()

= Question 9

Describe the transformations of $y = f \(x \)$ when asked to sketch the graph of $y = - f \(x - 4 \)$.

== Solution

$f \(x \)$ is reflected over the $x $-axis and translated 4 units to the right.

1 mark for vertical reflection

1 mark for horizontal translation

2 marks

#pagebreak()

= Question 10

Prove the identity below for all permissible values of $theta $ :

$  sin  theta + frac(cos  theta ,tan  theta )= frac(1 ,cos  theta  tan  theta )  $

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
[$   & sin  theta + frac(cos  theta ,tan  theta ) \  & sin  theta + frac(cos  theta ,frac(sin  theta ,cos  theta ))   $ ], [$   & frac(1 ,cos  theta  tan  theta ) \  & frac(1 ,cos  theta  frac(sin  theta ,cos  theta )) \  & frac(1 ,sin  theta )   $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove an identity

3 marks

#pagebreak()

= Question 11

Describe how to use the graphs of $f \(x \)= 3  sin  x $ and $g \(x \)= 2 $ to solve the equation $3  sin  x = 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/7c0ba9f2-ef05-4567-9bb3-c01bb6b60d51-11_748_957_539_595.jpg", width: 45.0%)

== Solution

The solution will be the $x $-values where the two graphs intersect.

#pagebreak()

= Question 12

A hockey arena has 5 doors.

Determine the number of ways that you can enter through one door but exit through a different

door.

== Solution

$  5  dot.c  4 = 20  " ways "  $

#pagebreak()

= Question 13

Given that $\(x + 3 \)$ is one of the factors\, express $2  x ^(3 )+ 7  x ^(2 )+ 2  x - 3 $ as a product of factors.

== Solution

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[-3 ], [], [7 ], [2 ], [-3 ],
table.hline(stroke: .5pt),
[], [2 ], [1 ], [-1 ], [0 ],
table.hline(stroke: .5pt),
[],
);

$\(x + 3 \)lr(\( 2  x ^(2 )+ x - 1 \) )$

or

$  \(x + 3 \)\(2  x - 1 \)\(x + 1 \)  $

$frac(1 ,2 )$ mark for $x = - 3 $

1 mark for synthetic division \(or for any other equivalent strategy\)

$frac(1 ,2 )$ mark for consistent product of factors

2 marks

#pagebreak()

= Question 14

Identify the maximum number of $x $-intercepts for a polynomial function of degree 3 .

*A.*

1

*B.*

2

*C.*

3

*D.*

4

== Solution

Correct answer: C

3

#pagebreak()

= Question 15

The graph of $y = f \(x \)$ contains the point $\(a \, b \)$. The graph of $g \(x \)$ is a transformation of the

graph of $f \(x \)$ and contains the point \( $3  a \, b $ \).

Identify the function that represents $g \(x \)$.

*A.*

$g \(x \)= f \(3  x \)$

*B.*

$g \(x \)= 3  f \(x \)$

*C.*

$g \(x \)= f lr(\( frac(x ,3 )\) )$

*D.*

$g \(x \)= frac(1 ,3 ) f \(x \)$

== Solution

Correct answer: C

$g \(x \)= f lr(\( frac(x ,3 )\) )$

#pagebreak()

= Question 16

The angle 2.95 radians\, in standard position\, terminates in quadrant:

*A.*

I

*B.*

II

*C.*

III

*D.*

IV

== Solution

Correct answer: B

II

#pagebreak()

= Question 17

Evaluate:

$  2  sin  frac(pi ,8 ) cos  frac(pi ,8 )  $

*A.*

$frac(1 ,2 )$

*B.*

$frac(sqrt(2 ),2 )$

*C.*

1

*D.*

$sqrt(2 )$

== Solution

Correct answer: B

$frac(sqrt(2 ),2 )$

#pagebreak()

= Question 18

Identify which of the following represents the 5th term in the expansion of $lr(\( 4  x ^(2 )- 2  y ^(3 )\) )^(15 )$.

*A.*

$ "" _(15 ) C _(5 )lr(\( 4  x ^(2 )\) )^(10 )lr(\( - 2  y ^(3 )\) )^(5 )$

*B.*

$ "" _(15 ) C _(5 )lr(\( 4  x ^(2 )\) )^(11 )lr(\( - 2  y ^(3 )\) )^(4 )$

*C.*

$ "" _(15 ) C _(4 )lr(\( 4  x ^(2 )\) )^(10 )lr(\( - 2  y ^(3 )\) )^(5 )$

*D.*

$ "" _(15 ) C _(4 )lr(\( 4  x ^(2 )\) )^(11 )lr(\( - 2  y ^(3 )\) )^(4 )$

== Solution

Correct answer: D

$ "" _(15 ) C _(4 )lr(\( 4  x ^(2 )\) )^(11 )lr(\( - 2  y ^(3 )\) )^(4 )$

#pagebreak()

= Question 19

Identify which of the following graphs of polynomial functions has a zero with a multiplicity

of 3 .

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-03_604_624_494_401.jpg", width: 29.4%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-03_594_617_494_1134.jpg", width: 29.0%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-03_599_620_1213_416.jpg", width: 29.2%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-03_598_615_1211_1160.jpg", width: 28.9%)

== Solution

Correct answer: B

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-03_594_617_494_1134.jpg", width: 29.0%)

#pagebreak()

= Question 20

A non-permissible value of $x $ for the function $f \(x \)= frac(1 ,cos  x + 1 )$ is:

*A.*

-1

*B.*

0

*C.*

$pi $

*D.*

$frac(3  pi ,2 )$

== Solution

Correct answer: C

$pi $

#pagebreak()

= Question 21

Identify which of the following statements is true for the rational function $f \(x \)= frac(4 \(x - 1 \)\(x - 2 \),\(x - 1 \)\(x + 3 \))$.

*A.*

The equation of the horizontal asymptote is $y = 4 $.

*B.*

The equation of the vertical asymptote is $x = 1 $.

*C.*

The $y $-intercept is 0 .

*D.*

There is a point of discontinuity \(hole\) when $x = 2 $.

== Solution

Correct answer: A

The equation of the horizontal asymptote is $y = 4 $.

#pagebreak()

= Question 22

Determine the equation of the polynomial function\, $p \(x \)$\, represented by the graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-05_914_882_431_259.jpg", width: 41.5%)

$p \(x \)= $

== Solution

$p \(x \)= 3 \(x + 2 \)^(2 )\(x - 1 \)^(2 )$

1 mark for factors

1 mark for multiplicity of 2 \( $frac(1 ,2 )$ mark for each\)

1 mark for correct value of $a $ \(consistent with

factors and multiplicity\)

3 marks

#pagebreak()

= Question 23

Evaluate:

$log  _(4 ) 2 $

== Solution

$  frac(1 ,2 )  $

#pagebreak()

= Question 24

Evaluate:

$  lr(\( cos  frac(11  pi ,3 )\) )lr(\( csc  frac(11  pi ,6 )\) )  $

== Solution

$lr(\( frac(1 ,2 )\) )\(- 2 \)$

1 mark for $cos  frac(11  pi ,3 )$ \( $frac(1 ,2 )$ mark for the quadrant\, $frac(1 ,2 )$ mark for the value\)

1 mark for $csc  frac(11  pi ,6 )$ \( $frac(1 ,2 )$ mark for the quadrant\, $frac(1 ,2 )$ mark for the value\)

-1

2 marks

#pagebreak()

= Question 25

Estimate the value of $log  _(2 ) 5 $.

Justify your answer.

== Solution

$  lr( mat(delim: #none,  log  _(2 ) 4 = 2  "" ; log  _(2 ) 8 = 3  )\} ) quad  frac(1 ,2 ) " mark for justification "  $

1 mark

#pagebreak()

= Question 26

If $theta $ terminates in quadrant III and $cos  theta = - frac(6 ,7 )$\, determine the exact value of $tan  theta $.

== Solution

$   cos  theta  & = frac(x ,r ) & & \  x ^(2 )+ y ^(2 ) & = r ^(2 ) & & \  y ^(2 ) & = \(7 \)^(2 )- \(- 6 \)^(2 ) & & 1  \/ 2  " mark for substitution of " x = - 6  " and " r = 7  \  y ^(2 ) & = 13  & & \  y  & =  plus.minus  sqrt(13 ) & & 1  \/ 2  " mark for solving for " y  \  tan  theta  & = frac(sqrt(13 ),6 ) & & 1  " mark for the value of " tan  theta lr(\( frac(1 ,2 ) " mark for the quadrant, " frac(1 ,2 ) ) " mark for the value) "   $

#pagebreak()

= Question 27

Given $f \(x \)= x ^(2 )+ x - 4 $ and $g \(x \)= sqrt(x + 5 )$\, Taz was asked to find $f \(g \(x \)\)$.

Taz's solution:

$   f \(g \(x \)\) & = \(sqrt(x + 5 )\)^(2 )+ x - 4  \  & = x + 5 + x - 4  \  & = 2  x + 1 \, x  >= - 5    $

Describe the error in Taz's solution.

== Solution

Taz must substitute $g \(x \)$ in both terms containing $x $ in $f \(x \)$ and then simplify.

#pagebreak()

= Question 28

Sketch the graph of the function $f \(x \)= 3  log  _(2 )\(x + 1 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-11_949_948_588_524.jpg", width: 44.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/839a1b74-eb73-46b8-825b-6d9f99ade6b8-25_917_941_587_148.jpg", width: 44.3%)

1 mark for increasing logarithmic function

1 mark for vertical stretch

1 mark for asymptotic behaviour at $x = - 1 $

3 marks

#pagebreak()

= Question 29

Write an equation of a rational function that would not have any vertical asymptotes.

== Solution

Various equations\, such as the following\, are possible:

$  y = frac(\(x - 2 \)\(x + 1 \),\(x - 2 \))  $

or

$  y = frac(4 ,x ^(2 )+ 4 )  $

#pagebreak()

= Question 30

Determine the exact value of $tan  75 ^(degree )$.

== Solution

$   tan  75 ^(degree ) & = tan  lr(\( 30 ^(degree )+ 45 ^(degree )\) ) \  & = frac(tan  30 ^(degree )+ tan  45 ^(degree ),1 - tan  30 ^(degree ) tan  45 ^(degree )) \  & = frac(frac(1 ,sqrt(3 ))+ 1 ,1 - frac(1 ,sqrt(3 ))\(1 \)) \  & = frac(frac(1 + sqrt(3 ),sqrt(3 )),frac(sqrt(3 )- 1 ,sqrt(3 ))) \  & = frac(1 + sqrt(3 ),sqrt(3 )- 1 )   $

or

$  = frac(sqrt(3 )+ 3 ,3 - sqrt(3 ))  $

1 mark for combination

1 mark for exact values \( $frac(1 ,2 )$ mark for each\)

2 marks

- Other combinations are possible.

#pagebreak()

= Question 31

Sketch the graph of the following function:

$  f \(x \)= frac(\(x + 3 \)\(x - 3 \),x \(x - 3 \))  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-14_893_946_657_569.jpg", width: 44.5%)

== Solution

$   f \(x \)=  & frac(\(x + 3 \)\(x  \/- 3 \),x \(y - 3 \)) \  & = frac(x + 3 ,x )\, x  !=  3    $

∴ there is a point of discontinuity \(hole\) at $\(3 \,2 \)$

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/839a1b74-eb73-46b8-825b-6d9f99ade6b8-28_980_849_1059_155.jpg", width: 40.0%)

1 mark for asymptotic behaviour at $y = 1 $

1 mark for asymptotic behaviour at $x = 0 $

1 mark for point of discontinuity \(hole\) at $\(3 \,2 \)$

\( $frac(1 ,2 )$ mark for $x = 3 \, frac(1 ,2 )$ mark for $y = 2 $ \)

$frac(1 ,2 )$ mark for graph left of vertical asymptote

$frac(1 ,2 )$ mark for graph right of vertical asymptote

4 marks

#pagebreak()

= Question 32

In the binomial expansion of $lr(\( frac(1 ,x ^(3 ))- 2  x ^(2 )\) )^(9 )$\, determine which term contains $x ^(3 )$.

== Solution

Method 1

$   x ^(3 ) & = lr(\( x ^(- 3 )\) )^(9 - k )lr(\( x ^(2 )\) )^(k ) \  x ^(3 ) & = x ^(- 27 + 3  k + 2  k ) \  3  & = - 27 + 3  k + 2  k  \  30  & = 5  k  \  6  & = k    $

∴ term 7 would contain $x ^(3 )$

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $k $

1 mark for identifying the 7th term

\(or consistent term with the value of $k $ \)

2 marks

Method 2

$   & lr(\( frac(1 ,x ^(3 ))\) )^(9 )\,lr(\( frac(1 ,x ^(3 ))\) )^(8 )lr(\( x ^(2 )\) )\,lr(\( frac(1 ,x ^(3 ))\) )^(7 )lr(\( x ^(2 )\) )^(2 ) \  & x ^(- 27 )\, x ^(- 22 )\, x ^(- 17 )   $

∴ term 7 would contain $x ^(3 )$

1 mark for determining the pattern

1 mark for identifying the 7th term

\(or consistent term with the pattern\)

2 marks

#pagebreak()

= Question 33

José and Dana get on a Ferris wheel\, which is 1 metre off the ground. The diameter of the Ferris

wheel is 16 metres. Their ride lasts for 4 minutes\, in which time the Ferris wheel makes one

revolution.

Determine the values of $upright(A )\, upright(B )\, upright(C )$\, and D \, if the sinusoidal function that models the situation is

$h \(t \)= A  cos  \[B \(t - C \)\]+ D $\, where $h $ is the height at which José and Dana are located on the

Ferris wheel\, from the ground\, in metres\, and $t $ is the time\, in minutes.

$upright(A )= $

$\_ \_ \_ \_ $

$upright(B )= $

$\_ \_ \_ \_ $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-16_472_618_747_951.jpg", width: 29.1%)

$upright(C )= $

$\_ \_ \_ \_ $

$upright(D )= $

$\_ \_ \_ \_ $

== Solution

$   A  & = frac(8 ,frac(pi ,2 )) \  B  & = frac(2 ,9 ) \  C  & = frac(2 ,D ) \  D  & = 9    $

$  " or " quad  mat(delim: #none,  A = frac(- 8 ,B = ) "" , 1  " mark for " A  "" ; C = frac(frac(pi ,2 ),0 ) "" , 1  " mark for " B  "" ; D = frac(9 ,1  " mark for " C ) "" ; 1  " mark for " D  )  $

4 marks

$\_ \_ \_ \_ $

Note\(s\)

- Other answers are possible.

#pagebreak()

= Question 34

Solve algebraically:

$   "" _(n ) P _(3 )= 4 ! \(n - 1 \)  $

== Solution

$   frac(n ! ,\(n - 3 \)! ) & = 4 ! \(n - 1 \) \  frac(n \(n - 1 \)\(n - 2 \)\(n - 3 \)! ,\(n - 3 \)! ) & = 4 ! \(n - 1 \) \  n \(n - 2 \) & = 24  \  n ^(2 )- 2  n - 24  & = 0  \  \(n - 6 \)\(n + 4 \) & = 0  \  n = 6  n  >= - 4  &   $

$frac(1 ,2 )$ mark for substitution

1 mark for factorial expansion

$frac(1 ,2 )$ mark for simplification of factorials

$frac(1 ,2 )$ mark for rejecting extraneous root

$frac(1 ,2 )$ mark for the value of $n $

3 marks

#pagebreak()

= Question 35

Given $f \(x \)= frac(2 ,x - 1 )$\, determine the equation of the inverse\, $f ^(- 1 )\(x \)$.

== Solution

Method 1

let $y = f \(x \)$

$  f \(x \)= frac(2 ,x - 1 )  $

$  y = frac(2 ,x - 1 )  $

$  x = frac(2 ,y - 1 )  $

$  y - 1 = frac(2 ,x )  $

$  y = frac(2 ,x )+ 1   $

$  f ^(- 1 )\(x \)= frac(2 ,x )+ 1   $

1 mark for switching $x $ and $y $ values

$frac(1 ,2 )$ mark for solving for $y $

$frac(1 ,2 )$ mark for writing equation of $f ^(- 1 )\(x \)$

Method 2

let $y = f \(x \)$

$  f \(x \)= frac(2 ,x - 1 )  $

$  y = frac(2 ,x - 1 )  $

$  x = frac(2 ,y - 1 )  $

$  x \(y - 1 \)= 2   $

$  x  y - x = 2   $

$  x  y = 2 + x   $

$  y = frac(2 + x ,x )  $

$  f ^(- 1 )\(x \)= frac(2 + x ,x )  $

2 marks

1 mark for switching $x $ and $y $ values

$frac(1 ,2 )$ mark for solving for $y $

$frac(1 ,2 )$ mark for writing equation of $f ^(- 1 )\(x \)$

2 marks

#pagebreak()

= Question 36

Solve:

$  4  log  _(3 ) 2 - frac(1 ,3 ) log  _(3 ) 8 = log  _(3 ) a   $

== Solution

Method 1

$   log  _(3 ) 2 ^(4 )- log  _(3 ) 8 ^(frac(1 ,3 )) & = log  _(3 ) a  \  log  _(3 ) 16 - log  _(3 ) 2  & = log  _(3 ) a  \  log  _(3 )lr(\( frac(16 ,2 )\) ) & = log  _(3 ) a  \  log  _(3 ) 8  & = log  _(3 ) a  \  a  & = 8    $

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

1 mark for quotient law

1 mark for equating arguments

3 marks

Method 2

$   log  _(3 ) 2 ^(4 )- log  _(3 ) 8 ^(frac(1 ,3 ))- log  _(3 ) a  & = 0  \  log  _(3 ) 16 - log  _(3 ) 2 - log  _(3 ) a  & = 0  \  log  _(3 )lr(\( frac(16 ,2  a )\) ) & = 0  \  log  _(3 )lr(\( frac(8 ,a )\) ) & = 0  \  3 ^(0 ) & = frac(8 ,a ) \  1  & = frac(8 ,a ) \  a  & = 8    $

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

1 mark for quotient law

1 mark for exponential form

3 marks

#pagebreak()

= Question 37

Sketch the graph of at least one period of the function $y = 3  cos  \(pi  x \)- 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-20_874_1221_534_337.jpg", width: 57.5%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/839a1b74-eb73-46b8-825b-6d9f99ade6b8-34_877_922_610_174.jpg", width: 43.4%)

$   " period " & = frac(2  pi ,pi ) \  & = 2    $

1 mark for amplitude

1 mark for period

1 mark for vertical translation

3 marks

#pagebreak()

= Question 38

Using the laws of logarithms\, fully expand the expression:

$  log  _(a )lr(\( frac(x ^(3 ),y  sqrt(z ))\) )  $

== Solution

$   log  _(a )lr(\( frac(x ^(3 ),y  sqrt(z ))\) ) & = log  _(a ) x ^(3 )- lr(\( log  _(a ) y + log  _(a ) sqrt(z )\) ) \  & = 3  log  _(a ) x - lr(\( log  _(a ) y + frac(1 ,2 ) log  _(a ) z \) ) \  & = 3  log  _(a ) x - log  _(a ) y - frac(1 ,2 ) log  _(a ) z    $

1 mark for quotient law

1 mark for product law

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

3 marks

#pagebreak()

= Question 39

Sketch the graph of $f \(x \)= 3  sqrt(x - 2 )+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-22_961_1006_595_554.jpg", width: 47.3%)

== Solution

Method 1

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/839a1b74-eb73-46b8-825b-6d9f99ade6b8-36_898_952_614_204.jpg", width: 44.8%)

1 mark for horizontal translation

1 mark for vertical translation

1 mark for shape of a radical function

1 mark for vertical stretch

4 marks

Method 2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/839a1b74-eb73-46b8-825b-6d9f99ade6b8-36_904_980_1566_206.jpg", width: 46.1%)

1 mark for invariant points where $y = 0 $

and $y = 1 $ \( $frac(1 ,2 )$ mark for each point\)

1 mark for domain $\[2 \, oo \)$

$frac(1 ,2 )$ mark for shape between invariant

points

$frac(1 ,2 )$ mark for shape to the right of the

invariant points

1 mark for applying transformations

\( $frac(1 ,2 )$ mark for vertical stretch\, $frac(1 ,2 )$ mark for

vertical translation\)

4 marks

#pagebreak()

= Question 40

a\) Determine the domain of the graph of the function $f \(x \)= sqrt(x ^(2 )- 4 )$.

b\) Explain why the domain of $f \(x \)= sqrt(x ^(2 )- 4 )$ is restricted.

== Solution

a\)

$   \{ x  divides  x  <= - 2  union  x  >=  2 \}  \  " or " \  upright(D ): \(- oo \,- 2 \] union \[2 \, oo \)   $

1 mark for domain \( $frac(1 ,2 )$ mark for $x  <= - 2 \, frac(1 ,2 )$ mark

for $x  >=  2 $ \)

1 mark

b\) The domain is restricted because you cannot take

the square root of a negative number.

#pagebreak()

= Question 41

a\) 1 mark b\) 1 mark $quad  "" _(136 )^(135 )$

Given the point $\(- 12 \,- 18 \)$ on the graph of $f \(x \)$\, determine the new points after the following

transformations of $f \(x \)$.

a\) $frac(1 ,f \(x \))$

b\) $f \(- x \)+ 10 $

== Solution

a\) $lr(\( - 12 \, frac(- 1 ,18 )\) )$

b\) \(12\, -8\)

1 mark \( $frac(1 ,2 )$ mark for $x $-value\, $frac(1 ,2 )$ mark for $y $-value \)

1 mark

#pagebreak()

= Question 42

Explain why there is no solution for the equation $csc  theta = - frac(1 ,2 )$.

== Solution

The value of $csc  theta $ cannot be between -1 and 1 .

or

The value of $sin  theta $ cannot be less than -1 .

#pagebreak()

= Question 43

Given the graph of $y = f \(x \)$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-26_880_927_472_348.jpg", width: 43.6%)

sketch the graph of $y = | f \(2  x \)| + 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-26_891_927_1574_386.jpg", width: 43.6%)

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

1 mark for absolute value
1 mark for horizontal compression
1 mark for vertical translation
3 marks
y
x
1
1



y
x

#pagebreak()

= Question 44

Given $f \(x \)= 2 ^(x )+ 1 $\, state the equation of the horizontal asymptote.

== Solution

$  y = 1   $

#pagebreak()

= Question 45

Given the following graphs of $f \(x \)= x - 3 $ and $g \(x \)= x + 1 $\,

$f \(x \)$

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-28_678_676_528_266.jpg", width: 31.8%)

$g \(x \)$

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-28_686_684_524_1108.jpg", width: 32.2%)

sketch the graph of $h \(x \)= \(f  dot.c  g \)\(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/89ed7ef7-6902-4193-9e15-e3119962ed93-28_686_678_1482_747.jpg", width: 31.9%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2016-jan/assets/839a1b74-eb73-46b8-825b-6d9f99ade6b8-42_672_668_1474_204.jpg", width: 31.4%)

1 mark for operation of multiplication

1 mark for shape representing the given operation

2 marks