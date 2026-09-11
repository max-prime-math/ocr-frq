#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2019-jun

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Avery has 4 adventure books\, 5 mystery books\, and 1 comic book.

Determine the number of ways he can arrange all of the books on his shelf if each type of book

must be grouped together.

== Solution

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[3! ], [4! ], [- 5! ], [- 1! ], [$= 17280 $ ways ],
table.hline(stroke: .5pt),
[types of books ], [adventure books ], [mystery books ], [comic book ], [],
table.hline(stroke: .5pt),
[],
);

1 mark for arrangement of types of books

1 mark for arrangement of adventure\,

mystery\, and comic books

2 marks

Note:

- 1! does not need to be shown.

#pagebreak()

= Question 2

Solve the following equation\, algebraically\, over the interval $\[0 \,2  pi \]$.

$  5  cos  ^(2 ) theta - cos  theta - sin  ^(2 ) theta = 0   $

== Solution

Use $sin^2 theta=1-cos^2 theta$:

$ 5cos^2 theta-cos theta-(1-cos^2 theta) &= 0 \
  6cos^2 theta-cos theta-1 &= 0 \
  (3cos theta+1)(2cos theta-1) &= 0 $

Hence $cos theta=-frac(1,3)$ or $cos theta=frac(1,2)$.

For $cos theta=-frac(1,3)$, the solutions on $[0,2pi]$ are

$ theta=arccos(-frac(1,3)) approx 1.911, quad theta=2pi-arccos(-frac(1,3)) approx 4.373. $

For $cos theta=frac(1,2)$, $theta=pi/3$ or $theta=5pi/3$.

Thus $theta approx 1.047, 1.911, 4.373, 5.236$ radians.

Scoring: 1 mark for the identity substitution; 1 mark for solving for $cos theta$; 2 marks for the four angle values.

#pagebreak()

= Question 3

Given that $- 6048  x ^(2 ) y ^(5 )$ is the sixth term in the expansion of $\(3  x - m \)^(7 )$\, determine $m $.

== Solution

$   - 6048  x ^(2 ) y ^(5 ) & =  "" _(7 ) C _(5 )\(3  x \)^(2 )\(- m \)^(5 ) & & 2  " marks "lr(\( 1  " mark for " "" _(7 ) C _(5 ) \; 1  \/ 2  " mark for each consistent factor "\) ) \  - 6048  x ^(2 ) y ^(5 ) & = 21 lr(\( 9  x ^(2 )\) )lr(\( - m ^(5 )\) ) & & \  - 6048  x ^(2 ) y ^(5 ) & = - 189  x ^(2 ) m ^(5 ) & & \  32  y ^(5 ) & = m ^(5 ) & & 1  \/ 2  " mark for simplification " \  2  y  & = m  & & 1  \/ 2  " mark for " m    $

3 marks

#pagebreak()

= Question 4

A series of blood tests measures the concentration of a prescribed drug. This concentration

decreases according to the formula $A = P  e ^(r  t )$ where:

$A $ is the concentration at time $t $

$P $ is the initial concentration

$r $ is the rate of change

$t $ is the time\, in hours\, after the first blood test

The initial concentration is 3.8900 units $\/ upright(m L )$. Three hours later\, the concentration is 1.7505 units $\/ upright(m L )$.

a\) Determine the rate of change\, $r $\, algebraically.

b\) Determine the concentration of the prescribed drug four hours after the initial concentration of

3.8900 units $\/ upright(m L )$ was measured. Express the answer correct to 4 decimal places.

Note: A calculator is not required for the remaining test questions.

== Solution

a\)

$   1.7505  & = 3.8900  e ^(r \(3 \)) & & 1  \/ 2  " mark for substitution " \  0.45  & = e ^(3  r ) & & \  ln  0.45  & = 3  r  ln  e  & & 1  \/ 2  " mark for applying logarithms " \  frac(ln  0.45 ,3 ) & = r  & & 1  \/ 2  " mark for power law " \  & & & 1  \/ 2  " mark for value of " r    $

