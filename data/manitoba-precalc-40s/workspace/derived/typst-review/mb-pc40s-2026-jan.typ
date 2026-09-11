#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2026-jan

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

Liam went for a ride on a Ferris wheel with a radius of 5 metres. Determine the distance he

travelled if the Ferris wheel stopped after rotating $1260 ^(degree )$.

== Solution

$   & theta = 1260 ^(degree ) dot.c  frac(pi ,180 ^(degree )) quad  1  " mark for conversion " \  & theta = 7  pi    $

or

$  theta = 21.991148  dots.h   $

$   & s = theta  r  \  & s = 7  pi \(5 \) \  & s = 35  pi  " metres " \  & " or " \  & s = 109.956  " metres "   $

1 mark for substitution

2 marks

#pagebreak()

= Question 2

Determine and simplify the term that contains $x ^(12 )$ in the binomial expansion of $lr(\( 2  x ^(4 )- 3 \) )^(7 )$.

== Solution

Method 1

$   & lr(\( x ^(4 )\) )^(7 )\,lr(\( x ^(4 )\) )^(6 )\,lr(\( x ^(4 )\) )^(5 )\, dots.h  \  & x ^(28 )\, x ^(24 )\, x ^(20 )\, dots.h  \  t _(5 )=  &  "" _(7 ) C _(4 )lr(\( 2  x ^(4 )\) )^(3 )\(- 3 \)^(4 ) \  =  & 22680  x ^(12 )   $

1 mark for determining a pattern

2 marks \( 1 mark for $ "" _(7 ) C _(4 ) \; frac(1 ,2 )$ mark for each consistent factor\)

1 mark for simplification \( $frac(1 ,2 )$ mark for coefficient\, $frac(1 ,2 )$ mark

for exponent\)

4 marks

Method 2

$   x ^(12 ) & = lr(\( x ^(4 )\) )^(7 - k )lr(\( x ^(0 )\) )^(k ) \  12  & = 28 - 4  k  \  - 16  & = - 4  k  \  4  & = k  \  t _(5 ) & =  "" _(7 ) C _(4 )lr(\( 2  x ^(4 )\) )^(3 )\(- 3 \)^(4 ) \  & = 22680  x ^(12 )   $

$frac(1 ,2 )$ mark for substitution

$frac(1 ,2 )$ mark for solving for $k $

2 marks \( 1 mark for $ "" _(7 ) C _(4 ) \; frac(1 ,2 )$ mark for each consistent factor\)

1 mark for simplification \( $frac(1 ,2 )$ mark for coefficient\, $frac(1 ,2 )$ mark

for exponent\)

4 marks

#pagebreak()

= Question 3

The normal healing of wounds can be modeled by an exponential function. The area of the

wound decreases according to the formula\,

$  A = A _(0 ) e ^(- 0.35  t )  $

where: $A $ is the area of the wound in $upright(c m )^(2 )$\, after $t $ days\,

$A _(0 )$ is the initial area of the wound in $upright(c m )^(2 )$\, and

$t $ is the time\, in days\, after healing begins.

If a wound has an initial area of $25  upright(space.nobreak c m )^(2 )$\, determine:

a\) the area of the wound after 3 days.

b\) the amount of time it will take for the area of the wound to decrease to $4  upright(space.nobreak c m )^(2 )$.

== Solution

a\)

$   & A = 25  e ^(- 0.35 \(3 \)) \  & A = 8.748  upright(space.nobreak c m )^(2 )   $

1 mark

b\)

