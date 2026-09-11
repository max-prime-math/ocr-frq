#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2018-jun

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Pierre pushes his car into a garage. The radius of a tire on his car is 22 cm . Determine the

distance travelled by his car if the tire rotated a total of $1000 ^(degree )$.

== Solution

$   theta  & = \(1000 \)lr(\( frac(pi ,180 )\) ) \  & = frac(50  pi ,9 )   $

$  1  " mark for conversion "  $

$   s  & = theta  r  \  s  & = lr(\( frac(50  pi ,9 )\) )\(22 \) \  & = frac(1100  pi ,9 ) upright(space.nobreak c m )   $

1 mark for substitution

2 marks

$  s = 383.972  upright(space.nobreak c m )  $

#pagebreak()

= Question 2

Solve\, algebraically.

$  7 ^(frac(x ,2 ))= 85   $

== Solution

$  frac(x ,2 ) log  7 = log  85   $

$  x  log  7 = 2  log  85   $

$  x = frac(2  log  85 ,log  7 )  $

$  x = 4.566142   $

$  x = 4.566   $

$frac(1 ,2 )$ mark for applying logarithms

1 mark for power law

$frac(1 ,2 )$ mark for evaluating quotient of logarithms

2 marks

#pagebreak()

= Question 3

Solve\, algebraically\, over the interval $\[0 \,2  pi \)$.

$  sin  x \(sec  x + 3 \)= 0   $

== Solution

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[$sin  x = 0 $ ], [$sec  x = - 3 $ ], [$frac(1 ,2 )$ mark for solving for $sin  x  frac(1 ,2 )$ mark for solving for $sec  x $ ],
table.hline(stroke: .5pt),
[], [$cos  x = - frac(1 ,3 )$ ], [1 mark for reciprocal ],
table.hline(stroke: .5pt),
[], [$x _(r )= 1.230959 $ ], [],
table.hline(stroke: .5pt),
[$x = 0 \, pi $ ], [$x = 1.911 \,4.373 $ ], [2 marks for values of $x $ \(1 mark for each branch\) ],
table.hline(stroke: .5pt),
[], [], [4 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 4

\"

Brahim invests $dollar  2500 $ at an annual interest rate of $6.75  % $ compounded monthly. Determine\,

algebraically\, how many years it will take for his investment to reach an amount of $dollar  10500 $.

Use the formula:

$  A = P lr(\( 1 + frac(r ,n )\) )^(n  t )  $

where $A = $ the amount of the investment after $t $ years

$P = $ the principal of the investment

$r = $ the annual interest rate \(as a decimal\)

$n = $ the number of compounding periods per year

$t = $ the length of the investment in years

== Solution

$   10500  & = 2500 lr(\( 1 + frac(0.0675 ,12 )\) )^(12  t ) \  4.2  & = \(1.005625 \)^(12  t ) \  log  4.2  & = 12  t  log  1.005625  \  frac(log  4.2 ,12  log  1.005625 ) & = t  \  21.320250  & = t  \  21.320  " years " & = t    $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for simplification

$frac(1 ,2 )$ mark for applying logarithms

1 mark for power law

$frac(1 ,2 )$ mark for evaluating quotient of logarithms

3 marks

#pagebreak()

= Question 5

There are 13 adults and 18 children who can be selected to go on a trip. Determine the number

of ways 4 adults and 7 children can be selected if Sandra\, one of the adults\, must be selected.

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$ "" _(1 ) C _(1 ) dot.c  "" _(12 ) C _(3 ) dot.c  "" _(18 ) C _(7 )$ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[1 mark for $ "" _(12 ) C _(3 )$ ],
[$frac(1 ,2 )$ mark for $ "" _(18 ) C _(7 )$ ],
); ],
table.hline(stroke: .5pt),
[7001280 ], [$frac(1 ,2 )$ mark for product of combinations ],
table.hline(stroke: .5pt),
[], [2 marks ],
table.hline(stroke: .5pt),
[],
);

Note:

- $I _(1 ) C _(1 )$ does not need to be shown.

#pagebreak()

= Question 6

\(2417\)

In the binomial expansion of $lr(\( frac(2 ,x ^(2 ))- x ^(3 )\) )^(9 )$\, determine and simplify the $6  "" ^("th ")$ term.