or

$- 0.266169  dots.h = r $

2 marks

b\)

$   & A = 3.8900  e ^(- 0.266169 \(4 \)) \  & A = 1.341424  dots.h  \  & A = 1.3414  " units " \/ upright(m L )   $

1 mark for answer consistent with a\)

#pagebreak()

= Question 5

Ariane uses the formula $s = theta  r $ to determine the arc length of a circle that has a central angle of

$20 ^(degree )$ and a radius of 15 cm .

Below is Ariane's work:

$   & S = theta  r  \  & S = \(20 \)\(15 \) \  & S = 300  upright(space.nobreak c m )   $

Describe her error.

== Solution

When using the formula $s = theta  r $\, the angle must be in radians. Ariane did not convert the central

angle from degrees to radians.

#pagebreak()

= Question 6

Using the graphs below\, state the solution of the equation $2  x + 3 = 2  sqrt(- x )- 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/939644d1-2f7d-4085-8238-9942fda840a8-06_891_916_459_601.jpg", width: 43.1%)

== Solution

$  x = - 1   $

1 mark

#pagebreak()

= Question 7

Solve\, algebraically.

$  log  _(2 )\(x + 3 \)= 5 - log  _(2 )\(x - 1 \)  $

== Solution

Method 1

$   log  _(2 )\(x + 3 \)+ log  _(2 )\(x - 1 \) & = 5  \  log  _(2 )\[\(x + 3 \)\(x - 1 \)\] & = 5  \  x ^(2 )+ 2  x - 3  & = 2 ^(5 ) \  x ^(2 )+ 2  x - 3  & = 32  \  x ^(2 )+ 2  x - 35  & = 0  \  \(x + 7 \)\(x - 5 \) & = 0    $

$frac(1 ,2 )$ mark for solving for the permissible value of $x $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

3 marks

Method 2

$   log  _(2 )\(x + 3 \)+ log  _(2 )\(x - 1 \) & = 5  \  log  _(2 )\[\(x + 3 \)\(x - 1 \)\] & = log  _(2 ) 2 ^(5 ) \  x ^(2 )+ 2  x - 3  & = 32  \  x ^(2 )+ 2  x - 35  & = 0  \  \(x + 7 \)\(x - 5 \) & = 0  \  x  & = 5    $

$frac(1 ,2 )$ mark for the permissible value of $x $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

3 marks

#pagebreak()

= Question 8

Explain why the value of $n $ must be greater than or equal to the value of $r $\, when using $C _(n )$.

== Solution

The number of objects to select\, $r $\, cannot be greater than the total number of objects\, $n $.

1 mark

#pagebreak()

= Question 9

3 marks

110

Given that $y = | x | $\, determine the equation of the resulting function\, $g \(x \)$\, after the following

transformations:

- reflection in the $x $-axis

- vertical translation 5 units down

- horizontal stretch by a factor of 3

$g \(x \)= $

== Solution

$  g \(x \)= quad - lr(|  frac(1 ,3 ) x |  )- 5   $

1 mark for vertical reflection

1 mark for vertical translation

1 mark for horizontal stretch

3 marks

#pagebreak()

= Question 10

Explain why the graph of $y = frac(x - 1 ,x ^(2 )+ x - 6 )$ has a horizontal asymptote at $y = 0 $.

== Solution

As $x $ approaches positive or negative infinity\, $y $ approaches zero.

1 mark

or

The degree of the numerator is less than the degree of the denominator.

#pagebreak()

= Question 11

Given the graphs of $f \(x \)$ and $g \(x \)$\, evaluate $g \(f \(2 \)\)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/939644d1-2f7d-4085-8238-9942fda840a8-09_822_826_1417_285.jpg", width: 38.9%)

== Solution

$f \(2 \)= 4  quad  frac(1 ,2 )$ mark for the value of $f \(2 \)$

