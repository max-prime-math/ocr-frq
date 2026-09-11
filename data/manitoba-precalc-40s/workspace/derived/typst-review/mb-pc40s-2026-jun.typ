#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2026-jun

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Jack rolled a water bottle from one edge of his desk to the other. The desk measures 60 cm

from edge to edge. The water bottle has a diameter of 7 cm . Determine the angle that the

water bottle rotated\, in degrees.

== Solution

$   & s = theta  r  \  & theta = frac(s ,r ) \  & theta = frac(60 ,3.5 ) \  & theta = 17.142857  dots.h  \  & theta = \(17.142857  dots.h \)lr(\( frac(180 ^(degree ),pi )\) ) \  & theta = 982.213363  dots.h  \  & theta = 982.213 ^(degree )   $

1 mark for substitution

1 mark for conversion

2 marks

#pagebreak()

= Question 2

There are 15 dogs and 12 cats in an animal shelter. Determine the number of ways that three

dogs and two cats can be selected if Scout\, one of the dogs\, must be selected.

== Solution

$   &  "" _(1 ) C _(1 ) dot.c  "" _(14 ) C _(2 ) dot.c  "" _(12 ) C _(2 ) \  & 6006    $

$   & 1  " mark for " "" _(14 ) C _(2 ) \  & frac(1 ,2 ) op("mark") " for " "" _(12 ) C _(2 )   $

$frac(1 ,2 )$ mark for product of combinations

2 marks

Note:

$ "" _(1 ) C _(1 )$ does not need to be shown.

#pagebreak()

= Question 3

Emily wants to save money to buy a car. She invests $dollar  180 $ per month at an annual interest rate

of $4.5  % $\, compounded monthly.

Determine\, algebraically\, the number of monthly investments she will need to make to obtain at

least $dollar  15000 $. Express the final answer as a whole number.

Use the formula: $F  V = frac(R lr(\[ \(1 + i \)^(n )- 1 \] ),i )$

where $F  V = $ the future value

$   & R = " the investment amount each period " \  & i = lr(\[ frac(" the annual interest rate (as a decimal) "," the number of compounding periods per year ")\] ) \  & n = " the number of investments "   $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$  15000 = frac(180 lr(\[ lr(\( 1 + frac(0.045 ,12 )\) )^(n )- 1 \] ),frac(0.045 ,12 ))  $ $  15000 = frac(180 lr(\[ \(1 + 0.00375 \)^(n )- 1 \] ),0.00375 )  $ $   log  \(1.3125 \) & = log  \(1.00375 \)^(n ) \  log  \(1.3125 \) & = n  log  \(1.00375 \) \  n  & = frac(log  \(1.3125 \),log  \(1.00375 \)) \  n  & = 72.651539  dots.h    $ $  therefore  73  " monthly investments are needed "  $ ], [#table(stroke: none,
columns: 1,
align: (left, ),

[$frac(1 ,2 )$ mark for substitution ],
[$frac(bold(1 ),bold(2 ))$ mark for simplification ],
[$frac(1 ,2 )$ mark for applying logarithms ],
[1 mark for power law ],
[$frac(1 ,2 )$ mark for evaluating quotient of logarithms ],
[3 marks ],
); ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 4

Determine and simplify the $4 ^("th ")$ term in the binomial expansion of $lr(\( 3  x - frac(2 ,x ^(2 ))\) )^(6 )$.

== Solution

$   t _(4 ) & =  "" _(6 ) C _(3 )\(3  x \)^(3 )lr(\( - frac(2 ,x ^(2 ))\) )^(3 ) \  & = 20 lr(\( 27  x ^(3 )\) )lr(\( frac(- 8 ,x ^(6 ))\) ) \  & = frac(- 4320 ,x ^(3 ))   $

2 marks \( 1 mark for $ "" _(6 ) C _(3 ) \; frac(1 ,2 )$ mark for each consistent factor\)

1 mark for simplification \( $frac(1 ,2 )$ mark for coefficient\, $frac(1 ,2 )$ mark for exponent\)