Note: A calculator is not required for the remaining test questions.

== Solution

$t _(6 )=  "" _(9 ) C _(5 )lr(\( frac(2 ,x ^(2 ))\) )^(4 )lr(\( - x ^(3 )\) )^(5 ) 2 $ marks \(1 mark for $ "" _(9 ) C _(5 ) \; frac(1 ,2 )$ mark for each consistent factor\)

$t _(6 )= 126 lr(\( frac(16 ,x ^(8 ))\) )lr(\( - x ^(15 )\) )$

$t _(6 )= - 2016  x ^(7 ) quad  1 $ mark for simplification \( $frac(1 ,2 )$ mark for coefficient\; $frac(1 ,2 )$ mark for exponent\)

3 marks

#pagebreak()

= Question 7

Given that $f \(x \)= \{ \(- 1 \,0 \)\,\(0 \,2 \)\,\(1 \,- 3 \)\,\(2 \,4 \)\} $\, evaluate $f \(f \(0 \)\)$.

== Solution

$  mat(delim: #none,  f \(f \(0 \)\) "" , "" ; f \(2 \) "" , 1  \/ 2  " mark for " f \(0 \)= 2  "" ; 4  "" , 1  \/ 2  " mark for " f \(f \(0 \)\) "" ; "" , bold(1 ) " mark " )  $

#pagebreak()

= Question 8

The point $lr(\( - frac(5 ,6 )\, b \) )$ is on the unit circle and is in quadrant III.

Determine the exact value of $b $.

== Solution

$   lr(\( - frac(5 ,6 )\) )^(2 )+ b ^(2 ) & = 1  quad  1  \/ 2  " mark for substitution " \  b ^(2 ) & = 1 - frac(25 ,36 ) \  b ^(2 ) & = frac(11 ,36 ) \  b  & =  plus.minus  frac(sqrt(11 ),6 ) \  b  & = - frac(sqrt(11 ),6 ) quad  1  \/ 2  " mark for the exact value of " b    $

1 mark

#pagebreak()

= Question 9

Given the following row of Pascal's Triangle\, determine the values of the next row.

$  mat(delim: #none,  1  "" , 6  "" , 15  "" , 20  "" , 15  "" , 6  "" , 1  )  $

== Solution

$mat(delim: #none, 1  "" , 7  "" , 21  "" , 35  "" , 35  "" , 21  "" , 7  "" , 1 )$

#pagebreak()

= Question 10

The following transformations are applied to $f \(x \)$\, resulting in a new function\, $g \(x \)$.

- reflection over the $x $-axis

- vertical stretch by a factor of 3

- horizontal stretch by a factor of 4

State the equation of $g \(x \)$ in terms of $f \(x \)$.

$  g \(x \)=   $

== Solution

$  g \(x \)= - 3  f lr(\( frac(1 ,4 ) x \) )  $

1 mark for vertical reflection

1 mark for vertical stretch

1 mark for horizontal stretch

3 marks

#pagebreak()

= Question 11

Given the graph of $f \(x \)$\, sketch the graph of $y + 1 = 2  f \(x - 3 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/070bfe8b-d8ea-4b70-aeb1-e61007762045-11_800_803_526_663.jpg", width: 37.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/070bfe8b-d8ea-4b70-aeb1-e61007762045-11_804_805_1405_663.jpg", width: 37.9%)

The graph of

$f \(x \)$ has

already been

drawn for your

reference.

No marks will

be awarded for

the graph of

$f \(x \)$

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-11_791_793_1369_260.jpg", width: 37.3%)

1 mark for vertical stretch

1 mark for horizontal translation

1 mark for vertical translation

3 marks

#pagebreak()

= Question 12

State the equation of the horizontal asymptote of $f \(x \)= frac(2  x ^(2 )- 3  x + 5 ,4  x ^(2 )+ 2  x - 7 )$.

== Solution

$  y = frac(1 ,2 )  $

1 mark

#pagebreak()

= Question 13

Given that $\(x + 4 \)$ is one of the factors of $p \(x \)= x ^(3 )+ 6  x ^(2 )- 32 $\, express $p \(x \)$ in completely

factored form.

$p \(x \)= $

== Solution

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[-4 ], [1 ], [6 ], [0 ], [-32 ],
table.hline(stroke: .5pt),
[], [↓ ], [-4 ], [-8 ], [32 ],
table.hline(stroke: .5pt),
[], [1 ], [2 ], [-8 ], [0 ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for $x = - 4 $

1 mark for synthetic division \(or any equivalent strategy\)

$   & p \(x \)= \(x + 4 \)lr(\( x ^(2 )+ 2  x - 8 \) ) \  & p \(x \)= \(x + 4 \)\(x + 4 \)\(x - 2 \)   $

$frac(1 ,2 )$ mark for consistent product of factors

or

2 marks

$  p \(x \)= \(x + 4 \)^(2 )\(x - 2 \)  $

#pagebreak()

= Question 14

Prove the identity for all permissible values of $theta $.

$  frac(2  cos  ^(2 ) theta ,1 - cot  theta )= frac(sin  2  theta ,tan  theta - 1 )  $

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
[$   & frac(2  cos  ^(2 ) theta ,1 - frac(cos  theta ,sin  theta )) \  & frac(2  cos  ^(2 ) theta ,frac(sin  theta - cos  theta ,sin  theta )) \  & frac(2  cos  ^(2 ) theta  sin  theta ,sin  theta - cos  theta )   $ ], [$   & frac(2  sin  theta  cos  theta ,frac(sin  theta ,cos  theta )- 1 ) \  & frac(2  sin  theta  cos  theta ,frac(sin  theta - cos  theta ,cos  theta )) \  & frac(2  sin  theta  cos  ^(2 ) theta ,sin  theta - cos  theta )   $ ],
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
[$frac(2  cos  ^(2 ) theta ,1 - cot  theta )$ ], [$   & frac(2  sin  theta  cos  theta ,frac(sin  theta ,cos  theta )- 1 ) \  & frac(2  sin  theta  cos  theta ,frac(sin  theta - cos  theta ,cos  theta )) \  & frac(2  sin  theta  cos  ^(2 ) theta ,sin  theta - cos  theta ) \  & frac(sin  theta lr(\( 2  cos  ^(2 ) theta \) ),sin  theta lr(\( 1 - frac(cos  theta ,sin  theta )\) )) \  & frac(2  cos  ^(2 ) theta ,1 - cot  ^(2 ) theta )   $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

Method 3

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ],
table.hline(stroke: .5pt),
[$   & frac(2  cos  ^(2 ) theta ,1 - cot  theta ) \  & frac(2  cos  ^(2 ) theta ,1 - frac(1 ,tan  theta )) \  & frac(2  cos  ^(2 ) theta ,frac(tan  theta - 1 ,tan  theta )) \  & frac(2  cos  ^(2 ) theta ,tan  theta - 1 )\(tan  theta \) \  & frac(2  cos  ^(2 ) theta lr(\( frac(sin  theta ,cos  theta )\) ),tan  theta - 1 ) \  & frac(2  cos  theta  sin  theta ,tan  theta - 1 ) \  & frac(sin  2  theta ,tan  theta - 1 )   $ ], [$frac(sin  2  theta ,tan  theta - 1 )$ ],
table.hline(stroke: .5pt),
[],
);

1 mark for algebraic strategies

1 mark for logical process to prove the identity

1 mark for correct substitution of identities

3 marks

#pagebreak()

= Question 15

Restaurant A has 5 types of hamburgers\, 2 types of french fries\, and 10 types of drinks.

Restaurant B has 4 types of hamburgers\, 5 types of french fries\, and 6 types of drinks.

If a meal is made up of a hamburger\, french fries\, and a drink\, justify which restaurant offers a

greater variety of meals.

== Solution

Restaurant A: $bold(5 ) dot.c  bold(2 ) dot.c  bold(10 )= 100 $ meals

Restaurant B: $4  dot.c  5  dot.c  6 = 120 $ meals

Restaurant B offers a greater variety of meals.

#pagebreak()

= Question 16

Express $log  _(7 )\(2  x - 5 \)+ 2  log  _(7 ) 3 $ as a single logarithm.

== Solution

$  mat(delim: #none,  log  _(7 )\(2  x - 5 \)+ log  _(7 ) 3 ^(2 ) "" , 1  " mark for power law " "" ; log  _(7 )\(2  x - 5 \)+ log  _(7 ) 9  "" , "" ; log  _(7 )\(9 \(2  x - 5 \)\) "" , 1  " mark for product law " "" ; " or " "" , 2  " marks " "" ; log  _(7 )\(18  x - 45 \) "" , )  $

#pagebreak()

= Question 17

Explain why 11 ! is not the total number of 11-letter arrangements that can be made from the

word CELEBRATION.

== Solution

The total number of possible arrangements is half of 11 ! because switching the two Es creates

duplicate arrangements.

1 mark

#pagebreak()

= Question 18

Given $f \(x \)= x - 1 $\, identify a point on the graph of $y = sqrt(f \(x \))$.

*A.*

$\(0 \,- 1 \)$

*B.*

$\(3 \,2 \)$

*C.*

$\(1 \,0 \)$

*D.*

$\(0 \,1 \)$

== Solution

Correct answer: C

$\(1 \,0 \)$

#pagebreak()

= Question 19

Identify the total number of possible arrangements of 6 adults and 4 children seated in a row if

the children must sit together.

*A.*

$6 ! 4 ! $

*B.*

$7 ! 4 $ !

*C.*

10 !

*D.*

6 !

== Solution

Correct answer: B

$7 ! 4 $ !

#pagebreak()

= Question 20

Identify the exact value of $sec  lr(\( - frac(7  pi ,3 )\) )$.

*A.*

-2

*B.*

$- frac(2 ,sqrt(3 ))$

*C.*

$frac(2 ,sqrt(3 ))$

*D.*

2

== Solution

Correct answer: D

2

#pagebreak()

= Question 21

Given $log  _(x )lr(\( frac(1 ,25 )\) )= - 2 $\, identify the value of $x $.

*A.*

-5

*B.*

$- frac(1 ,5 )$

*C.*

$frac(1 ,5 )$

*D.*

5

== Solution

Correct answer: D

5

#pagebreak()

= Question 22

Identify the equation for all of the asymptotes on the graph of $y = tan  x $.

*A.*

$x = k  pi \, k  in  bb(Z )$

*B.*

$x = 2  k  pi \, k  in  bb(Z )$

*C.*

$x = frac(pi ,2 )+ k  pi \, k  in  bb(Z )$

*D.*

$x = frac(pi ,2 )+ 2  k  pi \, k  in  bb(Z )$

== Solution

Correct answer: C

$x = frac(pi ,2 )+ k  pi \, k  in  bb(Z )$

#pagebreak()

= Question 23

If $p \(x \)= 3 \(m \)\(x + 1 \)^(2 )$ is a cubic function with a $y $-intercept of -12 \, identify the missing factor\, $m $.

*A.*

$m = x - 4 $

*B.*

$m = x + 4 $

*C.*

$m = x + 12 $

*D.*

$m = x - 12 $

== Solution

Correct answer: A

$m = x - 4 $

#pagebreak()

= Question 24

Identify the number of negative terms in the binomial expansion of $\(x - y \)^(5 )$.

*A.*

2

*B.*

3

*C.*

5

*D.*

6

== Solution

Correct answer: B

3

#pagebreak()

= Question 25

Given $f \(x \)= x ^(2 )$\, identify which equation represents the graph of $y = f \(x \)$ after a translation

of 5 units to the left.

*A.*

$y = \(x + 5 \)^(2 )$

*B.*

$y = \(x - 5 \)^(2 )$

*C.*

$y = x ^(2 )- 5 $

*D.*

$y = x ^(2 )+ 5 $

== Solution

Correct answer: A

$y = \(x + 5 \)^(2 )$

#pagebreak()

= Question 26

When a polynomial\, $p \(x \)$\, is divided by \( $x - 7 $ \)\, the remainder is 24 . Identify the only

statement that must be true.

*A.*

$x = 7 $ is a zero of $p \(x \)$

*B.*

$p \(7 \)= 24 $

*C.*

$x = 24 $ is a zero of $p \(x \)$

*D.*

the $y $-intercept is 24

== Solution

Correct answer: B

$p \(7 \)= 24 $

#pagebreak()

= Question 27

Given $f \(x \)= frac(\(2  x + 1 \)\(x - 8 \),\(x - 8 \)\(x + 4 \))$\, state the equation\(s\) of the vertical asymptote\(s\).

== Solution

$  x = - 4  quad  bold(1 ) " mark "  $

#pagebreak()

= Question 28

Given the graph of $\(f  dot.c  g \)\(x \)$ and $g \(x \)$\, sketch the graph of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-05_798_763_504_262.jpg", width: 35.9%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-05_798_761_504_1102.jpg", width: 35.8%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-05_768_768_1514_253.jpg", width: 36.1%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-24_773_765_1620_258.jpg", width: 36.0%)

1 mark for operation of division

1 mark for restricted domain

2 marks

#pagebreak()

= Question 29

Brian was asked to state the zeros of the polynomial $p \(x \)= \(x + 2 \)\(x - 5 \)\(x - 1 \)$.

Brian's response:

$  " Zeros: "\(x + 2 \)\,\(x - 5 \)\,\(x - 1 \)  $

Explain why his response is incorrect.

== Solution

Brian stated the factors instead of the zeros.

#pagebreak()

= Question 30

Simplify $ "" _(n + 3 ) C _(2 )$.

== Solution

$frac(\(n + 3 \)! ,\(n + 3 - 2 \)! 2 ! )$

$frac(\(n + 3 \)! ,\(n + 1 \)! 2 ! )$

$frac(\(n + 3 \)\(n + 2 \)\(n + 1 \)! ,\(n + 1 \)! 2 )$

$frac(\(n + 3 \)\(n + 2 \),2 )$

or

$frac(n ^(2 )+ 5  n + 6 ,2 )$

$frac(1 ,2 )$ mark for substitution

1 mark for factorial expansion

$frac(1 ,2 )$ mark for simplification of factorials

2 marks

#pagebreak()

= Question 31

Verify that the equation $2  cos  ^(2 ) x = sin  x + 1 $ is true for $x = frac(pi ,6 )$.

== Solution

#table(stroke: none,
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ], [],
table.hline(stroke: .5pt),
[$2  cos  ^(2 )lr(\( frac(pi ,6 )\) )$ ], [$sin  lr(\( frac(pi ,6 )\) )+ 1 $ ], [$frac(1 ,2 )$ mark for substitution ],
table.hline(stroke: .5pt),
[$2 lr(\( frac(sqrt(3 ),2 )\) )^(2 )$ ], [$frac(1 ,2 )+ 1 $ ], [1 mark for exact values \( $frac(1 ,2 )$ mark for each\) ],
table.hline(stroke: .5pt),
[$2 lr(\( frac(3 ,4 )\) )$ ], [], [],
table.hline(stroke: .5pt),
table.cell(colspan: 2)[∴ LHS = RHS ], [2 marks ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 32

The height of a fish jumping out of the water can be modelled by the function

$h \(t \)= - t \(t - 1 \)\(t - 4 \)\(t - 5 \)$ where $h \(t \)$ is the height of the fish above or below the water in cm \,

and $t $ is the time in seconds\, $t  >=  0 $.

a\) Sketch a graph representing the height of the fish with respect to time over the interval $\[0 \,5 \]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-09_936_916_734_661.jpg", width: 43.1%)

b\) State\, from the graph in a\)\, the total number of seconds that the fish is above the water.