$g \(4 \)= - 2  quad  frac(1 ,2 )$ mark for consistent value of $g \(f \(2 \)\)$

1 mark

#pagebreak()

= Question 12

Kennedy was asked to solve the equation $tan  theta = 1 $ over all real numbers.

Below is Kennedy's solution:

$   & tan  theta = 1  \  & theta = frac(pi ,4 )\, frac(5  pi ,4 )   $

Describe her error.

== Solution

Kennedy did not include the general solution in her answer.

#pagebreak()

= Question 13

Solve\, algebraically.

$   "" _(n ) C _(3 )= 3 lr(\(  "" _(n ) P _(2 )\) )  $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$frac(n ! ,\(n - 3 \)! 3 ! )= frac(3  n ! ,\(n - 2 \)! )$ ], [1 mark for substitution into equation \( $frac(1 ,2 )$ mark for each side\) ],
table.hline(stroke: .5pt),
[$frac(n ! \(n - 2 \)! ,\(n - 3 \)! 3 ! )= 3  n ! $ ], [],
table.hline(stroke: .5pt),
[$frac(n ! \(n - 2 \)\(n - 3 \)! ,\(n - 3 \)! )= 3 ! \(3  n ! \)$ ], [1 mark for factorial expansion ],
table.hline(stroke: .5pt),
[$n - 2 = 3 ! \(3 \)$ ], [$frac(1 ,2 )$ mark for simplification of factorials ],
table.hline(stroke: .5pt),
[$n - 2 = 18 $ ], [],
table.hline(stroke: .5pt),
[$n = 20 $ ], [$frac(1 ,2 )$ mark for solving for $n $ ],
table.hline(stroke: .5pt),
[],
);

3 marks

#pagebreak()

= Question 14

Given the graph of $y = f \(x \)$\, sketch the graph of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/939644d1-2f7d-4085-8238-9942fda840a8-12_888_936_485_592.jpg", width: 44.0%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/939644d1-2f7d-4085-8238-9942fda840a8-12_897_942_1486_592.jpg", width: 44.3%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-14_855_900_1543_245.jpg", width: 42.4%)

1 mark for restricting domain

$frac(1 ,2 )$ mark for shape between invariant points

$frac(1 ,2 )$ mark for shape to the right of invariant points

2 marks

#pagebreak()

= Question 15

Prove the identity for all permissible values of $theta $.

$  frac(sec  theta - tan  theta  sin  theta ,tan  theta  sin  theta )= csc  ^(2 ) theta - 1   $

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
[$  frac(frac(1 ,cos  theta )- frac(sin  theta ,cos  theta ) dot.c  sin  theta ,frac(sin  theta ,cos  theta ) dot.c  sin  theta )  $ $  frac(frac(1 - sin  ^(2 ) theta ,cos  theta ),frac(sin  ^(2 ) theta ,cos  theta ))  $ $  frac(1 - sin  ^(2 ) theta ,sin  ^(2 ) theta )  $ $  frac(1 ,sin  ^(2 ) theta )- frac(sin  ^(2 ) theta ,sin  ^(2 ) theta )  $ $  csc  ^(2 ) theta - 1   $ ], [$csc  ^(2 ) theta - 1 $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 16

Sketch the angle of $- frac(pi ,12 )$ radians in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/939644d1-2f7d-4085-8238-9942fda840a8-14_734_849_534_653.jpg", width: 40.0%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-17_786_1502_681_428.jpg", width: 70.7%)

Note:

- If the directional arrow is not indicated\, deduct an E1 error \(final answer not stated\)

#pagebreak()

= Question 17

Given that $h \(x \)= 2  x ^(2 )- 7  x - 15 $\, determine possible equations of the functions $f \(x \)$ and

$g \(x \)$ if $h \(x \)= f \(x \) dot.c  g \(x \)$.

$f \(x \)= $

$\_ \_ \_ \_ $

$g \(x \)= $