$  mat(delim: #none,  4  "" , = 25  e ^(- 0.35  t ) "" , "" , "" ; 0.16  "" , = e ^(- 0.35  t ) "" , "" , "" ; ln  0.16  "" , = ln  e ^(- 0.35  t ) "" , "" , 1  " mark for applying logarithms " "" ; ln  0.16  "" , = - 0.35  t  ln  e  "" , "" , 1  \/ 2  " mark for power law " "" ; frac(ln  0.16 ,- 0.35 ) "" , = t  "" , "" , "" ; t  "" , = 5.235947  dots.h  "" , "" , "" ; t  "" , = 5.236  " days " "" , 1  \/ 2  " mark for the value of " t  )  $

2 marks

#pagebreak()

= Question 4

During a hockey practice\, 4 players are wearing a green jersey and 5 players are wearing a red

jersey. Determine the number of ways three players can be selected if at least two of the players

must be wearing a red jersey.

== Solution

Case 1: $ "" _(5 ) C _(2 ) dot.c  "" _(4 ) C _(1 )= 40 $

1 mark for Case 1

Case 2: $ "" _(5 ) C _(3 ) dot.c  "" _(4 ) C _(0 )= 10 $

1 mark for Case 2

$40 + 10 = 50 $ ways

1 mark for addition of cases

3 marks

Note:

$ "" _(4 ) C _(0 )$ does not need to be shown.

#pagebreak()

= Question 5

Solve\, algebraically\, over the interval $\[0 \,2  pi \]$.

$  2  sin  ^(2 ) x + 5  cos  x + 1 = 0   $

== Solution

$  mat(delim: #none,  2 lr(\( 1 - cos  ^(2 ) x \) )+ 5  cos  x + 1 = 0  "" ; 2 - 2  cos  ^(2 ) x + 5  cos  x + 1 = 0  "" ; - 2  cos  ^(2 ) x + 5  cos  x + 3 = 0  "" ; 2  cos  ^(2 ) x - 5  cos  x - 3 = 0  "" ; \(2  cos  x + 1 \)\(cos  x - 3 \)= 0  "" ; cos  x = - frac(1 ,2 ) quad  cos  x = 3  "" ; x = frac(2  pi ,3 )\, frac(4  pi ,3 ) quad  " no solution " )  $

1 mark for substitution of an appropriate identity

1 mark for solving for $cos  x $

2 marks for solving for $x $ \( $frac(1 ,2 )$ mark for each value\; 1 mark

for indicating no solution\)

4 marks

#pagebreak()

= Question 6

The function\, $y = f \(x \)$\, has a domain of $\[- 8 \,4 \]$. The domain of the graph of $y = f \(b  x \)$ is $\[- 4 \,2 \]$.

State the value of $b $.

== Solution

$b = 2 $

1 mark

#pagebreak()

= Question 7

Describe the difference between the graph of $f \(x \)= frac(\(x + 3 \)\(x - 4 \),\(x + 3 \))$ and the graph of $g \(x \)= x - 4 $.

== Solution

The graph of $f \(x \)$ has a point of discontinuity at $x = - 3 $\, where as the graph of $g \(x \)$ does not.

1 mark

#pagebreak()

= Question 8

Determine if the point $lr(\( - frac(3 ,5 )\, frac(2 ,sqrt(3 ))\) )$ is on the unit circle. Justify your answer.

== Solution

Method 1

$  x ^(2 )+ y ^(2 )= 1   $

$   " Left-Hand Side " & = lr(\( - frac(3 ,5 )\) )^(2 )+ lr(\( frac(2 ,sqrt(3 ))\) )^(2 ) \  & = frac(9 ,25 )+ frac(4 ,3 ) \  & = frac(27 ,75 )+ frac(100 ,75 )   $

$frac(127 ,75 ) !=  1 $

Therefore the point $lr(\( - frac(3 ,5 )\, frac(2 ,sqrt(3 ))\) )$ is not on the unit circle.

1 mark for justification

1 mark

Method 2

Since $frac(2 ,sqrt(3 ))> 1 $\, the point is not on the unit circle.

1 mark for justification

1 mark

#pagebreak()

= Question 9

Given the graph of $f \(x \)$\, sketch the graph of $g \(x \)= f \(- \(x - 1 \)\)+ 3 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/bc379c80-2403-4957-bb62-c70c91fc0848-09_854_858_552_507.jpg", width: 40.4%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/bc379c80-2403-4957-bb62-c70c91fc0848-09_864_853_1463_507.jpg", width: 40.1%)

The graph of $f \(x \)$

has already been

drawn for your

reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-09_812_808_589_247.jpg", width: 38.0%)

1 mark for horizontal reflection

1 mark for horizontal translation

1 mark for vertical translation

3 marks

#pagebreak()

= Question 10

Bonnie was asked to determine the factors of $p \(x \)= - 3  x ^(4 )+ 2  x ^(2 )- 4  x + 5 $.

Describe the error she made in her set up of synthetic division.

$1 lr(floor.l  mat(delim: #none, - 3  "" , 2  "" , - 4  "" , 5 ) )$

== Solution

Bonnie did not write the coefficient of 0 for the missing term\, $x ^(3 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-10_159_307_1044_247.jpg", width: 14.4%)

#pagebreak()

= Question 11

Given the functions\, $f \(x \)= frac(1 ,x - 1 )$ and $g \(x \)= x - 3 $\,

a\) state the equation of $f \(g \(x \)\)$.

$f \(g \(x \)\)= $

$\_ \_ \_ \_ $

b\) state the domain of $f \(g \(x \)\)$.

Domain:

$\_ \_ \_ \_ $

== Solution

a\) $f \(g \(x \)\)= frac(frac(1 ,x - 4 ),"" )$

1 mark

b\) Domain:

$\_ \_ \_ \_ $

$\{ x  divides  x  !=  4 \, x  in  bb(R )\} $

or

Domain:

$\_ \_ \_ \_ $

#pagebreak()

= Question 12

Prove the identity for all permissible values of $x $.

$  tan  2  x = frac(2 ,cot  x - tan  x )  $

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
[$tan  2  x $ ], [$frac(2 ,frac(cos  x ,sin  x )- frac(sin  x ,cos  x ))$ ],
table.hline(stroke: .5pt),
[], [$frac(2 ,frac(cos  ^(2 ) x - sin  ^(2 ) x ,sin  x  cos  x ))$ ],
table.hline(stroke: .5pt),
[], [$frac(2  sin  x  cos  x ,cos  ^(2 ) x - sin  ^(2 ) x )$ ],
table.hline(stroke: .5pt),
[], [$frac(sin  2  x ,cos  2  x )$ ],
table.hline(stroke: .5pt),
[], [$tan  2  x $ ],
table.hline(stroke: .5pt),
[],
);

1 mark for correct substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 13

Given $f \(x \)= - x ^(2 )+ 2 $ and $g \(x \)= x ^(2 )- 1 $\,

a\) determine the equation of $h \(x \)= g \(x \)- f \(x \)$.

$h \(x \)= $

$\_ \_ \_ \_ $

b\) state the range of $h \(x \)$.

Range:

$\_ \_ \_ \_ $

== Solution

a\) $h \(x \)= g \(x \)- f \(x \)$

$   & h \(x \)= lr(\( x ^(2 )- 1 \) )- lr(\( - x ^(2 )+ 2 \) ) \  & h \(x \)= x ^(2 )- 1 + x ^(2 )- 2  \  & h \(x \)= 2  x ^(2 )- 3    $

b\) Range:

$\{ y  divides  y  >= - 3 \, y  in  bb(R )\} $

$\_ \_ \_ \_ $

or

Range:

$\[- 3 \, oo \)$

$\_ \_ \_ \_ $

1 mark for subtraction of $g \(x \)- f \(x \)$

1 mark

1 mark for range consistent with $h \(x \)$

1 mark

#pagebreak()

= Question 14

Given the graph of $f \(x \)$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/bc379c80-2403-4957-bb62-c70c91fc0848-14_639_637_526_743.jpg", width: 30.0%)

a\) sketch the graph after a reflection over the line $y = x $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/bc379c80-2403-4957-bb62-c70c91fc0848-14_642_639_1314_743.jpg", width: 30.1%)

The graph of $f \(x \)$

has already been

drawn for your

reference.

No marks will be

awarded for the