== Solution

a\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-28_1005_1697_920_266.jpg", width: 79.9%)

b\) 2 seconds 1 mark for time consistent with graph in a\)

1 mark

Note:

- Scale values on $h $-axis are not required.

#pagebreak()

= Question 33

Describe the behaviour of the graph of $y = 5 ^(x )+ 4 $ as it approaches $y = 4 $.

== Solution

There is a horizontal asymptote at $y = 4 $\, so the graph approaches $y = 4 $ without ever touching it.

1 mark

#pagebreak()

= Question 34

Sketch the angle of 6 radians in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-11_917_1066_577_522.jpg", width: 50.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-30_533_559_559_249.jpg", width: 26.3%)

$frac(1 ,2 )$ mark for an angle in quadrant IV

$frac(1 ,2 )$ mark for an appropriate angle

1 mark

Note:

- If the directional arrow is not indicated\, deduct an E1 error \(final answer not stated\).

#pagebreak()

= Question 35

Sketch the graph of the function $y = 4  sin  lr(\( frac(pi ,3 ) x \) )- 2 $ over the domain $\[- 3 \,6 \]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-12_938_1378_571_352.jpg", width: 64.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-31_1005_1321_653_245.jpg", width: 62.2%)

Note:

- Deduct $frac(1 ,2 )$ mark for procedural error for not completing the domain of \[-3\, 6\].