$\_ \_ \_ \_ $

== Solution

$f \(x \)= underline(2  x + 3 ) quad  1 $ mark for two correct factors of $h \(x \)$

$  g \(x \)= x - 5   $

1 mark

Note:

- Other answers are possible.

#pagebreak()

= Question 18

The range of $y = f \(x \)$ is $- 6  <=  y  <=  12 $. The range of the transformed function $y = a  f \(x \)$ is

$- 2  <=  y  <=  4 $. Identify the value of $a $.

*A.*

-3

*B.*

$- frac(1 ,3 )$

*C.*

$frac(1 ,3 )$

*D.*

3

== Solution

Correct answer: C

$frac(1 ,3 )$

#pagebreak()

= Question 19

Identify the expression which is equivalent to $3  log  y - frac(1 ,2 ) log  x + log  z $.

*A.*

$log  lr(\( frac(y ^(3 ),sqrt(x ) z )\) )$

*B.*

$log  lr(\( frac(y ^(3 ) z ,sqrt(x ))\) )$

*C.*

$log  lr(\( frac(y ^(3 ),x ^(2 ) z )\) )$

*D.*

$log  lr(\( frac(y ^(3 ) z ,x ^(2 ))\) )$

== Solution

Correct answer: B

$log  lr(\( frac(y ^(3 ) z ,sqrt(x ))\) )$

#pagebreak()

= Question 20

Identify the measure of the angle $- frac(2  pi ,9 )$ in degrees.

*A.*

$- 400 ^(degree )$

*B.*

$- 40 ^(degree )$

*C.*

$40 ^(degree )$

*D.*

$320 ^(degree )$

== Solution

Correct answer: B

$- 40 ^(degree )$

#pagebreak()

= Question 21

If $y = f \(x \)$ has a domain of \[2\,5\] and a range of \[6\,10\]\, identify the domain of $y = f ^(- 1 )\(x \)$.

*A.*

$lr(\[ frac(1 ,2 )\, frac(1 ,5 )\] )$

*B.*

$\[- 5 \,- 2 \]$

*C.*

$\[- 10 \,- 6 \]$

*D.*

$\[6 \,10 \]$

== Solution

Correct answer: D

$\[6 \,10 \]$

#pagebreak()

= Question 22

Identify which of the following is a polynomial function.

*A.*

$p \(x \)= - frac(1 ,2 )\(x + 2 \)^(3 )\(x - 3 \)$

*B.*

$p \(x \)= 2  x ^(frac(1 ,2 ))+ x - 3 $

*C.*

$p \(x \)= 3  x ^(- 4 )+ x ^(2 )- 6 $

*D.*

$p \(x \)= 2 ^(x )+ 3 $

== Solution

Correct answer: A

$p \(x \)= - frac(1 ,2 )\(x + 2 \)^(3 )\(x - 3 \)$

#pagebreak()

= Question 23

Identify the total number of terms in the expansion of $\(x - y \)^(9 )$.

*A.*

8

*B.*

9

*C.*

10

*D.*

11

== Solution

Correct answer: C

10

#pagebreak()

= Question 24

Identify the exact value of $2  cos  ^(2 )lr(\( 15 ^(degree )\) )- 1 $.

*A.*

1

*B.*

$frac(1 ,2 )$

*C.*

$frac(sqrt(3 ),2 )$

*D.*

$sqrt(3 )$

== Solution

Correct answer: C

$frac(sqrt(3 ),2 )$

#pagebreak()

= Question 25

The zeros of the function $y = f \(x \)$ are $x = - 2 $ and $x = 3 $. Identify the zeros of the function

$g \(x \)= 2  f \(x - 4 \)$.

*A.*

$x = - 6 $ and $x = - 1 $

*B.*

$x = 2 $ and $x = 7 $

*C.*

$x = - 4 $ and $x = 6 $

*D.*

$x = 0 $ and $x = 10 $

== Solution

Correct answer: B