graph of $f \(x \)$.

b\) state a restriction on the domain of $f \(x \)$ in order for its inverse to be a function.

== Solution

a\)



#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-16_634_629_1390_292.jpg", width: 29.6%)

1 mark

b\) $\{ x  divides  x  >= - 2 \, x  in  bb(R )\} $

or

$\{ x  divides  x  <= - 2 \, x  in  bb(R )\} $

1 mark

Note:

Other answers are possible for b\).

#pagebreak()

= Question 15

Describe a transformation of a function that would not affect its domain.

== Solution

vertical stretch by a factor of $a $

or

vertical reflection

or

vertical translation $k $ units up\/down

1 mark

#pagebreak()

= Question 16

Given the graph of $f \(x \)$\, sketch the graph of the function $y = | f \(x \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/bc379c80-2403-4957-bb62-c70c91fc0848-16_878_875_545_556.jpg", width: 41.2%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/bc379c80-2403-4957-bb62-c70c91fc0848-16_873_871_1437_558.jpg", width: 41.0%)

The graph of $f \(x \)$

has already been

drawn for your

reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-18_859_853_589_247.jpg", width: 40.1%)

1 mark

#pagebreak()

= Question 17

Determine\, algebraically\, all of the zeros of the polynomial function\, $p \(x \)= 3  x ^(3 )+ x ^(2 )- 20  x + 12 $.

== Solution

$   & p \(x \)= 3  x ^(3 )+ x ^(2 )- 20  x + 12  \  & p \(2 \)= 3 \(2 \)^(3 )+ \(2 \)^(2 )- 20 \(2 \)+ 12  \  & p \(2 \)= 0  \  & therefore \(x - 2 \) " is a factor "   $

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[2 ], [3 ], [1 ], [-20 ], [12 ],
table.hline(stroke: .5pt),
[], [], [6 ], [14 ], [-12 ],
table.hline(stroke: .5pt),
[], [3 ], [7 ], [-6 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or equivalent strategy\)

$   p \(x \)= \(x - 2 \)lr(\( 3  x ^(2 )+ 7  x - 6 \) ) \  0 = \(x - 2 \)\(3  x - 2 \)\(x + 3 \) \  x = 2 \, quad  x = frac(2 ,3 )\, quad  x = - 3    $

$frac(1 ,2 )$ mark for consistent factors

$frac(1 ,2 )$ mark for consistent zeros

3 marks

#pagebreak()

= Question 18

Given $theta = 240 ^(degree )$\, identify the coordinates of the point\, $P \(theta \)$\, on the unit circle.

*A.*

$lr(\( - frac(sqrt(3 ),2 )\,- frac(1 ,2 )\) )$

*B.*

$lr(\( - frac(sqrt(2 ),2 )\,- frac(sqrt(2 ),2 )\) )$

*C.*

$lr(\( - frac(1 ,2 )\,- frac(sqrt(3 ),2 )\) )$

*D.*

$lr(\( frac(1 ,2 )\,- frac(sqrt(3 ),2 )\) )$

== Solution

Correct answer: C

$lr(\( - frac(1 ,2 )\,- frac(sqrt(3 ),2 )\) )$

#pagebreak()

= Question 19

Given the functions\, $f \(x \)= - 3  x + 5 $ and $g \(x \)= x ^(2 )+ x - 1 $\, identify the value of $g \(f \(2 \)\)$.

*A.*

-10

*B.*

-5

*C.*

-3

*D.*

-1

== Solution

Correct answer: D

-1

#pagebreak()

= Question 20

Given $f \(x \)= sqrt(x )+ 5 $\, identify the equation of the transformed graph that has the same

$y $-intercept.

*A.*

$quad  y = f \(x - 3 \)$

*B.*

$quad  y = - 3  f \(x \)$

*C.*

$y = f \(- 3  x \)$

*D.*

$y = f \(x \)- 3 $

== Solution

Correct answer: C

$y = f \(- 3  x \)$

#pagebreak()

= Question 21

