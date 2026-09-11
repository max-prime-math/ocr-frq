#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2017-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

\(4ini

There are 24 different movies Kiandra can download to her computer. Determine the number of ways

she can select 15 movies.

== Solution

$ "" _(24 ) C _(15 )= 1307504 $ combinations

#pagebreak()

= Question 2

Given $theta = 40 ^(degree )$\,

a\) convert $theta $ to radians.

b\) determine the coterminal angles of $theta $ where $theta  in  bb(R )$.

== Solution

a\)

$   theta = 40 lr(\( frac(pi ,180 )\) ) \  theta = frac(2  pi ,9 )   $

or

$  theta = 0.698   $

b\)

$  theta = frac(2  pi ,9 )+ 2  pi  k  in  bb(Z )  $

or

$  theta = 0.698 + 2  pi  k  in  bb(Z )  $

or

$  theta = 40 ^(degree )+ 360 ^(degree ) k \, k  in  bb(Z )  $

#pagebreak()

= Question 3

\(4111

Peter invests $dollar  560 $ per month at an annual interest rate of $4.2  % $\, compounded monthly. Determine how

many monthly investments he will need to make to obtain at least $dollar  500000 $.

Express your answer as a whole number.

Use the formula:

$  upright(F V )= frac(upright(R )lr(\[ \(1 + i \)^(n )- 1 \] ),i )  $

where $upright(F V )= $ the future value

$upright(R )= $ the investment amount each period

$i = frac(" the annual interest rate "," the number of compounding periods per year ")$

$n = $ the number of investments

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$500000 = frac(560 lr(\[ lr(\( 1 + frac(0.042 ,12 )\) )^(n )- 1 \] ),frac(0.042 ,12 )) 500000 = frac(560 lr(\[ \(1 + 0.0035 \)^(n )- 1 \] ),0.0035 ) 500000 = 160000 lr(\( 1.0035 ^(n )- 1 \) ) 3.125 = 1.0035 ^(n )- 14.125 = 1.0035 ^(n ) log  4.125 = log  1.0035 ^(n ) log  4.125 = n  log  1.0035  n = frac(log  4.125 ,log  1.0035 ) n = 405.584 $ ∴ 406 monthly investments are needed. ], [$frac(1 ,2 )$ mark for substitution $frac(1 ,2 )$ mark for simplification $frac(1 ,2 )$ mark for applying logarithms 1 mark for power law $frac(1 ,2 )$ mark for solving for $n $ 3 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 4

Ishmael has 4 dogs\, 5 cats\, and 3 horses.

If he arranges all of them in a row\, determine how many ways they can be arranged if each type of

animal must be grouped together.

== Solution

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[3! • ], [4! ], [- 5! ], [- 3! ], [$= 103680 $ ways ],
table.hline(stroke: .5pt),
[types ], [dogs ], [cats ], [horses ], [],
table.hline(stroke: .5pt),
[of ], [], [], [], [],
table.hline(stroke: .5pt),
[animals ], [], [], [], [],
table.hline(stroke: .5pt),
[],
);

1 mark for arrangement of types of animals

1 mark for arrangement of dogs\, cats\, and horses

#pagebreak()

= Question 5

Solve the following equation algebraically over the interval $0  <=  theta  <=  2  pi $.

$  2  cos  ^(2 ) theta + 9  cos  theta - 5 = 0   $

== Solution

$   & 2  cos  ^(2 ) theta + 9  cos  theta - 5 = 0  \  & \(2  cos  theta - 1 \)\(cos  theta + 5 \)= 0  \  & cos  theta = frac(1 ,2 ) quad  cos  theta = - 5  \  & quad  theta = frac(pi ,3 )\, frac(5  pi ,3 ) quad  " no solution "   $

1 mark for solving for $cos  theta $

2 marks for solving for $theta $

\( $frac(1 ,2 )$ mark for each value\, 1 mark for indicating no solution\)

3 marks

#pagebreak()

= Question 6

Determine which term contains $frac(1 ,x ^(6 ))$ in the binomial expansion of $lr(\( frac(2 ,x ^(3 ))+ 3  x ^(2 )\) )^(7 )$.

== Solution

Method 1

$   lr(\( x ^(- 3 )\) )^(7 - k )lr(\( x ^(2 )\) )^(k ) & = x ^(- 6 ) \  x ^(- 21 + 3  k ) x ^(2  k ) & = x ^(- 6 ) \  x ^(- 21 + 5  k ) & = x ^(- 6 ) \  - 21 + 5  k  & = - 6  \  5  k  & = 15  \  k  & = 3    $