$x = 2 $ and $x = 7 $

#pagebreak()

= Question 26

Identify the value of $log  _(4 )lr(\( frac(1 ,4 )\) )$.

*A.*

-16

*B.*

-1

*C.*

1

*D.*

16

== Solution

Correct answer: B

-1

#pagebreak()

= Question 27

Sketch the graph of at least one period of the function $y = - cos  lr(\( x + frac(pi ,4 )\) )+ 3 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-04_1071_1567_504_266.jpg", width: 73.7%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-22_1040_1633_627_258.jpg", width: 76.8%)

#pagebreak()

= Question 28

Justify that $\(x - 5 \)$ is not a possible factor of the function $P \(x \)= x ^(3 )- 3  x ^(2 )- 4  x + 12 $.

== Solution

When $x = 5 $ is substituted into $P \(x \)\, P \(5 \)$ does not equal 0 .

1 mark

#pagebreak()

= Question 29

Sketch the graph of $f \(x \)= frac(6 ,\(x + 2 \)\(x - 3 \))$ and state the $y $-intercept.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-06_1292_1301_571_259.jpg", width: 61.2%)

$y $-intercept:

$\_ \_ \_ \_ $

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-24_859_917_595_204.jpg", width: 43.2%)

$\_ \_ \_ \_ $

-1

1 mark for vertical asymptotic behaviour

\( $frac(1 ,2 )$ mark for behaviour approaching $x = - 2 $\; $frac(1 ,2 )$ mark for behaviour approaching $x = 3 $ \)

1 mark for horizontal asymptotic behaviour approaching $y = 0 $

$1  frac(1 ,2 )$ marks for shape \( $frac(1 ,2 )$ mark for shape in each section\)

$frac(1 ,2 )$ mark for $y $-intercept

4 marks

#pagebreak()

= Question 30

Determine how many 3 -digit odd numbers less than 300 are possible using the digits $1 \,2 \,3 \,4 \,5 \,6 $

if repetition is not allowed.

== Solution

case $1 :  frac(1 ,1 ) bullet  frac(4 ,"" ) bullet  frac(2 ," odd ")= 8 $

$frac(1 ,2 )$ mark for case 1

case $2 :  frac(1 ,2 ) dot.c  underline(4 ) dot.c  frac(3 ," odd ")= 12 $

$frac(1 ,2 )$ mark for case 2

$8 + 12 = 20 $ numbers

1 mark for addition of cases

2 marks

#pagebreak()

= Question 31

Given that $cos  alpha = - frac(5 ,13 )$ and $sin  beta = frac(2 ,3 )$\, where $alpha $ and $beta $ terminate in the same quadrant\, determine the exact value of $cos  \(alpha - beta \)$.