Given the graph of $p \(x \)= a  x ^(3 )+ b  x ^(2 )+ c  x + d $\, identify the statement that is true.

*A.*

$quad  a > 0 \, d < 0 $

*B.*

$quad  a > 0 \, d > 0 $

*C.*

$quad  a < 0 \, d < 0 $

*D.*

$a < 0 \, d > 0 $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-02_429_476_1237_936.jpg", width: 22.4%)

== Solution

Correct answer: A

$quad  a > 0 \, d < 0 $

#pagebreak()

= Question 22

Identify the general solution of the equation\, $csc  theta = - 1 $.

*A.*

$quad  theta = frac(pi ,2 )+ k  pi \, k  in  bb(Z )$

*B.*

$quad  theta = frac(3  pi ,2 )+ 2  k  pi \, k  in  bb(Z )$

*C.*

$quad  theta = frac(3  pi ,2 )+ k  pi \, k  in  bb(Z )$

*D.*

$theta = pi + 2  k  pi \, k  in  bb(Z )$

== Solution

Correct answer: B

$quad  theta = frac(3  pi ,2 )+ 2  k  pi \, k  in  bb(Z )$

#pagebreak()

= Question 23

Identify the equation of a radical function with a domain of $\[- 6 \, oo \)$ and a range of $\(- oo \, 3 \]$.

*A.*

$y = - sqrt(x + 6 )- 3 $

*B.*

$y = - sqrt(x + 6 )+ 3 $

*C.*

$y = sqrt(- \(x + 3 \))- 6 $

*D.*

$y = sqrt(x - 6 )+ 3 $

== Solution

Correct answer: B

$y = - sqrt(x + 6 )+ 3 $

#pagebreak()

= Question 24

1 mark

Identify the value of $n $ in the equation\, $ "" _(n ) C _(3 )=  "" _(n ) C _(7 )$.

*A.*

3

*B.*

4

*C.*

7

*D.*

10

== Solution

Correct answer: D

10

#pagebreak()

= Question 25

Identify the remainder when $p \(x \)= x ^(5 )- 1 $ is divided by $\(x + 1 \)$.

*A.*

-2

*B.*

-1

*C.*

0

*D.*

4

== Solution

Correct answer: A

-2

#pagebreak()

= Question 26

Match each function with its corresponding graph.

Write the corresponding letter in this column.

$   & y = sqrt(x )- 3  \  & y = sqrt(- x )+ 3  \  & y = - sqrt(x + 3 ) \  & y = - sqrt(- \(x - 3 \))   $

A\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-04_634_633_1044_367.jpg", width: 29.8%)

B\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-04_634_637_1044_1248.jpg", width: 30.0%)

C\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-04_633_633_1789_367.jpg", width: 29.8%)

D\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-04_633_635_1789_1250.jpg", width: 29.9%)

== Solution

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

C

$\_ \_ \_ \_ $

$\_ \_ \_ \_ $

$frac(1 ,2 )$ mark for each correct answer

2 marks

A\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-23_627_627_1130_367.jpg", width: 29.5%)

B\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-23_632_627_1126_1253.jpg", width: 29.5%)

C\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-23_629_629_1803_367.jpg", width: 29.6%)

D\)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-23_629_629_1790_1253.jpg", width: 29.6%)

#pagebreak()

= Question 27

The amplitude\, $A $\, of the sinusoidal function can be determined using the equation $A = 20 - n $.

State the values of $m $ and $n $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-05_940_1015_541_571.jpg", width: 47.8%)

== Solution

$m = frac(2  pi ,3 )$

$n = 5 $

1 mark for value of $m $

1 mark for value of $n $

2 marks

#pagebreak()

= Question 28

Solve\, algebraically.

$   "" _(n - 1 ) P _(2 )= 20   $

== Solution

