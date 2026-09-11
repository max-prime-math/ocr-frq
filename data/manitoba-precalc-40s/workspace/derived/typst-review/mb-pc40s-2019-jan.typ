#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2019-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Determine the length of the radius\, $r $\, given an arc length of 20 metres and a central angle of $160 ^(degree )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/78f19bd5-5c04-4554-8f6f-5adc61245e46-01_287_298_502_833.jpg", width: 14.0%)

== Solution

$   theta  & = \(160 \)lr(\( frac(pi ,180 )\) ) \  & = frac(8  pi ,9 )   $

$   & r = frac(s ,theta ) \  & r = frac(20 ,lr(\( frac(8  pi ,9 )\) )) \  & r = frac(180 ,8  pi ) upright(space.nobreak m )   $

1 mark for conversion

$  1  " mark for substitution "  $

2 marks

or

$  r = 7.162  upright(space.nobreak m )  $

#pagebreak()

= Question 2

\(4hash 1

There are eight cars parked in a row. Determine the number of possible arrangements of these

eight cars if Mrs. Jones must always park in the third spot and Mr. Rodriguez must always park

in the last spot.

== Solution

$  6  dot.c  5  dot.c  1  dot.c  4  dot.c  3  dot.c  2  dot.c  1  dot.c  1   $

#pagebreak()

= Question 3

Bill wins $dollar  1300000 $ in a lottery and invests the entire amount at an annual interest rate of $2.5  % $

compounded quarterly. He will withdraw $dollar  10000 $ at the end of every three months.

Determine\, algebraically\, the total number of withdrawals\, including the partial amount\, that Bill

can make until there is no money left. Express your answer as a whole number.

Use the formula:

$  P  V = frac(R lr(\[ 1 - \(1 + i \)^(- n )\] ),i )  $

where

$   P  V  & = " the present value deposited " \  R  & = " the amount of each withdrawal " \  n  & = " the number of equal withdrawals " \  i  & = frac(" the annual interest rate (in decimal form) "," the number of compounding periods ")   $

== Solution

$   1300000  & = frac(10000 lr(\[ 1 - lr(\( 1 + frac(0.025 ,4 )\) )^(- n )\] ),frac(0.025 ,4 )) \  8125  & = 10000 lr(\[ 1 - \(1.00625 \)^(- n )\] ) \  0.8125  & = 1 - \(1.00625 \)^(- n ) \  - 0.1875  & = - \(1.00625 \)^(- n ) \  log  \(0.1875 \) & = - n  log  1.00625  \  - frac(log  \(0.1875 \),log  \(1.00625 \)) & = n  \  268.672348  & = n    $

Bill can make 269 withdrawals.

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for simplification

$frac(1 ,2 )$ mark for applying logarithms

1 mark for power law

$frac(1 ,2 )$ mark for solving for $n $

3 marks

#pagebreak()

= Question 4

\(Mill\)

Determine and simplify the $12  "" ^("th ")$ term in the binomial expansion of $lr(\( x ^(3 )- frac(1 ,2  x ^(2 ))\) )^(12 )$.

== Solution

$t _(12 )=  "" _(12 ) C _(11 )lr(\( x ^(3 )\) )^(1 )lr(\( - frac(1 ,2  x ^(2 ))\) )^(11 )$

2 marks \( 1 mark for $ "" _(12 ) C _(11 )$\; $frac(1 ,2 )$ mark for each consistent factor\)

$   & t _(12 )= \(12 \)lr(\( x ^(3 )\) )lr(\( - frac(1 ,2048  x ^(22 ))\) ) \  & t _(12 )= - frac(12 ,2048  x ^(19 ))   $

or

1 mark for simplification \( $frac(1 ,2 )$ mark for coefficient\; $frac(1 ,2 )$ mark for

exponent\)

3 marks

$  t _(12 )= - frac(3 ,512  x ^(19 ))  $

or

$  t _(12 )= - 0.006  x ^(- 19 )  $

#pagebreak()

= Question 5

\(Mili\)

Solve\, algebraically.

$  e ^(2  x - 3 )= 7 ^(x + 1 )  $

== Solution

$   ln  e ^(2  x - 3 ) & = ln  7 ^(x + 1 ) \  \(2  x - 3 \) ln  e  & = \(x + 1 \) ln  7  \  2  x - 3  & = x  ln  7 + ln  7  \  2  x - x  ln  7  & = ln  7 + 3  \  x \(2 - ln  7 \) & = ln  7 + 3  \  x  & = frac(ln  7 + 3 ,2 - ln  7 ) \  x  & = 91.438783  \  x  & = 91.439    $

$frac(1 ,2 )$ mark for applying logarithms

1 mark for power law

$frac(1 ,2 )$ mark for collecting terms with $x $

$frac(1 ,2 )$ mark for isolating $x $

$frac(1 ,2 )$ mark for evaluating quotient of logarithms

3 marks

#pagebreak()

= Question 6

Sketch the angle $frac(7  pi ,3 )$ in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/78f19bd5-5c04-4554-8f6f-5adc61245e46-06_730_849_562_623.jpg", width: 40.0%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-06_724_838_642_260.jpg", width: 39.4%)