determine the exact value of $cos  \(alpha - beta \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-26_415_460_670_245.jpg", width: 21.6%)

$  lr( limits(frac(root(3 ,5 ),arrow.t ))^(2  <--  beta ^(j ))|  )_(arrow.b ) ^(limits(4 )^(y )) x   $

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  25 + y ^(2 ) & = 169  \  y ^(2 ) & = 144  \  y  & =  plus.minus  12    $

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  x ^(2 )+ 4  & = 9  \  x ^(2 ) & = 5    $

$frac(1 ,2 )$ mark for value of $y $

$   cos  \(alpha - beta \) & = cos  alpha  cos  beta + sin  alpha  sin  beta  \  & = lr(\( - frac(5 ,13 )\) )lr(\( - frac(sqrt(5 ),3 )\) )+ lr(\( frac(12 ,13 )\) )lr(\( frac(2 ,3 )\) ) \  & = frac(5  sqrt(5 ),39 )+ frac(24 ,39 ) \  & = frac(5  sqrt(5 )+ 24 ,39 )   $

$frac(1 ,2 )$ mark for $cos  beta $

$frac(1 ,2 )$ mark for $sin  alpha $

1 mark for substitution into correct identity

3 marks

Notes:

- Accept any of the following values for $x :  x =  plus.minus  sqrt(5 )\, x = sqrt(5 )$\, or $x = - sqrt(5 )$.

- Accept any of the following values for $y :  y =  plus.minus  12 $ or $y = 12 $.

#pagebreak()

= Question 32

Given the graph of $y = 4 ^(x )$\, sketch the graph of $y = 2 \(4 \)^(x - 3 )+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-09_833_957_534_571.jpg", width: 45.0%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-09_831_951_1486_573.jpg", width: 44.8%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-27_821_945_550_191.jpg", width: 44.5%)

1 mark for vertical stretch

1 mark for horizontal translation

1 mark for vertical translation

3 marks

#pagebreak()

= Question 33

Determine the coterminal angle of $frac(pi ,5 )$ over the interval $\[- 2  pi \, 0 \]$.

== Solution

$  - frac(9  pi ,5 )  $

1 mark

#pagebreak()

= Question 34

State the domain of the graph of $y = log  \(x - 4 \)- 8 $.

== Solution

$  x > 4   $

1 mark

or

$\(4 \, oo \)$

#pagebreak()

= Question 35

Given the graph of $y = 5  sin  lr(\[ 2 lr(\( x + frac(pi ,4 )\) )\] )- 3 $\, determine the exact value of the $x $-coordinate in

the point P .

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-11_970_832_573_554.jpg", width: 39.2%)

== Solution

$  x = frac(pi ,2 ) quad  1  " mark "  $

#pagebreak()

= Question 36

Verify that the following equation is true for $x = frac(5  pi ,6 )$.

$  frac(cos  x ,1 - sin  x )= frac(1 + sin  x ,cos  x )  $

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
[$frac(cos  frac(5  pi ,6 ),1 - sin  frac(5  pi ,6 ))$ ], [$frac(1 + sin  frac(5  pi ,6 ),cos  frac(5  pi ,6 ))$ ],
table.hline(stroke: .5pt),
[$frac(- frac(sqrt(3 ),2 ),1 - frac(1 ,2 ))$ ], [$frac(1 + frac(1 ,2 ),- frac(sqrt(3 ),2 )) quad lr(\( frac(1 ,2 ) )$ mark for $cos  frac(5  pi ,6 ) \; 1  \/ 2 $ mark for $lr( sin  frac(5  pi ,6 )\) )$ ],
table.hline(stroke: .5pt),
[$frac(- frac(sqrt(3 ),2 ),frac(1 ,2 ))$ ], [$frac(frac(3 ,2 ),- frac(sqrt(3 ),2 ))$ ],
table.hline(stroke: .5pt),
[$- frac(sqrt(3 ),1 )$ ], [- $3  .  sqrt(3 ) 1 $ mark for simplification ],
table.hline(stroke: .5pt),
[$- sqrt(3 )$ ], [$- sqrt(3 ) quad  2 $ marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 37

Given that $\(x + 1 \)$ is one of the factors of $P \(x \)= x ^(3 )- x ^(2 )+ k  x - 8 $\, determine the value of $k $.

== Solution

Method 1

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$x = - 1 $ ], [$frac(1 ,2 )$ mark for $x = - 1 $ ],
table.hline(stroke: .5pt),
[$0 = \(- 1 \)^(3 )- \(- 1 \)^(2 )+ k \(- 1 \)- 8 $ ], [1 mark for remainder theorem ],
table.hline(stroke: .5pt),
[$0 = - 1 - 1 - k - 8 $ ], [],
table.hline(stroke: .5pt),
[$k = - 10 $ ], [$frac(1 ,2 )$ mark for solving for $k $ ],
table.hline(stroke: .5pt),
[],
);

Method 2

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$x = - 1 $ ], [$frac(1 ,2 )$ mark for $x = - 1 $ ],
table.hline(stroke: .5pt),
[],
);