3 marks

#pagebreak()

= Question 5

Solve\, algebraically\, over the interval $\[0 \,2  pi \]$.

$  4  cos  ^(2 ) x - 3  cos  x - 1 = 0   $

== Solution

$   & 4  cos  ^(2 ) x - 3  cos  x - 1 = 0  \  & \(4  cos  x + 1 \)\(cos  x - 1 \)= 0  \  & cos  x = - frac(1 ,4 ) quad  cos  x = 1  quad  1  " mark for solving for " cos  x \(1  \/ 2  " mark for each branch "\) \  & quad  x _(r )= 1.318116  dots.h  \  & quad  x = 1.823 \,4.460  quad  x = 0 \,2  pi  quad  2  " marks for solving for " x \(1  \/ 2  " mark for each value "\)   $

3 marks

#pagebreak()

= Question 6

State an equation for a rational function\, $g \(x \)$\, whose graph has a vertical asymptote at $x = 7 $.

$g \(x \)= $

== Solution

$  g \(x \)= frac(1 ,x - 7 )  $

1 mark

Note:

Other equations are possible.

#pagebreak()

= Question 7

State an equation of a radical function\, $f \(x \)$\, with a domain of $x  <=  0 $ and a range of $y  >=  1 $.

$f \(x \)= $

$\_ \_ \_ \_ $

== Solution

$f \(x \)= underline(sqrt(- x )+ 1 ) quad  1 $ mark for a radical function with a domain of $x  <=  0 $

1 mark for a radical function with a range of $y  >=  1 $

2 marks

Note:

Other equations are possible.

#pagebreak()

= Question 8

Prove the identity for all permissible values of $x $.

$  frac(cos  x + sin  ^(2 ) x  sec  x ,sin  x )= sec  x  csc  x   $

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
[$   frac(cos  x + sin  ^(2 ) x  sec  x ,sin  x ) \  frac(cos  x + frac(sin  ^(2 ) x ,cos  x ),sin  x ) \  frac(cos  ^(2 ) x + sin  ^(2 ) x ,cos  x ) \    frac(sin  x ,frac(1 ,cos  x )) \  sin  x  \  frac(1 ,cos  x ) dot.c  frac(1 ,sin  x ) \  sec  x  csc  x    $ ], [$sec  x  csc  x $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 9

Given the graph of\, $y = f \(x \)$\, sketch the graph of $y = 2 | f \(- x \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/77052c8c-b56e-4088-a63f-96d745fc89b6-09_994_985_455_247.jpg", width: 46.4%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/77052c8c-b56e-4088-a63f-96d745fc89b6-09_1007_994_1488_240.jpg", width: 46.8%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-11_982_975_556_245.jpg", width: 45.9%)

1 mark for horizontal reflection

1 mark for absolute value

1 mark for vertical stretch

3 marks

#pagebreak()

= Question 10

Solve\, algebraically.

$  log  \(x - 1 \)+ log  \(x + 2 \)= 1   $

== Solution

$  mat(delim: #none,  log  \[\(x - 1 \)\(x + 2 \)\] "" , = 1  "" , 1  " mark for product law " "" ; \(x - 1 \)\(x + 2 \) "" , = 10 ^(1 ) "" , 1  " mark for exponential form " "" ; x ^(2 )+ x - 2  "" , = 10  "" , "" ; x ^(2 )+ x - 12  "" , = 0  "" , "" ; \(x + 4 \)\(x - 3 \) "" , = 0  "" , )  $

$frac(1 ,2 )$ mark for the permissible value of $x $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

3 marks

#pagebreak()

= Question 11

Justify that there are only two negative terms in the expansion of $\(- 2  x + 5  y \)^(4 )$.

== Solution

$   & t _(1 )=  "" _(4 ) C _(0 )\(- 2  x \)^(4 )\(5  y \)^(0 ) -> +  \  & t _(2 )=  "" _(4 ) C _(1 )\(- 2  x \)^(3 )\(5  y \)^(1 ) -> -  \  & t _(3 )=  "" _(4 ) C _(2 )\(- 2  x \)^(2 )\(5  y \)^(2 ) -> +  \  & t _(4 )=  "" _(4 ) C _(3 )\(- 2  x \)^(1 )\(5  y \)^(3 ) -> -  \  & t _(5 )=  "" _(4 ) C _(4 )\(- 2  x \)^(0 )\(5  y \)^(4 ) -> +    $

∴ The term is negative only when $\(- 2  x \)$ has an odd exponent\, which occurs twice.

1 mark

#pagebreak()

= Question 12

The graph of $y = 5  sin  \(2  x \)+ 3 $ below can be used to solve the equation $0 = 5  sin  \(2  x \)+ 3 $.

State how many solutions there are to the equation $0 = 5  sin  \(2  x \)+ 3 $ over the interval $\[0 \,2  pi \]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/77052c8c-b56e-4088-a63f-96d745fc89b6-12_1370_871_558_638.jpg", width: 41.0%)

== Solution

There are four solutions.

1 mark

#pagebreak()

= Question 13

Given the functions\, $f \(x \)= x ^(2 )- 1 $ and $g \(x \)= x + 1 $\,

a\) state the equation of $h \(x \)= frac(f \(x \),g \(x \))$.

$h \(x \)= $

$\_ \_ \_ \_ $

b\) sketch the graph of $h \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/77052c8c-b56e-4088-a63f-96d745fc89b6-13_912_906_1531_242.jpg", width: 42.6%)

== Solution

a\)