∴ the fourth term contains $frac(1 ,x ^(6 ))$

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $k $

1 mark for the $4  "" ^("th ")$ term \(or a term

consistent with the value of $k $ \)

2 marks

Method 2

$   & lr(\( frac(1 ,x ^(3 ))\) )^(7 )\,lr(\( frac(1 ,x ^(3 ))\) )^(6 )lr(\( x ^(2 )\) )\,lr(\( frac(1 ,x ^(3 ))\) )^(5 )lr(\( x ^(2 )\) )^(2 )\, dots.h  \  & frac(1 ,x ^(21 ))\, frac(1 ,x ^(16 ))\, frac(1 ,x ^(11 ))\, dots.h  \  & therefore  " the fourth term contains " frac(1 ,x ^(6 ))   $

1 mark for determining a pattern

1 mark for the $4  "" ^("th ")$ term \(or a term

consistent with the pattern\)

2 marks

#pagebreak()

= Question 7

Determine the radius of a circle which has an arc length of 5 cm with a central angle of 3 radians.

== Solution

$   & s = theta  r  \  & 5 = 3  r  \  & r = frac(5 ,3 ) upright(space.nobreak c m )   $

#pagebreak()

= Question 8

Tyler incorrectly sketched the angle $theta = - frac(7  pi ,4 )$ in standard position.

Describe his error.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-08_557_654_653_225.jpg", width: 30.8%)

== Solution

Tyler incorrectly indicated the direction of the angle as positive.

or

Tyler sketched the reference angle\, not $theta = - frac(7  pi ,4 )$.

#pagebreak()

= Question 9

Given the identity $sec  theta + cos  theta = frac(2 - sin  ^(2 ) theta ,cos  theta )$\,

a\) determine the non-permissible values of $theta $\, over the interval $0  <=  theta  <=  2  pi $.

b\) prove the identity for all permissible values of $theta $.

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

a\) $cos  theta = 0 $

$  theta = frac(pi ,2 )\, frac(3  pi ,2 )  $

1 mark for non-permissible values

\( $frac(1 ,2 )$ mark for each value\)

1 mark

Method 1

