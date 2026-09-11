#set page(paper: "a4", margin: 15mm)

#set text(size: 10pt)

= mb-pc40s-2024-jun

Typst conversion review. OCR content and mathematical accuracy require editorial review.

#pagebreak()

= Question 1

A soccer team consists of 14 players. Determine the number of ways a captain and an assistant

captain can be selected.

== Solution

$   "" _(14 ) P _(2 )= 182   $

1 mark

or

$  underline(14 ) dot.c  underline(13 )= 182   $

#pagebreak()

= Question 2

The pH of a person's blood can be found using the formula

$  upright(p H )= 6.1 + log  lr(\( frac(B ,C )\) )  $

where $B $ represents the concentration of bicarbonate in the blood\, in mEq\/L

$C $ represents the concentration of carbonic acid in the blood\, in $upright(m E q ) \/ upright(L )$

Kansas has a blood pH of 7.41. In her blood sample\, the concentration of carbonic acid is $1.41  upright(m E q ) \/ upright(L )$.

Determine the concentration of bicarbonate in her blood.

Express the answer correct to one decimal place.

== Solution

Method 1

$  mat(delim: #none,  7.41 = 6.1 + log  lr(\( frac(B ,1.41 )\) ) "" , 1  \/ 2  " mark for substitution " "" ; 1.31 = log  lr(\( frac(B ,1.41 )\) ) "" , "" ; 10 ^(1.31 )= frac(B ,1.41 ) "" , 1  " mark for exponential form " "" ; B = 28.788505  dots.h  "" , "" ; B = 28.8  upright(m E q ) \/ upright(L ) "" , 1  \/ 2  " mark for solving for " B  )  $

2 marks

Method 2

$  mat(delim: #none,  7.41 = 6.1 + log  lr(\( frac(B ,1.41 )\) ) "" , 1  \/ 2  " mark for substitution " "" ; 1.31 = log  lr(\( frac(B ,1.41 )\) ) "" , "" ; 1.31 = log  B - log  1.41  "" , 1  " mark for quotient law " "" ; 1.31 + log  1.41 = log  B  "" , "" ; 1.4592  dots.h = log  B  "" , "" ; B = 28.788505  dots.h  "" , "" ; B = 28.8  upright(m E q ) \/ upright(L ) "" , 1  \/ 2  " mark for solving for " B  "" ; "" , 2  " marks " )  $

#pagebreak()

= Question 3

Solve $\(2  tan  x - 1 \)\(tan  x + 1 \)= 0 $ where $x  in  bb(R )$.

== Solution

Method 1

$  mat(delim: #none,  2  tan  x - 1 = 0  "" , tan  x + 1 = 0  "" ; tan  x = frac(1 ,2 ) "" , tan  x = - 1  "" ; x _(r )= 0.463647  dots.h  "" , )  $

$  x = frac(7  pi ,4 )  $

2 marks for solving for $x $ \( $frac(1 ,2 )$ mark for each value\)

$  lr( mat(delim: #none,  x = 0.464 + 2  k  pi  "" ; x = 3.605 + 2  k  pi  "" ; x = frac(3  pi ,4 )+ 2  k  pi  "" ; x = frac(7  pi ,4 )+ 2  k  pi  )\} ) k  in  bb(Z )  $

1 mark for general solution

3 marks

Method 2

$  lr( mat(delim: #none,  tan  x = frac(1 ,2 ) "" , tan  x = - 1  "" ; x _(r )= 0.463647  dots.h  "" , x = frac(3  pi ,4 ) "" ; x = 0.464  "" , "" ; x = 0.464 + k  pi  "" ; x = frac(3  pi ,4 )+ k  pi  )\} ) k  in  bb(Z ) quad  " "  $

2 marks for solving for $x $ \(1 mark for each branch\)

1 mark for general solution

3 marks

#pagebreak()

= Question 4

Determine and simplify the 7 th term in the binomial expansion of $lr(\( frac(2 ,x ^(2 ))+ 3  x \) )^(9 )$.

== Solution

$   t _(7 ) & =  "" _(9 ) C _(6 )lr(\( frac(2 ,x ^(2 ))\) )^(3 )\(3  x \)^(6 ) \  & = 84 lr(\( frac(8 ,x ^(6 ))\) )lr(\( 729  x ^(6 )\) ) \  & = 489888    $

3 marks

#pagebreak()

= Question 5

A winch\, with a diameter of 14 cm \, is used to pull a boat out of the water. As the winch rotates\, it

pulls in a cable. Determine the length of cable that is pulled in if the winch rotates $526 ^(degree )$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-05_614_596_575_730.jpg", width: 28.0%)

== Solution

$   & theta = \(526 \)lr(\( frac(pi ,180 )\) ) quad  1  " mark for conversion " \  & theta = frac(263  pi ,90 ) \  & theta = 9.180431  dots.h    $

$   s  & = theta  r  \  s  & = lr(\( frac(263  pi ,90 )\) )\(7 \) quad  1  " mark for substitution " \  s  & = frac(1841  pi ,90 ) upright(space.nobreak c m ) quad  2  " marks " \  " or " & \  s  & = 64.263  upright(space.nobreak c m )   $

#pagebreak()

= Question 6

Sketch the graph of $f \(x \)= sqrt(frac(1 ,3 ) x )- 1 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-06_882_866_569_610.jpg", width: 40.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-06_874_855_617_245.jpg", width: 40.2%)

1 mark for shape of a radical function

1 mark for horizontal stretch

1 mark for vertical translation

3 marks

#pagebreak()

= Question 7

Given $y = f \(x \)$\, determine the equation of the resulting function\, $g \(x \)$\, after the following

transformations:

- reflection over the $y $-axis

- vertical stretch by a factor of 3

- horizontal translation 2 units left

$g \(x \)= $

== Solution

$  g \(x \)= 3  f \(- \(x + 2 \)\)  $

1 mark for horizontal reflection

1 mark for vertical stretch

1 mark for horizontal translation

3 marks

#pagebreak()

= Question 8

Explain why the graph of $y = frac(6  x + 7 ,3  x + 5 )$ has a horizontal asymptote at $y = 2 $.

== Solution

When the degree of the numerator and the denominator are the same\, the horizontal asymptote is

$y = frac(a ,b )$ where $a $ is the leading coefficient in the numerator and $b $ is the leading coefficient in the

denominator.

#pagebreak()

= Question 9

Given the graph of $y = f \(x \)$\, sketch the graph of $y = - sqrt(f \(x \))+ 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-09_878_879_519_610.jpg", width: 41.4%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-09_880_866_1516_610.jpg", width: 40.8%)

The graph of

$f \(x \)$ has already

been drawn for

your reference.

No marks will be

awarded for the

graph of $f \(x \)$.

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-09_862_851_591_245.jpg", width: 40.0%)

1 mark for shape of $sqrt(f \(x \))$

1 mark for vertical reflection

1 mark for vertical translation

3 marks

#pagebreak()

= Question 10

Using the laws of logarithms\, completely expand the given expression.

$  log  lr(\( frac(A ,root(3 ,B ) dot.c  C ^(4 ))\) )  $

== Solution

$log  A - frac(1 ,3 ) log  B - 4  log  C $

1 mark for product law

1 mark for power law \( $frac(1 ,2 )$ mark for each\)

1 mark for quotient law

3 marks

#pagebreak()

= Question 11

Prove the following identity for all permissible values of $theta $.

$  cot  theta - tan  theta = frac(2  cos  2  theta ,sin  2  theta )  $

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

1 mark for substitution of appropriate identities

1 mark for algebraic strategies

1 mark for logical process to prove the identity

3 marks

#pagebreak()

= Question 12

Express $p \(x \)= - 2  x ^(3 )+ x ^(2 )+ 13  x + 6 $ in completely factored form.

$  p \(x \)=   $

== Solution

$   & p \(- 2 \)= - 2 \(- 2 \)^(3 )+ \(- 2 \)^(2 )+ 13 \(- 2 \)+ 6  \  & p \(- 2 \)= - 2 \(- 8 \)+ 4 - 26 + 6  \  & p \(- 2 \)= 0  \  & therefore \(x + 2 \) " is a factor. "   $

1 mark for identifying one zero of $p \(x \)$

#table(stroke: none,
columns: 5,
align: (left, left, left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3), table.vline(stroke: .5pt, x: 4), table.vline(stroke: .5pt, x: 5),
table.hline(stroke: .5pt),
[-2 ], [-2 ], [1 ], [13 ], [6 ],
table.hline(stroke: .5pt),
[], [↓ ], [4 ], [-10 ], [-6 ],
table.hline(stroke: .5pt),
[], [-2 ], [5 ], [3 ], [0 ],
table.hline(stroke: .5pt),
[],
);

1 mark for synthetic division \(or any equivalent

strategy\)

$   & p \(x \)= \(x + 2 \)lr(\( - 2  x ^(2 )+ 5  x + 3 \) ) \  & p \(x \)= - \(x + 2 \)lr(\( 2  x ^(2 )- 5  x - 3 \) ) \  & p \(x \)= - \(x + 2 \)\(2  x + 1 \)\(x - 3 \)   $

1 mark for consistent product of factors

3 marks

#pagebreak()

= Question 13

Kaitlyn was asked to sketch the graph of the polynomial function\, $p \(x \)= - \(x - 1 \)\(x + 3 \)^(3 )$.

Kaitlyn's graph:

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-13_790_908_545_590.jpg", width: 42.7%)

Describe an error on her graph.

== Solution

Kaitlyn's graph shows a multiplicity of 3 at $x = 1 $ instead of at $x = - 3 $.

#pagebreak()

= Question 14

Sketch the angle of -5 radians in standard position.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-14_1030_1024_556_532.jpg", width: 48.2%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-14_819_810_569_621.jpg", width: 38.1%)

$frac(1 ,2 )$ mark for an appropriate angle in quadrant I

$frac(1 ,2 )$ mark for the correct direction of an angle in standard position

1 mark

#pagebreak()

= Question 15

The graph of a sinusoidal function is sketched below. The point A is a maximum and the point B

is a minimum. State the value of $k $ if the amplitude of the function is 6 .

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-15_915_1142_519_569.jpg", width: 53.7%)

== Solution

$  k = 2   $

#pagebreak()

= Question 16

Given the graphs of $f \(x \)$ and $g \(x \)$\, state the domain of $\(f + g \)\(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-16_834_832_466_236.jpg", width: 39.2%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/5ca99424-6ce4-46bd-9414-1054cd96c83b-16_836_834_464_1100.jpg", width: 39.2%)

Domain:

$\_ \_ \_ \_ $

== Solution

Domain: $quad \{ x  divides - 1 < x  <=  2 \, x  in  bb(R )\} $

1 mark

or

Domain: \(-1\,2\]

#pagebreak()

= Question 17

Given that the point $\(- 13 \,7 \)$ is on the graph of $y = f \(x \)$\, identify the corresponding point on

the graph of $y = f ^(- 1 )\(x + 2 \)$.

*A.*

$\(7 \,- 11 \)$

*B.*

$\(5 \,- 13 \)$

*C.*

$\(7 \,- 15 \)$

*D.*

$\(9 \,- 13 \)$

== Solution

Correct answer: B

$\(5 \,- 13 \)$

#pagebreak()

= Question 18

Given that $x = 0 \, x = 1 \, x = 2 $ and $x = - 3 $ are zeros of the polynomial function $p \(x \)$\, identify a

possible equation for $p \(x \)$.

*A.*

$p \(x \)= - 3  x \(x + 1 \)\(x - 2 \)$

*B.*

$p \(x \)= \(x + 1 \)\(x + 2 \)\(x - 3 \)^(2 )$

*C.*

$p \(x \)= x \(x + 3 \)^(2 )\(x - 1 \)\(x - 2 \)$

*D.*

$p \(x \)= \(x - 2 \)\(x - 1 \)^(3 )\(x + 3 \)$

== Solution

Correct answer: C

$p \(x \)= x \(x + 3 \)^(2 )\(x - 1 \)\(x - 2 \)$

#pagebreak()

= Question 19

1 mark

Identify the interval where the angle\, $theta $\, could exist if $cos  theta = - frac(4 ,5 )$ and $csc  theta = frac(5 ,3 )$.

*A.*

$lr(\( 0 \, frac(pi ,2 )\) )$

*B.*

$lr(\( frac(pi ,2 )\, pi \) )$

*C.*

$lr(\( pi \, frac(3  pi ,2 )\) )$

*D.*

$lr(\( frac(3  pi ,2 )\, 2  pi \) )$

== Solution

Correct answer: B

$lr(\( frac(pi ,2 )\, pi \) )$

#pagebreak()

= Question 20

Identify a non-permissible value of $theta $ in the identity\, $frac(cot  theta ,csc  theta )= cos  theta $.

*A.*

$pi $

*B.*

$frac(pi ,4 )$

*C.*

$frac(3  pi ,2 )$

*D.*

$frac(pi ,2 )$

== Solution

Correct answer: A

$pi $

#pagebreak()

= Question 21

Identify the solution of the equation\, $e ^(2  x )= 16 $.

*A.*

$x = ln  8 $

*B.*

$x = 8 $

*C.*

$x = frac(ln  16 ,2 )$

*D.*

$x = frac(log  16 ,2 )$

== Solution

Correct answer: C

$x = frac(ln  16 ,2 )$

#pagebreak()

= Question 22

A committee of 6 people is to be selected from 90 students. Identify an expression that represents

the number of possible committees if two of the students\, Evelyn and Wayne\, must be on the

committee.

*A.*

$ "" _(90 ) C _(4 )$

*B.*

$ "" _(90 ) C _(6 )$

*C.*

$ "" _(88 ) C _(6 )$

*D.*

$ "" _(88 ) C _(4 )$

== Solution

Correct answer: D

$ "" _(88 ) C _(4 )$

#pagebreak()

= Question 23

Identify the expression for the number of arrangements of the letters in the word RUSSELL.

*A.*

$frac(7 ! ,4 ! )$

*B.*

7 !

*C.*

$frac(7 ! ,2 ! )$

*D.*

$frac(7 ! ,2 ! 2 ! )$

== Solution

Correct answer: D

$frac(7 ! ,2 ! 2 ! )$

#pagebreak()

= Question 24

Given the row of Pascal's triangle below\, identify the third value of the next row.

1

7

21

35

35

21

7

1

*A.*

8

*B.*

28

*C.*

56

*D.*

70

== Solution

Correct answer: B

28

#pagebreak()

= Question 25

Identify the equation represented by the graph sketched below.

*A.*

$y = lr(\( frac(1 ,2 )\) )^(x )+ 1 $

*B.*

$y = 2 ^(x - 1 )+ 1 $

*C.*

$y = 2 ^(x + 1 )+ 1 $

*D.*

$y = lr(\( frac(1 ,2 )\) )^(x + 1 )+ 1 $

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-03_592_616_1916_1196.jpg", width: 29.0%)

== Solution

Correct answer: B

$y = 2 ^(x - 1 )+ 1 $

#pagebreak()

= Question 26

Match the following functions with their correct graphs.

Place the appropriate letter in this column.

$f \(x \)= frac(1 ,x - 2 )$

$g \(x \)= frac(- x ,x - 2 )$

$\_ \_ \_ \_ $

$h \(x \)= frac(2  x ,x - 1 )$

$\_ \_ \_ \_ $

$k \(x \)= frac(2  x ,x + 1 )$

$\_ \_ \_ \_ $

A.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-04_634_669_1216_352.jpg", width: 31.5%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-04_646_647_1226_1147.jpg", width: 30.4%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-04_637_686_1927_326.jpg", width: 32.3%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-04_635_663_1929_1149.jpg", width: 31.2%)

== Solution

$\_ \_ \_ \_ $

D

$  h \(x \)= frac(2  x ,x - 1 )  $

A

$  frac(1 ,2 ) " mark for each answer "  $

$  k \(x \)= frac(2  x ,x + 1 )  $

B

$  2  " marks "  $

A.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-20_632_666_1246_359.jpg", width: 31.3%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-20_645_651_1250_1149.jpg", width: 30.6%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-20_634_690_1951_322.jpg", width: 32.5%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-20_634_662_1951_1147.jpg", width: 31.2%)

#pagebreak()

= Question 27

Evaluate.

$  sin  ^(2 )lr(\( frac(11  pi ,3 )\) ) cot  lr(\( frac(pi ,4 )\) )+ csc  lr(\( frac(11  pi ,6 )\) )  $

== Solution

$lr(\( frac(- sqrt(3 ),2 )\) )^(2 )\(1 \)+ \(- 2 \)$

$lr(\( frac(3 ,4 )\) )\(1 \)- 2 $

$frac(3 ,4 )- 2 $

$- frac(5 ,4 )$

1 mark for $sin  lr(\( frac(11  pi ,3 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

1 mark for $cot  lr(\( frac(pi ,4 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value $\)$

1 mark for $csc  lr(\( frac(11  pi ,6 )\) )lr(\( frac(1 ,2 ) )$ mark for quadrant\; $frac(1 ,2 )$ mark for value\)

3 marks

or

$  - 1  frac(1 ,4 )  $

#pagebreak()

= Question 28

Sketch the graph of $y = log  _(2 )\[- \(x - 2 \)\]$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-06_886_889_537_603.jpg", width: 41.8%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-22_941_879_614_256.jpg", width: 41.4%)

1 mark for shape of a logarithmic function

1 mark for horizontal reflection

1 mark for horizontal translation

3 marks

#pagebreak()

= Question 29

Justify that $ "" _(12 ) C _(7 )=  "" _(12 ) C _(5 )$.

== Solution

$    "" _(12 ) C _(7 ) & = frac(12 ! ,\(12 - 7 \)! 7 ! ) \  & = frac(12 ! ,5 ! 7 ! )   $

$    "" _(12 ) C _(5 ) & = frac(12 ! ,\(12 - 5 \)! 5 ! ) \  & = frac(12 ! ,7 ! 5 ! )   $

$  frac(12 ! ,5 ! 7 ! )= frac(12 ! ,7 ! 5 ! )  $

1 mark

#pagebreak()

= Question 30

Solve\, algebraically.

$  lr(\( frac(1 ,4 )\) )^(3  x )= 8 ^(x - 3 )  $

== Solution

$   lr(\( 2 ^(- 2 )\) )^(3  x ) & = lr(\( 2 ^(3 )\) )^(x - ) \  2 ^(- 6  x ) & = 2 ^(3  x - 9 ) \  - 6  x  & = 3  x - 9  \  - 9  x  & = - 9  \  x  & = 1    $

1 mark for changing to a common base \( $frac(1 ,2 )$ mark for each side\)

$frac(1 ,2 )$ mark for exponent law

$frac(1 ,2 )$ mark for equating exponents

2 marks

#pagebreak()

= Question 31

State the domain and range of the function $y = - sqrt(x - 5 )+ 4 $.

Domain:

$\_ \_ \_ \_ $

Range:

$\_ \_ \_ \_ $

== Solution

Domain: $\{ x  divides  x  >=  5 \, x  in  bb(R )\}  quad  1 $ mark for domain

Range: $\{ y  divides  y  <=  4 \, y  in  bb(R )\}  quad  1 $ mark for range

or

Domain: $\[5 \, oo \) 1 $ mark for domain

Range: $\(- oo \, 4 \] quad  1 $ mark for range

2 marks

#pagebreak()

= Question 32

Sketch at least one period of the graph of $y = 4  cos  lr(\[ 3 lr(\( x + frac(pi ,6 )\) )\] )+ 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-10_955_1118_586_470.jpg", width: 52.6%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-26_990_1106_640_243.jpg", width: 52.0%)

1 mark for shape of a sinusoidal function with correct amplitude

1 mark for period

1 mark for horizontal translation

1 mark for vertical translation

4 marks

#pagebreak()

= Question 33

Determine\, algebraically\, the equation of $p \(x \)$ that satisfies all of the following conditions:

- $p \(x \)$ is a polynomial function of degree 4

- $p \(x \)$ has zeros at -5 and 1

- all zeros of $p \(x \)$ have a multiplicity of 2

- the graph of $p \(x \)$ has a $y $-intercept at 75

$p \(x \)= $

== Solution

$   p \(x \) & = a \(x + 5 \)^(2 )\(x - 1 \)^(2 ) & & 1  " mark for multiplicity of " 2  " at " x = - 5  " and " x = 1  \  75  & = a \(5 \)^(2 )\(- 1 \)^(2 ) & & \  75  & = 25  a  & & 1  " mark for consistent value of " a  \  a  & = 3  & & 2  " marks "   $

#pagebreak()

= Question 34

Vitaly was asked to solve the exponential equation $5 ^(2  x + 7 )= 3  dot.c  7 ^(x )$.

Vitaly's work:

$   log  lr(\( 5 ^(2  x + 7 )\) ) & = log  lr(\( 3  dot.c  7 ^(x )\) ) \  \(2  x + 7 \) log  5  & = log  lr(\( 21 ^(x )\) ) \  2  x  log  5 + 7  log  5  & = x  log  21  \  7  log  5  & = x  log  21 - 2  x  log  5  \  7  log  5  & = x \(log  21 - 2  log  5 \) \  x  & = frac(7  log  5 ,log  21 - 2  log  5 )   $

Describe his error.

== Solution

In step 2\, Vitaly incorrectly simplified $3  dot.c  7 ^(x )$ to $21 ^(x )$.

He should have applied the product law of logarithms.

#pagebreak()

= Question 35

Given the graph of $f \(x \)$\,

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-13_433_534_446_814.jpg", width: 25.1%)

a\) sketch the graph of $g \(x \)= - f \(x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-13_433_510_983_825.jpg", width: 24.0%)

b\) sketch the graph of $k \(x \)= | f \(x \)| $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-13_439_512_1523_825.jpg", width: 24.1%)

c\) sketch the graph of $r \(x \)= f \(2  x \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-13_433_511_2062_824.jpg", width: 24.0%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-29_430_503_980_821.jpg", width: 23.7%)

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-29_428_516_1470_821.jpg", width: 24.3%)



#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-29_430_505_2028_819.jpg", width: 23.8%)

#pagebreak()

= Question 36

Determine the exact value of $sin  lr(\( frac(17  pi ,12 )\) )$.

== Solution

$   sin  lr(\( frac(17  pi ,12 )\) ) & = sin  lr(\( frac(pi ,6 )+ frac(5  pi ,4 )\) ) \  & = sin  lr(\( frac(pi ,6 )\) ) cos  lr(\( frac(5  pi ,4 )\) )+ cos  lr(\( frac(pi ,6 )\) ) sin  lr(\( frac(5  pi ,4 )\) ) \  & = lr(\( frac(1 ,2 )\) )lr(\( frac(- sqrt(2 ),2 )\) )+ lr(\( frac(sqrt(3 ),2 )\) )lr(\( frac(- sqrt(2 ),2 )\) ) \  & = frac(- sqrt(2 )- sqrt(6 ),4 )   $

1 mark for substitution into correct identity

2 marks for exact values \( $frac(1 ,2 )$ mark for each\)

3 marks

Note:

- Other combinations are possible.

#pagebreak()

= Question 37

Given $f \(x \)= sqrt(x + 3 )$ and $g \(x \)= x - 8 $\,

a\) determine the value of $g \(f \(1 \)\)$.

b\) justify that the value of $\(f - g \)\(- 5 \)$ is undefined.