$   frac(\(n - 1 \)! ,\(n - 1 - 2 \)! ) & = 20  \  frac(\(n - 1 \)! ,\(n - 3 \)! ) & = 20  \  frac(\(n - 1 \)\(n - 2 \)\(n - 3 \)! ,\(n - 3 \)! ) & = 20  \  n ^(2 )- 3  n + 2  & = 20  \  n ^(2 )- 3  n - 18  & = 0  \  \(n - 6 \)\(n + 3 \) & = 0  \  n = 6  quad  n >  & = - 3    $

$frac(1 ,2 )$ mark for substitution

1 mark for factorial expansion

$frac(1 ,2 )$ mark for simplification of factorials

$frac(1 ,2 )$ mark for the permissible value of $n $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

3 marks

#pagebreak()

= Question 29

Determine the exact value of $sin  lr(\( frac(23  pi ,12 )\) )$.

== Solution

$   sin  lr(\( frac(23  pi ,12 )\) ) & = sin  lr(\( frac(21  pi ,12 )+ frac(2  pi ,12 )\) ) \  sin  lr(\( frac(7  pi ,4 )+ frac(pi ,6 )\) ) & = sin  lr(\( frac(7  pi ,4 )\) ) cos  lr(\( frac(pi ,6 )\) )+ cos  lr(\( frac(7  pi ,4 )\) ) sin  lr(\( frac(pi ,6 )\) ) \  & = lr(\( - frac(sqrt(2 ),2 )\) )lr(\( frac(sqrt(3 ),2 )\) )+ lr(\( frac(sqrt(2 ),2 )\) )lr(\( frac(1 ,2 )\) ) \  & = frac(- sqrt(6 )+ sqrt(2 ),4 )   $

1 mark for substitution into correct identity

2 marks for exact values \( $frac(1 ,2 )$ mark for each\)

3 marks

Note:

Other combinations are possible.

#pagebreak()

= Question 30

Cameron was asked to solve the equation\, $log  _(3 )\(x - 4 \)= 2 $.

Cameron's solution:

$   x - 4  & = 2 ^(3 ) \  x - 4  & = 8  \  x  & = 12    $

Describe Cameron's error.

== Solution

Cameron mixed up the exponent and the base when changing to exponential form.

1 mark

#pagebreak()

= Question 31

Given the identity $sin  ^(2 ) theta = frac(tan  theta  sin  theta ,sec  theta )$\, state the non-permissible value of $theta $ over the

interval $\[pi \, 2  pi \]$.

== Solution

$cos  theta = 0 $

$theta = frac(3  pi ,2 )$

1 mark

#pagebreak()

= Question 32

Sketch the graph of $y = - 5  cos  lr(\( frac(pi ,2 ) x \) )+ 2 $ over the domain $\[0 \,5 \]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-10_1305_1353_608_414.jpg", width: 63.7%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-29_788_795_587_243.jpg", width: 37.4%)

1 mark for shape of a sinusoidal function with correct amplitude

1 mark for vertical reflection

1 mark for vertical translation

1 mark for period

4 marks

#pagebreak()

= Question 33

Describe the behaviour of the graph of the polynomial function\, $p \(x \)= \(x - 3 \)^(2 )\(x - 1 \)$\, as it

approaches the $x $-intercept at $x = 3 $.

== Solution

As it approaches $x = 3 $\, the graph touches but does not cross the $x $-axis.

1 mark

#pagebreak()

= Question 34

Sketch the angle of 4 radians in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-12_879_921_610_590.jpg", width: 43.3%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-31_825_866_569_243.jpg", width: 40.8%)

$frac(1 ,2 )$ mark for an appropriate angle

in quadrant III

$frac(1 ,2 )$ mark for the correct direction of an

angle in standard position

1 mark

#pagebreak()

= Question 35

Solve\, algebraically.

$  log  _(5 ) 12 + 2  log  _(5 ) x = log  _(5 ) 48   $

== Solution

Method 1