#table(stroke: none,
columns: 6,
align: (left, left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5), table.vline(stroke: .5pt, x: 6),
table.hline(stroke: .5pt),
[-1 ], [1 ], [-1 ], [$k $ ], [-8 ], [],
table.hline(stroke: .5pt),
[], [], [-1 ], [2 ], [$- k - 2 $ ], [1 mark for synthetic division ],
table.hline(stroke: .5pt),
[], [1 ], [-2 ], [$k + 2 $ ], [$- k - 10 $ ], [],
table.hline(stroke: .5pt),
[],
);

$   - k - 10  & = 0  \  k  & = - 10    $

$frac(1 ,2 )$ mark for solving for $k $

2 marks

#pagebreak()

= Question 38

Given the function $f \(x \)= sqrt(x )$\, describe how to use transformations to determine the domain of

the function $g \(x \)= f \(x + 2 \)+ 1 $.

== Solution

The graph of $g \(x \)$ is a horizontal translation 2 units to the left of the graph of $f \(x \)$\, which

changes the domain from $x  >=  0 $ to $x  >= - 2 $.

1 mark

#pagebreak()

= Question 39

Given the graph of $y = f \(x \)$\, state the equation of the vertical asymptote of $y = frac(1 ,f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-15_854_862_500_610.jpg", width: 40.6%)

== Solution

$  x = - 2   $

#pagebreak()

= Question 40

Solve\, algebraically.

$  16 ^(x )= 64 ^(2  x - 1 )  $

== Solution

$4 ^(2  x )= 4 ^(3 \(2  x - 1 \))$

$4 ^(2  x )= 4 ^(6  x - 3 )$

$2  x = 6  x - 3 $

$3 = 4  x $

$frac(3 ,4 )= x $

1 mark for changing to a common base \( $frac(1 ,2 )$ mark for each\)

$frac(1 ,2 )$ mark for exponent law

$frac(1 ,2 )$ mark for equating exponents

2 marks

#pagebreak()

= Question 41

Given one of the factors of $P \(x \)= x ^(3 )+ 2  x ^(2 )- 5  x - 6 $ is \( $x + 3 $ \)\, express $P \(x \)$ in completely

factored form.

$  P \(x \)=   $

== Solution

#table(stroke: none,
columns: 6,
align: (left, left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5), table.vline(stroke: .5pt, x: 6),
table.hline(stroke: .5pt),
[-3 ], [1 ], [2 ], [-5 ], [-6 ], [$frac(1 ,2 )$ mark for $x = - 3 $ ],
table.hline(stroke: .5pt),
[], [↓ ], [-3 ], [3 ], [6 ], [1 mark for synthetic division \(or any equivalent strategy\) ],
table.hline(stroke: .5pt),
[], [1 ], [-1 ], [-2 ], [0 ], [],
table.hline(stroke: .5pt),
[],
);

$   & P \(x \)= \(x + 3 \)lr(\( x ^(2 )- x - 2 \) ) \  & P \(x \)= \(x + 3 \)\(x - 2 \)\(x + 1 \) quad  1  \/ 2  " mark for consistent product of factors "   $

2 marks

#pagebreak()

= Question 42

Sketch the graph of $p \(x \)= 3 \(x + 1 \)^(2 )\(x - 2 \)^(2 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-18_1017_1120_584_507.jpg", width: 52.7%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-37_748_831_653_260.jpg", width: 39.1%)

1 mark for $x $-intercepts

$frac(1 ,2 )$ mark for $y $-intercept

1 mark for multiplicity of 2 at $x = - 1 $ and at $x = 2 $

\( $frac(1 ,2 )$ mark for each\)

$frac(1 ,2 )$ mark for end behaviour

3 marks

#pagebreak()

= Question 43

Given that $f \(x \)= x ^(2 )- 4 $ and $g \(x \)= sqrt(x )$\, determine $f \(g \(x \)\)$ and state its domain.

$  f \(g \(x \)\)=   $

== Solution