== Solution

a\)

$  mat(delim: #none,  f \(1 \) "" , = 2  "" , 1  \/ 2  " mark for the value of " f \(1 \) "" , "" ; g \(2 \) "" , = - 6  "" , "" , 1  \/ 2  " mark for consistent value of " g \(f \(1 \)\) "" ; g \(f \(1 \)\) "" , = - 6  "" , "" , bold(1 ) " mark " )  $

b\) The domain of $f \(x \)$ is $x  >= - 3  \; x = - 5 $ is outside the domain.

or

$   f \(- 5 \) & = sqrt(- 5 + 3 ) \  & = sqrt(- 2 )   $

It is not possible to evaluate the square root of a negative radicand\, therefore $f \(- 5 \)$ is undefined.

1 mark

#pagebreak()

= Question 38

Solve\, algebraically.

$  48 lr(\(  "" _(n ) C _(4 )\) )=  "" _(\(n + 1 \)) P _(4 )  $

== Solution

$   48 lr(\( frac(n ! ,\(n - 4 \)! 4 ! )\) ) & = frac(\(n + 1 \)! ,\(\(n + 1 \)- 4 \)! ) \  48 lr(\( frac(n ! ,\(n - 4 \)! 4 ! )\) ) & = frac(\(n + 1 \)! ,\(n - 3 \)! ) \  frac(48 ,4 ! ) & = frac(\(n - 4 \)! \(n + 1 \)! ,\(n - 3 \)! n ! ) \  frac(48 ,24 ) & = frac(\(n - 4 \)! \(n + 1 \)\(n \)! ,\(n - 3 \)\(n - 4 \)! \(n \)! ) \  2  & = frac(n + 1 ,n - 3 ) \  2  n - 6  & = n + 1  \  n  & = 7    $