b\)

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   & sec  theta + cos  theta  \  & frac(1 ,cos  theta )+ cos  theta  \  & frac(1 + cos  ^(2 ) theta ,cos  theta ) \  & frac(1 + 1 - sin  ^(2 ) theta ,cos  theta ) \  & frac(2 - sin  ^(2 ) theta ,cos  theta )   $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[$  frac(2 - sin  ^(2 ) theta ,cos  theta )  $ ],
[1 mark for correct substitution of appropriate identities ],
[1 mark for algebraic strategies ],
[1 mark for logical process to prove the identity ],
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
[$sec  theta + cos  theta $ ], [$   & frac(2 - sin  ^(2 ) theta ,cos  theta ) \  & frac(2 - lr(\( 1 - cos  ^(2 ) theta \) ),cos  theta ) \  & frac(1 + cos  ^(2 ) theta ,cos  theta ) \  & frac(1 ,cos  theta )+ frac(cos  ^(2 ) theta ,cos  theta ) \  & sec  theta + cos  theta    $ ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 10

Expand using the laws of logarithms.

$  log  lr(\( frac(a ,b ^(4 ))\) )  $

== Solution

$log  a - log  b ^(4 )$

$  log  a - 4  log  b   $

1 mark for quotient law

1 mark for power law

2 marks

#pagebreak()

= Question 11

State the equation of $g \(x \)$ in terms of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-11_815_895_468_193.jpg", width: 42.1%)

$  g \(x \)=   $

$\_ \_ \_ \_ $

== Solution

$  g \(x \)= f \(2  x \)+ 3   $

1 mark for horizontal compression

1 mark for vertical translation

2 marks

#pagebreak()

= Question 12

Explain why the inverse of the graph of $y = f \(x \)$ is not a function.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-12_755_932_451_227.jpg", width: 43.9%)

== Solution

The domain of $f \(x \)$ was not restricted to ensure there is only one value of $y $ for each $x $ and

one value of $x $ for each $y $.

or

The graph of the inverse will not pass the vertical line test.

or

The graph of $f \(x \)$ does not pass the horizontal line test.

#pagebreak()

= Question 13

Solve the following equation algebraically:

$  log  lr(\( x ^(2 )+ 5 \) )- log  lr(\( x ^(2 )+ 1 \) )= log  3   $

== Solution

$  frac(x ^(2 )+ 5 ,x ^(2 )+ 1 )= 3   $

$  x ^(2 )+ 5 = 3 lr(\( x ^(2 )+ 1 \) )  $

$  x ^(2 )+ 5 = 3  x ^(2 )+ 3   $

$  2 = 2  x ^(2 )  $

$  1 = x ^(2 )  $

$  plus.minus  1 = x   $

1 mark for quotient law

$frac(1 ,2 )$ mark for equating arguments

$frac(1 ,2 )$ mark for solving for $x $

2 marks

#pagebreak()

= Question 14

Describe the transformations used to obtain the graph of the function $y = 5  f \(x + 1 \)$ from the graph of

$y = f \(x \)$.

== Solution

Vertically stretch the graph by a factor of 5 and translate the graph one unit left.

1 mark for vertical stretch

1 mark for horizontal translation

2 marks

#pagebreak()

= Question 15

Solve algebraically:

$   "" _(n ) C _(2 )= 3  n + 4   $

== Solution

$  mat(delim: #none,  frac(n ! ,\(n - 2 \)! 2 ! ) "" , = 3  n + 4  "" ; frac(n \(n - 1 \)\(n - 2 \)! ,frac(\(n - 2 \)! ,n \(n - 1 \))) "" , = 2 ! \(3  n + 4 \) "" ; n ^(2 )- n  "" , = 6  n + 8  "" ; n ^(2 )- 7  n - 8  "" , = 0  "" ; \(n - 8 \)\(n + 1 \) "" , = 0  "" ; n = 8  "" , n = - 1  )  $

$frac(1 ,2 )$ mark for substitution into equation

1 mark for factorial expansion

$frac(1 ,2 )$ mark for simplification of factorials

$frac(1 ,2 )$ mark for rejecting the extraneous root

$frac(1 ,2 )$ mark for the value of $n $

3 marks

#pagebreak()

= Question 16

Given the graph of $f \(x \)$\, sketch the graph of $y = lr(|  frac(1 ,2 ) f \(x - 1 \)|  )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-16_706_779_489_225.jpg", width: 36.7%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-16_723_776_1336_335.jpg", width: 36.5%)

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

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-17_692_765_1298_204.jpg", width: 36.0%)

1 mark for vertical stretch

1 mark for horizontal translation

1 mark for absolute value

3 marks

#pagebreak()

= Question 17

Explain why $f \(x \)= \(x + 2 \)^(3 )\(x - 1 \)^(frac(1 ,2 ))$ is not a polynomial function.

== Solution

All factors in a polynomial function must have exponents that are whole numbers.

#pagebreak()

= Question 18

Given the graphs of $f \(x \)$ and $g \(x \)$\, sketch the graph of $h \(x \)= \(f  dot.c  g \)\(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-18_862_841_451_201.jpg", width: 39.6%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/ba01e0ee-030c-4799-9153-ce2c4f0a9405-18_858_841_1392_623.jpg", width: 39.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-19_857_829_1508_215.jpg", width: 39.0%)

#table(stroke: none,
columns: 4,
align: (left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4),
table.hline(stroke: .5pt),
[$x $ ], [$f \(x \)$ ], [$g \(x \)$ ], [$\(f  dot.c  g \)\(x \)$ ],
table.hline(stroke: .5pt),
[-1 ], [1 ], [-2 ], [-2 ],
table.hline(stroke: .5pt),
[1 ], [3 ], [-2 ], [-6 ],
table.hline(stroke: .5pt),
[3 ], [3 ], [2 ], [6 ],
table.hline(stroke: .5pt),
[],
);

1 mark for operation of multiplication

1 mark for restricted domain

2 marks

#pagebreak()

= Question 19

Identify the trigonometric function that is equivalent to $sin  frac(pi ,4 ) cos  frac(pi ,3 )+ cos  frac(pi ,4 ) sin  frac(pi ,3 )$.

*A.*

$quad  sin  frac(2  pi ,7 )$

*B.*

$quad  sin  frac(7  pi ,12 )$

*C.*

$quad  cos  frac(2  pi ,7 )$

*D.*

$quad  cos  frac(7  pi ,12 )$

== Solution

Correct answer: B

$quad  sin  frac(7  pi ,12 )$

#pagebreak()

= Question 20

Identify the logarithmic form of $5 ^(x )= 6 $.

*A.*

$log  _(5 ) x = 6 $

*B.*

$log  _(5 ) 6 = x $

*C.*

$log  _(6 ) x = 5 $

*D.*

$log  _(6 ) 5 = x $

== Solution

Correct answer: B

$log  _(5 ) 6 = x $

#pagebreak()

= Question 21

Given $f \(theta \)= 3  cos  2  theta - 1 $ and $g \(theta \)= sin  theta + 1 $\, identify which statement is true.

*A.*

Both functions have the same period.

*B.*

Both functions have the same amplitude.

*C.*

Both functions have the same minimum value.

*D.*

Both functions have the same maximum value.

== Solution

Correct answer: D

Both functions have the same maximum value.

#pagebreak()

= Question 22

Identify the fourth term in the expansion of $\(x + y \)^(5 )$.

*A.*

$10  x ^(4 ) y $

*B.*

$10  x ^(3 ) y ^(2 )$

*C.*

$10  x ^(2 ) y ^(3 )$

*D.*

$10  x  y ^(4 )$

== Solution

Correct answer: C

$10  x ^(2 ) y ^(3 )$

#pagebreak()

= Question 23

Given the graphs of $f \(x \)$ and $g \(x \)$\, identify the choice with all of the solutions of the equation

$f \(x \)= g \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-03_691_854_446_343.jpg", width: 40.2%)

*A.*

$x = - 2  pi \,- pi \, 0 \, pi \, 2  pi $

*B.*

$x = - frac(pi ,2 )\, 0 \, frac(pi ,2 )$

*C.*

$x = frac(pi ,2 )$

*D.*

$x = - 1 \,0 \,1 $

== Solution

Correct answer: B

$x = - frac(pi ,2 )\, 0 \, frac(pi ,2 )$

#pagebreak()

= Question 24

Identify the graph of $f ^(- 1 )\(x \)$ if $f \(x \)= x ^(2 )- 9 \, x  >=  0 $.

*A.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-04_644_677_519_292.jpg", width: 31.9%)

*B.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-04_644_676_519_1151.jpg", width: 31.8%)

*C.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-04_656_665_1375_296.jpg", width: 31.3%)

*D.*

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-04_663_695_1368_1151.jpg", width: 32.7%)

== Solution

Correct answer: D

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-04_663_695_1368_1151.jpg", width: 32.7%)

#pagebreak()

= Question 25

Using the remainder theorem\, identify which value of $x $ results in a remainder of zero given

$p \(x \)= x ^(3 )+ 7  x ^(2 )+ 14  x + 8 $.

*A.*

1

*B.*

0

*C.*

-1

*D.*

-3

== Solution

Correct answer: C

-1

#pagebreak()

= Question 26

Evaluate $cos  lr(\( cos  lr(\( frac(3  pi ,2 )\) )\) )$.

*A.*

1

*B.*

$frac(1 ,2 )$

*C.*

0

*D.*

-1

== Solution

Correct answer: A

1

#pagebreak()

= Question 27

Match the following equations with their graphs:

Place the appropriate letter

in this column.

$   & f \(x \)= \(x - 1 \)^(3 )\(x + 1 \)\(x - 3 \) \  & g \(x \)= \(x + 1 \)^(2 )\(x - 1 \)\(x + 3 \) \  & h \(x \)= - 2 \(x - 1 \)^(2 )\(x + 1 \)\(x - 3 \) \  & k \(x \)= 2 \(x + 1 \)^(2 )\(x - 1 \)\(x + 3 \)   $

A\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-06_587_611_1207_251.jpg", width: 28.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-06_562_592_1228_1082.jpg", width: 27.9%)