$frac(1 ,2 )$ mark for an appropriate angle in quadrant I

$frac(1 ,2 )$ mark for correct number of revolutions

1 mark

Note:

- If the directional arrow is not indicated\, deduct an E1 error \(final answer not stated\).

#pagebreak()

= Question 7

Determine\, algebraically\, all of the zeros of the polynomial function $P \(x \)= x ^(4 )- 5  x ^(3 )- 4  x ^(2 )+ 20  x $.

== Solution

$   & P \(x \)= x lr(\( x ^(3 )- 5  x ^(2 )- 4  x + 20 \) ) \  & P \(2 \)= 2 lr(\( 2 ^(3 )- 5 \(2 \)^(2 )- 4 \(2 \)+ 20 \) ) \  & P \(2 \)= 0  \  & therefore \(x - 2 \) " is a factor "   $

1 mark for identifying one possible value of $x $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [1 ], [-5 ], [-4 ], [20 ],
table.hline(stroke: .5pt),
[], [↓ ], [2 ], [-6 ], [-20 ],
table.hline(stroke: .5pt),
[], [1 ], [-3 ], [-10 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division

\(or any other equivalent strategy\)

$   P \(x \) & = x \(x - 2 \)lr(\( x ^(2 )- 3  x - 10 \) ) \  0  & = x \(x - 2 \)\(x - 5 \)\(x + 2 \) \  x  & = 0 \, x = 2 \, x = 5 \, x = - 2    $

$frac(1 ,2 )$ mark for identifying all the factors

$frac(1 ,2 )$ mark for consistent zeros

3 marks

#pagebreak()

= Question 8

Justify why four of the terms in the binomial expansion of $\(- x + y \)^(6 )$ are positive.

== Solution

$   & \(- x \)^(6 )\(y \)^(0 )\,\(- x \)^(5 )\(y \)^(1 )\,\(- x \)^(4 )\(y \)^(2 )\, dots.h  \  & x ^(6 )\,- x ^(5 ) y \, x ^(4 ) y ^(2 )\, dots.h    $

There are 7 terms. The first term is positive and the signs alternate.

1 mark for justification

1 mark

#pagebreak()

= Question 9

Determine the equation of $g \(x \)$ in terms of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/78f19bd5-5c04-4554-8f6f-5adc61245e46-09_803_804_489_670.jpg", width: 37.8%)

$  g \(x \)=   $

$\_ \_ \_ \_ $

== Solution

$  g \(x \)= - f \(x - 3 \) quad   & 1  " mark for vertical reflection " \  & 1  " mark for horizontal translation "   $

#pagebreak()

= Question 10

Prove the identity for all permissible values of $x $.

$  frac(sin  x + tan  x ,cot  x + csc  x )= frac(sin  ^(2 ) x ,cos  x )  $

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

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$  frac(sin  x + frac(sin  x ,cos  x ),frac(cos  x ,sin  x )+ frac(1 ,sin  x ))  $ $  frac(frac(sin  x  cos  x + sin  x ,cos  x ),frac(cos  x + 1 ,sin  x ))  $ $  frac(sin  x \(cos  x + 1 \),cos  x ) dot.c  frac(sin  x ,\(cos  x + 1 \))  $ $  frac(sin  ^(2 ) x ,cos  x )  $ ], [$frac(sin  ^(2 ) x ,cos  x )$ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

Method 2

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   & frac(sin  x + tan  x ,frac(1 ,tan  x )+ frac(1 ,sin  x )) \  & frac(sin  x + tan  x ,frac(sin  x + tan  x ,sin  x  tan  x ))   $ ], [$frac(sin  ^(2 ) x ,cos  x )$ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 11

Given that the point $\(- 2 \,1 \)$ is on the graph of $y = f \(x \)$\, describe how the coordinates of the

corresponding point on the graph of $y = f \(4  x \)$ are different.

== Solution

The $x $-value is divided by 4 .

1 mark

#pagebreak()

= Question 12

Using the laws of logarithms\, completely expand the expression:

$  log  lr(\( frac(x ^(2 ) sqrt(y ),w - 1 )\) )  $

== Solution

$2  log  x + frac(1 ,2 ) log  y - log  \(w - 1 \)$

1 mark for product law

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

1 mark for quotient law

3 marks

#pagebreak()

= Question 13

Given $sec  theta = - frac(5 ,4 )$ and $tan  theta > 0 $\, state the quadrant in which $theta $ terminates.

Justify your answer.

== Solution

Since $sec  theta $ is negative in quadrants II and III\, and $tan  theta $ is positive in quadrants I and III\,

$theta $ terminates in quadrant III.

1 mark for justification

1 mark

#pagebreak()

= Question 14

State an equation of a rational function that has a vertical asymptote at $x = - 8 $ and a horizontal

asymptote at $y = 9 $.

== Solution

$y = frac(9  x ,x + 8 )$

1 mark for vertical asymptote

1 mark for horizontal asymptote

2 marks

- Other equations are possible.

#pagebreak()

= Question 15

Given the point $\(5 \,1 \)$\, state the coordinates of the corresponding point after a reflection across

the line $y = x $.

== Solution

$\(1 \,5 \)$

1 mark

#pagebreak()

= Question 16

Simplify.

$  frac(\(n - 13 \)! ,\(n - 12 \)! )  $

== Solution

$  frac(frac(\(n - 13 \)! ,\(n - 12 \) frac(\(n - 13 \)! ,frac(1 ,n - 12 ))),"" )  $

1 mark for factorial expansion

1 mark

#pagebreak()

= Question 17

a\) 1 mark b\) 1 mark