- If period mark not awarded\, do not deduct for E9 error \(scale value on $x $-axis not indicated\).

#pagebreak()

= Question 36

Given $f \(x \)= 3  x - 12 $ and $g \(x \)= x - 4 $\,

a\) determine the equation of $h \(x \)= lr(\( frac(f ,g )\) )\(x \)$.

$  h \(x \)=   $

b\) describe what the non-permissible value represents on the graph of $h \(x \)$.

== Solution

a\) $h \(x \)= frac(3  x - 12 ,x - 4 )$

$  h \(x \)= frac(3 \(x - 4 \),\(x - 4 \))  $

$  h \(x \)= 3 \, x  !=  4   $

b\) The non-permissible value is a point of discontinuity \(hole\).

1 mark for division of $lr(\( frac(f ,g )\) )\(x \)$

1 mark

1 mark

#pagebreak()

= Question 37

Determine an equation of a radical function\, $f \(x \)$\, with a domain of $x  >=  5 $ and a range of $y  >= - 2 $.

$  f \(x \)=   $

== Solution

$  f \(x \)= sqrt(x - 5 )- 2   $

1 mark for horizontal translation

1 mark for vertical translation

2 marks

- Other equations are possible.

#pagebreak()

= Question 38

Determine the exact value of $cos  lr(\( frac(17  pi ,12 )\) )$.