1 mark for substitution into equation \( $frac(1 ,2 )$ mark for each side\)

1 mark for substitution into equation \( $frac(1 ,2 )$ mark for each side\)

$frac(1 ,2 )$ mark for solving for $n $

3 marks

#pagebreak()

= Question 39

Sketch the graph of $p \(x \)= \(x + 1 \)\(x + 2 \)\(x - 4 \)$.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-17_867_858_558_601.jpg", width: 40.4%)

== Solution

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/27bd5b29-4766-4b04-aea7-cdcc5a120315-33_862_855_587_243.jpg", width: 40.2%)

1 mark for $x $-intercepts

$frac(1 ,2 )$ mark for $y $-intercept

$frac(1 ,2 )$ mark for end behaviour

2 marks

#pagebreak()

= Question 40

Evaluate.

$  log  _(5 )lr(\( log  _(2 ) 32 \) )  $

== Solution

#table(stroke: none,
columns: 2,
align: (left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2),
table.hline(stroke: .5pt),
[$log  _(5 ) 5 $ ], [$frac(1 ,2 )$ mark for evaluating $log  _(2 ) 32 $ ],
table.hline(stroke: .5pt),
[1 ], [$frac(1 ,2 )$ mark for consistent value ],
table.hline(stroke: .5pt),
[], [1 mark ],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 41