Given the graphs of $y = f \(x \)$ and $y = g \(x \)$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/78f19bd5-5c04-4554-8f6f-5adc61245e46-15_652_656_455_380.jpg", width: 30.9%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/78f19bd5-5c04-4554-8f6f-5adc61245e46-15_652_656_455_1095.jpg", width: 30.9%)

a\) determine the value of $f \(g \(2 \)\)$.

b\) determine the value of $\(g - f \)\(- 3 \)$.

== Solution

$g \(2 \)= 0 $

$frac(1 ,2 )$ mark for the value of $g \(2 \)$

$f \(0 \)= 4 $

$frac(1 ,2 )$ mark for the value of $f \(g \(2 \)\)$ consistent with $g \(2 \)$

1 mark

b\) determine the value of $\(g - f \)\(- 3 \)$.

$   g \(- 3 \)- f \(- 3 \) \  1 - \(- 2 \)   $

$frac(1 ,2 )$ mark for the values of $g \(- 3 \)$ and $f \(- 3 \)$

3

$frac(1 ,2 )$ mark for value of $\(g - f \)\(- 3 \)$ consistent with $g \(- 3 \)$

and $f \(- 3 \)$

1 mark

#pagebreak()

= Question 18

Identify the remainder when $P \(x \)= 3  x ^(3 )- x ^(2 )+ 1 $ is divided by $\(x - 2 \)$.

*A.*

-27

*B.*

-19

*C.*

11

*D.*

21

== Solution

Correct answer: D

21

#pagebreak()

= Question 19

Identify the logarithmic form of $2 ^(x )= frac(1 ,4 )$.

*A.*

$log  _(2 ) x = frac(1 ,4 )$