$   h \(x \) & = frac(x ^(2 )- 1 ,x + 1 ) \  & = frac(\(x + 1 \)\(x - 1 \),\(x + 1 \)) \  & = x - 1 \, x  != - 1    $

1 mark

b\)



#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-15_907_898_1255_303.jpg", width: 42.3%)

1 mark for shape of graph

consistent with a\)

1 mark for point of discontinuity

\(hole\) at $x = - 1 $

2 marks

Note:

Deduct a maximum of 1 mark for the concept error of not restricting domain.

Deduct $frac(1 ,2 )$ mark for procedural error \(not stating domain of simplified function in part a\)

if graph shows the correct domain.

#pagebreak()

= Question 14

State an equation for $g \(x \)$\, in terms of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/77052c8c-b56e-4088-a63f-96d745fc89b6-14_955_970_474_590.jpg", width: 45.6%)

$g \(x \)= $

$\_ \_ \_ \_ $

== Solution

$g \(x \)= frac(1 ,2 ) f \(x \)- 3 $

1 mark for vertical compression

1 mark for vertical translation

2 marks

#pagebreak()

= Question 15

Sketch the graph of a polynomial function\, $p \(x \)$\, with the following characteristics:

- degree 5

- leading coefficient of -1

- a zero at -3 \, with a multiplicity of 3

- a zero at 1 \, with a multiplicity of 2

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/77052c8c-b56e-4088-a63f-96d745fc89b6-15_1034_1043_786_554.jpg", width: 49.1%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-17_902_915_855_245.jpg", width: 43.1%)

1 mark for $x $-intercept at -3

with a multiplicity of 3

1 mark for $x $-intercept at 1

with a multiplicity of 2

$frac(1 ,2 )$ mark for end behaviour

$frac(1 ,2 )$ mark for $y $-intercept

3 marks

#pagebreak()

= Question 16

Identify the expression that is equivalent to $tan  theta lr(\( csc  ^(2 ) theta - 1 \) )$.

*A.*

$cot  theta $

*B.*

$tan  theta $

*C.*

$sec  theta $

*D.*

$sin  theta $

== Solution

Correct answer: A

$cot  theta $

#pagebreak()

= Question 17

Identify the expression that represents the number of ways five books can be arranged on a

shelf if two of them must be together.

*A.*

$5 ! 2 $ !

*B.*

5!-2!

*C.*