C\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-06_583_611_1925_251.jpg", width: 28.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-06_561_587_1912_1091.jpg", width: 27.6%)

== Solution

$  f \(x \)= \(x - 1 \)^(3 )\(x + 1 \)\(x - 3 \)  $

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$  g \(x \)= \(x + 1 \)^(2 )\(x - 1 \)\(x + 3 \)  $

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$  h \(x \)= - 2 \(x - 1 \)^(2 )\(x + 1 \)\(x - 3 \)  $

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$frac(1 ,2 )$ mark for each correct answer

2 marks

A\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-25_580_610_1186_260.jpg", width: 28.7%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-25_546_580_1203_1104.jpg", width: 27.3%)

C\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-25_578_606_1891_262.jpg", width: 28.5%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-25_548_584_1878_1109.jpg", width: 27.5%)

#pagebreak()

= Question 28

If $log  6 = p \, log  5 = r $ and $log  2 = q $\, express $log  60 $ in terms of $p \, q $ and $r $.

== Solution

$   log  60  & = log  \(6  dot.c  5  dot.c  2 \) \  & = log  6 + log  5 + log  2  \  & = p + r + q    $

$frac(1 ,2 )$ mark for combination

1 mark for product law

$frac(1 ,2 )$ mark for substitution

2 marks