*B.*

$log  _(x ) 2 = frac(1 ,4 )$

*C.*

$log  _(2 )lr(\( frac(1 ,4 )\) )= x $

*D.*

$log  _(x )lr(\( frac(1 ,4 )\) )= 2 $

== Solution

Correct answer: C

$log  _(2 )lr(\( frac(1 ,4 )\) )= x $

#pagebreak()

= Question 20

Leah's Pizzeria offers 9 different pizza toppings. Identify the expression that represents the

number of different types of pizzas\, with 3 different toppings\, that can be made.

*A.*

$ "" _(9 ) C _(3 )$

*B.*

$ "" _(9 ) P _(3 )$

*C.*

$frac(9 ! ,3 ! )$

*D.*

$9 ! 3 ! $

== Solution

Correct answer: A

$ "" _(9 ) C _(3 )$

#pagebreak()

= Question 21

Given $\(5 \,- 4 \)$ is a point on the graph of $y = f \(x \)$\, identify the corresponding point on the

graph of $y = frac(1 ,f \(x \))$.

*A.*

$lr(\( frac(1 ,5 )\,- 4 \) )$

*B.*

$lr(\( 5 \,- frac(1 ,4 )\) )$

*C.*

$lr(\( frac(1 ,5 )\,- frac(1 ,4 )\) )$

*D.*

$\(- 4 \,5 \)$

== Solution

Correct answer: B

$lr(\( 5 \,- frac(1 ,4 )\) )$

#pagebreak()

= Question 22

Identify the non-permissible value of $x $ for $1 + sec  x $ over $\[0 \, pi \]$.

*A.*

0

*B.*

$frac(pi ,4 )$

*C.*

$frac(pi ,2 )$

*D.*

$pi $

== Solution

Correct answer: C

$frac(pi ,2 )$

#pagebreak()

= Question 23

Indicate the combination that represents the circled term in the given row of Pascal's triangle.

1

46

\(4\) 1

*A.*

$ "" _(4 ) C _(3 )$

*B.*

$ "" _(4 ) C _(4 )$

*C.*

$ "" _(5 ) C _(3 )$

*D.*

$ "" _(5 ) C _(4 )$

== Solution

Correct answer: A

$ "" _(4 ) C _(3 )$

#pagebreak()

= Question 24

Identify the $x $-intercept on the graph of $f \(x \)= sqrt(2 \(x + 5 \))$.

*A.*

-5

*B.*

0

*C.*

$sqrt(10 )$

*D.*

5

== Solution

Correct answer: A

-5

#pagebreak()

= Question 25

Identify the coterminal angle of $frac(pi ,5 )$ over the interval $- pi  <=  theta  <=  4  pi $.

*A.*

$- frac(9  pi ,5 )$

*B.*

$- frac(pi ,5 )$

*C.*

$frac(3  pi ,5 )$

*D.*

$frac(11  pi ,5 )$

== Solution

Correct answer: D

$frac(11  pi ,5 )$

#pagebreak()

= Question 26

Given $f \(x \)= \{ \(2 \,6 \)\,\(3 \,2 \)\,\(3 \,4 \)\,\(6 \,5 \)\} $\, identify the value of $f \(f \(2 \)\)$.

*A.*

3

*B.*

4

*C.*

5

*D.*

6

== Solution

Correct answer: C

5

#pagebreak()

= Question 27

The graph of $f \(x \)= \(x - 1 \)^(2 )$ is translated 2 units to the left and 3 units up. Identify the equation

of the transformed graph\, $g \(x \)$.

*A.*

$g \(x \)= \(x + 1 \)^(2 )+ 3 $

*B.*

$g \(x \)= \(x - 3 \)^(2 )+ 3 $

*C.*

$g \(x \)= \(x + 2 \)^(2 )+ 3 $

*D.*

$g \(x \)= \(x - 2 \)^(2 )+ 3 $

== Solution

Correct answer: A

$g \(x \)= \(x + 1 \)^(2 )+ 3 $

#pagebreak()

= Question 28

Given $csc  theta = - frac(8 ,5 )$\, determine the exact value of $cos  2  theta $.

== Solution