$4 ! 2 $ !

*D.*

$3 ! 2 $ !

== Solution

Correct answer: C

$4 ! 2 $ !

#pagebreak()

= Question 18

Identify the value of $x $ in the equation\, $log  _(8 ) x = - frac(1 ,3 )$.

*A.*

$quad - 2 $

*B.*

$- frac(1 ,2 )$

*C.*

$frac(1 ,2 )$

*D.*

2

== Solution

Correct answer: C

$frac(1 ,2 )$

#pagebreak()

= Question 19

Given the functions\, $f \(x \)= frac(1 ,x )$ and $g \(x \)= sqrt(x - 1 )$\, identify the domain of $f \(g \(x \)\)$.

*A.*

$\(- oo \, oo \)$

*B.*

$\(- oo \, 1 \) union \(1 \, oo \)$

*C.*

$\[1 \, oo \)$

*D.*

$\(1 \, oo \)$

== Solution

Correct answer: D

$\(1 \, oo \)$

#pagebreak()

= Question 20

Given $f \(x \)= frac(3 \(x + 2 \),5 \(x + 2 \)\(x - 2 \))$\, identify the equation of the horizontal asymptote.

*A.*

$quad  y = - 2 $

*B.*

$quad  y = 0 $

*C.*

$quad  y = frac(3 ,5 )$

*D.*

$y = 2 $

== Solution

Correct answer: B

$quad  y = 0 $

#pagebreak()

= Question 21

Identify the range of the sinusoidal function\, $f \(x \)= 2  sin  x + 3 $.

*A.*

$\{ y  divides  y  in  bb(R )\} $

*B.*

$\{ y  divides  2  <=  y  <=  4 \, y  in  bb(R )\} $

*C.*

$\{ y  divides - 2  <=  y  <=  2 \, y  in  bb(R )\} $

*D.*

$\{ y  divides  1  <=  y  <=  5 \, y  in  bb(R )\} $

== Solution

Correct answer: D

$\{ y  divides  1  <=  y  <=  5 \, y  in  bb(R )\} $

#pagebreak()

= Question 22

Given that $\(x - 3 \)$ is a factor of the polynomial $P \(x \)$\, identify which of the following is true.

*A.*

$quad  P \(3 \)= 0 $

*B.*

$quad  P \(0 \)= 3 $

*C.*

$P \(0 \)= - 3 $

*D.*

$P \(- 3 \)= 0 $

== Solution

Correct answer: A

$quad  P \(3 \)= 0 $

#pagebreak()

= Question 23

Identify the value that best represents the angle in standard position.

*A.*

-4.4 radians

*B.*

- 2 radians

*C.*

$quad  1.3 $ radians

*D.*

1.9 radians

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/cfc7480b-f0cd-4f20-a6be-fb2697e98a6f-03_450_441_1256_1188.jpg", width: 20.8%)

== Solution

Correct answer: A

-4.4 radians

#pagebreak()

= Question 24

Identify the expression that is equivalent to $log  _(a )\(x + 2 \)+ 3  log  _(a )\(x \)$.

*A.*

$log  _(a )\(3 \(x + 2 \)\)$

*B.*

$quad  log  _(a )lr(\( x ^(3 )\(x + 2 \)\) )$

*C.*

$log  _(a )lr(\( frac(\(x + 2 \),x ^(3 ))\) )$

*D.*

$log  _(a ) x + log  _(a ) 2 + log  _(a ) x ^(3 )$

== Solution

Correct answer: B

$quad  log  _(a )lr(\( x ^(3 )\(x + 2 \)\) )$

#pagebreak()

= Question 25

Evaluate.

$  tan  ^(3 )lr(\( frac(3  pi ,4 )\) )+ csc  lr(\( frac(- 4  pi ,3 )\) ) cos  lr(\( frac(13  pi ,6 )\) )  $

== Solution

$\(- 1 \)^(3 )+ lr(\( frac(2 ,sqrt(3 ))\) )lr(\( frac(sqrt(3 ),2 )\) )$