$   & f \(g \(x \)\)= \(sqrt(x )\)^(2 )- 4  \  & f \(g \(x \)\)= x - 4 \, x  >=  0    $

1 mark for composite function

1 mark for domain consistent with composite function

2 marks

#pagebreak()

= Question 44

Determine a possible equation of the function $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-20_826_828_545_281.jpg", width: 39.0%)

$  f \(x \)=   $

== Solution

$f \(x \)= 2  sqrt(- \(x - 1 \))$

or

$f \(x \)= sqrt(- 4 \(x - 1 \))$

1 mark for vertical stretch

1 mark for horizontal reflection

1 mark for horizontal translation

3 marks

1 mark for horizontal compression

1 mark for horizontal reflection

1 mark for horizontal translation

3 marks

#pagebreak()

= Question 45

Explain why the graph of $y = log  _(2 ) x $ does not have a $y $-intercept.

== Solution

The domain of the graph is $x > 0 $.

1 mark

or

There is a vertical asymptote at $x = 0 $.

#pagebreak()

= Question 46

Evaluate.

$  sin  ^(2 )lr(\( - frac(pi ,3 )\) )+ cos  lr(\( frac(17  pi ,6 )\) ) sec  lr(\( frac(pi ,6 )\) )  $

== Solution

$  mat(delim: #none,  lr(\( - frac(sqrt(3 ),2 )\) )^(2 )+ lr(\( - frac(sqrt(3 ),2 )\) )lr(\( frac(2 ,sqrt(3 ))\) ) "" , 1  " mark for " sin  lr(\( - frac(pi ,3 )\) )\(1  \/ 2  " mark for quadrant; " 1  \/ 2  " mark for value "\) "" ; frac(3 ,4 )- 1  "" , 1  " mark for " cos  lr(\( frac(17  pi ,6 )\) )\(1  \/ 2  " mark for quadrant; " 1  \/ 2  " mark for value "\) "" ; - frac(1 ,4 ) "" , 1  " mark for " sec  lr(\( frac(pi ,6 )\) )\(1  \/ 2  " mark for quadrant; " 1  \/ 2  " mark for value "\) )  $

3 marks

#pagebreak()

= Question 47

Determine the coordinates of the point of discontinuity \(hole\) on the graph of $y = frac(x ^(2 )- 3  x ,x )$.

== Solution

$\(0 \,- 3 \) quad  1 $ mark for point of discontinuity \(hole\) at $x = 0 $

1 mark

Note:

- Deduct $frac(1 ,2 )$ mark for procedural error of incorrect $y $-value.

#pagebreak()

= Question 48

Given the graphs of $f \(x \)$ and $g \(x \)$\, sketch the graph of $h \(x \)= f \(x \)+ g \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-24_851_800_466_253.jpg", width: 37.6%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/3e0793eb-2abb-4d3d-8d6a-842ded1e4d7d-24_792_794_1430_253.jpg", width: 37.4%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-43_788_795_1439_254.jpg", width: 37.4%)

1 mark for operation of addition

1 mark for restricted domain

2 marks

#pagebreak()

= Question 49

Given that $csc  theta = - frac(4 ,sqrt(7 ))$ and $cos  theta > 0 $\, determine the exact value of $tan  theta $.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jun/assets/813a39f8-3eb3-48fb-9d35-b1d3fa2dee84-44_428_524_617_610.jpg", width: 24.7%)

$   & sin  theta = - frac(sqrt(7 ),4 ) \  & x ^(2 )+ \(sqrt(7 )\)^(2 )= \(4 \)^(2 ) \  & x ^(2 )= 16 - 7  \  & x ^(2 )= 9  \  & x =  plus.minus  3  \  & tan  theta = - frac(sqrt(7 ),3 )   $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $x $

1 mark for $tan  theta $ \( $frac(1 ,2 )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

2 marks

Note:

- Accept any of the following values for $x :  x =  plus.minus  3 \, x = 3 $\, or $x = - 3 $.