$   cos  2  theta  & = 1 - 2  sin  ^(2 ) theta  \  & = 1 - 2 lr(\( - frac(5 ,8 )\) )^(2 ) \  & = frac(14 ,64 )   $

1 mark for the value of $sin  theta $

1 mark for substitution into correct identity

2 marks

$   & " or " \  & = frac(7 ,32 )   $

#pagebreak()

= Question 29

Determine the period of the sinusoidal function\, $f \(x \)= - 6  cos  lr(\( frac(pi ,6 )\(x + 1 \)\) )+ 5 $.

== Solution

$   " Period " & = frac(2  pi ,lr(\( frac(pi ,6 )\) )) \  & = 12    $

1 mark

#pagebreak()

= Question 30

Determine\, algebraically\, the equation of $P \(x \)$\, given the graph of the polynomial function $P \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-07_998_843_487_625.jpg", width: 39.7%)

$P \(x \)= $

$\_ \_ \_ \_ $

== Solution

$   P \(x \) & = a \(x - 3 \)^(2 )\(x - 1 \)\(x + 2 \) \  - 36  & = a \(- 3 \)^(2 )\(- 1 \)\(2 \) \  - 36  & = - 18  a  \  a  & = 2    $

$  P \(x \)= 2 \(x - 3 \)^(2 )\(x - 1 \)\(x + 2 \)  $

$frac(1 ,2 )$ mark for factors of $P \(x \)$

$frac(1 ,2 )$ mark for multiplicity of 2 at $x = 3 $

$frac(1 ,2 )$ mark for substitution of $P \(0 \)= - 36 $

$frac(1 ,2 )$ mark for correct value of $a $

2 marks

#pagebreak()

= Question 31

Solve $2  sin  ^(2 ) theta - 7  sin  theta - 4 = 0 $ where $theta  in  bb(R )$.

== Solution

$  mat(delim: #none,  \(2  sin  theta + 1 \)\(sin  theta - 4 \)= 0  "" , "" ; sin  theta = - frac(1 ,2 ) "" , sin  theta = 4  "" ; quad  theta = frac(7  pi ,6 )\, frac(11  pi ,6 ) quad  "" , 1  " mark for solving for " sin  theta lr(\( frac(1 ,2 ) " mark for each branch "\) ) "" ; theta = frac(7  pi ,6 )+ 2  k  pi \, k  in  bb(Z ) "" , "" ; theta = frac(11  pi ,6 )+ 2  k  pi \, k  in  bb(Z ) "" , 1  " marks for solving for " theta \(1  " mark for each branch "\) "" ; "" , 4  " marks " )  $

#pagebreak()

= Question 32

Justify that the shapes of the graphs of $f \(x \)= \(x + 1 \)^(2 )\(x - 1 \)$ and $g \(x \)= \(x + 1 \)^(2 )\(x - 1 \)^(3 )$ are

different as they approach the $x $-intercept at $x = 1 $.

== Solution

At $x = 1 $\, both graphs pass through the $x $-axis\, however\, the graph of $g \(x \)$ flattens as it passes

through the $x $-axis.

#pagebreak()

= Question 33

Determine the exact value of $cot  theta $ if $cos  theta = - frac(4 ,7 )$ and $sin  theta $ is positive.

== Solution

$  mat(delim: #none,  x ^(2 )+ y ^(2 )= r ^(2 ) "" , "" ; \(- 4 \)^(2 )+ y ^(2 )= \(7 \)^(2 ) "" , 1  \/ 2  " mark for substitution " "" ; y ^(2 )= 49 - 16  "" , "" ; y =  plus.minus  sqrt(33 ) "" , 1  \/ 2  " mark for solving for " y  "" ; cot  theta = frac(- 4 ,sqrt(33 )) "" , 1  " mark for consistent value of " cot  theta lr(\( frac(1 ,2 ) " mark for quadrant; " 1  \/ 2  " mark for value "\) ) "" ; " or " "" , bold(2 ) " marks " "" ; cot  theta = frac(- 4  sqrt(33 ),33 ) "" , )  $

Note:

- Accept any of the following values for $y :  y =  plus.minus  sqrt(33 )\, y = sqrt(33 )$\, or $y = - sqrt(33 )$.

#pagebreak()

= Question 34

Sketch the graph of $f \(x \)= - log  _(2 )\(x \)+ 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-11_798_803_554_661.jpg", width: 37.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-29_788_793_569_260.jpg", width: 37.3%)

1 mark for asymptotic behaviour approaching $x = 0 $

1 mark for vertical reflection

1 mark for vertical translation

3 marks

#pagebreak()

= Question 35

State the range of $f \(x \)= sqrt(x + 4 )$.

Range:

== Solution

Range: $\[0 \, oo \)$

1 mark

or

Range: $\{ y  in  bb(R ) divides  y  >=  0 \} $

#pagebreak()

= Question 36

Sophie correctly solved the logarithmic equation\, $log  _(7 )\(x - 1 \)= log  _(7 )\(2  x - 2 \)$.

$   x - 1  & = 2  x - 2  \  - 1 + 2  & = 2  x - x    $

Explain why $x = 1 $ is an extraneous root.

== Solution

The root\, $x = 1 $\, is an extraneous root because the argument of a logarithm cannot be zero.

#pagebreak()

= Question 37

Sketch the graph of $f \(x \)= sqrt(4  x )- 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-14_794_802_640_644.jpg", width: 37.7%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-32_793_793_582_256.jpg", width: 37.3%)