$- 1 + 1 $

0

1 mark for $tan  lr(\( frac(3  pi ,4 )\) )\(1  \/ 2 $ mark for value\, $1  \/ 2 $ mark for quadrant $\)$

1 mark for $csc  lr(\( frac(- 4  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for value\, $frac(1 ,2 )$ mark for quadrant\)

1 mark for $cos  lr(\( frac(13  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for value\, $frac(1 ,2 )$ mark for quadrant $\)$

3 marks

#pagebreak()

= Question 26

If $a = log  4 $ and $b = log  3 $\, express $log  36 $ in terms of $a $ and $b $.

== Solution

$   log  36  & = log  4 + log  3 ^(2 ) \  & = log  4 + 2  log  3  \  & = a + 2  b    $

1 mark for product law

1 mark for power law

2 marks

#pagebreak()

= Question 27

Justify that $tan  2  x $ has a non-permissible value at $x = frac(pi ,4 )$.

== Solution

Method 1

$tan  2  x $

Let $x = frac(pi ,4 )$\,

$tan  lr(\( 2  dot.c  frac(pi ,4 )\) ) quad  1 $ mark for substitution

$tan  frac(pi ,2 )$

$frac(1 ,0 )$ which is undefined

1 mark for justification

$therefore  x  !=  frac(pi ,4 )$

2 marks

Method 2

$tan  2  x = frac(2  tan  x ,1 - tan  ^(2 ) x )$

$1 - tan  ^(2 ) x  !=  0 $

$tan  ^(2 ) x  !=  1 $

$tan  x  !=  plus.minus  1 $

$therefore  x  !=  frac(pi ,4 )$

1 mark for correct substitution of appropriate identity

1 mark for justification

2 marks

#pagebreak()

= Question 28

Determine the exact value of $tan  theta $\, if $sec  theta = frac(6 ,5 )$ and $theta $ terminates in quadrant IV.

== Solution

Method 1

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-25_561_617_698_243.jpg", width: 29.0%)

$   cos  theta  & = frac(5 ,6 ) \  5 ^(2 )+ y ^(2 ) & = 6 ^(2 ) \  y ^(2 ) & = 36 - 25  \  y ^(2 ) & = 11    $

1 mark for value of $y $

1 mark for $tan  theta $ \( $frac(1 ,2 )$ mark for quadrant\, $frac(1 ,2 )$ mark for value\)

2 marks

Note:

Accept any of the following values for $y :  y =  plus.minus  sqrt(11 )\, y = sqrt(11 )\, y = - sqrt(11 )$.

#pagebreak()

= Question 29

Given the function\, $g \(x \)= frac(4 ,x ^(2 )+ 1 )$\,

a\) sketch the graph of $g \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/cfc7480b-f0cd-4f20-a6be-fb2697e98a6f-08_1192_1193_691_468.jpg", width: 56.1%)

b\) state the range of the graph of $g \(x \)$.

== Solution

a\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-27_967_1083_868_290.jpg", width: 51.0%)

1 mark for asymptotic

behaviour approaching

$y = 0 $

1 mark for shape

\( $frac(1 ,2 )$ mark for graph left of $x = 0 $\;

$frac(1 ,2 )$ mark for graph right of $x = 0 $ \)

2 marks

b\) Range: $\{ y  divides  0 < y  <=  4 \, y  in  bb(R )\} $

or

Range: \(0\,4\]

1 mark for range

consistent with a\)

1 mark

#pagebreak()

= Question 30

Given $y = x ^(2 )- 4 $\,

a\) determine the equation of the inverse.

$y = $

$\_ \_ \_ \_ $

b\) state a restriction on the domain of $y = x ^(2 )- 4 $\, in order for its inverse to be a function.

== Solution

a\)

$   & y = x ^(2 )- 4  \  & x = y ^(2 )- 4  \  & y ^(2 )= x + 4  \  & y =  plus.minus  sqrt(x + 4 )   $

1 mark for switching $x $ and $y $