== Solution

$   cos  lr(\( frac(17  pi ,12 )\) ) & = cos  lr(\( frac(3  pi ,4 )+ frac(2  pi ,3 )\) ) \  & = cos  frac(3  pi ,4 ) cos  frac(2  pi ,3 )- sin  frac(3  pi ,4 ) sin  frac(2  pi ,3 ) \  & = lr(\( - frac(sqrt(2 ),2 )\) )lr(\( - frac(1 ,2 )\) )- lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(sqrt(3 ),2 )\) ) \  & = frac(sqrt(2 ),4 )- frac(sqrt(6 ),4 ) \  & = frac(sqrt(2 )- sqrt(6 ),4 )   $

1 mark for substitution into correct identity

2 marks for exact values \( $frac(1 ,2 )$ mark for each\)

3 marks

Note:

- Other combinations are possible.

- Deduct a maximum $frac(1 ,2 )$ mark for arithmetic errors in simplification.

#pagebreak()

= Question 39

Sketch the graph of $y = frac(1 ,2 ) sqrt(- x )+ 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-16_856_872_509_620.jpg", width: 41.0%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-35_849_859_587_254.jpg", width: 40.4%)

1 mark for shape of a radical function

1 mark for vertical compression

1 mark for horizontal reflection

1 mark for vertical translation