1 mark for shape of a radical function

1 mark for horizontal compression

1 mark for vertical translation

3 marks

#pagebreak()

= Question 38

Solve\, algebraically.

$   "" _(n ) C _(2 )= 2  n + 7   $

== Solution

$   frac(n ! ,\(n - 2 \)! 2 ! ) & = 2  n + 7  \  frac(n \(n - 1 \)\(n - 2 \)! ,frac(\(n - 2 \)! ,"" )) & = 2 ! \(2  n + 7 \) \  n \(n - 1 \) & = 2 \(2  n + 7 \) \  n ^(2 )- n  & = 4  n + 14  \  n ^(2 )- 5  n - 14  & = 0  \  \(n + 2 \)\(n - 7 \) & = 0  \  n  >= - 2  quad  n  & = 7    $

$frac(1 ,2 )$ mark for simplification

$frac(1 ,2 )$ mark for the permissible value of $n $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

#pagebreak()

= Question 39

Given $f \(x \)= x ^(2 )- 1 $ and $g \(x \)= x - 3 $\, explain why the domain of $h \(x \)= frac(f \(x \),g \(x \))$ has a

restriction when $x = 3 $.

== Solution

When $x = 3 $\, the denominator is equal to zero and it is not possible to divide by zero.

1 mark

#pagebreak()

= Question 40

Evaluate.

$  frac(cot  lr(\( frac(11  pi ,6 )\) ) sin  lr(\( - frac(4  pi ,3 )\) ),cos  lr(\( frac(2  pi ,3 )\) ))  $

== Solution