1 mark for solving for $y $

2 marks

b\) Domain: $\{ x  divides  x  >=  0 \, x  in  bb(R )\} $

or

1 mark

Domain: $\[0 \, oo \)$

Note:

Other solutions are possible for b\).

#pagebreak()

= Question 31

Given $cos  alpha = - frac(1 ,3 )$ and $sin  beta = - frac(2 ,3 )$ where $alpha $ and $beta $ terminate in the same quadrant\, determine

the exact value of $sin  \(alpha - beta \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-29_464_524_692_241.jpg", width: 24.7%)

$  limits(<--> )^(c ) "" ^(x ) "" ^(limits(beta _(r ))_(3 ))  $

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  1 + y ^(2 ) & = 9  \  y ^(2 ) & = 8  \  y  & =  plus.minus  sqrt(8 ) \  y  & = - sqrt(8 )   $

$   x ^(2 )+ y ^(2 ) & = r ^(2 ) \  x ^(2 )+ 4  & = 9  \  x ^(2 ) & = 5  \  x  & =  plus.minus  sqrt(5 ) \  x  & = - sqrt(5 )   $

$frac(1 ,2 )$ mark for value of $x $

$frac(1 ,2 )$ mark for value of $y $

$   & sin  \(alpha - beta \)= sin  alpha  cos  beta - cos  alpha  sin  beta  \  &= lr(\( frac(- sqrt(8 ),3 )\) )lr(\( frac(- sqrt(5 ),3 )\) )- lr(\( frac(- 1 ,3 )\) )lr(\( frac(- 2 ,3 )\) ) \  &= frac(sqrt(40 ),9 )- frac(2 ,9 ) \  &= frac(sqrt(40 )- 2 ,9 ) \  & " or " \  &= frac(2  sqrt(10 )- 2 ,9 )   $

$frac(1 ,2 )$ mark for consistent value of $sin  alpha $

$frac(1 ,2 )$ mark for consistent value of $cos  beta $

1 mark for substitution into correct

identity

3 marks

Note:

Accept any of the following values for $x :  x =  plus.minus  sqrt(5 )\, x = - sqrt(5 )\, x = sqrt(5 )$.

Accept any of the following values for $y :  y =  plus.minus  sqrt(8 )\, y = - sqrt(8 )\, y = sqrt(8 )$.

#pagebreak()

= Question 32

Sketch the graph of $y + 2 = - sqrt(4  x )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/cfc7480b-f0cd-4f20-a6be-fb2697e98a6f-11_1124_1123_524_491.jpg", width: 52.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-30_1117_1109_602_245.jpg", width: 52.2%)

1 mark for shape of

a radical function

1 mark for vertical

reflection

1 mark for horizontal

compression

1 mark for vertical

translation

4 marks

#pagebreak()

= Question 33

Express $p \(x \)= x ^(4 )- x ^(3 )- 6  x ^(2 )+ 4  x + 8 $ in completely factored form\, given that \( $x + 1 $ \) is a factor

of $p \(x \)$.

$p \(x \)= $

== Solution

#table(stroke: none,
columns: 6,
align: (left, left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5), table.vline(stroke: .5pt, x: 6),
table.hline(stroke: .5pt),
[-1 ], [1 ], [-1 ], [-6 ], [4 ], [8 ],
table.hline(stroke: .5pt),
[], [], [-1 ], [2 ], [4 ], [-8 ],
table.hline(stroke: .5pt),
[], [1 ], [-2 ], [-4 ], [8 ], [0 ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for synthetic division

\(or equivalent strategy\)

$   & p \(x \)= \(x + 1 \)lr(\( x ^(3 )- 2  x ^(2 )- 4  x + 8 \) ) \  & p \(2 \)= \(2 + 1 \)lr(\( 2 ^(3 )- 2 \(2 \)^(2 )- 4 \(2 \)+ 8 \) ) \  & p \(2 \)= 0    $

1 mark for identifying a second zero

of $p \(x \)$

$therefore \(x - 2 \)$ is a factor

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [1 ], [-2 ], [-4 ], [8 ],
table.hline(stroke: .5pt),
[], [], [2 ], [0 ], [-8 ],
table.hline(stroke: .5pt),
[], [1 ], [0 ], [-4 ], [0 ],
table.hline(stroke: .5pt),
[],
);