Describe how to use the graph to solve the equation $sqrt(x - 2 )= x - 2 $.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-19_927_967_446_610.jpg", width: 45.5%)

== Solution

State the $x $-coordinates of the points of intersection.

#pagebreak()

= Question 42

Verify\, by substitution\, that the equation $frac(sec  theta ,tan  theta + cot  theta )= sin  2  theta $ is true for $theta = frac(pi ,3 )$.

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
columns: 3,
align: (left, left, left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1), table.vline(stroke: .5pt, x: 2), table.vline(stroke: .5pt, x: 3),
table.hline(stroke: .5pt),
[Left-Hand Side ], [Right-Hand Side ], [],
table.hline(stroke: .5pt),
table.cell(colspan: 3)[LHS = RHS ],
table.hline(stroke: .5pt),
[], [], [],
table.hline(stroke: .5pt),
[],
);

#pagebreak()

= Question 43

Describe the transformation\(s\) to the graph of $y = 3 ^(x )$ which results in a graph with a $y $-intercept

of -2 .

== Solution

A vertical translation down 3 units.

1 mark

Note:

- Other answers are possible.

#pagebreak()

= Question 44

Determine the equation of the rational function represented by the graph.

#image("../pqp-mathpix/pqp/manitoba-pc40s-2024-jun/assets/42032140-b058-4882-8c4c-26adacdb7c12-22_972_1002_459_550.jpg", width: 47.2%)