4 marks

#pagebreak()

= Question 40

Given $f \(x \)= frac(3  x ,4 )+ 9 $\, determine the equation of $f ^(- 1 )\(x \)$.

== Solution

Let $y = f \(x \)$

$   y  & = frac(3  x ,4 )+ 9  & & \  x  & = frac(3  y ,4 )+ 9  & & 1  " mark for switching " x  " and " y  " values " \  4  x  & = 3  y + 36  & & \  3  y  & = 4  x - 36  & & \  y  & = frac(4 ,3 ) x - 12  & & 1  \/ 2  " mark for solving for " y  \  f ^(- 1 )\(x \) & = frac(4  x ,3 )- 12  & & 1  \/ 2  " mark for writing equation of " f ^(- 1 )\(x \)   $

2 marks

#pagebreak()

= Question 41

Describe the end behaviour of the polynomial function $p \(x \)= - \(x - 2 \)\(x + 3 \)^(2 )$.

== Solution

The graph rises as $x $ approaches negative infinity and falls as $x $ approaches positive infinity.

1 mark

#pagebreak()

= Question 42

Given $csc  theta = - 4 $ and $theta $ is in quadrant IV\,

a\) determine the exact value of $cos  theta $.

b\) determine the exact value of $cot  theta $.

== Solution

a\) $sin  theta = - frac(1 ,4 ) quad  1 $ mark for reciprocal