$frac(1 ,2 )$ mark for synthetic division

\(or equivalent strategy\)

1 mark for consistent product of factors

3 marks

#pagebreak()

= Question 34

Sketch at least one period of the graph of $y = - sin  lr(\( 2 lr(\( x - frac(pi ,4 )\) )\) )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/cfc7480b-f0cd-4f20-a6be-fb2697e98a6f-13_778_1469_640_330.jpg", width: 69.1%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-32_1059_1446_632_346.jpg", width: 68.0%)

1 mark for shape of a sinusoidal function with correct amplitude

1 mark for vertical reflection

1 mark for horizontal translation

1 mark for period

4 marks

#pagebreak()

= Question 35

Given $g \(x \)= log  _(2 )\(x \)- 3 $\,

a\) determine the $x $-intercept of the graph.

b\) sketch the graph of $g \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/cfc7480b-f0cd-4f20-a6be-fb2697e98a6f-14_1283_1283_1205_421.jpg", width: 60.4%)

== Solution

a\)

$   0  & = log  _(2 )\(x \)- 3  \  3  & = log  _(2 )\(x \) \  2 ^(3 ) & = x  \  x  & = 8    $

b\)



#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/c04ec89a-3da3-4596-ac07-225fd3815b99-33_1141_1091_1358_322.jpg", width: 51.3%)

1 mark

1 mark for shape of

increasing logarithmic

function with base 2

1 mark for vertical

translation

2 marks

#pagebreak()

= Question 36

Modesola incorrectly evaluated the expression\, $cos  ^(2 )lr(\( 30 ^(degree )\) )- sin  ^(2 )lr(\( 30 ^(degree )\) )$.

Modesola's answer:

$   & cos  ^(2 )lr(\( 30 ^(degree )\) )- sin  ^(2 )lr(\( 30 ^(degree )\) ) \  & = 2  cos  lr(\( 30 ^(degree )\) ) \  & = 2 lr(\( frac(sqrt(3 ),2 )\) ) \  & = sqrt(3 )   $

Describe their error.

== Solution

Modesola incorrectly applied the double angle identity. They should have written $cos  2 lr(\( 30 ^(degree )\) )$

instead of $2  cos  lr(\( 30 ^(degree )\) )$.

1 mark

#pagebreak()

= Question 37

Given the graph of $y = f \(x \)$\, state the range of $y = sqrt(f \(x \))$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jun/assets/cfc7480b-f0cd-4f20-a6be-fb2697e98a6f-16_966_975_519_575.jpg", width: 45.9%)

== Solution

$  \{ y  divides  0  <=  y  <=  1 \, y  in  bb(R )\}   $

or

$  \[0 \,1 \]  $

1 mark

#pagebreak()

= Question 38

Determine a value of $x $ that satisfies $sin  ^(2 )\(2  x - 1 \)+ cos  ^(2 )\(x + 5 \)= 1 $.

== Solution

$   2  x - 1  & = x + 5  \  x  & = 6    $

1 mark

#pagebreak()

= Question 39

Solve\, algebraically.

$9 ^(2  x + 3 )= lr(\( frac(1 ,3 )\) )^(x + 1 )$

== Solution

$   lr(\( 3 ^(2 )\) )^(2  x + 3 ) & = lr(\( 3 ^(- 1 )\) )^(x + 1 ) & & 1  " mark for changing to a common base " \  3 ^(4  x + 6 ) & = 3 ^(- x - 1 ) & & \  4  x + 6  & = - x - 1  & & 1  " mark for equating exponents with a common base " \  5  x  & = - 7  & & 2  " marks " \  x  & = - frac(7 ,5 ) & &   $