$f \(x \)= $

$\_ \_ \_ \_ $

== Solution

#table(stroke: none,
columns: 1,
align: (left, ),
table.vline(stroke: .5pt, x: 0), table.vline(stroke: .5pt, x: 1),
table.hline(stroke: .5pt),
[$f \(x \)= frac(x - 4 ,\(x - 2 \)\(x - 4 \))$ ],
table.hline(stroke: .5pt),
[],
);

1 mark for factor of $\(x - 2 \)$ in denominator

1 mark for factor of $\(x - 4 \)$ in both numerator and denominator

2 marks

#pagebreak()

= Question 45

Justify that $f \(x \)= 3  x + 2 $ and $g \(x \)= frac(x - 3 ,2 )$ are not inverses of each other.

== Solution

Method 1

Let $y = f \(x \)$

$  y = 3  x + 2   $

Let $y = f ^(- 1 )\(x \)$

$  mat(delim: #none,  x = 3  y + 2  "" , 1  " mark for switching " x  " and " y  "" ; frac(x - 2 ,3 )= y  "" , "" ; frac(x - 2 ,3 )= f ^(- 1 )\(x \) "" , 1  " mark for justification " "" ; g \(x \) !=  f ^(- 1 )\(x \) "" , )  $

2 marks

Method 2

If they are inverses\, then $g \(f \(x \)\)= x $\, and $f \(g \(x \)\)= x $.

$   g \(3  x + 2 \) & = frac(3  x + 2 - 3 ,2 ) \  & = frac(3  x - 1 ,2 )   $

1 mark for $g \(f \(x \)\)$ or $f \(g \(x \)\)$

Since $g \(f \(x \)\) !=  x $\, they are not inverses of each other.

1 mark for justification

2 marks

#pagebreak()

= Question 46

The terminal arm of an angle\, $theta $\, in standard position passes through the point $\(- 3 \,6 \)$ and

intersects the unit circle at the point $P \(theta \)$. Determine the coordinates of the point $P \(theta \)$.

== Solution

$  mat(delim: #none,  x ^(2 )+ y ^(2 )= r ^(2 ) "" , "" ; \(- 3 \)^(2 )+ \(6 \)^(2 )= r ^(2 ) "" , 1  \/ 2  " mark for substitution " "" ; 9 + 36 = r ^(2 ) "" , "" ; 45 = r ^(2 ) "" , "" ; sqrt(45 )= r  "" , 1  \/ 2  " mark for solving for " r  "" ; P \(theta \)= lr(\( frac(- 3 ,sqrt(45 ))\, frac(6 ,sqrt(45 ))\) ) "" , mat(delim: #none,  1  " mark for the coordinates of " P \(theta \) "" ; \(1  \/ 2  " mark for " x  "-coordinate " \; 1  \/ 2  " mark for " y  "-coordinate "\) ) "" ; quad  " or " "" , 2  " marks " "" ; P \(theta \)= lr(\( frac(- 1 ,sqrt(5 ))\, frac(2 ,sqrt(5 ))\) ) "" , )  $

or

$  P \(theta \)= lr(\( frac(- sqrt(5 ),5 )\, frac(2  sqrt(5 ),5 )\) )  $

#pagebreak()

= Question 47

Determine the exact value of $2  sin  theta  cos  theta $ if $theta = frac(pi ,12 )$.

== Solution

$  mat(delim: #none,  2  sin  theta  cos  theta  "" , = sin  2  theta  "" , "" , 1  " mark for substitution into correct identity " "" ; "" , = sin  lr(\( 2 lr(\( frac(pi ,12 )\) )\) ) "" , "" ; "" , = sin  lr(\( frac(pi ,6 )\) ) "" , "" , "" ; "" , = frac(1 ,2 ) "" , "" , 1  " mark for consistent value " )  $