#pagebreak()

= Question 29

Sketch the graph of $y = sqrt(- 2  x )+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-08_845_884_554_618.jpg", width: 41.6%)

== Solution

Method 1

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-27_580_855_679_206.jpg", width: 40.2%)

1 mark for shape of a radical function

1 mark for horizontal compression

1 mark for vertical translation

1 mark for horizontal reflection

4 marks

Method 2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-27_640_909_1392_174.jpg", width: 42.8%)

$frac(1 ,2 )$ mark for shape between invariant points

$frac(1 ,2 )$ mark for shape to the left of the invariant points

1 mark for invariant points where

$y = 0 $ and $y = 1 $ \( $frac(1 ,2 )$ mark for each point\)

1 mark for domain of $\(- oo \, 0 \]$

1 mark for vertical translation

4 marks

#pagebreak()

= Question 30

Justify why the letters of the word FRANCE have a greater number of possible arrangements than the

letters of the word CANADA.

== Solution

CANADA has repeated letters that\, when placed in different orders\, do not change the arrangements

of the letters.

FRANCE: 6!

CANADA: $frac(6 ! ,3 ! )$

1 mark

∴ France has a greater number of arrangements.

#pagebreak()

= Question 31

a\) 1 mark

b\) 3 marks

Given $f \(x \)= frac(1 ,x - 2 )$ and $g \(x \)= x + 5 $\,

a\) determine the equation for $f \(g \(x \)\)$.

$f \(g \(x \)\)= $

b\) sketch the graph of $f \(g \(x \)\)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-10_856_879_1555_277.jpg", width: 41.4%)

== Solution

a\)

$   f \(g \(x \)\) & = frac(1 ,\(x + 5 \)- 2 ) \  & = frac(1 ,x + 3 )   $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-29_851_956_1164_183.jpg", width: 45.0%)

#pagebreak()

= Question 32

a\) 3 marks

b\) 1 mark

127 128

Given that $sin  alpha = frac(3 ,7 )$\, where $alpha $ is in Quadrant II\, and $cos  beta = frac(4 ,5 )$\, where $beta $ is in Quadrant IV\,

determine the exact value of:

a\) $sin  \(alpha - beta \)$

b\) $cos  2  alpha $

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-30_1102_700_741_200.jpg", width: 32.9%)

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  x ^(2 )+ 9  & = 49  \  x ^(2 ) & = 40  \  x  & =  plus.minus  sqrt(40 ) quad  1  \/ 2  " mark for value of " x    $

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  16 + y ^(2 ) & = 25  \  y ^(2 ) & = 9  \  y  & =  plus.minus  3  quad  1  \/ 2  " mark for value of " y    $

$   sin  \(alpha - beta \) & = sin  alpha  cos  beta - cos  alpha  sin  beta  \  & = lr(\( frac(3 ,7 )\) )lr(\( frac(4 ,5 )\) )- lr(\( frac(- sqrt(40 ),7 )\) )lr(\( frac(- 3 ,5 )\) ) \  & = frac(12 ,35 )- frac(3  sqrt(40 ),35 ) \  & = frac(12 - 3  sqrt(40 ),35 ) " or " frac(12 - 6  sqrt(10 ),35 )   $

$frac(1 ,2 )$ mark for $cos  alpha $

$frac(1 ,2 )$ mark for $sin  beta $

1 mark for substitution into correct

identity

3 marks

Note\(s\):

- accept any of the following values for $x $ : $x =  plus.minus  sqrt(40 )\, x = - sqrt(40 )$ or $x = sqrt(40 )$

- accept any of the following values for $y :  y =  plus.minus  3 \, y = - 3 $ or $y = 3 $