$  mat(delim: #none,  log  _(5 ) 12 + 2  log  _(5 ) x  "" , = log  _(5 ) 48  "" ; log  _(5 ) 12 + log  _(5 ) x ^(2 ) "" , = log  _(5 ) 48  "" ; log  _(5 ) 12  x ^(2 ) "" , = log  _(5 ) 48  "" ; 12  x ^(2 ) "" , = 48  "" ; x ^(2 ) "" , = 4  "" ; x = 2  "" , x < - 2  )  $

$frac(1 ,2 )$ mark for permissible value of $x $

$frac(1 ,2 )$ mark for showing the rejection of the extraneous root

4 marks

Method 2

$   log  _(5 ) 12 + 2  log  _(5 ) x  & = log  _(5 ) 48  & & \  log  _(5 ) 12 + log  _(5 ) x ^(2 )- log  _(5 ) 48  & = 0  & & 1  " mark for power law " \  log  _(5 )lr(\( frac(12  x ^(2 ),48 )\) ) & = 0  & & mat(delim: #none,  1  \/ 2  " mark for product law " "" ; 1  \/ 2  " mark for quotient law " ) \  frac(12  x ^(2 ),48 ) & = 5 ^(0 ) & & 1  " mark for exponential form " \  x ^(2 ) & = 4  & &   $

4 marks

#pagebreak()

= Question 36

State the equation of the exponential function represented by the graph of $f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-14_968_978_517_539.jpg", width: 46.0%)

$f \(x \)= $

$\_ \_ \_ \_ $

== Solution

$f \(x \)= 2 ^(x )+ 3 $

1 mark for exponential function with a base of 2

1 mark for vertical translation

2 marks

#pagebreak()

= Question 37

Evaluate.

$  cos  lr(\( frac(11  pi ,3 )\) )+ csc  lr(\( - frac(pi ,3 )\) ) cot  lr(\( frac(11  pi ,6 )\) )  $

== Solution

$lr(\( frac(1 ,2 )\) )+ lr(\( - frac(2 ,sqrt(3 ))\) )lr(\( - frac(sqrt(3 ),1 )\) )$

$frac(1 ,2 )+ 2 $

$frac(5 ,2 )$

1 mark for $cos  lr(\( frac(11  pi ,3 )\) )lr(\( 1  \/ 2  )$ mark for value\; $frac(1 ,2 )$ mark for quadrant $\)$

1 mark for $csc  lr(\( - frac(pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for value\; $frac(1 ,2 )$ mark for quadrant $\)$

1 mark for $cot  lr(\( frac(11  pi ,6 )\) )lr(\( 1  \/ 2  )$ mark for value\; $frac(1 ,2 )$ mark for quadrant \)

3 marks

#pagebreak()

= Question 38

Min Li has a 3-digit code for his lock. Determine the number of possible codes for his lock\, if

repetition is allowed.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-16_714_790_571_577.jpg", width: 37.2%)

== Solution

$  10  dot.c  underline(10 ) dot.c  underline(10 )= 1000   $

1 mark

#pagebreak()

= Question 39

Solve\, algebraically.

$  lr(\( frac(1 ,6 )\) )^(3  x + 2 )= 6 ^(2  x )  $

== Solution

$   lr(\( 6 ^(- 1 )\) )^(3  x + 2 ) & = 6 ^(2  x ) \  6 ^(- 3  x - 2 ) & = 6 ^(2  x ) \  - 3  x - 2  & = 2  x  \  - 5  x  & = 2  \  x  & = - frac(2 ,5 )   $

1 mark for changing to a common base

1 mark for equating exponents

2 marks

#pagebreak()

= Question 40

Sketch the graph of $f \(x \)= frac(5 ,\(x - 1 \)\(x + 3 \))$ and state the $y $-intercept.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-18_996_998_575_586.jpg", width: 47.0%)

$y $-intercept:

$\_ \_ \_ \_ $

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-37_1044_1087_584_468.jpg", width: 51.2%)

$lr(\( 0 \,- frac(5 ,3 )\) )$

$\_ \_ \_ \_ $

1 mark for vertical asymptotic behaviour

\( $frac(1 ,2 )$ mark for behaviour approaching $x = - 3  \; frac(1 ,2 )$ mark for behaviour approaching $x = 1 $ \)

1 mark for horizontal asymptotic behaviour approaching $y = 0 $

$1  frac(1 ,2 )$ marks for shape \( $frac(1 ,2 )$ mark for shape of each branch\)

$frac(1 ,2 )$ mark for $y $-intercept

4 marks

#pagebreak()

= Question 41

Given $log  _(2 ) x = 5 $\, determine the value of $log  _(4 )\(2  x \)$.

== Solution

$  mat(delim: #none,  x = 2 ^(5 ) "" , 1  " mark for solving for " x  "" ; x = 32  "" , )  $

$   log  _(4 )\(2 \(32 \)\) \  log  _(4 )\(64 \)   $

3

1 mark for evaluating the logarithm

2 marks

#pagebreak()

= Question 42

Henry was asked to prove the identity\, $csc  ^(2 ) theta - 2  cos  ^(2 ) theta + 1 = cot  ^(2 ) theta + 2  sin  ^(2 ) theta $\, for all permissible

values of $theta $.

His work:

#table(stroke: none,
columns: 2,
align: (center, center, ),
table.vline(stroke: .5pt, x: 1),
[], [Left-Hand side ],
table.hline(stroke: .5pt),
[$csc  ^(2 )lr(\( frac(pi ,4 )\) )- 2  cos  ^(2 )lr(\( frac(pi ,4 )\) )+ 1 $ ], [$cot  ^(2 )lr(\( frac(pi ,4 )\) )+ 2  sin  ^(2 )lr(\( frac(pi ,4 )\) )$ ],
[$\(sqrt(2 )\)^(2 )- 2 lr(\( frac(sqrt(2 ),2 )\) )^(2 )+ 1 $ ], [$\(1 \)^(2 )+ 2 lr(\( frac(sqrt(2 ),2 )\) )^(2 )$ ],
[$2 - 1 + 1 $ ], [$1 + 1 $ ],
[2 ], [2 ],
[LHS ], [RHS ✓ ],
);

Explain why his proof is insufficient.

== Solution

Henry proved the identity for $theta = frac(pi ,4 )$\, but not for all permissible values of $theta $.

1 mark

#pagebreak()

= Question 43

Sketch the graph of $y - 2 = - sqrt(x - 1 )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-21_988_992_620_588.jpg", width: 46.7%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/178076f7-0138-4ae9-baaf-5759b1afa911-40_965_967_574_258.jpg", width: 45.5%)

1 mark for shape of a radical function

1 mark for vertical reflection

1 mark for horizontal translation

1 mark for vertical translation

4 marks

#pagebreak()

= Question 44

Evaluate.

$log  _(3 ) 54 - log  _(3 ) 6 $

== Solution

$log  _(3 )lr(\( frac(54 ,6 )\) )$

$log  _(3 ) 9 $

2

1 mark for quotient law

1 mark for evaluating the logarithm

2 marks

#pagebreak()

= Question 45

Determine\, algebraically\, the equation of the graph of the polynomial function\, $p \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2026-jan/assets/e945c5f5-8e34-4839-8fe8-013766e26b7b-23_807_819_627_580.jpg", width: 38.5%)

$p \(x \)= $

$\_ \_ \_ \_ $

== Solution

$p \(x \)= a \(x - 1 \)^(3 )\(x + 3 \)\(x - 4 \)$

$p \(0 \)= a \(0 - 1 \)^(3 )\(0 + 3 \)\(0 - 4 \)$

$   & 6 = a \(- 1 \)^(3 )\(3 \)\(- 4 \) \  & 6 = 12  a  \  & frac(1 ,2 )= a    $

$p \(x \)= frac(1 ,2 )\(x - 1 \)^(3 )\(x + 3 \)\(x - 4 \)$

$frac(1 ,2 )$ mark for factors of $p \(x \)$

$frac(1 ,2 )$ mark for multiplicity of 3 at $x = 1 $

1 mark for consistent value of $a $

2 marks