$\(- sqrt(3 )\)\(sqrt(3 )\) 1 $ mark for $cot  lr(\( frac(11  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

1 mark for $sin  lr(\( - frac(4  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

1 mark for $cos  lr(\( frac(2  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

$lr(\( - frac(3 ,2 )\) )lr(\( - frac(2 ,1 )\) )$

3 marks

3

#pagebreak()

= Question 41

Solve\, algebraically.

$  log  _(2 )lr(\( log  _(3 ) x \) )= 2   $

== Solution

$   2 ^(2 ) & = log  _(3 ) x  & & 1  \/ 2  " mark for exponential form " \  4  & = log  _(3 ) x  & & 1  \/ 2  " mark for exponential form " \  x  & = 3 ^(4 ) & & bold(1  space.nobreak  m  a  r  k )   $

#pagebreak()

= Question 42

Sketch the graph of the function $y = 5  sin  lr(\( frac(pi ,4 ) x \) )+ 1 $ over the domain $\[- 4 \,8 \]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-19_1109_1642_595_225.jpg", width: 77.3%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-37_941_1175_653_412.jpg", width: 55.3%)

#pagebreak()

= Question 43

Given the graph of $y = f \(x \)$\, sketch the graph of $y = | f \(- x \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-20_796_802_534_644.jpg", width: 37.7%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-20_807_802_1413_640.jpg", width: 37.7%)

The graph of

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-20_89_91_1594_1770.jpg", width: 5.0%)

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-38_793_797_1442_266.jpg", width: 37.5%)

1 mark for horizontal reflection

1 mark for absolute value

2 marks

#pagebreak()

= Question 44

Savannah used the graph of $y = f \(x \)$ to sketch the graph of $y = sqrt(f \(x \))$. Her solution is given

below. Describe her error.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-21_884_1069_605_554.jpg", width: 50.3%)

== Solution

Savannah did not restrict the domain at $x = 2 $.

#pagebreak()

= Question 45

Determine the exact value of $sin  lr(\( frac(13  pi ,12 )\) )$.

== Solution

$   sin  lr(\( frac(3  pi ,4 )+ frac(pi ,3 )\) ) & = sin  lr(\( frac(3  pi ,4 )\) ) cos  lr(\( frac(pi ,3 )\) )+ cos  lr(\( frac(3  pi ,4 )\) ) sin  lr(\( frac(pi ,3 )\) ) \  & = lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(1 ,2 )\) )+ lr(\( - frac(sqrt(2 ),2 )\) )lr(\( frac(sqrt(3 ),2 )\) ) \  & = frac(sqrt(2 ),4 )- frac(sqrt(6 ),4 ) \  & = frac(sqrt(2 )- sqrt(6 ),4 )   $

1 mark for substitution into correct identity

2 marks \( $frac(1 ,2 )$ mark for each exact value\)

3 marks

Note:

- Other combinations are possible.

#pagebreak()

= Question 46

State the equation of the horizontal asymptote of $f \(x \)= frac(3  x ,x - 1 )$.

== Solution

$y = 3 $

1 mark

#pagebreak()

= Question 47

Sketch the graph of $f \(x \)= frac(5  x - 10 ,x ^(2 )+ x - 6 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-24_802_804_655_696.jpg", width: 37.8%)

== Solution

$   f \(x \) & = frac(5  x - 10 ,x ^(2 )+ x - 6 ) \  & = frac(5 \(x - 2 \),\(x - 2 \)\(x + 3 \)) \  & = frac(5 ,x + 3 )\, x  !=  2    $

∴ there is a point of discontinuity \(hole\) at $\(2 \,1 \)$

vertical asymptote at $x = - 3 $

horizontal asymptote at $y = 0 $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-42_870_819_1326_211.jpg", width: 38.5%)

1 mark for asymptotic behaviour approaching $x = - 3 $

1 mark for asymptotic behaviour approaching $y = 0 $

1 mark for a point of discontinuity \(hole\) at $\(2 \,1 \)$

$frac(1 ,2 )$ mark for graph left of $x = - 3 $

$frac(1 ,2 )$ mark for graph right of $x = - 3 $

4 marks

#pagebreak()

= Question 48

Determine\, algebraically\, the inverse of $f \(x \)= 3  x + 4 $.

== Solution

Let $f \(x \)= y $

$  mat(delim: #none,  y = 3  x + 4  "" , "" ; x = 3  y + 4  "" , 1  " mark for switching " x  " and " y  "-values " "" ; x - 4 = 3  y  "" , "" ; frac(x - 4 ,3 )= y  "" , 1  \/ 2  " mark for solving for " y  )  $

$f ^(- 1 )\(x \)= frac(x - 4 ,3 ) quad  frac(1 ,2 )$ mark for writing equation of $f ^(- 1 )\(x \)$

2 marks

#pagebreak()

= Question 49

Sketch the graph of $P \(x \)= - \(x + 1 \)\(x - 2 \)\(x + 3 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/11b7ca38-d2f2-40c6-b269-d84792c85b2c-26_843_841_545_646.jpg", width: 39.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2019-jan/assets/a7c9dd39-81fe-4e05-b003-1ace5b5362ae-44_840_836_580_243.jpg", width: 39.3%)

1 mark for $x $-intercepts

$frac(1 ,2 )$ mark for $y $-intercept

$frac(1 ,2 )$ mark for end behaviour

2 marks