$   cos  2  alpha  & = cos  ^(2 ) alpha - sin  ^(2 ) alpha  \  & = lr(\( frac(- sqrt(40 ),7 )\) )^(2 )- lr(\( frac(3 ,7 )\) )^(2 ) \  & = frac(40 ,49 )- frac(9 ,49 ) \  & = frac(31 ,49 )   $

or

$   cos  2  alpha  & = 2  cos  ^(2 ) alpha - 1  \  & = 2 lr(\( frac(- sqrt(40 ),7 )\) )^(2 )- 1  \  & = 2 lr(\( frac(40 ,49 )\) )- 1  \  & = frac(80 ,49 )- 1  \  & = frac(31 ,49 )   $

or

$   cos  2  alpha  & = 1 - 2  sin  ^(2 ) alpha  \  & = 1 - 2 lr(\( frac(3 ,7 )\) )^(2 ) \  & = 1 - 2 lr(\( frac(9 ,49 )\) ) \  & = 1 - frac(18 ,49 ) \  & = frac(31 ,49 )   $

1 mark for substitution of an appropriate identity

1 mark

#pagebreak()

= Question 33

Determine the domain and range of $f \(x \)= sqrt(x - 5 )- 1 $.

Domain:

$\_ \_ \_ \_ $

Range:

$\_ \_ \_ \_ $

== Solution

Domain: $\{ x  in  bb(R ) divides  x  >=  5 \}  quad $ or $\[5 \, oo \) quad  1 $ mark for domain

Range: $\{ y  in  bb(R ) divides  y  >= - 1 \} $ or $\[- 1 \, oo \) quad  1 $ mark for range

2 marks

#pagebreak()

= Question 34

Justify why 4.7 is a better estimate than 4.3 for the value of $log  _(2 ) 26 $.

== Solution

$  2 ^(4 )= 16  quad  2 ^(5 )= 32   $

or

$  log  _(2 ) 16 = 4  quad  log  _(2 ) 32 = 5   $

26 is closer to 32 than 16 \; therefore $log  _(2 ) 26 $ is closer to 5 than 4 .

#pagebreak()

= Question 35

Sketch the graph of the function:

$  f \(x \)= frac(x \(x - 2 \)\(x - 4 \),\(x - 2 \))  $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-14_841_826_623_620.jpg", width: 38.9%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-34_666_660_735_217.jpg", width: 31.1%)

1 mark for point of discontinuity \(hole\) at \(2\, -4\)

\( $frac(1 ,2 )$ mark for $x $ value\, $frac(1 ,2 )$ mark for $y $ value\)

$frac(1 ,2 )$ mark for shape of a parabola

$frac(1 ,2 )$ mark for end behaviour

2 marks

#pagebreak()

= Question 36

Evaluate:

$  sec  ^(2 )lr(\( frac(pi ,6 )\) )+ tan  lr(\( frac(7  pi ,6 )\) ) csc  lr(\( - frac(2  pi ,3 )\) )  $

== Solution