$   1 ^(2 )- lr(\( - frac(1 ,4 )\) )^(2 ) & = cos  ^(2 ) theta  \  frac(15 ,16 ) & = cos  ^(2 ) theta  \  plus.minus  frac(sqrt(15 ),4 ) & = cos  theta  \  cos  theta  & = frac(sqrt(15 ),4 ) quad  1  " mark for " cos  theta lr(\( frac(1 ,2 ) " mark for quadrant; " 1  \/ 2  " mark for value "\) )   $

2 marks

b\)

$   cot  theta  & = frac(frac(sqrt(15 ),4 ),- frac(1 ,4 )) \  & = - sqrt(15 )   $

1 mark for $cot  theta $ consistent with answer in a\)

\( $frac(1 ,2 )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

1 mark

#pagebreak()

= Question 43

Sketch the graph of the function $f \(x \)= frac(10 ,x ^(2 )+ 2 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-20_921_919_562_605.jpg", width: 43.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-39_853_1096_591_249.jpg", width: 51.6%)

1 mark for asymptotic behaviour approaching $y = 0 $

1 mark for shape \( $frac(1 ,2 )$ mark for graph left of $y $-axis\; $frac(1 ,2 )$ mark for graph right of $y $-axis\)

2 marks

#pagebreak()

= Question 44

Explain why only one of the following equations could be solved algebraically without using

logarithms.

$  3 ^(5  x )= 6 ^(2  x - 1 ) quad  " or " quad  16 ^(2  x + 3 )= lr(\( frac(1 ,2 )\) )^(4  x - 5 )  $

== Solution

The equation $16 ^(2  x + 3 )= lr(\( frac(1 ,2 )\) )^(4  x - 5 )$ can be solved without the use of logarithms because 16 and $frac(1 ,2 )$

can be changed to a common base of 2.

#pagebreak()

= Question 45

Given a graph of $y = f \(x \)$\, describe how to sketch the graph of $y = | f \(x \)| $.

== Solution

Reflect all the points with negative $y $-values over the $x $-axis.

1 mark

#pagebreak()

= Question 46

Sketch the graph of $y = log  _(3 )\(x + 4 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/1b8ee833-dc19-4822-81a9-e48d087146e0-23_783_781_485_674.jpg", width: 36.8%)

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2018-jun/assets/89fe0cee-373a-4420-942b-32d40d1cdfb6-42_920_883_559_251.jpg", width: 41.6%)

1 mark for increasing logarithmic function

1 mark for asymptotic behaviour

approaching $x = - 4 $

2 marks

#pagebreak()

= Question 47

Solve\, algebraically.

$  log  x + log  4 - log  \(x - 2 \)= log  5   $

== Solution

Method 1

$   log  lr(\( frac(4  x ,x - 2 )\) ) & = log  5  \  frac(4  x ,x - 2 ) & = 5  \  4  x  & = 5 \(x - 2 \) \  4  x  & = 5  x - 10  \  10  & = x    $

1 mark for product law

1 mark for quotient law

$frac(1 ,2 )$ mark for equating arguments

$frac(1 ,2 )$ mark for solving for $x $

3 marks

Method 2

$   log  x + log  4 - log  \(x - 2 \)- log  5  & = 0  \  log  lr(\( frac(4  x ,5 \(x - 2 \))\) ) & = 0  \  10 ^(0 ) & = frac(4  x ,5 \(x - 2 \)) \  5 \(x - 2 \) & = 4  x  \  5  x - 10  & = 4  x  \  x  & = 10    $

1 mark for product law

1 mark for quotient law

$frac(1 ,2 )$ mark for converting to exponential form

$frac(1 ,2 )$ mark for solving for $x $

3 marks

#pagebreak()

= Question 48

Given $sin  theta = frac(1 ,2 )$\, determine all possible values of $theta $ over the interval $\[- 2  pi \, 2  pi \]$.

== Solution

$theta = - frac(11  pi ,6 )\,- frac(7  pi ,6 )\, frac(pi ,6 )\, frac(5  pi ,6 )$

1 mark for positive values of $theta $ \( $frac(1 ,2 )$ mark for each\)

1 mark for negative values of $theta $ \( $frac(1 ,2 )$ mark for each\)

2 marks