#pagebreak()

= Question 40

Determine the total number of arrangements of the letters in the word GUIDES if the vowels

and consonants must alternate.

== Solution

Method 1

$  underline(6 ) dot.c  underline(3 ) dot.c  underline(2 ) dot.c  underline(2 ) dot.c  underline(1 ) dot.c  underline(1 )= 72   $

1 mark for beginning with any letter

1 mark for alternating consonants and vowels

2 marks

Method 2

case 1: $frac(3 ,v ) dot.c  frac(3 ,c ) dot.c  frac(2 ,v ) dot.c  frac(2 ,c ) dot.c  frac(1 ,v ) dot.c  frac(1 ,c )= 36 $

case 2: $frac(3 ,c ) dot.c  frac(3 ,v ) dot.c  frac(2 ,c ) dot.c  frac(2 ,v ) dot.c  frac(1 ,c ) dot.c  frac(1 ,v )= 36 $

1 mark for alternating consonants and vowels

$frac(1 ,2 )$ mark for second case

$frac(1 ,2 )$ mark for addition of cases

2 marks

#pagebreak()

= Question 41

Solve\, algebraically.

$  frac(5 ! \(n - 5 \)! ,3 ! \(n - 6 \)! )= 80   $

== Solution

$   frac(5  dot.c  4  dot.c  3 ! \(n - 5 \)\(n - 6 \)! ,3 ! \(n - 6 \)! ) & = 80  \  20 \(n - 5 \) & = 80  \  n - 5  & = 4  \  n  & = 9    $

1 mark for factorial expansion \( $frac(1 ,2 )$ mark for each\)

$frac(1 ,2 )$ mark for simplification of factorials

$frac(1 ,2 )$ mark for solving for $n $

2 marks

#pagebreak()

= Question 42

Justify that 2.1 is a better estimate than 2.6 for the value of $log  _(5 ) 29 $.

== Solution

$  5 ^(2 )= 25   $

$  5 ^(3 )= 125   $

$  log  _(5 ) 25 = 2   $

$  log  _(5 ) 125 = 3   $

29 is closer to 25 than 125

$therefore  log  _(5 ) 29 $ is closer to 2 than 3

1 mark

#pagebreak()

= Question 43

When $p \(x \)= x ^(3 )+ k  x + 6 $ is divided by \( $x + 2 $ \)\, the remainder is 4 . Determine the value of $k $.

== Solution

Method 1

$   & 4 = \(- 2 \)^(3 )+ k \(- 2 \)+ 6  \  & 4 = - 8 - 2  k + 6  \  & 4 = - 2 - 2  k  \  & 6 = - 2  k  \  & k = - 3    $

$frac(1 ,2 )$ mark for $x = - 2 $

1 mark for remainder theorem

$frac(1 ,2 )$ mark for solving for $k $

2 marks

Method 2

$  x = - 2   $

$frac(1 ,2 )$ mark for $x = - 2 $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[-2 ], [1 ], [0 ], [k ], [6 ],
table.hline(stroke: .5pt),
[], [], [-2 ], [4 ], [$- 2  k - 8 $ ],
table.hline(stroke: .5pt),
[], [1 ], [-2 ], [$k + 4 $ ], [$- 2  k - 2 $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or equivalent strategy\)

$   - 2  k - 2  & = 4  \  - 2  k  & = 6  \  k  & = - 3    $

$frac(1 ,2 )$ mark for solving for $k $

2 marks

#pagebreak()

= Question 44

Describe the transformations used to obtain the graph of the function $y = - f \(7  x + 14 \)$

from the graph of $y = f \(x \)$.

== Solution

- reflection over the $x $-axis

- horizontal stretch by a factor of $frac(1 ,7 )$

- horizontal translation 2 units to the left

1 mark for vertical reflection

1 mark for horizontal stretch

1 mark for horizontal translation

3 marks

Note:

Deduct a maximum of 1 mark for concept error of incorrect order of horizontal transformations.