$lr(\( frac(2 ,sqrt(3 ))\) )^(2 )+ lr(\( frac(sqrt(3 ),3 )\) )lr(\( - frac(2 ,sqrt(3 ))\) ) quad  1 $ mark for $sec  lr(\( frac(pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for value\, $frac(1 ,2 )$ mark for quadrant $\)$

$lr(\( frac(4 ,3 )\) )- lr(\( frac(2 ,3 )\) )$

1 mark for $tan  lr(\( frac(7  pi ,6 )\) )$ \( $frac(1 ,2 )$ mark for value\, $frac(1 ,2 )$ mark for quadrant\)

1 mark for $csc  lr(\( - frac(2  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for value\, $frac(1 ,2 )$ mark quadrant $\)$

$frac(2 ,3 )$

3 marks

#pagebreak()

= Question 37

The graph of $f \(x \)= 3  x + 7 $ is reflected over the $y $-axis.

Determine the equation of the new function.

$  y =   $

== Solution

$  y = - 3  x + 7   $

or

$  y = f \(- x \)  $

1 mark

#pagebreak()

= Question 38

Determine the equations of all of the asymptotes of the function:

$  y = frac(2  x + 1 ,x - 3 )  $

== Solution

Horizontal asymptote at $y = 2 $

Vertical asymptote at $x = 3 $

1 mark for horizontal asymptote

1 mark for vertical asymptote

2 marks

#pagebreak()

= Question 39

One of the zeros of $p \(x \)= x ^(3 )+ 6  x ^(2 )- 32 $ is $x = 2 $. Determine all of the other zeros of $p \(x \)$.

== Solution

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [1 ], [6 ], [0 ], [-32 ],
table.hline(stroke: .5pt),
[], [↓ ], [2 ], [16 ], [32 ],
table.hline(stroke: .5pt),
[], [1 ], [8 ], [16 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or any equivalent strategy\)

$   & 0 = x ^(2 )+ 8  x + 16  \  & 0 = \(x + 4 \)\(x + 4 \) \  & x = - 4    $

$frac(1 ,2 )$ mark for the other factors

$frac(1 ,2 )$ mark for the other zeros

2 marks

#pagebreak()

= Question 40

Sketch the graph of $y = - 2 ^(x )+ 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-18_890_927_610_451.jpg", width: 43.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-39_713_773_602_236.jpg", width: 36.4%)

1 mark for shape of an exponential function

1 mark for vertical reflection

1 mark for asymptotic behaviour approaching $y = 2 $

3 marks

#pagebreak()

= Question 41

Given the function $f \(x \)= frac(2 ,x )- 1 $\, justify why $f \(f \(2 \)\)$ is undefined.

== Solution

$   f \(2 \) & = frac(2 ,2 )- 1  \  & = 1 - 1  \  & = 0    $

$f \(f \(2 \)\)= frac(2 ,0 )- 1 $\, which is undefined because the denominator

1 mark for justification

cannot be zero.

#pagebreak()

= Question 42

The following graph represents the volume of air in an adult's lungs. If $V \(t \)$ is the volume of air in

litres and $t $ is the time in seconds\, determine an equation that represents this sinusoidal function.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-20_731_830_552_210.jpg", width: 39.1%)

$V \(t \)= $

$\_ \_ \_ \_ $

== Solution

$   & V \(t \)= 2  sin  lr(\( frac(pi ,4 ) t \) )+ 4  \  & " or " \  & V \(t \)= 2  cos  lr(\[ frac(pi ,4 )\(t - 2 \)\] )+ 4    $

1 mark for amplitude

$frac(1 ,2 )$ mark for period

$frac(1 ,2 )$ mark for consistent value of $b $

1 mark for vertical translation

3 marks

#pagebreak()

= Question 43

Explain why the domain of $y = log  _(2 )\(x - 1 \)$ is $x > 1 $.

== Solution

The argument of a logarithmic function must be positive.

#pagebreak()

= Question 44

The point \( $- 2 \,7 $ \) is on the terminal arm of an angle in standard position.

Determine the coordinates of the corresponding point\, $P \(theta \)$\, on the unit circle.

== Solution

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) & & \  \(- 2 \)^(2 )+ \(7 \)^(2 ) & = r ^(2 ) & & 1  \/ 2  " mark for substitution of " x =  plus.minus  2  " and " y = 7  \  4 + 49  & = r ^(2 ) & & 1  \/ 2  " mark for solving for " r  \  53  & = r ^(2 ) & & 1  " mark for " P \(theta \)lr(\( frac(1 ,2 ) " mark for each coordinate "\) ) \  sqrt(53 ) & = r  & & 2  " marks "   $

#pagebreak()

= Question 45

Sketch a graph of $P \(x \)$ that satisfies all of the following conditions:

- $P \(x \)$ is a polynomial function of degree 3 .

- $P \(x \)$ has a zero at -3 with a multiplicity of 2 .

- $P \(x \)$ has a zero at 1 .

- $P \(x \)$ has a leading coefficient of -3 .

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/f3177ba0-85c3-4d33-bf0c-0701e65c42cc-23_1032_1041_870_543.jpg", width: 49.0%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2017-jan/assets/5665d807-3c85-4cac-967b-56709ae1fa6f-44_969_975_862_198.jpg", width: 45.9%)

#pagebreak()

= Question 46

Determine how many 4 -digit numbers greater than 4000 can be made using the digits $2 \,3 \,4 \,5 $\, and 6 if

repetitions are not allowed.

== Solution

$  frac(3 ,4 \,5 \,6 ) dot.c  frac(4 ," remaining options ") dot.c  frac(3 ,"" )= 72   $

1 mark for restriction of first digit

1 mark for fundamental counting principle

2 marks